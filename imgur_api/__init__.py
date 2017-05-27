async def extract_elements_from_response(response_json):
    data = response_json.get("data")
    if not data or len(data) == 0:
        return
    extracted_elements = [
        (entry.get("title"), f"https://i.imgur.com/{entry.get('cover')}.jpg", entry.get("link")) for entry in data
    ]
    return extracted_elements
