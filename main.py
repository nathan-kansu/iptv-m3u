import asyncio
from db import query_db
from check_streams import check_streams
from write_m3u import write_m3u
from parse import parse_categories, parse_channel_name

print(f"Welcome to the IPTV Playlist Tool.")

print(f"Finding channels...")
data = query_db()
print(f"Found {len(data)} channels")

print(f"Checking streams...")
urls: list[str] = data["stream_url"].drop_duplicates().dropna().tolist()
print(f"Found {len(urls)} urls")
working_streams = asyncio.run(check_streams(urls))

print(f"Updating database...")
data["working"] = data["stream_url"].isin(working_streams)
data['channel_name'] = data['channel_name'].apply(parse_channel_name)
data['channel_categories'] = data['channel_categories'].apply(parse_categories)
working_data = data[data["working"]]

print(f"Writing playlist...")
write_m3u(data)

print(f"Playlist generated with {len(data)} channels")



