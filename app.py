import asyncio
import aiohttp
import aiohttp.web
import aiohttp.web_request
import actions
import config
import webhook_handler


def make_app(aiohttp_app: aiohttp.web.Application, config_dict: dict) -> aiohttp.web.Application:
    async def hub(request: aiohttp.web_request.Request):
        hub_challenge = request.rel_url.query.get('hub.challenge')
        hub_verify_token = request.rel_url.query.get('hub.verify_token')
        config_verify_token = config_dict["facebook-messenger"]["verify-token"]

        if hub_verify_token == config_verify_token:
            return aiohttp.web.Response(text=hub_challenge)
        else:
            return aiohttp.web.Response(text='')

    async def dispatcher(request: aiohttp.web_request.Request):
        page_id, user_id, user_entry = await webhook_handler.extract_data_from_request(request)
        client_session = aiohttp.ClientSession(loop=aiohttp_app.loop)
        actions_mapping_dict = {
            "GET_STARTED_PAYLOAD": lambda: actions.welcome(user_id, client_session, config_dict),
            "HOT_VIRAL": lambda: actions.hot_viral(user_id, client_session, config_dict)
        }
        action = actions_mapping_dict.get(user_entry)
        if not action:
            await actions.default(user_id, client_session, config_dict)
        else:
            await action()
        await client_session.close()
        return aiohttp.web.Response(text='')

    def add_routes(the_app):
        the_app.router.add_get('/', hub)
        the_app.router.add_post('/', dispatcher)

    add_routes(aiohttp_app)
    return aiohttp_app


"""
Starting the app!
"""
app = make_app(
    aiohttp.web.Application(loop=asyncio.get_event_loop()),
    config.config()
)
