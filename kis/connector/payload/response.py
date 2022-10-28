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
    message: str = Field(alias="msg1", description="응답 메시지")
    message_code: str = Field(alias="msg_cd", description="응답 코드", repr=False)
    header: dict = Field(description="response header", default={}, exclude=True)

    @classmethod
    def get_first(cls, v: list or dict):
        if isinstance(v, list) and v:
            return v[0]
        return v

    @validator("message")
    def strip_str(cls, v: str):
        return v.strip()

    def dict(self, by_alias=True, **kwargs):
        return super().dict(by_alias=True, **kwargs)


class DomesticBalanceResponse(APIResponse):
    class HoldingDetail(Response):
        symbol: str = Field(alias="pdno", description="상품번호")
        name: str = Field(alias="prdt_name", description="상품명")
        trade_type: str = Field(alias="trad_dvsn_name", description="매매구분명")
        prev_buy_qty: str = Field(alias="bfdy_buy_qty", description="전일매수수량")
        prev_sell_qty: str = Field(alias="bfdy_sll_qty", description="전일매도수량")
        buy_qty: str = Field(alias="thdt_buy_qty", description="금일매수수량")
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

    class BalanceDetail(Response):
        deposit: int = Field(alias="dnca_tot_amt", description="예수금총금액")
        next_day_execution_amt: int = Field(alias="nxdy_excc_amt", description="익일정산금액")
        estimated_execution_amt: int = Field(
            alias="prvs_rcdl_excc_amt", description="가수도정산금액"
        )
        cma_eval_amt: int = Field(alias="cma_evlu_amt", description="CMA평가금액")
        prev_bid_amt: int = Field(alias="bfdy_buy_amt", description="전일매수금액")
        bid_amt: int = Field(alias="thdt_buy_amt", description="금일매수금액")
        next_auto_repay_amt: int = Field(
            alias="nxdy_auto_rdpt_amt", description="익일자동상환금액"
        )
        prev_ask_amt: int = Field(alias="bfdy_sll_amt", description="전일매도금액")
        ask_amt: int = Field(alias="thdt_sll_amt", description="금일매도금액")
        d2_auto_repay_amt: int = Field(
            alias="d2_auto_rdpt_amt", description="D+2자동상환금액"
        )
        prev_charge: int = Field(alias="bfdy_tlex_amt", description="전일제비용금액")
        charge: int = Field(alias="thdt_tlex_amt", description="금일제비용금액")
        total_loan: int = Field(alias="tot_loan_amt", description="총대출금액")
        eval_amt: int = Field(alias="scts_evlu_amt", description="유가평가금액")
        total_amt: int = Field(alias="tot_evlu_amt", description="총평가금액")
        net_asset: int = Field(alias="nass_amt", description="순자산금")

        prev_eval_amt: int = Field(
            alias="bfdy_tot_asst_evlu_amt", description="전일총자산평가금액"
        )
        asset_change: int = Field(alias="asst_icdc_amt", description="자상증감액")
        asset_change_return: Decimal = Field(
            alias="asst_icdc_erng_rt", description="자산증감수익률"
        )

    search_key: str = Field(alias="ctx_area_fk100", description="연속조회검색조건", repr=False)
    next_key: str = Field(alias="ctx_area_nk100", description="연속조회키", repr=False)

    holdings: List[HoldingDetail] = Field(alias="output1")
    balance: Union[BalanceDetail, List[BalanceDetail]] = Field(alias="output2")

    @validator("holdings", "balance")
    def strip_str(cls, v: str):
        return v.strip()

    @validator("balance")
    def get_first(cls, v: list or dict):
        return super().get_first(v)


