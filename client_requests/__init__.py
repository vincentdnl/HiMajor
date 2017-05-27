import json
import settings


async def get_hot_viral_content(client_session, client_id):
    response = await client_session.get(
        await settings.get_imgur_hot_viral_url(),
        headers={
            "Authorization": f"Client-ID {client_id}"
        })

    response_json = await response.json()
    log_response("IMGUR GET", response.status, response_json)
    assert response.status == 200
    return response_json


async def send_response_to_user(client_session, fb_response, page_access_token):
    response = await client_session.post(
        settings.get_me_message_url(page_access_token),
        headers={'Content-Type': 'application/json'},
        data=json.dumps(fb_response)
    )

    response_json = await response.json()
    log_response("MESSENGER POST", response.status, response_json)
    return response_json


def log_response(name, status, response_json):
    try:
        response_string = json.dumps(response_json)
        response_string = response_string if len(response_string) < 200 else response_string[:200] + "..."
        settings.logger.info(f"[{name}][{status}] {response_string}")
    except TypeError as e:
        settings.logger.info(f"[{name}] {e}")

