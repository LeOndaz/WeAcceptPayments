"""
Payments for different payment gateways.
"""
import urllib3
import json
from .exceptions import AuthError, OrderError, PaymentError
from .misc import EVENTS
from .consts import WeAcceptConsts


class WeAcceptAuth:
    http_pool = None

    def __init__(self, api_key=None):
        WeAcceptAuth.http_pool = urllib3.PoolManager()

        self.api_key = api_key
        self.headers = WeAcceptConsts.headers

        self.request = None
        self.response = None
        self.token = None
        self.merchant_id = None

    def start(self):
        try:
            self.request = WeAcceptAuth.http_pool.request('POST',
                                        WeAcceptConsts.AUTH_URL,
                                        body=json.dumps({'api_key': self.api_key}),
                                        headers=self.headers)

            if self.request.status == 201:  # returns 201 as the token is created.
                self.response = json.loads(self.request.data.decode('utf-8'))
                self.token = self.response.get('token', None)
                self.merchant_id = self.response.get('profile', {}).get('id', None)  # @todo
                return EVENTS.SUCCESS
            else:
                raise AuthError(f'Authentication error with status code {self.request.status}')
        except Exception:  # for now, will be improved @todo
            raise AuthError("A problem occurred while authenticating.")

    def __getitem__(self, item):
        if self.response is not None:
            return self.response[item]
        else:
            raise KeyError(f'Trying to access response data without calling start on {self.__class__}')

    def __repr__(self):
        return f"Payment(api_key={self.api_key})"


class WeAcceptOrder:
    http_pool = None

    __MUST_INCLUDE_IN_ORDER_DATA = [
        'auth_token', 'merchant_id', 'merchant_order_id'
    ]

    def __init__(self,
                 we_accept_auth_object,
                 order_data,
                 merchant_order_id,
                 amount_cents,
                 currency='EGP',
                 shipping_data=None,
                 delivery_needed=False):

        WeAcceptOrder.http_pool = urllib3.PoolManager()

        self.auth_token = we_accept_auth_object.token
        self.merchant_id = we_accept_auth_object.merchant_id
        self.merchant_order_id = merchant_order_id
        self.amount_cents = amount_cents
        self.currency = currency
        self.delivery_needed = delivery_needed
        self.shipping_data = shipping_data

        self.order_data = order_data
        self.order_data['auth_token'] = we_accept_auth_object.token
        self.order_data['merchant_id'] = self.merchant_id
        self.order_data['merchant_order_id'] = merchant_order_id
        self.order_data['currency'] = 'EGP'
        self.order_data['amount_cents'] = amount_cents

        self.headers = WeAcceptConsts.headers
        self.request = None
        self.response = None
        self.order_id = None

        if self.delivery_needed is True and 'shipping_data' not in self.order_data:
            raise OrderError(f"Delivery is needed but you didn't specify shipping_data")

        if self.delivery_needed is True and self.shipping_data is not None:
            self.order_data['shipping_data'] = self.shipping_data

    def order(self):
        for item in WeAcceptOrder.__MUST_INCLUDE_IN_ORDER_DATA:
            if item not in self.order_data:
                raise OrderError(f'Missing {item} in order_data')

        self.request = WeAcceptOrder.http_pool.request('POST',
                                    WeAcceptConsts.ORDERS_URL,
                                    body=json.dumps(self.order_data),
                                    headers=self.headers)

        self.response = json.loads(self.request.data.decode('utf-8'))

        if self.request.status == 201: # order created
            self.order_id = self.response['id']
            return EVENTS.SUCCESS
        else:
            raise OrderError('This order exists, and YOU MUST SPECIFY order_id for the instance YOURSELF')

    def __getitem__(self, item):
        if self.response is not None:
            return self.response[item]
        else:
            raise KeyError(f'Trying to access response data without calling start on {self.__class__}')

    def __setitem__(self, key, value):
        self.order_data[key] = value


class WeAcceptPayment:
    http_pool = None

    __MUST_INCLUDE_IN_PAYMENT_DATA = [
        'auth_token', 'order_id', 'integration_id', 'billing_data', 'currency', 'amount_cents'
    ]

    def __init__(self,
                 we_accept_auth_obj,
                 we_accept_order_obj,
                 payment_data,
                 billing_data,
                 integration_id,
                 amount_cents,
                 currency='EGP',
                 lock_order_when_paid=False
                 ):

        WeAcceptPayment.http_pool = urllib3.PoolManager()
        self.auth_token = we_accept_auth_obj.token
        self.order_id = we_accept_order_obj.order_id
        self.payment_data = payment_data
        self.billing_data = billing_data
        self.integration_id = integration_id
        self.amount_cents = amount_cents
        self.currency = currency
        self.lock_order_when_paid = lock_order_when_paid

        self.payment_data['auth_token'] = self.auth_token
        self.payment_data['order_id'] = self.order_id
        self.payment_data['billing_data'] = billing_data
        self.payment_data['integration_id'] = integration_id
        self.payment_data['amount_cents'] = amount_cents
        self.payment_data['currency'] = currency

        if lock_order_when_paid:
            self.payment_data['lock_order_when_paid'] = lock_order_when_paid

        self.request = None
        self.response = None
        self.status_code = None
        self.token = None

    def start(self):
        for item in self.payment_data:
            if item not in WeAcceptPayment.__MUST_INCLUDE_IN_PAYMENT_DATA:
                raise PaymentError(f'Missing {item} in payment_data')

        self.request = WeAcceptPayment.http_pool.request('POST', WeAcceptConsts.PAYMENT_KEY_URL, body=json.dumps(
            self.payment_data
        ), headers=WeAcceptConsts.headers)

        self.response = json.loads(self.request.data.decode('utf-8'))
        if 'token' in self.response: # means it worked.
            self.token = self.response['token']
            self.status_code = self.request.status
            return EVENTS.SUCCESS
            
        else:
            return self.response

    def __getitem__(self, item):
        if self.response is not None:
            return self.response[item]
        else:
            raise KeyError(f'Trying to access response data without calling start on {self.__class__}')

