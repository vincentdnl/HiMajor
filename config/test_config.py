import config
from mock import mock_open, patch


def test_valid_config_file():
    fake_yml_config = """facebook-messenger:
  page-access-token: page_access_token_test
  verify-token: verify_token_test
  
imgur:
  client-id: client_id_test
    """

    with patch("builtins.open", mock_open(read_data=fake_yml_config)):
        config_dict = config.config()
        facebook_messenger = config_dict.get("facebook-messenger")
        assert facebook_messenger
        assert facebook_messenger.get("page-access-token") == "page_access_token_test"
        assert facebook_messenger.get("verify-token") == "verify_token_test"
        imgur = config_dict.get("imgur")
        assert imgur
        assert imgur.get("client-id") == "client_id_test"
