import logging.handlers


"""
Facebook Messenger API settings
"""
GRAPH_BASE_URL = 'https://graph.facebook.com'
VERSION = 'v2.6'


def get_me_message_url(access_token):
    return f"{GRAPH_BASE_URL}/{VERSION}/me/messages?access_token={access_token}"


def get_me_messenger_profile_url(access_token):
    return f"{GRAPH_BASE_URL}/{VERSION}/me/messenger_profile?access_token={access_token}"


"""
Imgur API settings
"""
async def get_imgur_hot_viral_url():
    return "https://api.imgur.com/3/gallery/hot/viral/0.json"


"""
Logger settings
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(
    'logs/app.log', mode='a', maxBytes=100000, backupCount=5, encoding='UTF-8', delay=0
)
handler.setFormatter(formatter)
logger.addHandler(handler)
