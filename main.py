import dataclasses
import io
import json
import os

from dotenv import load_dotenv

import eopr
from eopr.indicators import rsi
from eopr.utils import candle_parser

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


def analyze_candles(
    chartContainer: CandleChartContainer, rsiParams: rsi.RSIParameters
) -> None:
    candles: list[list[float]] = []
    for candle_datum in chartContainer.candles:
        candles.append(candle_parser.parse_candles_data(candle_datum))

    rsiParams.prices = candles
    rsi_ = rsi.rsi(rsiParams)
    rsi_.overbought = 70
    rsi_.oversold = 30
    result = rsi.interpret_rsi(rsi_)

    print(result.model_dump_json())
    print("-" * 50)


def my_strategy(
    message: bytes,
    chartContainer: CandleChartContainer,
    period: int,
    rsiParams: rsi.RSIParameters,
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
    rsiParams = rsi.RSIParameters(prices=[], period=period)

    eopr.reader(
        eopr.ReaderParams(
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
