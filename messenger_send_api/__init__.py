async def get_text_message(user_id, text):
    return {
        "recipient": {
            "id": user_id
        },
        "message": {
            "text": text
        }
    }

async def get_generic_template(user_id, elements):
    return {
        "recipient": {
            "id": user_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [get_generic_template_element(*element) for element in elements[:10]]
                }
            }
        }
    }


def get_generic_template_element(title, thumbnail_url, image_url):
    title = title[:80] if len(title) > 80 else title
    image_url = image_url.replace("http://", "https://")
    return {
        "title": title,
        "image_url": thumbnail_url,
        "default_action": {
            "type": "web_url",
            "url": image_url,
            "messenger_extensions": True,
            "webview_height_ratio": "tall",
            "fallback_url": image_url
        }
    }
