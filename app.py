import asyncio
import aiohttp
import aiohttp.web
from config import config
import settings
from webhook_handler import extract_data_from_request
import aiohttp.web_request
import json


def make_app(aiohttp_app: aiohttp.web.Application, config_dict: dict) -> aiohttp.web.Application:
    async def hub(request: aiohttp.web_request.Request):
        hub_challenge = request.rel_url.query.get('hub.challenge')
        hub_verify_token = request.rel_url.query.get('hub.verify_token')
        config_verify_token = config_dict["facebook-messenger"]["verify-token"]

        if hub_verify_token == config_verify_token:
            return aiohttp.web.Response(text=hub_challenge)
        else:
            return aiohttp.web.Response(text='')

    async def hot_viral(request: aiohttp.web_request.Request):
        client_session = aiohttp.ClientSession(loop=aiohttp_app.loop)
        json_response: dict = await get_hot_viral_content(
            client_session,
            config_dict["imgur"]["client-id"]
        )
        elements = await extract_elements_from_response(json_response)
        if not elements:
            return aiohttp.web.Response(text='')
        page_id, user_id, user_text = await extract_data_from_request(request)
        fb_response = await get_generic_template(user_id, elements)
        await send_response_to_user(client_session, page_id, user_id, fb_response)
        await client_session.close()
        return aiohttp.web.Response(text='')

    async def send_response_to_user(client_session, page_id, user_id, fb_response):
        response = await client_session.post(
            settings.get_me_message_url(config_dict["facebook-messenger"]["page-access-token"]),
            headers={'Content-Type': 'application/json'},
            data=json.dumps(fb_response)
        )
        return await response.json()

    def add_routes(the_app):
        the_app.router.add_get('/', hub)
        the_app.router.add_post('/', hot_viral)

    add_routes(aiohttp_app)
    return aiohttp_app


async def extract_elements_from_response(response_json):
    data = response_json.get("data")
    if not data or len(data) == 0:
        return
    extracted_elements = [
        (entry.get("title"), f"https://i.imgur.com/{entry.get('cover')}.jpg", entry.get("link")) for entry in data
    ]
    return extracted_elements


async def get_hot_viral_content(client_session, client_id):
    api_url = "https://api.imgur.com/3/gallery/hot/viral/0.json"
    response = await client_session.get(
        api_url,
        headers={
            "Authorization": f"Client-ID {client_id}"
        })

    assert response.status == 200
    return await response.json()


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


"""
Starting the app!
"""
app = make_app(
    aiohttp.web.Application(loop=asyncio.get_event_loop()),
    config()
)
