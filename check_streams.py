import asyncio
import ffmpeg

async def is_playable(url: str, timeout: int = 7) -> bool:
    try:
        probe = await asyncio.wait_for(asyncio.to_thread(ffmpeg.probe, url), timeout=timeout)

        video_stream = next(
            (stream for stream in probe["streams"]
             if stream["codec_type"] == "video"),
            None
        )

        if video_stream is None:
            return False

        width = int(video_stream["width"])
        height = int(video_stream["height"])

        valid = width >= 1920 and height >= 1080 and width <= 3840 and height <= 2160

        if valid:
            print(f'✅ {url}')
            return True
        else:
            return False
    except (ffmpeg.Error, asyncio.TimeoutError) as exc:
        print(f'❌ {url}')

        if isinstance(exc, ffmpeg.Error):
          print(exc.stderr) # type: ignore
        else:
         print(exc)

        return False

async def check_streams(urls: list[str], concurrency:int=10 ) -> list[str]:
    semaphore = asyncio.Semaphore(concurrency)
    playable_urls: list[str] = []

    async def check_url(url:str):
        async with semaphore:
            if await is_playable(url):
                playable_urls.append(url)

    tasks = [check_url(url) for url in urls]
    await asyncio.gather(*tasks)
    return playable_urls
