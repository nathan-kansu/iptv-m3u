import asyncio
import urllib.request
import ffmpeg
from typing import Any
from backend.app.services.stream_probe import (
    get_bit_rate,
    is_stream_type,
    is_valid_bit_rate,
    is_valid_codec,
    is_valid_dimensions,
    is_valid_frame_rate,
)
from dataclasses import dataclass

from backend.app.types.types import StreamQuality


@dataclass(frozen=True)
class StreamCheckResult:
    url: str
    is_playable: bool
    audio_language: str | None


async def check_stream(
    url: str, quality: StreamQuality, timeout: int = 5
) -> StreamCheckResult:
    invalid_stream = StreamCheckResult(url=url, is_playable=False, audio_language=None)

    try:
        request = urllib.request.urlopen(url, timeout=timeout)
        if request.status != 200:
            return invalid_stream

        chunk = request.read(4096)
        if chunk is None:
            return invalid_stream

        thread = asyncio.to_thread(ffmpeg.probe, url)
        probe: dict[str, Any] = await asyncio.wait_for(thread, timeout=timeout)
        streams = probe.get("streams", [])

        video_streams = (
            stream for stream in streams if is_stream_type(stream, "video")
        )
        audio_streams = (
            stream for stream in streams if is_stream_type(stream, "audio")
        )

        audio_stream = next(audio_streams, None)
        video_stream = next(video_streams, None)

        if video_stream is None or audio_stream is None:
            return invalid_stream

        language = audio_stream.get("tags").get("language", None)
        width = video_stream.get("width", None)
        height = video_stream.get("height", None)
        avg_frame_rate = video_stream.get("avg_frame_rate", None)
        codec = video_stream.get("codec_name", None)
        variant_bit_rate = int(video_stream.get("tags", {}).get("variant_bitrate"))
        bit_rate = get_bit_rate(variant_bit_rate)

        int(probe["format"].get("bit_rate", 0))

        playable = (
            is_valid_dimensions(width, height, quality)
            and is_valid_bit_rate(bit_rate, quality)
            and is_valid_frame_rate(avg_frame_rate, quality)
            and is_valid_codec(codec)
        )

        return StreamCheckResult(url=url, is_playable=playable, audio_language=language)

    except Exception:
        return invalid_stream


async def check_streams(
    urls: list[str], quality: StreamQuality, concurrency: int = 10
) -> dict[str, StreamCheckResult]:
    semaphore = asyncio.Semaphore(concurrency)
    results: dict[str, StreamCheckResult] = {}

    async def check_url(url: str):
        async with semaphore:
            result = await check_stream(url, quality)
            results[url] = result

            if result.is_playable:
                print(f"✅ {url}")
            else:
                print(f"❌ {url}")

    tasks = [check_url(url) for url in urls]
    await asyncio.gather(*tasks)
    return results
