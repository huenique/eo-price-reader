import datetime
import json
import typing

import pydantic
from websocket._app import WebSocketApp


def on_message(
    ws: WebSocketApp,
    message: bytes,
    strategy_handler: typing.Callable[[WebSocketApp, typing.Any], typing.Any],
) -> None:
    strategy_handler(ws, message)


def on_error(ws: WebSocketApp, error: str) -> None:
    print(f"Error: {error}")


def on_close(ws: WebSocketApp, close_status_code: str, close_msg: str) -> None:
    print(f"Closed: {close_msg=}, {close_status_code=}")


def on_open(ws: WebSocketApp, token: str, device_token: str, asset_id: int) -> None:
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
                "token": device_token,
                "token_type": "web_fcm",
            },
            "token": token,
            "ns": 7,
        },
        {
            "action": "assetHistoryCandles",
            "message": {
                "assetid": asset_id,
                "periods": [
                    [
                        int(datetime.datetime.now().timestamp()),
                        int(datetime.datetime.now().timestamp()) + 5400,
                    ]
                ],
                "timeframes": [5],
            },
            "token": token,
            "ns": 8,
        },
    ]

    for message in messages:
        ws.send(json.dumps(message))


class ReaderParams(pydantic.BaseModel):
    url: str
    token: str
    device_token: str
    asset_id: int
    on_message_strategy: typing.Callable[[WebSocketApp, bytes], typing.Any]


def read(
    main_args: ReaderParams,
) -> None:
    def _on_open(ws: WebSocketApp) -> None:
        return on_open(ws, main_args.token, main_args.device_token, main_args.asset_id)

    def _on_message(ws: WebSocketApp, message: bytes) -> None:
        return on_message(ws, message, main_args.on_message_strategy)

    ws = WebSocketApp(
        main_args.url,
        on_open=_on_open,
        on_message=_on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(reconnect=5)  # type: ignore
