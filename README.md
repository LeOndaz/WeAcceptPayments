
## WeAcceptPayments  
Make payments using weaccept.co API and Python.  

### import 
<code> from weacceptpayments.weaccept import WeAcceptAuth, WeAcceptOrder, WeAcceptPayment </code>  
  
###  - specify auth data  
``` auth = WeAcceptAuth.as_instance(api_key='YOUR_API_KEY') ```

__PLEASE NOTE:__ 
- NEVER STORE YOUR API_KEY IN YOUR .py FILES, STORE IT IN AN ENVIRONMENT VARIABLE OR .env FILE AND USE python-dotenv  
### - create your order 
``` 
order = WeAcceptOrder.as_instance(auth=auth,
                                  merchant_id=auth.merchant_id,
                                  amount_cents=20000,
                                  merchant_order_id='gv12c4ttr',
                                   items=[  
                                           {  
                                             'name': 'taz1',  
                                             'amount_cents': 20000  
                                           }])
```

What kwargs are allowed? ``
```
_allowed_kwargs = { 
    'delivery_needed', 'merchant_id', 'amount_cents', 'currency', 'merchant_order_id',  
    'items', 'shipping_data', 'auth', 'auth_token', 'merchant_id'  
}
```
__PLEASE NOTE:__ 
- Specifying `auth` (takes in a `WeAcceptAuth` object) is an alternative way of specifying `auth_token` and `merchant_id`, Don't specify both at the same time.

Now you've access to `order.order_id`  
-  DONT TRY TO CREATE THE SAME ORDER TWICE.  
--  In case you did, `order.id` won't be created and you have to specify it manually. This is not a bug, When you create the order twice, The server returns 'duplicate' in the second time, And `order.id` is not in the `.response` so you need to specify it manually.  
  
### specify payment data  
```
payment = WeAcceptPayment.as_instance(auth_token=auth.auth_token,
                                                 order_id=order.order_id,
                                                 amount_cents=200,
                                                 integration_id=16639,
                                                 billing_data={  
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
                                                               ))
  ```
Now we have access to `.token` 
Again, What kwargs are allowed? 

```
_allowed_kwargs = {  
    'amount_cents', 'expiration', 'billing_data', 'currency', 'integration_id',  
    'lock_order_when_paid', 'auth', 'auth_token', 'order', 'order_id'  
}
```
- What kwargs are a mandatory? 
```
_MANDATORY_KWARGS = {  
    # amount cents must be specified and the server says duplicate order if it's not.  
    'merchant_order_id', 'merchant_id', 'amount_cents'  
}
```

  __PLEASE NOTE:__ 
  - Specifying `auth` (takes in a `WeAcceptAuth` object) is an alternative way of specifying `auth_token`, Don't specify both at the same time.
  - Specifying `order` (takes in a `WeAcceptOrder` object) is an alternative way of specifying `order_id`. Don't specify both at the same time.
  
  <hr>
Now, add an iFrame with the integration_id of the card in your payment integrations section and the payment_token you got from here.  
  
Tada! This is magic btw.  
  

  
- __In each of those objects, You have access to .request, .response, .headers, other things too (Explore or use IntelliCode)__  
- <br>
- __In each of those objects, You can access the response as obj[key] BUT after you call .start() otherwise, Exceptions are raised.__  
  
 ### @TODO
- Verification of `merchant_order_id` which is an alpha-numeric value.
- Verification of `shipping data` if `delivery_needed` is specified as True.
  
Feel free to explore.  
