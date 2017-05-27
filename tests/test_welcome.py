import aiohttp.test_utils
import unittest.mock
import aiohttp.client
import settings
import conftest
import tests.data
import tests.utils
import asynctest
import json
import actions


def mocked_get_requests(*args, **kwargs):
    class ClientResponseMock:
        def __init__(self, status_code):
            self.status = status_code

        @staticmethod
        async def json():
            return tests.data.imgur_api_response_example

    return ClientResponseMock(200)


async def test_hot_viral(cli: aiohttp.test_utils.TestClient):
    mocked_post = asynctest.CoroutineMock()
    mocked_get = asynctest.CoroutineMock(side_effect=mocked_get_requests)
    aiohttp.client.ClientSession.post: unittest.mock.Mock() = mocked_post
    aiohttp.client.ClientSession.get: unittest.mock.Mock() = mocked_get

    payload = await tests.utils.make_postback("GET_STARTED_PAYLOAD")
    response = await cli.post('/', json=payload)

    imgur_call = unittest.mock.call(
        "https://api.imgur.com/3/gallery/hot/viral/0.json",
        headers={
            "Authorization": f"Client-ID {conftest.CLIENT_ID}"
        }
    )
    mocked_get.assert_has_calls(
        [imgur_call],
        any_order=True
    )

    welcome_message = unittest.mock.call(
        settings.get_me_message_url(conftest.PAGE_ACCESS_TOKEN),
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "recipient": {
                "id": "1234567891011121"
            },
            "message": {
                "text": actions.welcome_message
            }
        })
    )
    use_the_menu = unittest.mock.call(
        settings.get_me_message_url(conftest.PAGE_ACCESS_TOKEN),
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "recipient": {
                "id": "1234567891011121"
            },
            "message": {
                "text": actions.use_the_menu
            }
        })
    )
    example_introduction = unittest.mock.call(
        settings.get_me_message_url(conftest.PAGE_ACCESS_TOKEN),
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "recipient": {
                "id": "1234567891011121"
            },
            "message": {
                "text": actions.example_introduction
            }
        })
    )
    facebook_carrousel_call = unittest.mock.call(
        settings.get_me_message_url(conftest.PAGE_ACCESS_TOKEN),
        headers={'Content-Type': 'application/json'},
        data=json.dumps(tests.data.facebook_data_example)
    )
    mocked_post.assert_has_calls(
        [
            welcome_message,
            use_the_menu,
            example_introduction,
            facebook_carrousel_call
        ],
        any_order=True
    )

    assert response.status == 200
