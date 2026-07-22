def parse_channel_name(channel_name: str) -> str:
     return channel_name.title()

def parse_categories(categories: list[str]) -> str:
     category_string = ", ".join(map(str.lower, categories))

     if('music' in category_string ):
        return 'Music'
     elif('kids' in category_string ):
        return 'Kids'
     elif('movies' in category_string ):
        return 'Movies'
     elif('sport' in category_string ):
        return 'Sports'
     else:
        return 'General'
