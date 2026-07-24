from pathlib import Path
from backend.app.services.playlist import generate_playlist


def main() -> None:
    print("Welcome to the IPTV Playlist Tool.")
    result = generate_playlist(output_path=Path("playlist.m3u"), quality="HD")
    print(f"Playlist generated with {result.playlist_channels} channels")


if __name__ == "__main__":
    main()
