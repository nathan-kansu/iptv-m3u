from pandas import Series
from typing import cast
from backend.app.services.channels import ChannelType
from backend.app.services.stream_checks import StreamCheckResult
from backend.app.services.countries import fetch_countries


def parse_channel_name(channel_name: str) -> str:
    return channel_name.title()


def parse_categories(categories: list[str]) -> str:
    category_string = ", ".join(map(str.lower, categories))

    if "music" in category_string:
        return "Music"
    elif "kids" in category_string:
        return "Kids"
    elif "movies" in category_string:
        return "Movies"
    elif "sport" in category_string:
        return "Sports"
    else:
        return "General"


def parse_country_flag(
    row: Series, stream_results: dict[str, StreamCheckResult]
) -> str:
    channel = cast(ChannelType, row)
    channel_country = channel.get("channel_country")
    country_flag = channel.get("country_flag")
    stream_url = channel.get("stream_url")
    stream_result = stream_results.get(stream_url)

    if not stream_result:
        return country_flag

    stream_language = stream_result.audio_language
    if not stream_language:
        return country_flag

    countries = fetch_countries().explode("languages")
    matching_countries = countries[countries["languages"] == stream_language]
    matching_countries_languages = matching_countries[
        matching_countries["code"] == channel_country
    ]

    if matching_countries.empty or len(matching_countries_languages):
        return country_flag

    match stream_language:
        case "rus":
            return "🇷🇺"
        case "esp":
            return "🇪🇸"
        case _:
            return "🇺🇸"
