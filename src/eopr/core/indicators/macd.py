import typing

import pydantic

from eopr import errors
from eopr.core.indicators.common import CandlePrice, FloatArray, TrendAnalysis

MACDLine = FloatArray
SignalLine = FloatArray
Histogram = FloatArray
Interpretation = str


class MACDParameters(pydantic.BaseModel):
    prices: list[CandlePrice]
    fast: int
    slow: int
    signal: int
    err_handler: typing.Callable[[Exception], None] = pydantic.Field(
        default=errors.default_error_callback, exclude=True
    )


class MACDIndicator(pydantic.BaseModel):
    macd_line: MACDLine
    signal_line: SignalLine
    histogram: Histogram
    analysis: TrendAnalysis
    err_handler: typing.Callable[[Exception], None] = pydantic.Field(
        default=errors.default_error_callback, exclude=True
    )


def ema(prices: FloatArray, period: int) -> FloatArray:
    alpha = 2 / (period + 1)
    ema = [prices[0]]
    for price in prices[1:]:
        ema.append(price * alpha + ema[-1] * (1 - alpha))

    return ema


def macd(macd_params: MACDParameters) -> MACDIndicator:
    @errors.error_handler(macd_params.err_handler)
    def _macd(macd_params: MACDParameters):
        close_prices = [candle[4] for candle in macd_params.prices]
        macd_line = [
            fast_ema - slow_ema
            for fast_ema, slow_ema in zip(
                ema(close_prices, macd_params.fast), ema(close_prices, macd_params.slow)
            )
        ]
        signal_line = ema(macd_line, macd_params.signal)
        histogram = [macd - signal for macd, signal in zip(macd_line, signal_line)]

        return MACDIndicator(
            macd_line=macd_line,
            signal_line=signal_line,
            histogram=histogram,
            analysis=TrendAnalysis(bullish=False, bearish=False),
        )

    return _macd(macd_params)


def interpret_macd(macd: MACDIndicator) -> MACDIndicator:
    """Interpret the MACD indicator.

    This function takes as input the MACD line, the signal line, and the histogram. It
    determines the trends of these lines by comparing their last two values. If the last
    value is greater than the second-to-last value, the trend is considered to be
    “rising”. Otherwise, it is considered to be “falling”.

    The function also calculates the distance between the MACD and signal lines by
    taking the absolute value of their difference. This distance can be used to gauge
    the strength of the current trend.

    Finally, the function returns a string that describes the current trends of the MACD
    line, signal line, and histogram. This string includes information about whether
    these lines are rising or falling, as well as information about the distance between
    the MACD and signal lines.

    Args:
        macd_line (FloatArray): The MACD line values.
        signal_line (FloatArray): The signal line values.
        histogram (FloatArray): The histogram values.

    Returns:
        str: The interpretation of the MACD indicator.
    """

    @errors.error_handler(macd.err_handler)
    def _interpret_macd(macd: MACDIndicator):
        macd_trend = "rising" if macd.macd_line[-1] > macd.macd_line[-2] else "falling"
        signal_trend = (
            "rising" if macd.signal_line[-1] > macd.signal_line[-2] else "falling"
        )
        histogram_trend = (
            "rising" if macd.histogram[-1] > macd.histogram[-2] else "falling"
        )
        distance = abs(macd.macd_line[-1] - macd.signal_line[-1])

        if macd_trend == signal_trend:
            trend = f"The MACD and signal lines are both {macd_trend}."
        else:
            trend = (
                f"The MACD line is {macd_trend} "
                "while the signal line is {signal_trend}."
            )

        trend += f" The distance between the MACD and signal lines is {distance:.2f}."

        if histogram_trend == "rising":
            trend += " The histogram is rising, indicating increasing bullish momentum."
        else:
            trend += (
                " The histogram is falling, indicating increasing bearish momentum."
            )

        macd.analysis = TrendAnalysis(
            bullish=macd_trend == "rising",
            bearish=macd_trend == "falling",
            interpretation=trend,
        )

        return macd

    return _interpret_macd(macd)


# if __name__ == "__main__":
#     # Example usage
#     prices = [
#         [30432.875, 30432.856, 30432.91, 30432.856, 30432.875],
#         [30432.717, 30432.856, 30432.91, 30432.717, 30432.717],
#         [30432.731, 30432.856, 30432.91, 30432.717, 30432.731],
#         [30432.975, 30432.856, 30432.975, 30432.717, 30432.975],
#         [30432.997, 30432.856, 30432.997, 30432.717, 30432.997],
#         [30433.045, 30432.856, 30433.045, 30432.717, 30433.045],
#         [30433.248, 30432.856, 30433.248, 30432.717, 30433.248],
#         [30433.251, 30432.856, 30433.251, 30432.717, 30433.251],
#         [30433.26, 30433.26, 30433.26, 30433.26, 30433.26],
#         [30433.447, 30433.26, 30433.447, 30433.26, 30433.447],
#         [30433.423, 30433.26, 30433.447, 30433.26, 30433.423],
#         [30433.423, 30433.26, 30433.447, 30433.26, 30433.423],
#         [30433.39, 30433.26, 30433.447, 30433.26, 30433.39],
#         [30433.39, 30433.26, 30433.447, 30433.26, 30433.39],
#         [30433.39, 30433.26, 30433.447, 30433.26, 30433.39],
#         [30433.697, 30433.26, 30433.697, 30433.26, 30433.697],
#         [30433.697, 30433.26, 30433.697, 30433.26, 30433.697],
#         [30433.696, 30433.26, 30433.697, 30433.26, 30433.696],
#     ]
#     fast = 12
#     slow = 26
#     signal = 9
#     macd_params = MACDParameters(prices=prices, fast=fast, slow=slow, signal=signal)
#     macd_indicator = macd(macd_params)
#     macd_indicator = interpret_macd(macd_indicator)
#     print(macd_indicator)
#     print(macd_indicator)
