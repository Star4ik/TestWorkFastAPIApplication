import os
import requests
from celery import Celery
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from app.models.ticker_models import TickerModel

REDIS_URL = os.getenv("REDIS_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

celery_app = Celery(
    "deribit_tasks",
    broker=REDIS_URL
)

celery_app.conf.beat_schedule = {
    "fetch-deribit-prices-every-60s": {
        "task": "app.parser.tasks.fetch_deribit_prices",
        "schedule": 60.0,
    },
}
celery_app.conf.timezone = "UTC"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

@celery_app.task
def fetch_deribit_prices():
    tickers = ["btc_usd", "eth_usd"]
    session = SessionLocal()

    try:
        for ticker in tickers:
            r = requests.get(
                "https://www.deribit.com/api/v2/public/get_index_price",
                params={"index_name": ticker},
                timeout=10
            )
            data = r.json()

            price = data["result"]["index_price"]
            timestamp = data["usIn"]

            stmt = insert(TickerModel).values(
                ticker=ticker,
                price=price,
                timestamp=timestamp
            )
            session.execute(stmt)

        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()
