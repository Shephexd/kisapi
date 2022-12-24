import datetime
import logging
from requests import RequestException
from decimal import Decimal
from typing import Union
from collections import OrderedDict
from pydantic import ValidationError
from fastapi import FastAPI, Header, HTTPException
from kis.connector import KISConnector
from kis.models import KISUser
from kis.configs import APIHOST, APPKEY, APPSECRET
from kis.connector.payload.oversea import (
    BasePayload,
    OverseaDailyPricePayload,
    OverseaQuotePricePayload,
    OverseaBidOrderPayload,
    OverseaAskOrderPayload,
    OverseaUpdateOrderPayload,
    OverseaCancelOrderPayload,
    OverseaBalancePayload,
    OverseaUnexecutedListPayload,
    OverseaOrderHistoryPayload,
    OverseaOrderHistoryNightPayload,
)
from kis.connector.payload.enum import OverseaPriceMarketCode, OverseaOrderMarketCode
from kis.connector.payload.response import (
    TokenResponse,
    OverseaBalanceResponse,
    OverseaDailyPriceResponse,
    OverseaQuotePriceResponse,
    OverseaBidOrderResponse,
    OverseaAskOrderResponse,
    OverseaChangeOrderResponse,
    OverseaUnexecutedListResponse,
    OverseaOrderHistoryResponse,
)

app = FastAPI()
default_user = KISUser(apihost=APIHOST, appkey=APPKEY, appsecret=APPSECRET)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/v1/token", response_model=TokenResponse)
def issue_token():
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    return connector.issue_token()


@app.get(
    "/api/v1/oversea/price/daily/{symbol}",
    tags=["price"],
    response_model=OverseaDailyPriceResponse,
)
def get_daily_price(
    symbol,
    start_date: datetime.date = "",
    base_date: datetime.date = "",
    market_code: OverseaPriceMarketCode = "NYS",
    access_token: Union[str, None] = Header(default=None),
):
    def is_date_filled(start_dt, last_dt):
        if not start_dt:
            return True

        last_dt = datetime.datetime.strptime(last_dt, "%Y%m%d").date()
        if start_dt < last_dt:
            return False
        return True

    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )

    if isinstance(base_date, datetime.date):
        base_date = base_date.strftime("%Y%m%d")
    payload: BasePayload = OverseaDailyPricePayload(
        market_code=market_code, symbol=symbol, base_date=base_date
    )
    try:
        resp = connector.send(access_token=access_token, payload=payload)
        last_date = resp.prices[-1].base_date
        while not is_date_filled(start_dt=start_date, last_dt=last_date):
            next_payload: BasePayload = OverseaDailyPricePayload(
                market_code=market_code, symbol=symbol, base_date=last_date
            )
            next_resp = connector.send(access_token=access_token, payload=next_payload)
            last_date = next_resp.prices[-1].base_date
            resp.prices += [
                p
                for p in next_resp.prices[1:]
                if p.base_date >= start_date.strftime("%Y%m%d")
            ]
        return resp.dict()
    except ValidationError as e:
        logging.debug(str(e))
        raise HTTPException(status_code=400, detail="parsing fail. check payload")


