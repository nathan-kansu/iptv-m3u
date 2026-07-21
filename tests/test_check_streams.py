import asyncio
import unittest
from unittest.mock import patch

import requests

from check_streams import is_playable


class CheckStreamsTests(unittest.TestCase):
    def test_is_playable_returns_false_when_request_times_out(self):
        with patch("check_streams.requests.get", side_effect=requests.exceptions.ReadTimeout):
            result = asyncio.run(is_playable("http://example.com/stream.m3u8"))

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
