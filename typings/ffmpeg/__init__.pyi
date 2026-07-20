from typing import Any

class Error(Exception):
    pass

def probe(filename: str, cmd: str = "ffprobe", **kwargs: Any) -> Any:
    ...
