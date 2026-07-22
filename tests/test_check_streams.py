import asyncio
import unittest
from unittest.mock import patch

import requests

from backend.app.services.stream_checks import is_playable


class CheckStreamsTests(unittest.TestCase):
    def test_is_playable_returns_false_when_request_times_out(self):
        with patch(
            "backend.app.services.stream_checks.urllib.request.urlopen",
            side_effect=requests.exceptions.ReadTimeout,
        ):
            result = asyncio.run(is_playable("http://example.com/stream.m3u8"))

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