class DomesticDailyPriceResponse(APIResponse):
    class DailyPriceDetail(BaseModel):
        base_date: str = Field(alias="stck_bsop_date", description="영업일")
        open: Decimal = Field(alias="stck_oprc", description="시가")
        high: Decimal = Field(alias="stck_hgpr", description="최고가")
        low: Decimal = Field(alias="stck_lwpr", description="최저가")
        close: Decimal = Field(alias="stck_clpr", description="종가")
        vol: int = Field(alias="acml_vol", description="누적 거래량")
        vol_rate_changes: Decimal = Field(
            alias="prdy_vrss_vol_rate", description="전일 대비 거래량 비율"
        )
        change: Decimal = Field(alias="prdy_vrss", description="전일 대비")
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
        symbol: str = Field(alias="ovrs_pdno", description="상품번호")
        name: str = Field(alias="ovrs_item_name", description="상품명", repr=False)
        profit_loss: Decimal = Field(alias="frcr_evlu_pfls_amt", description="외화평가손익금액")
        profit_loss_ratio: Decimal = Field(alias="evlu_pfls_rt", description="평가손익률")
        purchase_avg_price: Decimal = Field(
            alias="pchs_avg_pric", description="해당 종목의 매수 평균 단가"
        )
        holding_qty: Decimal = Field(alias="ovrs_cblc_qty", description="잔고수량")
        ord_possible_qty: Decimal = Field(
            alias="ord_psbl_qty", description="매도 가능한 주문 수량"
        )
        purchase_amt: Decimal = Field(
            alias="frcr_pchs_amt1", description="해당 종목의 외화 기준 매입금액"
        )
        eval_amt: Decimal = Field(alias="ovrs_stck_evlu_amt", description="평가금액")
        price: Decimal = Field(alias="now_pric2", description="현재가격")
        currency_code: str = Field(alias="tr_crcy_cd", description="거래통화코드")

    class BalanceDetail(Response):
        foreign_purchase_amt: Decimal = Field(
            alias="frcr_pchs_amt1", description="외화매입금액1"
        )
        realized_profit_loss: Decimal = Field(
            alias="ovrs_rlzt_pfls_amt", description="해외실현손익금액"
        )
        total_profit_loss: Decimal = Field(alias="ovrs_tot_pfls", description="해외총손익")
        realized_return: Decimal = Field(alias="rlzt_erng_rt", description="실현수익률")
        total_eval_amt: Decimal = Field(alias="tot_evlu_pfls_amt", description="총평가금액")
        total_return: Decimal = Field(alias="tot_pftrt", description="총수익률")
        exchange_amt: Decimal = Field(
            alias="frcr_buy_amt_smtl1", description="외화매수금액합계1"
        )
        realized_profit_loss2: Decimal = Field(
            alias="ovrs_rlzt_pfls_amt2", description="해외실현손익금액2"
        )
        exchange_amt2: Decimal = Field(
            alias="frcr_buy_amt_smtl2", description="외화매수금액합계2"
        )

    search_key: str = Field(alias="ctx_area_fk200", description="연속조회검색조건", repr=False)
    next_key: str = Field(alias="ctx_area_nk200", description="연속조회키", repr=False)

    holdings: List[HoldingDetail] = Field(alias="output1")
    balance: BalanceDetail = Field(alias="output2")

    @validator("search_key", "next_key")
    def strip_str(cls, v: str):
        return v.strip()


class OverseaDailyPriceResponse(APIResponse):
    class OverseaDailyPriceTicker(Response):
        rsym: str = Field(alias="symbol", description="종목코드")
        zdiv: str = Field(description="소수점자리수")
        nrec: Union[str, Decimal] = Field(alias="prev_close")

    class OverseaDailyPriceRow(Response):
        base_date: str = Field(alias="xymd", description="기준일")
        sign: Union[str, Decimal] = Field(description="대비기호", repr=False)
        diff: Union[str, Decimal] = Field(description="종가변동", repr=False)
        changes: Union[str, Decimal] = Field(alias="rate", description="전일비")
        open: Union[str, Decimal] = Field(description="시가")
        close: Union[str, Decimal] = Field(alias="clos", description="종가")
        high: Union[str, Decimal] = Field(description="고가")
        low: Union[str, Decimal] = Field(description="저가")
        volume: Union[str, Decimal] = Field(alias="tvol", description="거래량")
        trading_amount: Union[str, Decimal] = Field(alias="tamt", description="거래대금")

        pbid: Union[str, Decimal] = Field(description="매수호가", repr=False)
        vbid: Union[str, Decimal] = Field(description="매수호가잔량", repr=False)
        pask: Union[str, Decimal] = Field(description="매도호가", repr=False)
        vask: Union[str, Decimal] = Field(description="매도호가잔량", repr=False)

    ticker: OverseaDailyPriceTicker = Field(alias="output1")
    prices: List[OverseaDailyPriceRow] = Field(alias="output2")

    @validator("prices")
    def pop_empty(cls, prices: List[OverseaDailyPriceRow]):
        return [p for p in prices if p.close]


