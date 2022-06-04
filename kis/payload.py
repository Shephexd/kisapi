import json
from common.enums import StrEnum
import requests as req
from decimal import Decimal
from urllib.parse import urljoin, urlencode
from pydantic import Field, validator
from kis.response import (
    APIResponse,
    DomesticDailyPriceResponse,
    DomesticBalanceResponse,
    OverseaBalanceResponse,
    OverseaDailyPriceResponse,
    OverseaBidOrderResponse,
)

from pydantic import BaseModel


class MarketCode(StrEnum):
    NYSE = "NYS"
    NASDAQ = "NAS"
    AMEX = "AMS"


class BasePayload(BaseModel):
    tr_id = Field(default="", description="Transaction ID", exclude=True)

    @property
    def query_params(self):
        return urlencode(self.dict())

    @property
    def url_path(self):
        raise NotImplementedError("need to be implemented")

    @property
    def response_class(self) -> type:
        return APIResponse

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
        raise ValueError("Fail to validate AccountNumber")

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

    def get_body(self):
        return self.dict()


class GetHashKeyPayload(BasePayload):
    data: dict

    @property
    def url_path(self):
        return "/oauth2/tokenP"

    def get_body(self):
        return json.dumps(self.data)


class DomesticDailyPricePayload(BasePayload):
    tr_id: str = Field(
        default="FHKST01010400", description="Transaction ID", exclude=True
    )

    FID_COND_MRKT_DIV_CODE: str = Field(
        default="J", description="주식, ETF, ETN", repr=False
    )
    FID_INPUT_ISCD: str = Field(alias="symbol", description="종목코드")
    FID_PERIOD_DIV_CODE: str = Field(
        default="D", alias="period_code", description="기간 분류"
    )
    FID_ORG_ADJ_PRC: str = Field(default="1", alias="adj_flag", description="수정주가반영")

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


class OverseaOrderPayload(BaseAccountPayload):
    tr_id = Field(default="", description="Transaction ID", exclude=True)
    OVRS_EXCG_CD: MarketCode = Field(
        alias="market_code", default="NASD", description="해외거래소코드"
    )
    PDNO: str = Field(alias="symbol", description="종목코드")
    ORD_QTY: Decimal = Field(alias="qty", description="주문수량")
    OVRS_ORD_UNPR: Decimal = Field(alias="price", description="해외주문단가")
    CTAC_TLNO: str = Field(description="연락전화번호", default="", max_length=20)
    MGCO_APTM_ODNO: str = Field(description="운용사지정주문번호", default="", max_length=12)
    ORD_SVR_DVSN_CD: str = Field(default="0", description="주문서버구분코드", max_length=1)
    ORD_DVSN: str = Field(default="00", alias="order_", description="주문구분(기본값:지정가)")

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/order"


class OverseaBidOrderPayload(OverseaOrderPayload):
    tr_id = Field(default="JTTT1002U", description="Transaction ID", exclude=True)

    @property
    def response_class(self) -> type:
        return OverseaBidOrderResponse


class OverseaAskOrderPayload(OverseaOrderPayload):
    tr_id = Field(default="JTTT1006U", description="Transaction ID", exclude=True)
    SLL_TYPE: str = Field(default="00", description="판매유형", max_length=2)


class OverseaQuotePricePayload(BasePayload):
    AUTH: str = Field(default="", repr=False)
    EXCD: MarketCode = Field(default="NAS", alias="market_code", description="해외거래소코드")
    SYMB: str = Field(alias="symbol", description="종목코드")

    @property
    def url_path(self):
        return "/uapi/overseas-price/v1/quotations/price"

    @property
    def response_class(self) -> type:
        return


class OverseaDailyPricePayload(BasePayload):
    tr_id = Field(
        default="HHDFS76240000", description="Transaction ID", exclude=True, repr=False
    )

    AUTH: str = Field(default="", repr=False)
    EXCD: MarketCode = Field(default="NAS", alias="market_code", description="해외거래소코드")
    SYMB: str = Field(alias="symbol", description="종목코드")
    GUBN: str = Field(default="0", description="일/주/월 구분", repr=False)
    BYMD: str = Field(default="", alias="base_date")
    MODP: str = Field(alias="adj_flag", default="1", description="수정주가반영여부")
    KEYB: str = Field(alias="next_key", default="", repr=False)

    @property
    def url_path(self):
        return "/uapi/overseas-price/v1/quotations/dailyprice"

    @property
    def response_class(self) -> type:
        return OverseaDailyPriceResponse


class OverseaBalancePayload(BaseAccountPayload):
    tr_id = Field(default="JTTT3012R", description="Transaction ID", exclude=True)

    OVRS_EXCG_CD: str = Field(
        alias="market_code", default="NASD", description="해외거래소코드"
    )
    TR_CRCY_CD: str = Field(
        alias="currency_code", default="USD", description="통화구분", repr=False
    )
    CTX_AREA_FK200: str = Field(default="", description="연속조회조건검색", repr=False)
    CTX_AREA_NK200: str = Field(default="", description="연속조회키", repr=False)

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/inquire-balance"

    @property
    def response_class(self) -> type:
        return OverseaBalanceResponse

    def send(self, api_host, headers) -> req.Response:
        return self.get(api_host=api_host, headers=headers)
