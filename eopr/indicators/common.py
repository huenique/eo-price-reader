import pydantic

FloatArray = list[float]
CandlePrice = FloatArray


class TrendAnalysis(pydantic.BaseModel):
    bullish: bool
    bearish: bool
    interpretation: str = pydantic.Field(default="")
