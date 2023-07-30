"""
eopr.strategies.macd_rsi_crossover
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MACD RSI Crossover Trading Strategy is a popular trading strategy that uses the
Moving Average Convergence Divergence (MACD) and Relative Strength Index (RSI)
indicators to identify buying and selling opportunities in the market. The MACD
indicator is used to identify the trend of the market while the RSI indicator is used to
identify whether an asset is overbought or oversold. When the MACD line crosses above 
the signal line and the RSI indicates that the asset is either overbought or oversold,
it can be a signal to buy or sell
"""

import pydantic

from ..indicators import macd, rsi


class TradeSignal(pydantic.BaseModel):
    """A model for market analysis.

    Attributes:
        action: (str): The action to take (Buy, Sell, or No trade signal).
    """

    buy: bool = pydantic.Field(default=False)
    sell: bool = pydantic.Field(default=False)


def check_macd_cross(macd_line: macd.MACDLine, signal_line: macd.SignalLine) -> bool:
    """Check if the MACD line crosses the signal line (bullish or bearish).

    Args:
        macd_line (list[float]): The MACD line.
        signal_line (list[float]): The MACD signal line.

    Returns:
        bool: True if the MACD line crosses the signal line, False otherwise.
    """
    return macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]


def check_rsi_overbought(rsi_values: rsi.RSIValues, overbought: float) -> bool:
    """Check if the RSI is overbought.

    Args:
        rsi_values (RSIValues): The RSI values.
        overbought (float): The overbought level.

    Returns:
        bool: True if the RSI is overbought, False otherwise.
    """
    return rsi_values[-1] > overbought


def check_rsi_oversold(rsi_values: rsi.RSIValues, oversold: float) -> bool:
    """Check if the RSI is oversold.

    Args:
        rsi_values (list[float]): The RSI values.
        oversold (float): The oversold level.

    Returns:
        bool: True if the RSI is oversold, False otherwise.
    """
    return rsi_values[-1] < oversold


def get_macd_signal_trend(signal_line: macd.SignalLine) -> str:
    """Get the trend of the MACD signal line (rising or falling)."""
    if signal_line[-2] < signal_line[-1]:
        return "rising"
    elif signal_line[-2] > signal_line[-1]:
        return "falling"
    else:
        return "neutral"


def trade(rsi: rsi.RSIIndicator, macd: macd.MACDIndicator) -> TradeSignal:
    """Trade based on the MACD and RSI indicators.

    Args:
        rsi (RSIIndicator): The RSI indicator.
        macd (MACDIndicator): The MACD indicator.

    Returns:
        str: The action to take (Buy, Sell, or No trade signal).
    """

    macd_cross = check_macd_cross(macd.macd_line, macd.signal_line)
    trade_signal = TradeSignal()
    trade_signal.buy = macd_cross and check_rsi_overbought(rsi.rsi_values, rsi.oversold)
    trade_signal.sell = macd_cross and check_rsi_oversold(
        rsi.rsi_values, rsi.overbought
    )

    return trade_signal
