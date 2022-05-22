import unittest
from kis.payload import BasePayload, DomesticBalancePayload


class TestPayload(unittest.TestCase):
    def test_query_params(self):
        payload = DomesticBalancePayload(account_number="12345678")
        self.assertTrue(len(payload.account_number) == 10)
        self.assertIsInstance(payload, BasePayload)
        self.assertIsInstance(payload.dict(), dict)
        self.assertIsInstance(payload.query_params, str)
