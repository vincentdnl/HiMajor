import logging.handlers

"""
Facebook Messenger API configurations
"""
GRAPH_BASE_URL = 'https://graph.facebook.com'
VERSION = 'v2.6'


def get_me_message_url(access_token):
    return f"{GRAPH_BASE_URL}/{VERSION}/me/messages?access_token={access_token}"


"""
Logger configurations
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(
    'logs/app.log', mode='a', maxBytes=100000, backupCount=5, encoding='UTF-8', delay=0
)
handler.setFormatter(formatter)
logger.addHandler(handler)
