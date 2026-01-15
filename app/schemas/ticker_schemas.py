from pydantic import BaseModel

class TickerSchema(BaseModel):
    id: int
    ticker: str
    price: float
    timestamp: int

    class Config:
        orm_mode = True


class ResponseTickerSchema(BaseModel):
    ticker: str
    price: float
    timestamp: int



