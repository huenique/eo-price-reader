import io
import json
import os
import typing

import rel
import websocket
from dotenv import load_dotenv
from websocket._app import WebSocketApp


def on_message(ws: WebSocketApp, message: bytes, msg_io: io.TextIOWrapper) -> None:
    # decode the message and save to a file using msg_io
    msg = json.loads(message)
    if msg["action"] == "candles":
        msg_io.write(str(msg) + "\n")
        msg_io.flush()


def on_error(ws: WebSocketApp, error: str) -> None:
    print(f"Error: {error}")


def on_close(ws: WebSocketApp, close_status_code: str, close_msg: str) -> None:
    print(f"Closed: {close_msg=}, {close_status_code=}")


def on_open(ws: WebSocketApp, token: str) -> None:
    messages: typing.Any = [
        {
            "action": "setContext",
            "message": {"is_demo": 1},
            "token": token,
            "ns": 1,
        },
        {
            "action": "multipleAction",
            "message": {
                "actions": [
                    {
                        "action": "userGroup",
                        "ns": 1,
                        "token": token,
                    },
                    {
                        "action": "profile",
                        "ns": 2,
                        "token": token,
                    },
                    {
                        "action": "assets",
                        "message": {"mode": ["vanilla"], "subscribeMode": ["vanilla"]},
                        "ns": 3,
                        "token": token,
                    },
                    {
                        "action": "getCurrency",
                        "ns": 4,
                        "token": token,
                    },
                    {
                        "action": "getCountries",
                        "ns": 5,
                        "token": token,
                    },
                    {
                        "action": "environment",
                        "ns": 6,
                        "token": token,
                    },
                    {
                        "action": "defaultSubscribeCandles",
                        "message": {"modes": ["vanilla"], "timeframes": [0, 5]},
                        "ns": 7,
                        "token": token,
                    },
                    {
                        "action": "setTimeZone",
                        "message": {"timeZone": 480},
                        "ns": 8,
                        "token": token,
                    },
                    {
                        "action": "getCandlesTimeframes",
                        "ns": 9,
                        "token": token,
                    },
                    {
                        "action": "referralOfferInfo",
                        "ns": 10,
                        "token": token,
                    },
                ]
            },
            "token": token,
            "ns": 2,
        },
        {
            "action": "setContext",
            "message": {"is_demo": 1},
            "token": token,
            "ns": 1,
        },
        {
            "action": "multipleAction",
            "message": {
                "actions": [
                    {
                        "action": "userGroup",
                        "ns": 1,
                        "token": token,
                    },
                    {
                        "action": "profile",
                        "ns": 2,
                        "token": token,
                    },
                    {
                        "action": "assets",
                        "message": {
                            "mode": ["vanilla"],
                            "subscribeMode": ["vanilla"],
                        },
                        "ns": 3,
                        "token": token,
                    },
                    {
                        "action": "getCurrency",
                        "ns": 4,
                        "token": token,
                    },
                    {
                        "action": "getCountries",
                        "ns": 5,
                        "token": token,
                    },
                    {
                        "action": "environment",
                        "ns": 6,
                        "token": token,
                    },
                    {
                        "action": "defaultSubscribeCandles",
                        "message": {
                            "modes": ["vanilla"],
                            "timeframes": [0, 5],
                        },
                        "ns": 7,
                        "token": token,
                    },
                    {
                        "action": "setTimeZone",
                        "message": {"timeZone": 480},
                        "ns": 8,
                        "token": token,
                    },
                    {
                        "action": "getCandlesTimeframes",
                        "ns": 9,
                        "token": token,
                    },
                    {
                        "action": "referralOfferInfo",
                        "ns": 10,
                        "token": token,
                    },
                ]
            },
            "token": token,
            "ns": 2,
        },
        {
            "action": "pong",
            "message": {"data": "1688169369371"},
            "token": token,
            "ns": 3,
        },
        {
            "action": "multipleAction",
            "message": {
                "actions": [
                    {
                        "action": "openOptions",
                        "ns": 1,
                        "token": token,
                    },
                    {
                        "action": "tradeHistory",
                        "message": {
                            "index_from": 0,
                            "count": 20,
                            "is_demo": 1,
                        },
                        "ns": 2,
                        "token": token,
                    },
                    {
                        "action": "tradeHistory",
                        "message": {
                            "index_from": 0,
                            "count": 20,
                            "is_demo": 0,
                        },
                        "ns": 3,
                        "token": token,
                    },
                ]
            },
            "token": token,
            "ns": 4,
        },
        {
            "action": "historySteps",
            "token": token,
            "ns": 5,
        },
        {
            "action": "expertUnsubscribe",
            "token": token,
            "ns": 6,
        },
        {
            "action": "registerNewDeviceToken",
            "message": {
                "token": "exdJ08q9E2amowx2SrYcUd:APA91bHZOcoRT4nHvDn8lXRKYAwdJr7kXh249YGsmEU4vcp6xaIUNexCQNjwe7RgEICE_COmcpT2ZCGTgt7-7MVFId84IqI_EsPGlkVl7YCm3LnVkHM8_fIuCsfcpQb7zfG3xNEOvbtD",
                "token_type": "web_fcm",
            },
            "token": token,
            "ns": 7,
        },
        {
            "action": "assetHistoryCandles",
            "message": {
                "assetid": 160,
                "periods": [[1688165120, 1688170235]],
                "timeframes": [5],
            },
            "token": token,
            "ns": 8,
        },
    ]

    for message in messages:
        ws.send(json.dumps(message))


def main(url: str, token: str, msg_io: io.TextIOWrapper) -> None:
    websocket.enableTrace(True)  # type: ignore

    def _on_open(ws: WebSocketApp) -> None:
        return on_open(ws, token)

    def _on_message(ws: WebSocketApp, message: bytes) -> None:
        return on_message(ws, message, msg_io)

    ws = WebSocketApp(
        url,
        on_open=_on_open,
        on_message=_on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel, reconnect=5)  # type: ignore
    rel.signal(2, rel.abort)  # type: ignore
    rel.dispatch()  # type: ignore


if __name__ == "__main__":
    load_dotenv()
    eo_url = os.getenv("EO_URL")
    eo_token = os.getenv("EO_TOKEN")

    # Open a reusable file object and redirect stdout there so that we can store ws
    # messages for later
    msg_io = open("output.txt", "w")

    try:
        assert eo_url is not None and eo_url != ""
        assert eo_token is not None and eo_token != ""
    except AssertionError as e:
        raise ValueError("Please set EO_URL and EO_TOKEN environment variables") from e

    main(
        url=eo_url,
        token=eo_token,
        msg_io=msg_io,
    )
