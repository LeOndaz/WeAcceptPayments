from weacceptpayments.weaccept import WeAcceptAuth, WeAcceptOrder, WeAcceptPayment


auth = WeAcceptAuth.as_instance(api_key="api_key_here")

order = WeAcceptOrder.as_instance(auth=auth, amount_cents=200, merchant_order_id='casc', items=[
    {
        'name': 'product_1',
        'amount_cents': 200
    }
])

payment = WeAcceptPayment.as_instance(auth=auth, order=order, amount_cents=200, integration_id=16639, billing_data={
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
    },
    )

print(payment.token) # works

#  TODO: validate merchant_order_id
