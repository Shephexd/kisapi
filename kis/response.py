from decimal import Decimal
from typing import List, Union
from pydantic import BaseModel, Field, validator


class APIResponse(BaseModel):
    return_code: str = Field(alias="rt_cd", description="0: 성공, 0 이외의 값: 실패", repr=False)
    message: str = Field(alias="msg1", description="응답 메시지")
    message_code: str = Field(alias="msg_cd", description="응답 코드", repr=False)

    @classmethod
    def get_first(cls, v: list or dict):
        if isinstance(v, list) and v:
            return v[0]
        return v


class DomesticBalanceResponse(APIResponse):
    class HoldingDetail(BaseModel):
        symbol: str = Field(alias="pdno", description="상품번호")
        name: str = Field(alias="prdt_name", description="상품명")
        trade_type: str = Field(alias="trad_dvsn_name", description="매매구분명")
        prev_buy_qty: str = Field(alias="bfdy_buy_qty", description="전일매수수량")
        prev_sell_qty: str = Field(alias="bfdy_sll_qty", description="전일매도수량")
        buy_qty: str = Field(alias="thdt_buyqty", description="금일매수수량")
        sell_qty: str = Field(alias="thdt_sll_qty", description="금일매도수량")
        holding_qty: str = Field(alias="hldg_qty", description="보유수량")
        ord_possible_qty: str = Field(alias="ord_psbl_qty", description="주문가능수량")
        avg_price: str = Field(alias="pchs_avg_pric", description="매입평균가격")
        purchase_amt: str = Field(alias="pchs_amt", description="매입금액")
        price: str = Field(alias="prpr", description="현재가")
        eval_amt: str = Field(alias="evlu_amt", description="평가금액")
        profit_loss: str = Field(alias="evlu_pfls_amt", description="평가손익금액")
        profit_loss_ratio: str = Field(alias="evlu_pfls_rt", description="평가손익율")
        eval_return: str = Field(alias="evlu_erng_rt", description="평가수익율")
        changes: str = Field(alias="fltt_rt", description="등락율")
        changes_day: str = Field(alias="bfdy_cprs_icdc", description="전일대비증감")

    class BalanceDetail(BaseModel):
        deposit: int = Field(alias="dnca_tot_amt", description="예수금총금액")
        next_day_execution_amt: int = Field(alias="nxdy_excc_amt", description="익일정산금액")
        estimated_execution_amt: int = Field(alias="prvs_rcdl_excc_amt", description="가수도정산금액")
        cma_eval_amt: int = Field(alias="cma_evlu_amt", description="CMA평가금액")
        prev_bid_amt: int = Field(alias="bfdy_buy_amt", description="전일매수금액")
        bid_amt: int = Field(alias="thdt_buy_amt", description="금일매수금액")
        next_auto_repay_amt: int = Field(alias="nxdy_auto_rdpt_amt", description="익일자동상환금액")
        prev_ask_amt: int = Field(alias="bfdy_sll_amt", description="전일매도금액")
        ask_amt: int = Field(alias="thdt_sll_amt", description="금일매도금액")
        d2_auto_repay_amt: int = Field(alias="d2_auto_rdpt_amt", description="D+2자동상환금액")
        prev_charge: int = Field(alias="bfdy_tlex_amt", description="전일제비용금액")
        charge: int = Field(alias="thdt_tlex_amt", description="금일제비용금액")
        total_loan: int = Field(alias="tot_loan_amt", description="총대출금액")
        eval_amt: int = Field(alias="scts_evlu_amt", description="유가평가금액")
        total_amt: int = Field(alias="tot_evlu_amt", description="총평가금액")
        net_asset: int = Field(alias="nass_amt", description="순자산금")
        
        prev_eval_amt: int = Field(alias="bfdy_tot_asst_evlu_amt", description="전일총자산평가금액")
        asset_change: int = Field(alias="asst_icdc_amt", description="자상증감액")
        asset_change_return: Decimal = Field(alias="asst_icdc_erng_rt", description="자산증감수익률")

    search_key: str = Field(alias="ctx_area_fk100", description="연속조회검색조건", repr=False)
    next_key: str = Field(alias="ctx_area_nk100", description="연속조회키", repr=False)

    holdings: List[HoldingDetail] = Field(alias="output1")
    balance: Union[BalanceDetail, List[BalanceDetail]] = Field(alias="output2")

    @validator("message", "search_key", "next_key")
    def strip_str(cls, v: str):
        return v.strip()

    @validator("balance")
    def get_first(cls, v: list or dict):
        return super().get_first(v)


