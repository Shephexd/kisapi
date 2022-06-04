from enum import Enum
from decimal import Decimal
from typing import List, Union
from pydantic import BaseModel, Field, validator


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class Response(BaseModel):
    class Config:
        allow_population_by_field_name = True


class APIResponse(Response):
    rt_cd: str = Field(
        alias="return_code", description="0: 성공, 0 이외의 값: 실패", repr=False
    )
    msg1: str = Field(alias="message", description="응답 메시지")
    msg_cd: str = Field(alias="message_code", description="응답 코드", repr=False)

    @classmethod
    def get_first(cls, v: list or dict):
        if isinstance(v, list) and v:
            return v[0]
        return v

    @validator("msg1")
    def strip_str(cls, v: str):
        return v.strip()


class DomesticBalanceResponse(APIResponse):
    class HoldingDetail(Response):
        pdno: str = Field(alias="symbol", description="상품번호")
        prdt_name: str = Field(alias="name", description="상품명")
        trad_dvsn_name: str = Field(alias="trade_type", description="매매구분명")
        bfdy_buy_qty: str = Field(alias="prev_buy_qty", description="전일매수수량")
        bfdy_sll_qty: str = Field(alias="prev_sell_qty", description="전일매도수량")
        thdt_buyqty: str = Field(alias="buy_qty", description="금일매수수량")
        thdt_sll_qty: str = Field(alias="sell_qty", description="금일매도수량")
        hldg_qty: str = Field(alias="holding_qty", description="보유수량")
        ord_psbl_qty: str = Field(alias="ord_possible_qty", description="주문가능수량")
        pchs_avg_pric: str = Field(alias="avg_price", description="매입평균가격")
        pchs_amt: str = Field(alias="purchase_amt", description="매입금액")
        prpr: str = Field(alias="price", description="현재가")
        evlu_amt: str = Field(alias="eval_amt", description="평가금액")
        evlu_pfls_amt: str = Field(alias="profit_loss", description="평가손익금액")
        evlu_pfls_rt: str = Field(alias="profit_loss_ratio", description="평가손익율")
        evlu_erng_rt: str = Field(alias="eval_return", description="평가수익율")
        fltt_rt: str = Field(alias="changes", description="등락율")
        bfdy_cprs_icdc: str = Field(alias="changes_day", description="전일대비증감")

    class BalanceDetail(Response):
        dnca_tot_amt: int = Field(alias="deposit", description="예수금총금액")
        nxdy_excc_amt: int = Field(alias="next_day_execution_amt", description="익일정산금액")
        prvs_rcdl_excc_amt: int = Field(
            alias="estimated_execution_amt", description="가수도정산금액"
        )
        cma_evlu_amt: int = Field(alias="cma_eval_amt", description="CMA평가금액")
        bfdy_buy_amt: int = Field(alias="prev_bid_amt", description="전일매수금액")
        thdt_buy_amt: int = Field(alias="bid_amt", description="금일매수금액")
        nxdy_auto_rdpt_amt: int = Field(
            alias="next_auto_repay_amt", description="익일자동상환금액"
        )
        bfdy_sll_amt: int = Field(alias="prev_ask_amt", description="전일매도금액")
        thdt_sll_amt: int = Field(alias="ask_amt", description="금일매도금액")
        d2_auto_rdpt_amt: int = Field(
            alias="d2_auto_repay_amt", description="D+2자동상환금액"
        )
        bfdy_tlex_amt: int = Field(alias="prev_charge", description="전일제비용금액")
        thdt_tlex_amt: int = Field(alias="charge", description="금일제비용금액")
        tot_loan_amt: int = Field(alias="total_loan", description="총대출금액")
        scts_evlu_amt: int = Field(alias="eval_amt", description="유가평가금액")
        tot_evlu_amt: int = Field(alias="total_amt", description="총평가금액")
        nass_amt: int = Field(alias="net_asset", description="순자산금")

        bfdy_tot_asst_evlu_amt: int = Field(
            alias="prev_eval_amt", description="전일총자산평가금액"
        )
        asst_icdc_amt: int = Field(alias="asset_change", description="자상증감액")
        asst_icdc_erng_rt: Decimal = Field(
            alias="asset_change_return", description="자산증감수익률"
        )

    ctx_area_fk100: str = Field(alias="search_key", description="연속조회검색조건", repr=False)
    ctx_area_nk100: str = Field(alias="next_key", description="연속조회키", repr=False)

    output1: List[HoldingDetail] = Field(alias="holdings")
    output2: Union[BalanceDetail, List[BalanceDetail]] = Field(alias="balance")

    @validator("ctx_area_fk100", "ctx_area_nk100")
    def strip_str(cls, v: str):
        return v.strip()

    @validator("output2")
    def get_first(cls, v: list or dict):
        return super().get_first(v)


