import yaml


def config():
    with open("config.yml", "r") as f:
        config_dict = yaml.load(f)
        validate_config(config_dict)
        return config_dict


def validate_config(config_dict):
    facebook_messenger = config_dict.get("facebook-messenger")
    if (
        not facebook_messenger or
        not facebook_messenger.get("page-access-token") or
        not facebook_messenger.get("verify-token")
    ):
        raise InvalidConfigException()


class InvalidConfigException(Exception):
    pass
