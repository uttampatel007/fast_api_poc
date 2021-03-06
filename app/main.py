from loguru import logger
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import JSONResponse

from app.processor import (
    process_single_transaction,
    process_transaction_summary_by_sku,
    process_transaction_summary_by_category
)


app = FastAPI(
        title='Data Streaming Docs',
        description='Api docs for publisher/subscriber model'
    )


# default responses for documentation
responses = {
    404: {"description": "Item not found"},
    500: {"description": "Internal error"},
}


# pydantic models for validating response
class Transaction(BaseModel):
    transaction_id: int
    sku_name: str
    sku_price: float
    transaction_datetime: str


class SummaryBySKUObject(BaseModel):
    sku_name: str
    total_amount: float


class SummaryBySKU(BaseModel):
    summary: Optional[List[SummaryBySKUObject]]


class SummaryByCategoryObject(BaseModel):
    sku_category: str
    total_amount: float


class SummaryByCategory(BaseModel):
    summary: Optional[List[SummaryByCategoryObject]]


@app.get("/")
def read_root():
    return {
        "API Docs url 1": "localhost:8000/docs",
        "API Docs url 2": "localhost:8000/redoc"
        }


@app.get(
    "/transaction/{transaction_id}", 
    response_model= Transaction,
    responses={**responses},
    )
def get_transaction(transaction_id:int):
    """Api to get single tranaction"""
    try:
        payload, code = process_single_transaction(transaction_id)
        if code != 200:
            return JSONResponse(status_code=code, content=payload)
        return payload

    except Exception as e:
        logger.exception(e)
        payload = {"description": "Internal error"}
        return JSONResponse(status_code=500, content=payload)


@app.get(
    "/transaction-summary-bySKU/{last_n_days}",
    response_model=SummaryBySKU,
    responses={**responses}
    )
def get_transaction_summary_by_sku(last_n_days:int):
    """Api to get sku transaction summary"""
    try:
        payload, code = process_transaction_summary_by_sku(last_n_days)
        if code != 200:
            return JSONResponse(status_code=code, content=payload)
        return payload

    except Exception as e:
        logger.exception(e)
        payload = {"description": "Internal error"}
        return JSONResponse(status_code=500, content=payload)


@app.get(
    '/transaction-summary-bycategory/{last_n_days}',
    response_model=SummaryByCategory,
    responses={**responses}
    )
def get_transaction_summary_by_category(last_n_days:int):
    """Api to get sku category transacction summary"""
    try:
        payload, code = process_transaction_summary_by_category(last_n_days)
        if code != 200:
            return JSONResponse(status_code=code, content=payload)
        return payload

    except Exception as e:
        logger.exception(e)
        payload = {"description": "Internal error"}
        return JSONResponse(status_code=500, content=payload)