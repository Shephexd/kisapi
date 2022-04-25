from decimal import Decimal
from typing import List, Union
from pydantic import BaseModel, Field, validator


class APIResponse(BaseModel):
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
        ord_qty: str = Field(alias="ord_psbl_qty", description="주문가능수량")
        avg_price: str = Field(alias="pchs_avg_pric", description="매입평균가격")
        purchase_amount: str = Field(alias="pchs_amt", description="매입금액")
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
    return_code: str = Field(alias="rt_cd", description="", repr=False)
    message: str = Field(alias="msg1")
    message_code: str = Field(alias="msg_cd", repr=False)

    @validator("message", "search_key", "next_key")
    def strip_str(cls, v: str):
        return v.strip()

    @validator("balance")
    def get_first(cls, v: list or dict):
        return super().get_first(v)


class OverseaBalanceResponse(APIResponse):
    pass
