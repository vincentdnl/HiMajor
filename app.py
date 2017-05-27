import asyncio

import aiohttp
import aiohttp.web
import aiohttp.web_request

from client_requests import get_hot_viral_content, send_response_to_user
from config import config
from imgur_api import extract_elements_from_response
from messenger_send_api import get_generic_template
from webhook_handler import extract_data_from_request


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
        if not json_response:
            return aiohttp.web.Response(text='')

        elements: tuple = await extract_elements_from_response(json_response)
        if not elements:
            return aiohttp.web.Response(text='')

        page_id, user_id, user_text = await extract_data_from_request(request)
        fb_response = await get_generic_template(user_id, elements)
        await send_response_to_user(
            client_session,
            fb_response,
            config_dict["facebook-messenger"]["page-access-token"]
        )

        await client_session.close()

        return aiohttp.web.Response(text='')

    def add_routes(the_app):
        the_app.router.add_get('/', hub)
        the_app.router.add_post('/', hot_viral)

    add_routes(aiohttp_app)
    return aiohttp_app


"""
Starting the app!
"""
app = make_app(
    aiohttp.web.Application(loop=asyncio.get_event_loop()),
    config()
)
