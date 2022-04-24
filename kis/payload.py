from urllib.parse import urlencode
from pydantic import BaseModel, Field, validator


class BasePayload(BaseModel):
    tr_id = Field(default="", description="Transaction ID", exclude=True)

    @property
    def query_params(self):
        return urlencode(self.dict())


class BalancePayload(BasePayload):
    tr_id = Field(default="TTTC8434R", description="Transaction ID", exclude=True)

    CANO: str = Field(
        alias="account_number", description="AccountNumber", min_length=8, max_length=10
    )
    ACNT_PRDT_CD: str = Field(
        alias="product_code", default="01", description="", repr=False
    )
    AFHR_FLPR_YN: str = Field(default="N", description="시간외단일가")
    OFL_YN: str = Field(default="", description="Offline flag", repr=False)
    INQR_DVSN: str = Field(default="02", description="조회구분", repr=False)
    UNPR_DVSN: str = Field(default="01", description="단가구분", repr=False)
    FUND_STTL_ICLD_YN: str = Field(default="N", description="펀드결제분포함", repr=False)
    PRCS_DVSN: str = Field(default="00", description="전일매매포함")
    CTX_AREA_FK100: str = Field(default="", description="연속조회조건검색", repr=False)
    CTX_AREA_NK100: str = Field(default="", description="연속조회키", repr=False)

    @validator("CANO")
    def validate_account_number(cls, v: str):
        if len(v) in [8, 10]:
            return v[:8]
        raise ValueError

    @property
    def account_number(self):
        return self.CANO + self.ACNT_PRDT_CD
