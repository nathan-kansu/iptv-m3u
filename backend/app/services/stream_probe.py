from fractions import Fraction
from typing import Any

def is_valid_frame_rate(avg_frame_rate: str)-> bool :
    FRAME_RATE = 20
    fps = float(Fraction(avg_frame_rate))
    return fps >= FRAME_RATE

def is_valid_bit_rate(bit_rate: str) -> bool:
    print(f"BIT RATE: ${bit_rate}")
    foo = int(bit_rate)
    print(f'BIT RATE: ${foo}')
    return foo >= 5

def is_stream_type(stream: dict[str, Any], type: str) -> bool:
   return stream.get("codec_type") == type

def is_valid_codec(codec: str) -> bool:
    print(f'CODEC: ${codec}')
    return codec in ['h264', 'hevc', 'h265']

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
