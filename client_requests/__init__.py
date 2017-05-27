import json
import settings


async def get_hot_viral_content(client_session, client_id):
    response = await client_session.get(
        await settings.get_imgur_hot_viral_url(),
        headers={
            "Authorization": f"Client-ID {client_id}"
        })

    assert response.status == 200
    return await response.json()


async def send_response_to_user(client_session, fb_response, page_access_token):
    response = await client_session.post(
        settings.get_me_message_url(page_access_token),
        headers={'Content-Type': 'application/json'},
        data=json.dumps(fb_response)
    )
    return await response.json()
