import dataclasses
import io
import json
import os
import typing

import rel
from dotenv import load_dotenv
from utils import candle_parser
from websocket._app import WebSocketApp

from eopr.indicators import rsi


def on_message(
    ws: WebSocketApp,
    message: bytes,
    strategy_handler: typing.Callable[[typing.Any], typing.Any],
) -> None:
    strategy_handler(message)


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
                "token": (
                    "exdJ08q9E2amowx2SrYcUd:"
                    "APA91bHZOcoRT4nHvDn8lXRKYAwdJr7kXh249YGsmEU4vcp6xaIUNexCQNjwe7RgEICE_COmcpT2ZCGTgt7-7MVFId84IqI_EsPGlkVl7YCm3LnVkHM8_fIuCsfcpQb7zfG3xNEOvbtD"
                ),
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


@dataclasses.dataclass
class MainArgs:
    url: str
    token: str
    on_message_strategy: typing.Callable[[bytes], typing.Any]


def main(
    main_args: MainArgs,
) -> None:
    def _on_open(ws: WebSocketApp) -> None:
        return on_open(ws, main_args.token)

    def _on_message(ws: WebSocketApp, message: bytes) -> None:
        return on_message(ws, message, main_args.on_message_strategy)

    ws = WebSocketApp(
        main_args.url,
        on_open=_on_open,
        on_message=_on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel, reconnect=5)  # type: ignore
    rel.signal(2, rel.abort)  # type: ignore
    rel.dispatch()  # type: ignore


# ----------------- Custom Strategy -----------------
CandleSeries = list[dict[str, float | list[float]]]
CandleExpTimes = list[list[int | list[list[float | int]]]]
CandleMessage = dict[str, int | CandleSeries | CandleExpTimes]
CandleData = dict[str, str | CandleMessage]


@dataclasses.dataclass
class CandleChartContainer:
    """A container for candle chart data.

    Attributes:
        candles (list[float]): The candle chart data.
    """

    candles: list[CandleData]


@dataclasses.dataclass
class RSIParams:
    """A container for Relative Strength Index parameters.

    Attributes:
        period (int): The period.
        overbought (int): The overbought value.
        oversold (int): The oversold value.
    """

    period: int
    overbought: int
    oversold: int


def analyze_candles(chartContainer: CandleChartContainer, rsiParams: RSIParams) -> None:
    candles: list[list[float]] = []
    for candle_datum in chartContainer.candles:
        candles.append(candle_parser.parse_candles_data(candle_datum))

    rsi_ = rsi.calculate_rsi(candles, rsiParams.period)
    result = rsi.analyze_rsi(rsi_, rsiParams.overbought, rsiParams.oversold)
    print(f"RSI: {rsi:.2f}, {result}")
    print("-" * 50)


def my_strategy(
    message: bytes,
    chartContainer: CandleChartContainer,
    period: int,
    rsiParams: RSIParams,
    msg_io: io.TextIOWrapper | None = None,
):
    parsed_msg = json.loads(message)
    if parsed_msg["action"] == "candles":
        chartContainer.candles.append(parsed_msg)

        if len(chartContainer.candles) >= (period * 2):
            chartContainer.candles = chartContainer.candles[period - 1 :]

        if msg_io is not None:
            msg_io.write(str(parsed_msg) + "\n")
            msg_io.flush()

    analyze_candles(chartContainer, rsiParams)


if __name__ == "__main__":
    load_dotenv()
    eo_url = os.getenv("EO_URL")
    eo_token = os.getenv("EO_TOKEN")

    try:
        assert eo_url is not None and eo_url != ""
        assert eo_token is not None and eo_token != ""
    except AssertionError as e:
        raise ValueError("Please set EO_URL and EO_TOKEN environment variables") from e

    # Open a reusable file object and redirect stdout there so that we can store ws
    # messages for later
    # msg_io = open("output.txt", "w")
    period = 14
    chartContainer = CandleChartContainer(candles=[])
    rsiParams = RSIParams(period=period, overbought=70, oversold=30)

    main(
        MainArgs(
            url=eo_url,
            token=eo_token,
            on_message_strategy=lambda message: my_strategy(
                message,
                chartContainer,
                period,
                rsiParams,
                # msg_io,
            ),
        )
    )
