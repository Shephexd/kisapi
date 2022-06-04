from pydantic import BaseModel


class KISUser(BaseModel):
    apihost: str
    appkey: str
    appsecret: str
