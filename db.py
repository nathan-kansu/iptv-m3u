
import duckdb
from pandas import DataFrame
from constants import channels_url, feeds_url, streams_url, logos_url, countries_url

#  channels.network AS channel_network,
# streams.title AS stream_title,
# OR streams.quality LIKE '%720%'
# channels.id AS channel_id,
# OR streams.quality LIKE '%720%'
# feeds.is_main AS feed_is_main,
# channels.id AS channel_id,
# AND channels.country = 'UK'
# OR streams.quality LIKE '720%'
# list_contains(channels.categories, 'kids')
# AND channel_country IN ['US', 'UK']
# AND channels.id IS NOT NULL
# AND (
#     channels.categories IS NOT NULL
#     AND array_length(channels.categories, 1) > 0
# )AND channels.network NOT LIKE '%Pluto%'
        # AND
        #     (
        #         channel_name NOT LIKE '%Latin%'
        #         AND channel_name NOT LIKE '%Jr%'
        #     )
        # AND (
        #         NOT list_contains(channels.categories, 'shop')
        #         AND NOT list_contains(channels.categories, 'religious')
        #     )
        # AND (
        #         streams.quality LIKE '%1080%'
        #         OR streams.quality LIKE '720%'
        #     )
        # ORDER BY channel_country, channel_categories, channel_name ASC
        # AND channels.country = 'RU'

def query_db() -> DataFrame:
    return duckdb.sql(
        f"""
        SELECT
            channels.id AS channel_id,
            channels.name AS channel_name,
            channels.categories as channel_categories,
            channels.country as channel_country,
            feeds.id as feeds_id,
            streams.quality as stream_quality,
            streams.url as stream_url,
            countries.flag as country_flag,
            logos.url as logo_url
        FROM '{channels_url}' AS channels
        LEFT JOIN '{logos_url}' AS logos
             ON channels.id = logos.channel
        JOIN '{feeds_url}' AS feeds
            ON channels.id = feeds.channel
        JOIN '{streams_url}' AS streams
            ON channels.name = streams.title
        JOIN '{countries_url}' AS countries
            ON channels.country = countries.code
        WHERE channels.closed IS NULL
        AND feeds.id = 'HD'
        AND streams.quality LIKE '%1080%'
        ORDER BY channel_categories, channel_name ASC
        """
    ).df()
