import typing

import pydantic

from eopr import errors
from eopr.core.indicators.common import CandlePrice, FloatArray, TrendAnalysis

RSIValues = FloatArray
Interpretation = str


class RSIParameters(pydantic.BaseModel):
    prices: list[CandlePrice]
    period: int
    err_handler: typing.Callable[[Exception], None] = pydantic.Field(
        default=errors.default_error_callback, exclude=True
    )


class RSIIndicator(pydantic.BaseModel):
    rsi_values: RSIValues
    overbought: float
    oversold: float
    analysis: TrendAnalysis
    err_handler: typing.Callable[[Exception], None] = pydantic.Field(
        default=errors.default_error_callback, exclude=True
    )


def rsi(rsi_params: RSIParameters) -> RSIIndicator:
    @errors.error_handler(rsi_params.err_handler)
    def _rsi(rsi_params: RSIParameters):
        close_prices = [candle[4] for candle in rsi_params.prices]
        changes = [
            close_prices[i] - close_prices[i - 1] for i in range(1, len(close_prices))
        ]
        gains = [change if change > 0 else 0 for change in changes]
        losses = [-change if change < 0 else 0 for change in changes]
        avg_gain = sum(gains[: rsi_params.period]) / rsi_params.period
        avg_loss = sum(losses[: rsi_params.period]) / rsi_params.period
        rsi_values: list[float] = []

        for i in range(rsi_params.period, len(changes)):
            avg_gain = (
                avg_gain * (rsi_params.period - 1) + gains[i]
            ) / rsi_params.period
            avg_loss = (
                avg_loss * (rsi_params.period - 1) + losses[i]
            ) / rsi_params.period
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)

        return RSIIndicator(
            rsi_values=rsi_values,
            overbought=70,
            oversold=30,
            analysis=TrendAnalysis(bullish=False, bearish=False),
            err_handler=rsi_params.err_handler,
        )

    return _rsi(rsi_params)


def interpret_rsi(rsi_indicator: RSIIndicator) -> RSIIndicator:
    @errors.error_handler(rsi_indicator.err_handler)
    def _interpret_rsi(rsi_indicator: RSIIndicator):
        last_rsi = rsi_indicator.rsi_values[-1]
        if last_rsi > rsi_indicator.overbought:
            rsi_indicator.analysis = TrendAnalysis(
                bullish=False,
                bearish=True,
                interpretation=(
                    f"The RSI value is {last_rsi:.2f}, "
                    "indicating that the asset is overbought."
                ),
            )
        elif last_rsi < rsi_indicator.oversold:
            rsi_indicator.analysis = TrendAnalysis(
                bullish=True,
                bearish=False,
                interpretation=(
                    f"The RSI value is {last_rsi:.2f}, "
                    "indicating that the asset is oversold."
                ),
            )
        else:
            rsi_indicator.analysis = TrendAnalysis(
                bullish=False,
                bearish=False,
                interpretation=(
                    f"The RSI value is {last_rsi:.2f}, "
                    "indicating that the asset is neither overbought nor oversold."
                ),
            )

        return rsi_indicator

    return _interpret_rsi(rsi_indicator)


# if __name__ == "__main__":
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
#     rsi_params = RSIParameters(prices, 14)
#     rsi_indicator = rsi(rsi_params)
#     rsi_indicator.overbought = 70
#     rsi_indicator.oversold = 30
#     rsi_interpretation = interpret_rsi(rsi_indicator)
#     print(rsi_interpretation)
#     rsi_interpretation = interpret_rsi(rsi_indicator)
#     print(rsi_interpretation)
