from fractions import Fraction
from typing import Any

from backend.app.types.types import StreamQuality


def get_bit_rate(variant_bit_rate: int):
    return int(variant_bit_rate / 1_000_000)


def is_valid_frame_rate(avg_frame_rate: str, quality: StreamQuality) -> bool:
    FRAME_RATE = 20 if quality == "SD" else 25
    fps = float(Fraction(avg_frame_rate))
    return fps >= FRAME_RATE


def is_valid_bit_rate(bit_rate: int, quality: StreamQuality) -> bool:
    valid_bit_rates: dict[StreamQuality, int] = {"SD": 2, "HD": 4}
    return bit_rate >= valid_bit_rates.get(quality, float("inf"))


def is_stream_type(stream: dict[str, Any], type: str) -> bool:
    return stream.get("codec_type") == type


def is_valid_codec(codec: str) -> bool:
    return codec in ["h264", "hevc", "h265"]


def is_valid_dimensions(
    width: int | None, height: int | None, quality: StreamQuality
) -> bool:
    if width is None or height is None:
        return False

    match quality:
        case "4K":
            return width >= 3840 and height >= 1080 and width <= 7680 and height <= 4320
        case "HD":
            return width >= 1920 and height >= 1080 and width <= 3840 and height <= 2160
        case _:
            return width >= 1280 and height >= 720 and width <= 3840 and height <= 2160
