import pytest
import aiohttp.web
import app
from config import config
from mock import mock_open, patch

PAGE_ACCESS_TOKEN = "page_access_token_test"
VERIFY_TOKEN = "verify_token_test"
CLIENT_ID = "client_id_test"


@pytest.fixture
def cli(loop, test_client):
    fake_yml_config = f"""facebook-messenger:
  page-access-token: {PAGE_ACCESS_TOKEN}
  verify-token: {VERIFY_TOKEN}
  
imgur:
  client-id: {CLIENT_ID}
    """

    with patch("builtins.open", mock_open(read_data=fake_yml_config)):
        test_app = app.make_app(
            aiohttp.web.Application(loop=loop),
            config()
        )
        return loop.run_until_complete(test_client(test_app))
