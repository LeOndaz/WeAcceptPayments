import unittest
from .weaccept import WeAcceptAuth, WeAcceptOrder, WeAcceptPayment


class WeAcceptTest(unittest.TestCase):
    def test(self):
        # Create auth obj
        auth = WeAcceptAuth.as_instance(
            api_key="ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SndjbTltYVd4bFgzQnJJam81TlRJMExDSnVZVzFsSWpvaU1UVTRPRGN4TVRVM015NHdOakkxT1RjaUxDSmpiR0Z6Y3lJNklrMWxjbU5vWVc1MEluMC5yVklBWjNhb3ZYdnVPcW9OVHN3S0VSeWdjOWFQellRV0NBSDNUYUhFbGpXM3BPdkhXblZmSUY3RUNNWjRmQVUzMnFfeUNBamhZWUw5UmpHVFk4NWI3dw====")

        # auth obj created
        self.assertIsNotNone(auth, 'Auth is none')

        # auth token changed from None to a value
        self.assertTrue(hasattr(auth, 'auth_token'), 'No auth token')

        # Dynamically created merchant_id was set to a value.
        self.assertTrue(hasattr(auth, 'merchant_id'), "merchant_id wasn't created.")

        # merchant_id is int
        self.assertTrue(isinstance(auth.merchant_id, int), 'merchant_id is not int')

        # Create order obj
        order = WeAcceptOrder.as_instance(auth_token=auth.auth_token, merchant_id=auth.merchant_id, amount_cents=20000,
                                          merchant_order_id='gv12cct241tr', items=[
                {
                    'name': 'taz1',
                    'amount_cents': 20000
                }
            ])

        # kwargs that are validated on the instance level not in the factory.
        self.assertIn('delivery_needed', order.kwargs)
        self.assertIn('auth_token', order.kwargs)
        self.assertIn('merchant_id', order.kwargs)
        self.assertIn('merchant_order_id', order.kwargs)
        self.assertRegex(order.kwargs['merchant_order_id'], r'\w+', msg='merchant_order_id is not alpha-numeric')

        # Dynamically created order_id
        self.assertTrue(hasattr(order, 'order_id'), 'no order_id attribute was created')

        # Create payment obj

        payment = WeAcceptPayment.as_instance(auth=auth, order_id=order.order_id, amount_cents=20000,
                                              integration_id=16639, billing_data={
                "apartment": "803",
                "email": "test@example.com",
                "floor": "42",
                "first_name": "LeOndaz",
                "street": "Python community",
                "building": "8028",
                "phone_number": "+0123456789",
                "shipping_method": "PKG",
                "postal_code": "01898",
                "city": "Jaskolskiburgh",
                "country": "CR",
                "last_name": "whatever",
                "state": "RANDOM"
            })

        self.assertIn('auth_token', payment.kwargs)
        self.assertIn('order_id', payment.kwargs)

        # Dynamically created token

        self.assertTrue(hasattr(payment, 'token'))


if __name__ == '__main__':
    unittest.main()
