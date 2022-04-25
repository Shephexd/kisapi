import requests as req
from urllib.parse import urljoin, urlencode
from pydantic import BaseModel, Field, validator
from kis.response import (
    APIResponse, DomesticBalanceResponse, OverseaBalanceResponse
)


class BasePayload(BaseModel):
    @property
    def query_params(self):
        return urlencode(self.dict())

    @property
    def url_path(self):
        raise NotImplementedError("need to be implemented")

    @property
    def response_class(self) -> type:
        return APIResponse

    def send(self, api_host, headers) -> req.Response:
        raise NotImplementedError("need to be implemented")

    def get(self, api_host, headers):
        return req.get(url=self.get_url(api_host=api_host, query_params=self.query_params), headers=headers)

    def post(self, api_host, headers):
        return req.post(url=self.get_url(api_host=api_host), headers=headers, json=self.dict())

    def get_url(self, api_host, query_params: str = ""):
        _url = urljoin(api_host, self.url_path)
        if query_params:
            _url = urljoin(_url, f"?{query_params}")
        return _url


class BaseAccountPayload(BasePayload):
    CANO: str = Field(
        alias="account_number", description="AccountNumber", min_length=8, max_length=10
    )
    ACNT_PRDT_CD: str = Field(
        alias="product_code", default="01", description="", repr=False
    )

    @validator("CANO")
    def validate_account_number(cls, v: str):
        if len(v) in [8, 10]:
            return v[:8]
        raise ValueError

    @property
    def account_number(self):
        return self.CANO + self.ACNT_PRDT_CD


class IssueTokenPayload(BasePayload):
    grant_type: str = Field(default="client_credentials")
    appkey: str = Field(repr=False, description="App Key")
    appsecret: str = Field(repr=False, description="App Secret")

    @property
    def url_path(self):
        return "/oauth2/tokenP"

    def send(self, api_host, headers) -> req.Response:
        return self.post(api_host=api_host, headers=headers)


class DomesticBalancePayload(BaseAccountPayload):
    tr_id = Field(default="TTTC8434R", description="Transaction ID", exclude=True)

    AFHR_FLPR_YN: str = Field(default="N", description="시간외단일가")
    OFL_YN: str = Field(default="N", description="Offline flag", repr=False)
    INQR_DVSN: str = Field(default="01", description="조회구분", repr=False)
    UNPR_DVSN: str = Field(default="01", description="단가구분", repr=False)
    FUND_STTL_ICLD_YN: str = Field(default="N", description="펀드결제분포함", repr=False)
    FNCG_AMT_AUTO_RDPT_YN: str = Field(default="N", description="융자금액자동상환여부", repr=False)
    PRCS_DVSN: str = Field(default="00", description="전일매매포함")
    CTX_AREA_FK100: str = Field(default="", description="연속조회조건검색", repr=False)
    CTX_AREA_NK100: str = Field(default="", description="연속조회키", repr=False)

    @property
    def url_path(self):
        return "/uapi/domestic-stock/v1/trading/inquire-balance"

    @property
    def response_class(self) -> type:
        return DomesticBalanceResponse

    def send(self, api_host, headers) -> req.Response:
        return self.get(api_host=api_host, headers=headers)


class OverseaBalancePayload(BaseAccountPayload):
    tr_id = Field(default="JTTT3012R", description="Transaction ID", exclude=True)

    OVRS_EXCG_CD: str = Field(alias="market_code", default="NASD", description="해외거래소코드")
    TR_CRCY_CD: str = Field(alias="currency_code", default="USD", description="거래통화코드")
    CTX_AREA_FK200: str = Field(default="", description="연속조회조건검색", repr=False)
    CTX_AREA_NK200: str = Field(default="", description="연속조회키", repr=False)

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/inquire-present-balance"

    @property
    def response_class(self) -> type:
        return OverseaBalanceResponse

    def send(self, api_host, headers) -> req.Response:
        return self.get(api_host=api_host, headers=headers)
