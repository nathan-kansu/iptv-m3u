
from pandas import DataFrame


def write_m3u(df: DataFrame):
    filtered_df = df.dropna(subset=["stream_url"])
    filtered_df = filtered_df[filtered_df["stream_url"].astype(str).str.strip() != ""]

    with open("custom-playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for _, row in filtered_df.iterrows():
            name = f"{row['channel_name']} {row['country_flag']}"
            f.write(
                f'#EXTINF:-1 tvg-id="{row["channel_id"]}" tvg-name="{name}" '
                f'group-title="{row["channel_categories"]}",{name}\n'
            )
            f.write(f'{row["stream_url"]}\n')

