import logging
from typing import Union
from collections import OrderedDict
from pydantic import ValidationError
from fastapi import FastAPI, Header, HTTPException
from kis.connector import KISOverseaConnector
from kis.models import KISUser
from kis.configs import apihost, appkey, appsecret
from kis.payload import MarketCode
from kis.response import (
    TokenResponse,
    OverseaBalanceResponse,
    OverseaDailyPriceResponse,
)

app = FastAPI()
default_user = KISUser(apihost=apihost, appkey=appkey, appsecret=appsecret)


@app.post("/api/v1/token", response_model=TokenResponse)
def issue_token():
    connector = KISOverseaConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    return connector.issue_token()


@app.get("/api/v1/oversea/price/{symbol}", response_model=OverseaDailyPriceResponse)
def get_price(
    symbol,
    market_code: MarketCode = "NYS",
    access_token: Union[str, None] = Header(default=None),
):
    connector = KISOverseaConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    try:
        resp = connector.get_daily_price(
            access_token=access_token, symbol=symbol, market_code=market_code
        )
        return resp.dict()
    except ValidationError as e:
        logging.debug(str(e))
        raise HTTPException(status_code=400, detail="pasring fail. check payload")


@app.get(
    "/api/v1/oversea/accounts/{account_nuber}/balance",
    response_model=OverseaBalanceResponse,
    response_model_exclude={"search_key", "next_key"},
)
def get_balance(
    account_number: str, access_token: Union[str, None] = Header(default=None)
) -> OverseaBalanceResponse:
    connector = KISOverseaConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    resp = connector.get_balance(
        access_token=access_token, account_number=account_number
    )
    return resp


@app.get(
    "/api/v1/oversea/accounts/{account_number}/weights",
)
def get_weights(
    account_number: str,
    access_token: Union[str, None] = Header(default=None),
    descend: bool = True,
):
    connector = KISOverseaConnector(
        apihost=default_user.apihost,
        appkey=default_user.appkey,
        appsecret=default_user.appsecret,
    )
    resp = connector.get_balance(
        access_token=access_token, account_number=account_number
    ).dict(by_alias=True)
    _weights = {
        a['symbol']: round(a['eval_amt'] / resp['balance']['total_eval_amt'], 4)
        for a in resp['holdings']
    }
    return OrderedDict(
        sorted(
            _weights.items(),
            key=lambda item: -item[1] if descend else item[1],
        )
    )
