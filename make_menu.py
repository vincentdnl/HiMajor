import asyncio
import aiohttp
import settings
import config
import json


async def make_menu(loop):
    config_dict = config.config()
    access_token = config_dict["facebook-messenger"]["page-access-token"]

    client_session = aiohttp.ClientSession(loop=loop)

    response = await client_session.post(
        settings.get_me_messenger_profile_url(access_token),
        headers={"Content-Type": "application/json"},
        data=json.dumps(await get_payload_dict())
    )
    print(await response.json())

    client_session.close()


async def get_payload_dict():
    return {
        "get_started": {
            "payload": "GET_STARTED_PAYLOAD"
        },
        "persistent_menu": [
            {
                "locale": "default",
                "composer_input_disabled": True,
                "call_to_actions": [
                    await get_postback("Most Viral", "HOT_VIRAL")
                ]
            }
        ]
    }


async def get_postback(title, payload):
    return {
        "type": "postback",
        "title": title,
        "payload": payload
    }


"""
Making the menu!
"""
the_loop = asyncio.get_event_loop()
the_loop.run_until_complete(make_menu(the_loop))
the_loop.close()
