
## WeAcceptPayments
Make payments using weaccept.co API and Python.

### import 
<code> from weacceptpayments.weaccept import WeAcceptAuth, WeAcceptOrder, WeAcceptPayment </code>

### specify auth data
<code> auth = WeAcceptAuth('YOUR_API_KEY') </code>

### start auth process
<code> auth.start() </code>

### create your order
<code> order = WeAcceptOrder(auth, {}, 'SPECIFY_A_MERCHANT_ORDER_ID', 200)</code>

### Order it
<code> order.order()</code>

### Now the order will get an order.id,
#  DONT TRY TO CREATE THE SAME ORDER TWICE.
### In case you did, order.id won't be created and you have to specify it manually. This is not a bug, When you create the order twice, The server returns 'duplicate' in the second time, And order.id is not in the response so you need to specify it manually.

### specify payment data
<code><pre>payment = WeAcceptPayment(auth, order, {}, {
&nbsp;        "apartment": "803",
&nbsp;        "email": "test@example.com",
&nbsp;        "floor": "42",
&nbsp;        "first_name": "LeOndaz",
&nbsp;        "street": "Python community",
&nbsp;        "building": "8028",
&nbsp;        "phone_number": "+0123456789",
&nbsp;        "shipping_method": "PKG",
&nbsp;        "postal_code": "01898",
&nbsp;        "city": "Jaskolskiburgh",
&nbsp;        "country": "CR",
&nbsp;        "last_name": "Nicolas",
&nbsp;        "state": "Utah"
&nbsp;   }, 13102, 200)</pre></code>

### start payment
<code> payment.start()</code>

<code> print(payment.token) # prints the token</code>

Now, add an iFrame with the integration_id of the card in your payment integrations section and the payment_token you got from here.

Tada! This is magic btw.

API Reference:
<ul>
 <li><code><pre>WeAcceptAuth(api_key)</pre></code></li>
        <li><code><pre>WeAcceptOrder(self,
                 we_accept_auth_object,
                 order_data,
                 merchant_order_id,
                 amount_cents,
                 currency='EGP',
                 shipping_data=None,
                 delivery_needed=False)</pre></code></li>
        <li><code><pre>WeAcceptPayment(self,
                 we_accept_auth_object,
                 order_data,
                 merchant_order_id,
                 amount_cents,
                 currency='EGP',
                 shipping_data=None,
                 delivery_needed=False)</pre></code></li>
                 
</ul>

#### In each of those objects, You have access to .requrest, .response, .headers, other things too (Explore or use intellicode)
#### In each of those objects, You can access the response as obj[key] BUT after you call .start() otherwise, Exceptions are raised.

Feel free to explore.
