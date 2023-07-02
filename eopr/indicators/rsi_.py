import dataclasses

from common import CandlePrice, FloatArray

RSIValues = FloatArray


@dataclasses.dataclass
class RSIParameters:
    prices: list[CandlePrice]
    period: int


def rsi(rsi_params: RSIParameters) -> RSIValues:
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
        avg_gain = (avg_gain * (rsi_params.period - 1) + gains[i]) / rsi_params.period
        avg_loss = (avg_loss * (rsi_params.period - 1) + losses[i]) / rsi_params.period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)

    return rsi_values


def interpret_rsi(rsi_values: RSIValues, overbought: float, oversold: float) -> str:
    last_rsi = rsi_values[-1]
    if last_rsi > overbought:
        return (
            f"The RSI value is {last_rsi:.2f}, indicating that the asset is overbought."
        )
    elif last_rsi < oversold:
        return (
            f"The RSI value is {last_rsi:.2f}, indicating that the asset is oversold."
        )
    else:
        return (
            f"The RSI value is {last_rsi:.2f}, indicating that the asset is neither"
            " overbought nor oversold."
        )


if __name__ == "__main__":
    prices = [
        [30432.875, 30432.856, 30432.91, 30432.856, 30432.875],
        [30432.717, 30432.856, 30432.91, 30432.717, 30432.717],
        [30432.731, 30432.856, 30432.91, 30432.717, 30432.731],
        [30432.975, 30432.856, 30432.975, 30432.717, 30432.975],
        [30432.997, 30432.856, 30432.997, 30432.717, 30432.997],
        [30433.045, 30432.856, 30433.045, 30432.717, 30433.045],
        [30433.248, 30432.856, 30433.248, 30432.717, 30433.248],
        [30433.251, 30432.856, 30433.251, 30432.717, 30433.251],
        [30433.26, 30433.26, 30433.26, 30433.26, 30433.26],
        [30433.447, 30433.26, 30433.447, 30433.26, 30433.447],
        [30433.423, 30433.26, 30433.447, 30433.26, 30433.423],
        [30433.423, 30433.26, 30433.447, 30433.26, 30433.423],
        [30433.39, 30433.26, 30433.447, 30433.26, 30433.39],
        [30433.39, 30433.26, 30433.447, 30433.26, 30433.39],
        [30433.39, 30433.26, 30433.447, 30433.26, 30433.39],
        [30433.697, 30433.26, 30433.697, 30433.26, 30433.697],
        [30433.697, 30433.26, 30433.697, 30433.26, 30433.697],
        [30433.696, 30433.26, 30433.697, 30433.26, 30433.696],
    ]
    rsi_params = RSIParameters(prices, 14)
    rsi_values = rsi(rsi_params)
    rsi_interpretation = interpret_rsi(rsi_values, 70, 30)
    print(rsi_interpretation)
