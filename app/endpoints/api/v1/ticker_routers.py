from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticker_models import TickerModel
from app.utils.database import get_db
from app.schemas.ticker_schemas import ResponseTickerSchema

router = APIRouter(prefix="/ticker", tags=["Ticker"])


@router.get("/{ticker}", response_model=List[ResponseTickerSchema])
async def get_all_data_by_ticker(ticker: str, session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(TickerModel).where(TickerModel.ticker == ticker).order_by(TickerModel.timestamp)
    )
    data = result.scalars().all()
    if not data:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return data


@router.get("/{ticker}/last", response_model=ResponseTickerSchema)
async def get_last_price_by_ticker(ticker: str, session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(TickerModel)
        .where(TickerModel.ticker == ticker)
        .order_by(desc(TickerModel.timestamp))
        .limit(1)
    )
    data = result.scalars().first()
    if not data:
        raise HTTPException(status_code=404, detail="Ticker not found")
    return data

@router.get("/{ticker}/price_by_time", response_model=List[ResponseTickerSchema])
async def get_price_by_time(
    ticker: str,
    from_ts: Optional[int] = Query(None),
    to_ts: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_db)
):
    filters = [TickerModel.ticker == ticker]
    if from_ts is not None:
        filters.append(TickerModel.timestamp >= from_ts)
    if to_ts is not None:
        filters.append(TickerModel.timestamp <= to_ts)

    result = await session.execute(
        select(TickerModel)
        .where(and_(*filters))
        .order_by(TickerModel.timestamp)
    )
    data = result.scalars().all()
    if not data:
        raise HTTPException(status_code=404, detail="Нет данных за указаный период.")
    return data