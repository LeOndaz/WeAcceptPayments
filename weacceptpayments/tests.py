import unittest
from .weaccept import WeAcceptAuth, WeAcceptOrder, WeAcceptPayment


class WeAcceptTest(unittest.TestCase):
    def test(self):
        auth = WeAcceptAuth.as_instance(
            api_key="api_key_here")

        self.assertIsNotNone(auth, 'Auth is none')
        self.assertIsNotNone(auth.auth_token, 'No auth token')

        order = WeAcceptOrder.as_instance(auth_token=auth.auth_token, merchant_id=auth.merchant_id, amount_cents=20000,
                                          merchant_order_id='gv12cttr', items=[
                {
                    'name': 'taz1',
                    'amount_cents': 20000
                }
            ])

        # to be continued
