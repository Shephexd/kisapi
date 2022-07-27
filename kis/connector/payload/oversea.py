from decimal import Decimal

from typing import Type
from .base import BasePayload, BaseAccountPayload
from .enum import (
    OverseaPriceMarketCode,
    OverseaOrderMarketCode,
    OrderChangeCode,
    OverseaPricePeriod,
)
from .response import (
    Response,
    OverseaBidOrderResponse,
    OverseaAskOrderResponse,
    OverseaChangeOrderResponse,
    OverseaBalanceResponse,
    OverseaDailyPriceResponse,
    OverseaQuotePriceResponse,
    OverseaUnexecutedListResponse,
)
from pydantic import Field


class OverseaQuotePricePayload(BasePayload):
    tr_id = Field(default="HHDFS00000300", description="Transaction ID", exclude=True)

    AUTH: str = Field(default="", repr=False)
    market_code: OverseaPriceMarketCode = Field(
        default="NAS", alias="EXCD", description="해외거래소코드"
    )
    symbol: str = Field(alias="SYMB", description="종목코드")

    @property
    def url_path(self):
        return "/uapi/overseas-price/v1/quotations/price"

    @property
    def response_class(self) -> type:
        return OverseaQuotePriceResponse


class OverseaDailyPricePayload(BasePayload):
    tr_id = Field(
        default="HHDFS76240000", description="Transaction ID", exclude=True, repr=False
    )

    AUTH: str = Field(default="", repr=False)
    market_code: str = Field(default="NAS", alias="EXCD", description="해외거래소코드")
    symbol: str = Field(alias="SYMB", description="종목코드")
    GUBN: str = Field(
        default=str(OverseaPricePeriod.DAILY), description="일/주/월 구분", repr=False
    )
    base_date: str = Field(default="", alias="BYMD")
    adj_flag: str = Field(alias="MODP", default="1", description="수정주가반영여부")
    next_key: str = Field(alias="KEYB", default="", repr=False)

    @property
    def url_path(self):
        return "/uapi/overseas-price/v1/quotations/dailyprice"

    @property
    def response_class(self) -> type:
        return OverseaDailyPriceResponse


class OverseaBalancePayload(BaseAccountPayload):
    tr_id = Field(default="JTTT3012R", description="Transaction ID", exclude=True)

    market_code: str = Field(
        alias="OVRS_EXCG_CD", default="NASD", description="해외거래소코드"
    )
    currency_code: str = Field(
        alias="TR_CRCY_CD", default="USD", description="통화구분", repr=False
    )
    search_key: str = Field(
        alias="CTX_AREA_FK200", default="", description="연속조회조건검색", repr=False
    )
    next_key: str = Field(
        alias="CTX_AREA_NK200", default="", description="연속조회키", repr=False
    )

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/inquire-balance"

    @property
    def response_class(self) -> type:
        return OverseaBalanceResponse


class OverseaUnexecutedListPayload(BaseAccountPayload):
    tr_id = Field(default="JTTT3018R", description="Transaction ID", exclude=True)

    market_code: str = Field(
        alias="OVRS_EXCG_CD", default="NASD", description="해외거래소코드"
    )
    order: str = Field(alias="SORT_SQN", default="DS", description="정렬순서")
    search_key: str = Field(
        alias="CTX_AREA_FK200", default="", description="연속조회조건검색", repr=False
    )
    next_key: str = Field(
        alias="CTX_AREA_NK200", default="", description="연속조회키", repr=False
    )

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/inquire-nccs"

    @property
    def response_class(self) -> type:
        return OverseaUnexecutedListResponse


class OverseaExecutedListPayload(BaseAccountPayload):
    tr_id = Field(default="JTTT3018R", description="Transaction ID", exclude=True)


class OverseaOrderPayload(BaseAccountPayload):
    tr_id = Field(default="", description="Transaction ID", exclude=True)
    market_code: OverseaOrderMarketCode = Field(
        alias="OVRS_EXCG_CD", default="NASD", description="해외거래소코드"
    )
    symbol: str = Field(alias="PDNO", description="종목코드")
    qty: int = Field(alias="ORD_QTY", description="주문수량")
    price: Decimal = Field(alias="OVRS_ORD_UNPR", description="해외주문단가")
    order_code: str = Field(default="00", alias="ORD_DVSN", description="주문구분(기본값:지정가)")

    CTAC_TLNO: str = Field(description="연락전화번호", default="", max_length=20)
    MGCO_APTM_ODNO: str = Field(description="운용사지정주문번호", default="", max_length=12)
    ORD_SVR_DVSN_CD: str = Field(default="0", description="주문서버구분코드", max_length=1)

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/order"

    @property
    def action_type(self):
        return "POST"


class OverseaBidOrderPayload(OverseaOrderPayload):
    tr_id = Field(default="JTTT1002U", description="Transaction ID", exclude=True)

    @property
    def response_class(self) -> Type[Response]:
        return OverseaBidOrderResponse


class OverseaAskOrderPayload(OverseaOrderPayload):
    tr_id = Field(default="JTTT1006U", description="Transaction ID", exclude=True)
    sell_type: str = Field(
        default="00", alias="SLL_TYPE", description="판매유형", max_length=2
    )

    @property
    def response_class(self) -> type:
        return OverseaAskOrderResponse


class OverseaUpdateOrderPayload(OverseaOrderPayload):
    tr_id = Field(default="JTTT1004U", description="Transaction ID", exclude=True)
    order_no: str = Field(alias="ORGN_ODNO", description="원주문번호")
    RVSE_CNCL_DVSN_CD: str = str(OrderChangeCode.UPDATE)

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/order-rvsecncl"

    @property
    def response_class(self) -> type:
        return OverseaChangeOrderResponse


class OverseaCancelOrderPayload(OverseaOrderPayload):
    tr_id = Field(default="JTTT1004U", description="Transaction ID", exclude=True)
    order_no: str = Field(alias="ORGN_ODNO", description="원주문번호")
    RVSE_CNCL_DVSN_CD: str = str(OrderChangeCode.CANCEL)

    @property
    def url_path(self):
        return "/uapi/overseas-stock/v1/trading/order-rvsecncl"

    @property
    def response_class(self) -> type:
        return OverseaChangeOrderResponse
