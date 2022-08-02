from urllib.parse import urljoin

import requests
import requests as req
from kis.connector.payload.base import (
    BasePayload,
    HashKeyPayload,
    IssueTokenPayload,
)


class KISAPIRequest:
    def __init__(self, host: str, headers: dict, payload: BasePayload):
        self.host = host
        self.headers = headers
        self.payload = payload

    def get(self) -> req.Response:
        return req.get(
            urljoin(self.host, self.payload.url_path, f"?{self.payload.query_params}"),
            headers=self.headers,
        )

    def post(self) -> req.Response:
        return req.post(
            urljoin(self.host, self.payload.url_path),
            headers=self.headers,
            json=self.payload.dict(),
        )


class KISConnector:
    def __init__(self, apihost, appkey, appsecret):
        self.apihost = apihost
        self.__appkey = appkey
        self.__appsecret = appsecret

    @property
    def default_headers(self):
        return {
            "content-type": "application/json;charset=utf-8",
            "appkey": self.__appkey.strip(),
            "appsecret": self.__appsecret.strip(),
            "custtype": "P",
        }

    def send(self, payload: BasePayload, access_token, **additional_headers):
        try:
            if payload.action_type == "GET":
                resp_header, parsed_resp = self.get_response(
                    payload=payload, access_token=access_token, **additional_headers
                )
            elif payload.action_type == "POST":
                resp_header, parsed_resp = self.post_response(
                    payload=payload, access_token=access_token, **additional_headers
                )
            else:
                raise KeyError({"detail": "Unsupported action type for payload"})
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(str(e))
        return payload.response_class(header=resp_header, **parsed_resp)

    def get_headers(self, tr_id=None, access_token=None):
        _headers = {
            **self.default_headers,
        }
        if tr_id is not None:
            _headers["tr_id"] = tr_id

        if access_token:
            _headers["Authorization"] = f"Bearer {access_token}"
        return _headers

    def check_response(self, resp: dict):
        if resp.get("rt_cd", -1) != "0":
            print(resp)
            raise requests.exceptions.InvalidJSONError(response=resp)

    def get_response(self, payload: BasePayload, access_token, **additional_headers):
        target_url = payload.get_url(
            api_host=self.apihost, query_params=payload.query_params
        )
        request_headers = self.get_headers(tr_id=payload.tr_id, access_token=access_token)
        request_headers.update(additional_headers)
        resp = req.request(
            method="get",
            url=target_url,
            headers=request_headers
        )
        parsed_resp = resp.json()
        self.check_response(resp=parsed_resp)
        return resp.headers, parsed_resp

    def post_response(self, payload: BasePayload, access_token: str, **additional_headers):
        target_url = payload.get_url(api_host=self.apihost)
        request_headers = self.get_headers(tr_id=payload.tr_id, access_token=access_token)
        body, hashkey = self.hash_data(data=payload.dict(by_alias=True))
        request_headers["hashkey"] = hashkey
        request_headers.update(additional_headers)

        resp = req.request(method="post", url=target_url, headers=request_headers, json=body)
        parsed_resp = resp.json()
        self.check_response(resp=parsed_resp)
        return resp.headers, parsed_resp

    def issue_token(self):
        payload: BasePayload = IssueTokenPayload(
            appkey=self.__appkey, appsecret=self.__appsecret
        )
        request = KISAPIRequest(
            host=self.apihost, headers=self.get_headers(), payload=payload
        )
        resp = request.post()
        return resp.json()

    def hash_data(self, data: dict) -> (dict, str):
        payload = HashKeyPayload(data=data)
        target_url = payload.get_url(api_host=self.apihost)
        resp = req.post(
            url=target_url, headers=self.get_headers(), data=payload.get_body()
        )
        resp.raise_for_status()
        resp_data = resp.json()
        return resp_data["BODY"], resp_data["HASH"]
