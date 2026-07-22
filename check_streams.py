import asyncio
import requests
import ffmpeg
from typing import Any
from probe import is_valid_frame_rate, is_video_stream, is_valid_codex, is_valid_dimensions

async def is_playable(url: str, timeout: int = 3) -> bool:
    try:
        request = requests.get(url, stream=True, timeout=timeout)
        if request.status_code != 200:
            return False

        chunk = next(request.iter_content(4096), None)
        if chunk is None:
            return False

        thread = asyncio.to_thread(ffmpeg.probe, url)
        probe: dict[str, Any] = await asyncio.wait_for(thread, timeout=timeout)
        streams = probe.get("streams", [])
        valid_streams = (stream for stream in streams if is_video_stream(stream))

        video_stream = next(valid_streams, None)
        if video_stream is None:
            return False

        width = video_stream.get("width")
        height = video_stream.get("height")
        avg_frame_rate = video_stream.get('avg_frame_rate')
        codec_name = video_stream.get('codec_name')

        return (
            is_valid_dimensions(width, height)
            and is_valid_frame_rate(avg_frame_rate)
            and is_valid_codex(codec_name)
        )
    except (Exception):
        return False

async def check_streams(urls: list[str], concurrency:int=10 ) -> list[str]:
    semaphore = asyncio.Semaphore(concurrency)
    playable_urls: list[str] = []

    async def check_url(url:str, index: str):
        remaining = len(urls) - int(index)

        async with semaphore:
            if await is_playable(url):
                print(f'✅ {remaining}: {url}')
                playable_urls.append(url)
            else:
                print(f'❌ {remaining}: {url}')

    tasks = [check_url(url, i) for i, url in urls]
    await asyncio.gather(*tasks)
    return playable_urls
