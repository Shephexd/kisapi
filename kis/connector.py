from urllib.parse import urljoin
import requests as req
from kis.payload import (
    BasePayload,
    IssueTokenPayload,
    DomesticBalancePayload,
    DomesticDailyPricePayload,
    OverseaBalancePayload,
    OverseaDailyPricePayload,
)


class KISAPIRequest:
    def __init__(self, host: str, headers: dict, payload: BasePayload):
        self.host = host
        self.headers = headers
        self.payload = payload

    def get(self) -> req.Response:
        return req.get(
            urljoin(self.host, f"?{self.payload.query_params}"), headers=self.headers
        )

    def post(self) -> req.Response:
        return req.post(self.host, headers=self.headers, json=self.payload.dict())


class KISConnector:
    def __init__(self, apihost, appkey, appsecret):
        self.apihost = apihost
        self.__appkey = appkey
        self.__appsecret = appsecret

    def get_payload(self):
        return

    @property
    def default_headers(self):
        return {
            "content-type": "application/json;charset=utf-8",
            "appkey": self.__appkey,
            "appsecret": self.__appsecret,
            "custtype": "P",
        }

    def get_headers(self, tr_id=None, access_token=None):
        _headers = {
            **self.default_headers,
            "appkey": self.__appkey,
            "appsecret": self.__appsecret,
        }
        if tr_id is not None:
            _headers["tr_id"] = tr_id

        if access_token:
            _headers["Authorization"] = f"Bearer {access_token}"
        return _headers

    def get_response(
        self, payload: BasePayload, access_token, auto_issue=True, **kwargs
    ):
        resp = payload.send(
            api_host=self.apihost,
            headers=self.get_headers(tr_id=payload.tr_id, access_token=access_token),
        )
        parsed_resp = resp.json()
        response = payload.response_class(**parsed_resp)
        return response.dict()

    def issue_token(self):
        payload: BasePayload = IssueTokenPayload(
            appkey=self.__appkey, appsecret=self.__appsecret
        )
        resp = payload.send(api_host=self.apihost, headers=self.get_headers())
        return resp.json().get("access_token")


class KISDomesticConnector(KISConnector):
    def get_balance(self, access_token, account_number):
        payload = DomesticBalancePayload(account_number=account_number)
        return self.get_response(payload=payload, access_token=access_token)

    def get_daily_price(self, access_token, symbol):
        payload = DomesticDailyPricePayload(symbol=symbol)
        return self.get_response(payload=payload, access_token=access_token)


class KISOverseaConnector(KISConnector):
    def get_balance(self, access_token, account_number):
        payload = OverseaBalancePayload(account_number=account_number)
        return self.get_response(payload=payload, access_token=access_token)

    def get_daily_price(self, access_token, symbol):
        payload = OverseaDailyPricePayload(symbol=symbol)
        return self.get_response(payload=payload, access_token=access_token)