class OverseaQuotePriceResponse(APIResponse):
    class OverseaQuotePriceDetail(Response):
        symbol: str = Field(description="실시간조회종목코드", alias="rsym")
        zdiv: int = Field(description="소수점자리수")
        prev_close: Decimal = Field(description="전일종가", alias="base")
        prev_vol: Decimal = Field(description="전일거래량", alias="pvol")
        last: Decimal = Field(description="현재가")
        sign: str = Field(description="대비기호")
        diff: str = Field(description="전일대비")
        tvol: Decimal = Field(description="거래량")
        tamt: Decimal = Field(description="거래대금")
        oderable: str = Field(description="매수가능여부", alias="ordy")

    detail: OverseaQuotePriceDetail = Field(alias="output")

    """
-RSYM	실시간조회종목코드	String	Y	16	
-ZDIV	소수점자리수	String	Y	1	
-BASE	전일종가	String	Y	12	전일의 종가
-PVOL	전일거래량	String	Y	14	전일의 거래량
-LAST	현재가	String	Y	12	당일 조회시점의 현재 가격
-SIGN	대비기호	String	Y	1	1 : 상한, 2 : 상승, 3 : 보합, 5 : 하락
-DIFF	대비	String	Y	12	전일 종가와 당일 현재가의 차이 (당일 현재가-전일 종가)
-FLTT_RT	등락율	String	Y	12	전일 대비 / 당일 현재가 * 100
-TVOL	거래량	String	Y	14	당일 조회시점까지 전체 거래량
-TAMT	거래대금	String	Y	14	당일 조회시점까지 전체 거래금액
-ORDY	매수가능여부	String	Y	20	매수주문 가능 종목 여부    
'rsym' = {str} 'DNASQQQ'
'zdiv' = {str} '4'
'base' = {str} '286.6700'
'pvol' = {str} '63741837'
'last' = {str} '291.8700'
'sign' = {str} '2'
'diff' = {str} '5.2000'
'rate' = {str} '+1.81'
'tvol' = {str} '63818149'
'tamt' = {str} '18572778698'
'ordy' = {str} '매도불가'
    """


class OverseaBidOrderResponse(APIResponse):
    class OverseaBidOrderDetail(Response):
        KRX_FWDG_ORD_ORGNO: str = Field(alias="krx_org_no", description="종목코드")
        ODNO: str = Field(alias="ord_no")
        ORD_TMD: str = Field(alias="order_time")

    detail: OverseaBidOrderDetail = Field(alias="output")


class OverseaAskOrderResponse(APIResponse):
    class OverseaAskOrderDetail(Response):
        KRX_FWDG_ORD_ORGNO: str = Field(alias="krx_org_no", description="종목코드")
        ord_no: str = Field(alias="ODNO")
        order_time: str = Field(alias="ORD_TMD")

    detail: OverseaAskOrderDetail = Field(alias="output")


class OverseaChangeOrderResponse(APIResponse):
    class OverseaChangeOrderDetail(Response):
        krx_org_no: str = Field(alias="KRX_FWDG_ORD_ORGNO", description="종목코드")
        ord_no: str = Field(alias="ODNO")
        order_time: str = Field(alias="ORD_TMD")

    detail: OverseaChangeOrderDetail = Field(alias="output")


