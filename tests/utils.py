async def make_postback(payload):
    return {
        "object": "page",
        "entry": [
            {
                "id": "123456789101112",
                "time": 1458692752478,
                "messaging": [
                    {
                        "sender": {
                            "id": "1234567891011121"
                        },
                        "recipient": {
                            "id": "123456789101112"
                        },
                        "postback": {
                            "payload": payload
                        }
                    }
                ]
            }
        ]
    }
