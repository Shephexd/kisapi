from common.enums import StrEnum


class OverseaOrderMarketCode(StrEnum):
    NYSE = "NYSE"
    NASDAQ = "NASD"
    AMEX = "AMEX"


class OverseaPriceMarketCode(StrEnum):
    NYSE = "NYS"
    NASDAQ = "NAS"
    AMEX = "AMS"


class OrderChangeCode(StrEnum):
    UPDATE = "01"
    CANCEL = "02"


class OverseaPricePeriod(StrEnum):
    DAILY = "0"
    WEEKLY = "1"
    MONTHLY = "2"