class OverseaUnexecutedListResponse(APIResponse):
    class OverseaUnexecutedDetail(Response):
        ord_dt: str
        ord_gno_brno: str
        odno: str
        orgn_odno: str
        pdno: str
        prdt_name: str
        sll_buy_dvsn_cd: str
        sll_buy_dvsn_cd_name: str
        rvse_cncl_dvsn_cd: str
        rvse_cncl_dvsn_cd_name: str
        rjct_rson: str
        rjct_rson_name: str
        ord_tmd: str
        tr_mket_name: str
        tr_crcy_cd: str
        natn_cd: str
        natn_kor_name: str
        ft_ord_qty: str
        ft_ccld_qty: str
        nccs_qty: str
        ft_ord_unpr3: str
        ft_ccld_unpr3: str
        ft_ccld_amt3: str
        ovrs_excg_cd: str
        prcs_stat_name: str
        loan_type_cd: str
        loan_dt: str
        usa_amk_exts_rqst_yn: str

    detail: List[OverseaUnexecutedDetail] = Field(alias="output")


class OverseaOrderHistoryResponse(APIResponse):
    class OverseaOrderHistoryRowResponse(Response):
        ord_dt: str = Field(alias="order_date", description="주문일자")
        ord_gno_brno: str = Field(alias="order_branch_no", description="주문채번지점번호(계좌 개설 시 관리점으로 선택한 영업점의 고유번호)")
        odno: str = Field(alias="order_no", description="주문번호(접수한 주문의 일련번호)")
        orgn_odno: str = Field(alias="origin_order_no", description="원주문번호(정정 또는 취소 대상 주문의 일련번호)")
        sll_buy_dvsn_cd: str = Field(alias="trade_type", description="매도매수구분코드 (01: 매도, 02: 매수)")
        sll_buy_dvsn_cd_name: str = Field(alias="trade_type_name", description="매도매수구분코드명")
        rvse_cncl_dvsn: str = Field(alias="cancel_code", description="정정취소구분(01: 정정 02: 취소)")
        rvse_cncl_dvsn_name: str = Field(alias="cancel_code_name", description="정정취소구분명")
        pdno: str = Field(alias="symbol", description="상품번호")
        prdt_name: str = Field(alias="product_name", description="상품명")
        ft_ord_qty: str = Field(alias="ord_qty", description="주문수량")
        ft_ord_unpr3: str = Field(alias="ord_price", description="주문단가(주문가격)")
        ft_ccld_qty: str = Field(alias="exec_qty", description="체결수량")
        ft_ccld_unpr3: str = Field(alias="exec_price", description="체결단가3")
        ft_ccld_amt3: str = Field(alias="exec_amt", description="체결금액3")
        nccs_qty: str = Field(alias="unexec_qty", description="미체결수량")
        prcs_stat_name: str = Field(alias="status_name", description="처리상태명")
        rjct_rson: str = Field(alias="reject_reason", description="거부사유(정상 처리되지 못하고 거부된 주문의 사유)")
        ord_tmd: str = Field(alias="order_time", description="주문시각(주문 접수 시간)")
        tr_mket_name: str = Field(alias="market_name", description="거래시장명")
        tr_natn: str = Field(alias="nation_code", description="거래국가")
        tr_natn_name: str = Field(alias="nation_name", description="거래국가명")
        ovrs_excg_cd: str = Field(alias="market_code", description="해외거래소코드(NASD: 나스닥, NYSE : 뉴욕, AMEX : 아멕스, SEHK : 홍콩, SHAA : 중국상해, SZAA : 중국심천, TKSE : 일본")
        tr_crcy_cd: str = Field(alias="currency_code", description="거래통화코드")
        dmst_ord_dt: str = Field(alias="order_date_kst", description="국내주문일자")
        thco_ord_tmd: str = Field(alias="order_time_kst", description="당사주문시각")
        loan_type_cd: str = Field(alias="loan_code", description="대출유형코드")
        mdia_dvsn_name: str = Field(alias="channel", description="매체구분명")
        loan_dt: str = Field(alias="loan_date", description="대출일자")
        rjct_rson_name: str = Field(alias="reject_reason_name", description="거부사유명")

    ctx_area_fk200: str = Field(description="연속조회검색조건200", alias="search_key")
    ctx_area_nk200: str = Field(description="연속조회키200", alias="next_key")
    output: List[OverseaOrderHistoryRowResponse] = Field(alias="history")

    @property
    def has_next(self):
        return self.header['tr_cont'] == "M"

    @property
    def is_last(self):
        return self.header['tr_cont'] == "D"
