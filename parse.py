def parse_channel_name(channel_name: str) -> str:
     return channel_name.title()

def parse_categories(categories: list[str]) -> str:
     return ", ".join(map(str.title, categories))
