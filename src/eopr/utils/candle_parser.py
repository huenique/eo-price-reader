import typing

T = typing.TypeVar("T")
CandleData = dict[str, list[T]]
Price = float | int


def parse_candles_data(data: dict[str, typing.Any]) -> list[float]:
    """The data is in the following format as of 2023-01-07:
    {"action":"candles","message":{"assetId":160,"candles":[{"tf":0,"tt":1688179038.5,"t":1688179038.5,"v":[30468.708]},{"tf":5,"tt":1688179038.5,"t":1688179035,"v":[30468.757,30468.757,30468.619,30468.708]}],"expTimes":[[1688179020,1688179050,[[30468.708,76,76,1],[30468.0986,77,2,2],[30469.3174,6,76,3]]],[1688179050,1688179080,[[30468.708,76,76,1],[30468.0986,76,5,2],[30469.3174,6,76,3]]],[1688179080,1688179110,[[30468.708,76,76,1],[30468.0986,76,6,2],[30469.3174,6,76,3]]],[1688179110,1688179140,[[30468.708,76,76,1],[30468.0986,76,6,2],[30469.3174,8,76,3]]]]}}

    Args:
        data (dict[str, typing.Any]): The data to parse from the websocket response from
            the server (eopr/__main__.py).

    Returns:
        list[float]: The parsed candles data.
    """
    candles_data: list[CandleData[Price]] = data.get("message", {}).get("candles", [])
    candles: list[Price] = []

    for candle in candles_data:
        values = candle.get("v", [])
        candles.extend(values)

    return candles
