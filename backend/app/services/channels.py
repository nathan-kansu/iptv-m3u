
import duckdb
from pandas import DataFrame
from backend.app.config import channels_url, feeds_url, streams_url, logos_url, countries_url

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
        AND array_length(channels.categories, 1) > 0
        AND NOT list_has_any(channels.categories, ['shop', 'religious'])
        ORDER BY channels.country, channel_categories, channel_name ASC
        """
    ).df()
