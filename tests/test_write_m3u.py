import os
import tempfile
import unittest

import pandas as pd

from write_m3u import write_m3u


class WriteM3UTests(unittest.TestCase):
    def test_write_m3u_skips_rows_without_stream_url(self):
        df = pd.DataFrame(
            {
                "channel_name": ["Alpha", "Beta"],
                "country_flag": ["🇺🇸", "🇬🇧"],
                "channel_id": ["1", "2"],
                "channel_categories": ["News", "Sports"],
                "stream_url": [None, ""],
            }
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            previous_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                write_m3u(df)
                with open("custom-playlist.m3u", "r", encoding="utf-8") as handle:
                    content = handle.read()
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(content, "#EXTM3U\n")


if __name__ == "__main__":
    unittest.main()
