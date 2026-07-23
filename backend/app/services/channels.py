import duckdb
from pandas import DataFrame
from backend.app.config import (
    channels_url,
    feeds_url,
    streams_url,
    logos_url,
    countries_url,
)
from typing import TypedDict


class ChannelType(TypedDict):
    channel_id: str
    channel_name: str
    channel_categories: str
    channel_country: str
    country_flag: str
    stream_url: str


def fetch_channels() -> DataFrame:
    return duckdb.sql(f"""
        SELECT
            channels.id AS channel_id,
            channels.name AS channel_name,
            channels.categories as channel_categories,
            channels.country as channel_country,
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
        ORDER BY channels.country, channels.categories, channels.name ASC
        """).df()
