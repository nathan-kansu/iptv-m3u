import asyncio
from get_iptv_data import get_iptv_data
from check_streams import check_streams
from write_m3u import write_m3u

data = get_iptv_data()
data = data.drop_duplicates("stream_url")
urls: list[str] = data["stream_url"].dropna().tolist()
working_streams = asyncio.run(check_streams(urls))
data["working"] = data["stream_url"].isin(working_streams)
working_data = data[data["working"]]
write_m3u(data)

print(f"Playlist generated with {len(data)} channels.")
# print(working_data)