class DomesticDailyPriceResponse(APIResponse):
    class DailyPriceDetail(BaseModel):
        stck_bsop_date: str = Field(alias="base_date", description="영업일")
        stck_oprc: Decimal = Field(alias="open", description="시가")
        stck_hgpr: Decimal = Field(alias="high", description="최고가")
        stck_lwpr: Decimal = Field(alias="low", description="최저가")
        stck_clpr: Decimal = Field(alias="close", description="종가")
        acml_vol: int = Field(alias="vol", description="누적 거래량")
        prdy_vrss_vol_rate: Decimal = Field(
            alias="vol_rate", description="전일 대비 거래량 비율"
        )
        prdy_vrss: Decimal = Field(alias="change", description="전일 대비")
        """
        TODO fields
        -PRDY_VRSS_SIGN	전일 대비 부호	String	Y	1
        -PRDY_CTRT	전일 대비율	String	Y	10
        -HTS_FRGN_EHRT	HTS 외국인 소진율	String	Y	10
        -FRGN_NTBY_QTY	외국인 순매수 수량	String	Y	12
        -FLNG_CLS_CODE	락 구분 코드	String	Y	2	01 : 권리락, 02 : 배당락, 03 : 분배락, 04 : 권배락
        05 : 중간(분기)배당락, 06 : 권리중간배당락, 07 : 권리분기배당락
        -ACML_PRTT_RATE	누적 분할 비율	String	Y	12
        """

    output: List[DailyPriceDetail] = Field(alias="prices")


class OverseaBalanceResponse(APIResponse):
    class HoldingDetail(Response):
        ovrs_pdno: str = Field(alias="symbol", description="상품번호")
        ovrs_item_name: str = Field(alias="name", description="상품명", repr=False)
        frcr_evlu_pfls_amt: Decimal = Field(alias="profit_loss", description="외화평가손익금액")
        evlu_pfls_rt: Decimal = Field(alias="profit_loss_ratio", description="평가손익률")
        pchs_avg_pric: Decimal = Field(
            alias="purchase_avg_price", description="해당 종목의 매수 평균 단가"
        )
        ovrs_cblc_qty: Decimal = Field(alias="holding_qty", description="잔고수량")
        ord_psbl_qty: Decimal = Field(
            alias="ord_possible_qty", description="매도 가능한 주문 수량"
        )
        frcr_pchs_amt1: Decimal = Field(
            alias="purchase_amt", description="해당 종목의 외화 기준 매입금액"
        )
        ovrs_stck_evlu_amt: Decimal = Field(alias="eval_amt", description="평가금액")
        now_pric2: Decimal = Field(alias="price", description="현재가격")
        tr_crcy_cd: str = Field(alias="currency_code", description="거래통화코드")

    class BalanceDetail(Response):
        frcr_pchs_amt1: Decimal = Field(
            alias="foreign_purchase_amt", description="외화매입금액1"
        )
        ovrs_rlzt_pfls_amt: Decimal = Field(
            alias="realized_profit_loss", description="해외실현손익금액"
        )
        ovrs_tot_pfls: Decimal = Field(alias="total_profit_loss", description="해외총손익")
        rlzt_erng_rt: Decimal = Field(alias="realized_return", description="실현수익률")
        tot_evlu_pfls_amt: Decimal = Field(alias="total_eval_amt", description="총평가금액")
        tot_pftrt: Decimal = Field(alias="total_return", description="총수익률")
        frcr_buy_amt_smtl1: Decimal = Field(
            alias="exchange_amt", description="외화매수금액합계1"
        )
        ovrs_rlzt_pfls_amt2: Decimal = Field(
            alias="realized_profit_loss2", description="해외실현손익금액2"
        )
        frcr_buy_amt_smtl2: Decimal = Field(
            alias="exchange_amt2", description="외화매수금액합계2"
        )

    ctx_area_fk200: str = Field(alias="search_key", description="연속조회검색조건", repr=False)
    ctx_area_nk200: str = Field(alias="next_key", description="연속조회키", repr=False)

    output1: List[HoldingDetail] = Field(alias="holdings")
    output2: BalanceDetail = Field(alias="balance")

    @validator("ctx_area_fk200", "ctx_area_nk200")
    def strip_str(cls, v: str):
        return v.strip()


class OverseaDailyPriceResponse(APIResponse):
    class OverseaDailyPriceTicker(Response):
        rsym: str = Field(alias="symbol", description="종목코드")
        nrec: Decimal = Field(alias="prev_close")

    class OverseaDailyPriceRow(Response):
        xymd: str = Field(alias="base_date", description="기준일")
        sign: Decimal = Field(description="대비기호", repr=False)
        diff: Decimal = Field(description="종가변동", repr=False)
        rate: Decimal = Field(alias="changes", description="전일비")
        open: Decimal = Field(description="시가")
        close: Decimal = Field(alias="clos", description="종가")
        high: Decimal = Field(description="고가")
        low: Decimal = Field(description="저가")
        tvol: Decimal = Field(alias="volume", description="거래량")
        tamt: Decimal = Field(alias="trading_amount", description="거래대금")
        pbid: Decimal = Field(description="매수호가", repr=False)
        vbid: Decimal = Field(description="매수호가잔량", repr=False)
        pask: Decimal = Field(description="매도호가", repr=False)
        vask: Decimal = Field(description="매도호가잔량", repr=False)

    output1: OverseaDailyPriceTicker = Field(alias="ticker")
    output2: List[OverseaDailyPriceRow] = Field(alias="prices")


class OverseaBidOrderResponse(APIResponse):
    class OverseaBidOrderDetail(BaseModel):
        KRX_FWDG_ORD_ORGNO: str = Field(alias="krx_org_no", description="종목코드")
        ODNO: str = Field(alias="ord_no")
        ORD_TMD: str = Field(alias="order_time")

    output: OverseaBidOrderDetail = Field(alias="detail")
