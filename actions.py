import aiohttp.web
import client_requests
import imgur_api
import messenger_send_api


welcome_message = "Hi, I'm HiMajor, a bot who sends Imgur content right to you via Messenger! :)"
use_the_menu = "You can use the menu to get the content anytime!"
example_introduction = "Here is an example of what I can do..."


async def hot_viral(user_id, client_session, config_dict):
    json_response: dict = await client_requests.get_hot_viral_content(
        client_session,
        config_dict["imgur"]["client-id"]
    )
    if not json_response:
        await client_session.close()
        return aiohttp.web.Response(text='')

    elements: tuple = await imgur_api.extract_elements_from_response(json_response)
    if not elements:
        await client_session.close()
        return aiohttp.web.Response(text='')

    fb_response = await messenger_send_api.get_generic_template(user_id, elements)
    await client_requests.send_response_to_user(
        client_session,
        fb_response,
        config_dict["facebook-messenger"]["page-access-token"]
    )


async def welcome(user_id, client_session, config_dict):
    await client_requests.send_response_to_user(
        client_session,
        await messenger_send_api.get_text_message(user_id, welcome_message),
        config_dict["facebook-messenger"]["page-access-token"]
    )
    await client_requests.send_response_to_user(
        client_session,
        await messenger_send_api.get_text_message(user_id, use_the_menu),
        config_dict["facebook-messenger"]["page-access-token"]
    )
    await client_requests.send_response_to_user(
        client_session,
        await messenger_send_api.get_text_message(user_id, example_introduction),
        config_dict["facebook-messenger"]["page-access-token"]
    )
    await hot_viral(user_id, client_session, config_dict)


async def default(user_id, client_session, config_dict):
    await client_requests.send_response_to_user(
        client_session,
        await messenger_send_api.get_text_message(user_id, use_the_menu),
        config_dict["facebook-messenger"]["page-access-token"]
    )
