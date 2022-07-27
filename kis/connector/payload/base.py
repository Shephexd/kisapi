import json
from common.enums import StrEnum
import requests as req
from urllib.parse import urljoin, urlencode
from pydantic import Field, validator
from kis.connector.payload.response import (
    APIResponse,
    DomesticDailyPriceResponse,
    DomesticBalanceResponse,
)

from pydantic import BaseModel


class MarketCode(StrEnum):
    NYSE = "NYSE"
    NASDAQ = "NASD"
    AMEX = "AMEX"


class OrderChangeCode(StrEnum):
    UPDATE = "01"
    CANCEL = "02"


class BasePayload(BaseModel):
    class Config:
        allow_population_by_field_name = True

    tr_id = Field(default="", description="Transaction ID", exclude=True)

    @property
    def query_params(self):
        return urlencode(self.dict(by_alias=True))

    @property
    def url_path(self):
        raise NotImplementedError("need to be implemented")

    @property
    def response_class(self) -> type:
        return APIResponse

    @property
    def action_type(self):
        return "GET"

    def get_body(self):
        return self.json()

    def send(self, api_host, headers) -> req.Response:
        raise NotImplementedError("need to be implemented")

    def get_url(self, api_host, query_params: str = ""):
        _url = urljoin(api_host, self.url_path)
        if query_params:
            _url = urljoin(_url, f"?{query_params}")
        return _url


class BaseAccountPayload(BasePayload):
    account_number: str = Field(
        alias="CANO", description="AccountNumber", min_length=8, max_length=10
    )
    product_code: str = Field(
        alias="ACNT_PRDT_CD", default="01", description="", repr=False
    )

    @validator("account_number")
    def validate_account_number(cls, v: str):
        if len(v) in [8, 10]:
            return v[:8]
        raise ValueError("Fail to validate AccountNumber")


class IssueTokenPayload(BasePayload):
    grant_type: str = Field(default="client_credentials")
    appkey: str = Field(repr=False, description="App Key")
    appsecret: str = Field(repr=False, description="App Secret")

    @property
    def url_path(self):
        return "/oauth2/tokenP"

    def get_body(self):
        return self.dict()


class HashKeyPayload(BasePayload):
    data: dict

    @property
    def url_path(self):
        return "/uapi/hashkey"

    def get_body(self):
        return json.dumps({k: str(v) for k, v in self.data.items()})


class DomesticDailyPricePayload(BasePayload):
    tr_id: str = Field(
        default="FHKST01010400", description="Transaction ID", exclude=True
    )

    FID_COND_MRKT_DIV_CODE: str = Field(
        default="J", description="주식, ETF, ETN", repr=False
    )
    symbol: str = Field(alias="FID_INPUT_ISCD", description="종목코드")
    period_code: str = Field(
        default="D", alias="FID_PERIOD_DIV_CODE", description="기간 분류"
    )
    adj_flag: str = Field(default="1", alias="FID_ORG_ADJ_PRC", description="수정주가반영")

    @property
    def url_path(self):
        return "/uapi/domestic-stock/v1/quotations/inquire-daily-price"

    @property
    def response_class(self) -> type:
        return DomesticDailyPriceResponse


class DomesticBalancePayload(BaseAccountPayload):
    tr_id = Field(default="TTTC8434R", description="Transaction ID", exclude=True)

    AFHR_FLPR_YN: str = Field(default="N", description="시간외단일가")
    OFL_YN: str = Field(default="N", description="Offline flag", repr=False)
    INQR_DVSN: str = Field(default="01", description="조회구분", repr=False)
    UNPR_DVSN: str = Field(default="01", description="단가구분", repr=False)
    FUND_STTL_ICLD_YN: str = Field(default="N", description="펀드결제분포함", repr=False)
    FNCG_AMT_AUTO_RDPT_YN: str = Field(
        default="N", description="융자금액자동상환여부", repr=False
    )
    PRCS_DVSN: str = Field(default="00", description="전일매매포함")
    CTX_AREA_FK100: str = Field(default="", description="연속조회조건검색", repr=False)
    CTX_AREA_NK100: str = Field(default="", description="연속조회키", repr=False)

    @property
    def url_path(self):
        return "/uapi/domestic-stock/v1/trading/inquire-balance"

    @property
    def response_class(self) -> type:
        return DomesticBalanceResponse
