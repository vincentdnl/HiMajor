import aiohttp.test_utils
import conftest


async def test_hub(cli: aiohttp.test_utils.TestClient):
    hub_challenge = '123456789abc'
    payload = {'hub.challenge': hub_challenge, 'hub.verify_token': conftest.VERIFY_TOKEN}

    response = await cli.get('/', params=payload)
    assert response.status == 200
    assert await response.text() == hub_challenge


async def test_no_payload_hub(cli: aiohttp.test_utils.TestClient):
    response = await cli.get('/')
    assert response.status == 200
    assert await response.text() == ''


async def test_invalid_verify_token_hub(cli: aiohttp.test_utils.TestClient):
    hub_challenge = '123456789abc'
    payload = {'hub.challenge': hub_challenge, 'hub.verify_token': 'INVALID_TOKEN'}

    response = await cli.get('/', params=payload)
    assert response.status == 200
    assert await response.text() == ''
