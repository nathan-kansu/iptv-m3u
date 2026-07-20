
import duckdb
from pandas import DataFrame
from constants import channels_url, feeds_url, streams_url, logos_url, countries_url

#  channels.network AS channel_network,
# streams.title AS stream_title,
# OR streams.quality LIKE '%720%'
# channels.id AS channel_id,
# OR streams.quality LIKE '%720%'
# feeds.is_main AS feed_is_main,

def get_iptv_data() -> DataFrame:
    return duckdb.sql(
        f"""
        SELECT
            channels.id AS channel_id,
            channels.name AS channel_name,
            logos.url AS logo_url,
            channels.country AS channel_country,
            channels.categories AS channel_categories,
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
