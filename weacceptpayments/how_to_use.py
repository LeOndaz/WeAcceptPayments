from weacceptpayments.weaccept import WeAcceptAuth, WeAcceptOrder, WeAcceptPayment

# this is okay, I change the api_key after each commit.
auth = WeAcceptAuth.as_instance(api_key="ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SndjbTltYVd4bFgzQnJJam81TlRJMExDSnVZVzFsSWpvaU1UVTRPRGN4TVRVM015NHdOakkxT1RjaUxDSmpiR0Z6Y3lJNklrMWxjbU5vWVc1MEluMC5yVklBWjNhb3ZYdnVPcW9OVHN3S0VSeWdjOWFQellRV0NBSDNUYUhFbGpXM3BPdkhXblZmSUY3RUNNWjRmQVUzMnFfeUNBamhZWUw5UmpHVFk4NWI3dw====")

print(auth.auth_token)

order = WeAcceptOrder.as_instance(auth=auth, merchant_id=auth.merchant_id, amount_cents=20000, merchant_order_id='h3hcc3466', items=[
    {
        "name": "taz1",
        "amount_cents": 20000
    }
])

print(order.order_id)

payment = WeAcceptPayment.as_instance(auth=auth, order_id=order.order_id, amount_cents=20000, integration_id=16639, billing_data={
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