@app.get(
    "/api/v1/oversea/price/quote/{symbol}",
    tags=["price"],
    response_model=OverseaQuotePriceResponse,
)
def get_quote(
    symbol,
    market_code: OverseaPriceMarketCode = "NYS",
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    payload: BasePayload = OverseaQuotePricePayload(
        market_code=market_code, symbol=symbol
    )
    try:
        resp = connector.send(access_token=access_token, payload=payload)
        return resp.dict()
    except ValidationError as e:
        logging.debug(str(e))
        raise HTTPException(status_code=400, detail="parsing fail. check payload")


@app.get(
    "/api/v1/oversea/accounts/balance",
    response_model=OverseaBalanceResponse,
    response_model_exclude={"search_key", "next_key"},
    tags=["account"],
)
def get_balance(
    account_number: str = Header(default=None),
    access_token: Union[str, None] = Header(default=None),
) -> OverseaBalanceResponse:
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    payload = OverseaBalancePayload(account_number=account_number)
    resp = connector.send(payload=payload, access_token=access_token)
    return resp


@app.get("/api/v1/oversea/accounts/weights", tags=["account"])
def get_weights(
    account_number: str = Header(default=None),
    access_token: Union[str, None] = Header(default=None),
    descend: bool = True,
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    payload = OverseaBalancePayload(account_number=account_number)
    resp = connector.send(payload=payload, access_token=access_token).dict()
    _weights = {
        a["symbol"]: round(a["eval_amt"] / resp["balance"]["total_eval_amt"], 4)
        for a in resp["holdings"]
    }
    return OrderedDict(
        sorted(
            _weights.items(),
            key=lambda item: -item[1] if descend else item[1],
        )
    )


@app.post(
    "/api/v1/oversea/order/bid", response_model=OverseaBidOrderResponse, tags=["order"]
)
def request_bid(
    market_code: OverseaOrderMarketCode,
    symbol: str,
    qty: Decimal,
    price: Decimal,
    account_number: str = Header(default=None),
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    payload = OverseaBidOrderPayload(
        account_number=account_number,
        symbol=symbol,
        market_code=market_code,
        qty=qty,
        price=price,
    )
    resp = connector.send(payload=payload, access_token=access_token).dict()
    return resp


@app.post(
    "/api/v1/oversea/order/ask", response_model=OverseaAskOrderResponse, tags=["order"]
)
def request_ask(
    market_code: OverseaOrderMarketCode,
    symbol: str,
    qty: float,
    price: float,
    account_number: str = Header(default=None),
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    try:
        payload = OverseaAskOrderPayload(
            account_number=account_number,
            symbol=symbol,
            market_code=market_code,
            qty=qty,
            price=price,
        )
        resp = connector.send(payload=payload, access_token=access_token).dict()
        return resp
    except RequestException as e:
        return e.response


@app.put(
    "/api/v1/oversea/order/{order_no}",
    response_model=OverseaChangeOrderResponse,
    tags=["order"],
)
async def update_order(
    order_no: int,
    market_code: OverseaOrderMarketCode,
    symbol: str,
    qty: float,
    price: float,
    account_number: str = Header(default=None),
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    try:
        payload = OverseaUpdateOrderPayload(
            account_number=account_number,
            order_no=order_no,
            symbol=symbol,
            market_code=market_code,
            qty=qty,
            price=price,
        )
        print(payload.dict(by_alias=True))
        resp = connector.send(payload=payload, access_token=access_token).dict()
        return resp
    except RequestException as e:
        return e.response


@app.delete(
    "/api/v1/oversea/order/{order_no}",
    response_model=OverseaChangeOrderResponse,
    tags=["order"],
)
def delete_order(
    order_no: int,
    account_number: str,
    market_code: OverseaOrderMarketCode,
    symbol: str,
    qty: int,
    price: float = 1,
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    try:
        payload = OverseaCancelOrderPayload(
            account_number=account_number,
            order_no=order_no,
            symbol=symbol,
            market_code=market_code,
            qty=qty,
            price=price,
        )
        resp = connector.send(payload=payload, access_token=access_token).dict()
        return resp
    except RequestException as e:
        return e.response


@app.get(
    "/api/v1/oversea/order/unexecuted",
    response_model=OverseaUnexecutedListResponse,
    tags=["order"],
)
def get_unexecuted(
    market_code: OverseaOrderMarketCode,
    account_number: str = Header(default=None),
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    try:
        payload = OverseaUnexecutedListPayload(
            account_number=account_number, market_code=market_code
        )
        resp = connector.send(payload=payload, access_token=access_token).dict()
        return resp
    except RequestException as e:
        return e.response


@app.get(
    "/api/v1/oversea/order/history",
    tags=["order"],
    response_model=OverseaOrderHistoryResponse,
)
def get_order_history(
    start_date: str,
    end_date: str,
    market_code: OverseaOrderMarketCode = "NASD",
    account_number: str = Header(default=None),
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    payload: BasePayload = OverseaOrderHistoryNightPayload(
        account_number=account_number,
        start_date=start_date,
        end_date=end_date,
        market_code=market_code,
    )
    try:
        resp: OverseaOrderHistoryResponse = connector.send(
            access_token=access_token, payload=payload
        )
        output_results = resp.output

        while resp.has_next:
            payload.CTX_AREA_NK200 = resp.ctx_area_nk200
            payload.CTX_AREA_FK200 = resp.ctx_area_fk200

            resp: OverseaOrderHistoryResponse = connector.send(
                access_token=access_token, payload=payload, tr_cont="N"
            )
            output_results += resp.output
        resp.output = output_results
        return resp
    except ValidationError as e:
        logging.debug(str(e))
        raise HTTPException(status_code=400, detail="parsing fail. check payload")
