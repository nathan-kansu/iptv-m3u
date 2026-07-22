from fractions import Fraction
from typing import Any

def is_valid_frame_rate(avg_frame_rate: str)-> bool :
    FRAME_RATE = 25
    fps = float(Fraction(avg_frame_rate))
    return fps >= FRAME_RATE

def is_video_stream(stream: dict[str, Any]) -> bool:
   return stream.get("codec_type") == "video"

def is_valid_codex(codex: str):
    return codex == 'h264'

def is_valid_dimensions(width: int|None, height: int|None) -> bool :
    if width is None or height is None:
        return False

    try:
        width = int(width)
        height = int(height)
    except (TypeError, ValueError):
        return False

    return width >= 1920 and height >= 1080
    # valid = width >= 1280 and height >= 720 and width <= 3840 and height <= 2160