class OverseaBalanceResponse(APIResponse):
    class HoldingDetail(BaseModel):
        symbol: str = Field(alias="ovrs_pdno", description="상품번호")
        name: str = Field(alias="ovrs_item_name", description="상품명", repr=False)
        profit_loss: Decimal = Field(alias="frcr_evlu_pfls_amt", description="외화평가손익금액")
        profit_loss_ratio: Decimal = Field(alias="evlu_pfls_rt", description="평가손익률")
        purchase_avg_price: Decimal = Field(alias="pchs_avg_pric", description="해당 종목의 매수 평균 단가")
        holding_qty: Decimal = Field(alias="ovrs_cblc_qty", description="잔고수량")
        ord_possible_qty: Decimal = Field(alias="ord_psbl_qty", description="매도 가능한 주문 수량")
        purchase_amt: Decimal = Field(alias="frcr_pchs_amt1", description="해당 종목의 외화 기준 매입금액")
        eval_amt: Decimal = Field(alias="ovrs_stck_evlu_amt", description="평가금액")
        price: Decimal = Field(alias="now_pric2", description="현재가격")
        currency_code: str = Field(alias="tr_crcy_cd", description="거래통화코드")

    class BalanceDetail(BaseModel):
        foreign_purchase_amt: Decimal = Field(alias="frcr_pchs_amt1", description="외화매입금액1")
        realized_profit_loss: Decimal = Field(alias="ovrs_rlzt_pfls_amt", description="해외실현손익금액")
        total_profit_loss: Decimal = Field(alias="ovrs_tot_pfls", description="해외총손익")
        realized_return: Decimal = Field(alias="rlzt_erng_rt", description="실현수익률")
        total_eval_profit_loss_amt: Decimal = Field(alias="tot_evlu_pfls_amt", description="총푱가손익금액")
        total_return: Decimal = Field(alias="tot_pftrt", description="총수익률")
        exchange_amt: Decimal = Field(alias="frcr_buy_amt_smtl1", description="외화매수금액합계1")
        realized_profit_loss2: Decimal = Field(alias="ovrs_rlzt_pfls_amt2", description="해외실현손익금액2")
        exchange_amt2: Decimal = Field(alias="frcr_buy_amt_smtl2", description="외화매수금액합계2")

    search_key: str = Field(alias="ctx_area_fk200", description="연속조회검색조건", repr=False)
    next_key: str = Field(alias="ctx_area_nk200", description="연속조회키", repr=False)

    holdings: List[HoldingDetail] = Field(alias="output1")
    balance: BalanceDetail = Field(alias="output2")


class OverseaDailyPriceResponse(APIResponse):
    class OverseaDailyPriceTicker(BaseModel):
        symbol: str = Field(alias="rsym", description="종목코드")
        prev_close: Decimal = Field(alias="nrec")

    class OverseaDailyPriceRow(BaseModel):
        base_date: str = Field(alias="xymd", description="기준일")
        sign: Decimal = Field(description="대비기호", repr=False)
        diff: Decimal = Field(description="종가변동", repr=False)
        changes: Decimal = Field(alias="rate", description="전일비")
        open: Decimal = Field(description="시가")
        close: Decimal = Field(alias="clos", description="종가")
        high: Decimal = Field(description="고가")
        low: Decimal = Field(description="저가")
        volume: Decimal = Field(alias="tvol", description="거래량")
        trading_amount: Decimal = Field(alias="tamt", description="거래대금")
        pbid: Decimal = Field(description="매수호가", repr=False)
        vbid: Decimal = Field(description="매수호가잔량", repr=False)
        pask: Decimal = Field(description="매도호가", repr=False)
        vask: Decimal = Field(description="매도호가잔량", repr=False)

    ticker: OverseaDailyPriceTicker = Field(alias="output1")
    prices: List[OverseaDailyPriceRow] = Field(alias="output2")
