"""
Relative Strength Index (RSI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The RSI is a momentum oscillator that measures the speed and change of price movements.
RSI oscillates between zero and 100. Traditionally, and according to Wilder, RSI is
considered overbought when above 70 and oversold when below 30. Signals can also be
generated by looking for divergences, failure swings and centerline crossovers. RSI can
also be used to identify the general trend.
"""


def calculate_average_price_change(price_changes: list[float]):
    upward_changes = [change for change in price_changes if change > 0]
    downward_changes = [abs(change) for change in price_changes if change < 0]

    average_upward_change = (
        sum(upward_changes) / len(upward_changes) if len(upward_changes) > 0 else 0
    )
    average_downward_change = (
        abs(sum(downward_changes)) / len(downward_changes)
        if len(downward_changes) > 0
        else 0
    )

    return average_upward_change, average_downward_change


def calculate_rsi(candlestick_data: list[list[float]], period: int) -> float:
    if len(candlestick_data) < period:
        raise ValueError(
            (
                "Insufficient data for the specified period: "
                f"{len(candlestick_data)} candlesticks."
            )
        )

    price_changes: list[float] = []
    for i in range(1, len(candlestick_data)):
        current_close = candlestick_data[i][4]
        previous_close = candlestick_data[i - 1][4]
        price_change = current_close - previous_close
        price_changes.append(price_change)

    # Consider only the last 'period' price changes
    price_changes = price_changes[-period:]

    average_upward_change, average_downward_change = calculate_average_price_change(
        price_changes
    )
    rsi = 100 - (100 / (1 + (average_upward_change / average_downward_change)))

    return rsi


def analyze_rsi(rsi: float, overbought_level: float, oversold_level: float) -> str:
    if rsi > overbought_level:
        return "overbought"
    elif rsi < oversold_level:
        return "oversold"
    else:
        return "neutral"


if __name__ == "__main__":
    # Example usage
    candles = [
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
    period = 14
    overbought_level = 50
    oversold_level = 50

    rsi = calculate_rsi(candles, period)
    result = analyze_rsi(rsi, overbought_level, oversold_level)
    print(f"RSI: {rsi}, Result: {result}")