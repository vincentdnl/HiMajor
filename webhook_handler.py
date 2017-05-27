from aiohttp.web_request import Request


async def extract_data_from_request(request: Request):
    request_json = await request.json()

    entry = request_json.get('entry')
    if not entry:
        return

    for one_entry in entry:
        return await handle_one_entry(one_entry)


async def handle_one_entry(one_entry):
    messaging = one_entry.get('messaging')

    if not messaging:
        return

    for one_messaging in messaging:
        return await handle_one_messaging(one_messaging)


async def handle_one_messaging(one_messaging):
    sender = one_messaging.get('sender')
    if not sender:
        return
    user_id = sender.get('id')
    if not user_id:
        return

    recipient = one_messaging.get('recipient')
    if not recipient:
        return
    page_id = recipient.get('id')
    if not page_id:
        return

    if 'message' in one_messaging:
        return await handle_messaging_message(one_messaging, page_id, user_id)

    if 'postback' in one_messaging:
        return await handle_messaging_postback(one_messaging, page_id, user_id)


async def handle_messaging_message(one_messaging, page_id, user_id):
    user_text = one_messaging['message'].get('text')
    if not user_text:
        return

    is_echo = one_messaging['message'].get('is_echo')
    if not is_echo:
        return page_id, user_id, user_text


async def handle_messaging_postback(one_messaging, page_id, user_id):
    user_postback = one_messaging['postback'].get('payload')
    if not user_postback:
        return

    return page_id, user_id, user_postback
