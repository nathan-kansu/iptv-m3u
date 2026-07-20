import duckdb
from pandas import DataFrame

channels_url = "https://iptv-org.github.io/api/channels.json"
feeds_url = "https://iptv-org.github.io/api/feeds.json"
streams_url = "https://iptv-org.github.io/api/streams.json"
logos_url = "https://iptv-org.github.io/api/logos.json"
countries_url = "https://iptv-org.github.io/api/countries.json"

#  channels.network AS channel_network,
# streams.title AS stream_title,
# OR streams.quality LIKE '%720%'
  # channels.id AS channel_id,

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


df = duckdb.sql(
    f"""
    SELECT
        channels.id AS channel_id,
        channels.name AS channel_name,
        logos.url AS logo_url,
        channels.country AS channel_country,
        channels.categories AS channel_categories,
        feeds.is_main AS feed_is_main,
        streams.url AS stream_url,
        streams.quality AS stream_quality,
        countries.flag AS country_flag,
    FROM '{channels_url}' AS channels
    JOIN '{feeds_url}' AS feeds
        ON channels.id = feeds.channel
    JOIN '{streams_url}' AS streams
        ON channels.name = streams.title
    JOIN '{logos_url}' AS logos
        ON channels.id = logos.channel
    JOIN '{countries_url}' AS countries
        ON channels.country = countries.code
    WHERE channels.closed IS NULL
      AND channels.network NOT LIKE '%Pluto%'
      AND (
        channels.categories IS NOT NULL
         AND array_length(channels.categories, 1) > 0
     )
      AND channels.country = 'UK'
      AND (
        NOT list_contains(channels.categories, 'shop')
        AND NOT list_contains(channels.categories, 'religious')
        )
      AND (
        streams.quality LIKE '%1080%'
        )
    ORDER BY channel_country, channel_categories ASC
    """
).df()

# OR streams.quality LIKE '%720%'
df = df.drop_duplicates("stream_url")
print(df)
write_m3u(df)

print(f"Playlist generated with {len(df)} channels.")


