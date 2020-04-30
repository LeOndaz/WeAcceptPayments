from weacceptpayments.weaccept import WeAcceptAuth, WeAcceptOrder, WeAcceptPayment


auth = WeAcceptAuth.as_instance(api_key="ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SnVZVzFsSWpvaWFXNXBkR2xoYkNJc0luQnliMlpwYkdWZmNHc2lPamsxTWpRc0ltTnNZWE56SWpvaVRXVnlZMmhoYm5RaWZRLkhPQ0VyTlVPOWdickllUHJ3bnpFOVNCajJPZEppTDZCUnJMM2RRcWY5RWhPVTFscjN0emhvOXpveVk0V25Qa3I0c3J5b0Frc3hHMVcybXpiUHhfNllR")

print(auth.auth_token)

order = WeAcceptOrder.as_instance(auth=auth, merchant_id=auth.merchant_id, amount_cents=20000, merchant_order_id='ccasfdqw', items=[
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