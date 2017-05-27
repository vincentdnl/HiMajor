import aiohttp.test_utils
import unittest.mock
import aiohttp.client
import settings
import conftest
import asynctest
import json
import actions
import tests.utils


async def test_hot_viral(cli: aiohttp.test_utils.TestClient):
    mocked_post = asynctest.CoroutineMock()
    aiohttp.client.ClientSession.post: unittest.mock.Mock() = mocked_post

    payload = await tests.utils.make_postback("DEFINITELY_NOT_AN_EXPECTED_PAYLOAD")
    response = await cli.post('/', json=payload)

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

    mocked_post.assert_has_calls(
        [
            use_the_menu
        ],
        any_order=True
    )

    assert response.status == 200
