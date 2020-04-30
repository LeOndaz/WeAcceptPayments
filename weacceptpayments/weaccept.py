"""
Payments for WeAccept.co
"""
from .exceptions import AuthError, OrderError, PaymentError, ItemFormatError
from .misc import HTTP_CODES
from .consts import WeAcceptConsts
from .mixins import NetworkingClassMixin, BaseSignatureMixin
import json
import logging


class WeAcceptAuth(BaseSignatureMixin, NetworkingClassMixin):
    _allowed_kwargs = [
        'api_key'
    ]

    _MANDATORY_KWARGS = [
        'api_key'
    ]

    def start(self):
        api_key = self.kwargs['api_key']

        try:
            self.request = self.http_pool.request('POST',
                                                  WeAcceptConsts.AUTH_URL,
                                                  body=json.dumps({
                                                      'api_key': api_key
                                                  }),
                                                  headers=self.get_headers())
        except ConnectionError as e:  # @todo
            raise AuthError(e)

        self.response = json.loads(self.request.data)

        if self.request.status == HTTP_CODES.CREATED:
            self.auth_token = self.response['token']
            setattr(self, 'merchant_id', self.response['profile']['id'])
        else:
            raise AuthError(self.response)


class WeAcceptOrder(BaseSignatureMixin, NetworkingClassMixin):
    _allowed_kwargs = [
        'delivery_needed', 'merchant_id', 'amount_cents', 'currency', 'merchant_order_id',
        'items', 'shipping_data', 'auth', 'auth_token', 'merchant_id'
    ]

    _MANDATORY_IN_ORDER_DATA = [
        'merchant_id', 'merchant_order_id',
    ]  # @TODO 'items' should be mandatory.

    _MANDATORY_IN_ITEM_DATA = [
        'name', 'amount_cents'
    ]  # @TODO

    _MANDATORY_KWARGS = [
        *_MANDATORY_IN_ORDER_DATA[1:]
    ]

    def _validate_items(self):
        """
        Should make sure that each item in items has a name & a price.
        Otherwise, We get a server error. This is important as the server
        doesn't respond well to this.
        """
        items = self.kwargs['items']

        if len(items) == 0:
            raise ItemFormatError('Empty items list.')

        for item in items:
            if len(item.keys()) == len(self.get_mandatory_in_item_data()):
                for key in self.get_mandatory_in_item_data():
                    if key not in item:
                        raise ItemFormatError(f'Missing {key} from {item}')
            else:
                raise ItemFormatError('Items should only have name and amount_cents')

    def _validate_order(self):
        """
        Should make sure that the must-include data are included.
        :return:
        """
        for key in self.get_mandatory_in_order_data():
            if key not in self.kwargs:
                raise OrderError(f'Missing {key} in order_data')

    def get_mandatory_in_item_data(self):
        """
        'name', 'amount_cents' are mandatory. Server error if they are not included.
        """
        return self._MANDATORY_IN_ITEM_DATA

    def get_mandatory_in_order_data(self):
        """
        'merchant_id', 'merchant_order_id' are mandatory.
        """
        return self._MANDATORY_IN_ORDER_DATA

    def start(self):

        auth = self.kwargs.pop('auth', None)

        if auth is None:
            if self.kwargs.get('auth_token', None) is None:
                raise OrderError('Unspecified auth_token in order.')

            if self.kwargs.get('merchant_id', None) is None:
                raise OrderError('Unspecified merchant_id in order.')

        self.kwargs.setdefault('currency', 'EGP')
        self.kwargs.setdefault('delivery_needed', False)

        self._validate_order()

        if self.kwargs.get('items', None) is not None:
            self._validate_items()

        try:
            self.request = self.http_pool.request('POST',
                                                  f'{WeAcceptConsts.ORDERS_URL}?token={self.kwargs.get("auth_token", None) or auth.auth_token}',
                                                  body=json.dumps(self.kwargs),
                                                  headers=self.get_headers())
        except ConnectionError as e:
            return logging.error(f'Connection error, {e}')

        self.response = json.loads(self.request.data)
        if self.request.status == HTTP_CODES.CREATED:
            setattr(self, 'order_id', self.response['id'])
        else:
            raise OrderError(self.response)


class WeAcceptPayment(BaseSignatureMixin, NetworkingClassMixin):
    _allowed_kwargs = [
        'amount_cents', 'expiration', 'billing_data', 'currency', 'integration_id',
        'lock_order_when_paid', 'auth', 'auth_token', 'order', 'order_id'
    ]

    _MANDATORY_IN_PAYMENT_DATA = [
        'order_id', 'currency', 'integration_id', 'billing_data', 'amount_cents',
    ]

    _MANDATORY_KWARGS = [
        *_MANDATORY_IN_PAYMENT_DATA[2:]
    ]

    def start(self):

        auth = self.kwargs.pop('auth', None)
        order = self.kwargs.pop('order', None)

        if auth is None:
            if self.kwargs.get('auth_token', None) is not None:
                pass
            else:
                raise PaymentError('Unspecified auth_token in order.')

        if order is None:
            if self.kwargs.get('order_id', None) is not None:
                pass
            else:
                raise PaymentError('order_id is not included.')

        self.kwargs.setdefault('currency', 'EGP')
        self.kwargs.setdefault('lock_order_when_paid', False)

        for item in self._MANDATORY_IN_PAYMENT_DATA:
            if item not in self.kwargs:
                raise PaymentError(f'Missing {item} in payment_data')

        self.request = self.http_pool.request('POST',
                                              f"{WeAcceptConsts.PAYMENT_KEY_URL}?token={self.kwargs['auth_token']}",
                                              body=json.dumps(self.kwargs),
                                              headers=self.get_headers())

        self.response = json.loads(self.request.data)

        if 'token' in self.response:
            setattr(self, 'token', self.response['token'])
        else:
            raise PaymentError(self.response)
