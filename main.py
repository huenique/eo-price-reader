import dataclasses
import io
import json
import os

from dotenv import load_dotenv

import eopr
from eopr.indicators import macd, rsi
from eopr.strategies import macd_rsi_crossover
from eopr.utils import candle_parser

# ----------------- Custom Strategy -----------------
CandleSeries = list[dict[str, float | list[float]]]
CandleExpTimes = list[list[int | list[list[float | int]]]]
CandleMessage = dict[str, int | CandleSeries | CandleExpTimes]
CandleData = dict[str, str | CandleMessage]


@dataclasses.dataclass
class Signal:
    """A signal for a buy or sell action.

    Attributes:
        buy (bool): True if a buy signal, False otherwise.
        sell (bool): True if a sell signal, False otherwise.
    """

    buy: bool
    sell: bool


@dataclasses.dataclass
class CandleChartContainer:
    """A container for candle chart data.

    Attributes:
        candles (list[float]): The candle chart data.
        signal (Signal): The signal for a buy or sell action.
    """

    candles: list[CandleData]
    signal: Signal


def analyze_candles(
    chart_container: CandleChartContainer, rsi_params: rsi.RSIParameters
) -> None:
    candles: list[list[float]] = []
    for candle_datum in chart_container.candles:
        candles.append(candle_parser.parse_candles_data(candle_datum))

    rsi_params.prices = candles
    rsi_ = rsi.rsi(rsi_params)
    rsi_.overbought = 50
    rsi_.oversold = 50
    macd_params = macd.MACDParameters(
        prices=candles,
        fast=12,
        slow=26,
        signal=9,
    )
    macd_ = macd.macd(macd_params)

    # Using built-in strategy
    trade_signal = macd_rsi_crossover.trade(rsi_, macd_)
    chart_container.signal.buy = trade_signal.buy
    chart_container.signal.sell = trade_signal.sell

    if trade_signal.buy:
        print("BUY")

    print("\033c", end="")
    print("-" * 80)
    print("Buy" if trade_signal.buy else "Sell" if trade_signal.sell else "---")
    print("-" * 80)


def my_strategy(
    message: bytes,
    chart_container: CandleChartContainer,
    rsi_params: rsi.RSIParameters,
    msg_io: io.TextIOWrapper | None = None,
):
    parsed_msg = json.loads(message)
    if parsed_msg["action"] == "candles":
        chart_container.candles.append(parsed_msg)

        # Prevent the list from growing too large
        if len(chart_container.candles) >= (rsi_params.period * 3):
            chart_container.candles = chart_container.candles[rsi_params.period - 1 :]

        if msg_io is not None:
            msg_io.write(str(parsed_msg) + "\n")
            msg_io.flush()

    analyze_candles(chart_container, rsi_params)


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
    signal = Signal(buy=False, sell=False)
    chart_container = CandleChartContainer(signal=signal, candles=[])
    rsi_params = rsi.RSIParameters(prices=[], period=14)

    eopr.reader(
        eopr.ReaderParams(
            url=eo_url,
            token=eo_token,
            on_message_strategy=lambda message: my_strategy(
                message,
                chart_container,
                rsi_params,
                # msg_io,
            ),
        )
    )
