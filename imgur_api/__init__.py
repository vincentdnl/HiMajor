async def extract_elements_from_response(response_json):
    data = response_json.get("data")
    if not data or len(data) == 0:
        return
    extracted_elements = [
        (entry.get("title"), await get_cover(entry), entry.get("link")) for entry in data
    ]
    return extracted_elements


async def get_cover(entry):
    cover = entry.get('cover')
    cover_link = f"https://i.imgur.com/{cover}b.jpg"
    if not cover:
        cover_link = entry.get("link")
    return cover_link
