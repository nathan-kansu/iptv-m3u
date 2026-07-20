
from pandas import DataFrame


def write_m3u(df: DataFrame):
    with open("custom-playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for _, row in df.iterrows():
            name = f"{row['channel_name']} {row['country_flag']}"
            f.write(
                f'#EXTINF:-1 tvg-id="{row["channel_id"]}" tvg-name="{name}" '
                f'group-title="{row["channel_categories"]}" '
                f'tvg-logo="{row["logo_url"]}",'
                f'{name}\n'
            )
            f.write(f'{row["stream_url"]}\n')
