import dataclasses

FloatArray = list[float]
CandlePrice = FloatArray


@dataclasses.dataclass
class TrendAnalysis:
    bullish: bool
    bearish: bool
    interpretation: str | None = None
