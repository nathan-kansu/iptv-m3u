import asyncio
import ffmpeg
import requests


async def is_playable(url: str, timeout: int = 2) -> bool:
    try:
        request = requests.get(url, stream=True, timeout=2)
        if request.status_code != 200:
            print(f'❌ {url} (status {request.status_code})')
            return False

        chunk = next(request.iter_content(4096), None)
        if chunk is None:
            print(f'❌ {url} (empty stream)')
            return False

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

        # valid = width >= 1920 and height >= 1080 and width <= 3840 and height <= 2160
        valid = width >= 1280 and height >= 720 and width <= 3840 and height <= 2160

        if valid:
            print(f'✅ {url}')
            return True
        else:
            print(f'❌ {url}')
            return False
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as exc:
        print(f'❌ {url} ({exc})')
        return False
    except (ffmpeg.Error, asyncio.TimeoutError) as exc:
        print(f'❌ {url} ({exc})')
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
