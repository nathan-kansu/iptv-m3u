import asyncio
import ffmpeg

async def is_playable(url: str, timeout: int = 7) -> bool:
    try:
        await asyncio.wait_for(asyncio.to_thread(ffmpeg.probe, url), timeout=timeout)
        print(f'✅ {url}')
        return True
    except (ffmpeg.Error, asyncio.TimeoutError):
        print(f'❌ {url}')
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
