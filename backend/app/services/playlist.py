# playlist.py
import asyncio
from dataclasses import dataclass
from pathlib import Path

from backend.app.services.stream_checks import check_streams
from backend.app.services.channels import query_db
from backend.app.services.channel_formatting import parse_categories, parse_channel_name
from backend.app.services.m3u import write_m3u

@dataclass(frozen=True)
class PlaylistResult:
    output_path: Path
    total_channels: int
    total_urls: int
    working_streams: int
    playlist_channels: int

def generate_playlist(output_path: Path) -> PlaylistResult:
    print("Finding channels...")
    channels = query_db()
    total_channels = len(channels)

    print(f"Found {total_channels} channels")

    print("Checking streams...")
    urls: list[str] = (
        channels["stream_url"]
        .drop_duplicates()
        .dropna()
        .astype(str)
        .tolist()
    )
    total_urls = len(urls)

    print(f"Found {total_urls} urls")
    working_streams = asyncio.run(check_streams(urls))

    print("Updating database...")
    channels["working"] = channels["stream_url"].isin(working_streams)
    channels["channel_name"] = channels["channel_name"].apply(parse_channel_name)
    channels["channel_categories"] = channels["channel_categories"].apply(parse_categories)

    print("Creating playlist...")
    working_channels = channels[channels["working"]].copy()
    working_channels = working_channels.dropna(subset=["stream_url"])
    working_channels = working_channels[working_channels["stream_url"].astype(str).str.strip() != ""]

    print("Writing playlist...")
    write_m3u(working_channels, output_path)

    return PlaylistResult(
        output_path=output_path,
        total_channels=total_channels,
        total_urls=total_urls,
        working_streams=len(working_streams),
        playlist_channels=len(working_channels),
    )
