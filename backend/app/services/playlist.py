# playlist.py
import asyncio
from dataclasses import dataclass
from pathlib import Path
from pandas import Series

from backend.app.services.stream_checks import StreamCheckResult, check_streams
from backend.app.services.channels import fetch_channels
from backend.app.services.channel_formatting import (
    parse_categories,
    parse_channel_name,
    parse_country_flag,
)
from backend.app.services.m3u import write_m3u


@dataclass(frozen=True)
class PlaylistResult:
    output_path: Path
    total_channels: int
    total_urls: int
    working_streams: int
    playlist_channels: int


def is_working_stream(stream_result: StreamCheckResult | None) -> bool:
    return stream_result is not None and stream_result.is_playable


def generate_playlist(output_path: Path) -> PlaylistResult:
    print("Finding channels...")
    channels = fetch_channels()
    total_channels = len(channels)

    print(f"Found {total_channels} channels")

    print("Checking streams...")
    urls: list[str] = channels["stream_url"].drop_duplicates().dropna().tolist()
    total_urls = len(urls)

    print(f"Found {total_urls} urls")
    stream_results = asyncio.run(check_streams(urls))

    print("Updating database...")
    stream_urls: Series[str] = channels["stream_url"].dropna()
    channels["working"] = stream_urls.map(
        lambda stream_url: is_working_stream(stream_results.get(str(stream_url)))
    )
    working_channels = channels[channels["working"]].copy()

    print("Creating playlist...")
    working_channels["channel_name"] = working_channels["channel_name"].apply(
        parse_channel_name
    )
    working_channels["channel_categories"] = working_channels[
        "channel_categories"
    ].apply(parse_categories)
    working_channels["country_flag"] = working_channels.apply(
        parse_country_flag, axis=1, stream_results=stream_results
    )
    working_channels = (
        working_channels.drop_duplicates(subset=["stream_url"])
        .dropna(subset=["stream_url"])
        .drop_duplicates(subset=["channel_name"])
    )
    # working_channels = working_channels[
    #     working_channels["stream_url"].astype(str).str.strip() != ""
    # ]

    print("Writing playlist...")
    write_m3u(working_channels, output_path)

    return PlaylistResult(
        output_path=output_path,
        total_channels=total_channels,
        total_urls=total_urls,
        working_streams=len(stream_results),
        playlist_channels=len(working_channels),
    )
