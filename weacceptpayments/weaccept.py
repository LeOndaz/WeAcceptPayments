"""
Payments for different payment gateways.
"""
import json
from .exceptions import AuthError, OrderError, PaymentError, DirectAccessError, ItemFormatError
from .misc import HTTP_CODES
from .consts import WeAcceptConsts
from .mixins import NetworkingClassMixin, WeAcceptSharedDataMixin, BaseSignatureMixin
import logging


class WeAcceptAuth(WeAcceptSharedDataMixin, BaseSignatureMixin, NetworkingClassMixin):
    _allowed_kwargs = [
        'api_key'
    ]

    _MUST_INCLUDE_KWARGS = [
        'api_key'
    ]

    def start(self):
        try:
            self.request = self.http_pool.request('POST',
                                                  WeAcceptConsts.AUTH_URL,
                                                  body=json.dumps({'api_key': self.kwargs['api_key']}),
                                                  headers=self.get_headers())
        except ConnectionError as e:  # @todo
            raise AuthError(e)

        self.response = json.loads(self.request.data)

        if self.request.status == HTTP_CODES.CREATED:
            self.auth_token = self.response['token']
            self.merchant_id = self.response['profile']['id']

        else:
            raise AuthError(self.response)


class WeAcceptOrder(WeAcceptSharedDataMixin, BaseSignatureMixin, NetworkingClassMixin):
    _allowed_kwargs = [
        'delivery_needed', 'merchant_id', 'amount_cents', 'currency', 'merchant_order_id',
        'items', 'shipping_data', 'auth'
    ]

    _MUST_INCLUDE_IN_ORDER_DATA = [
        'merchant_id', 'merchant_order_id',
    ]  # @TODO 'items'

    _MUST_ONLY_INCLUDE_IN_ITEM_DATA = [
        'name', 'amount_cents'
    ]  # @TODO implement

    _MUST_INCLUDE_KWARGS = [
        'auth', *_MUST_INCLUDE_IN_ORDER_DATA
    ]

    order_id = None

    def _validate_items(self):
        """
        Should make sure that each item in items has a name & a price.
        Otherwise, We get a server error.
        :return:
        """
        items = self.kwargs['items']

        if len(items):
            raise ItemFormatError('Empty items list.')

        for item in items:
            if len(item.keys()) == len(self._MUST_ONLY_INCLUDE_IN_ITEM_DATA):
                for key in self._MUST_ONLY_INCLUDE_IN_ITEM_DATA:
                    if key not in item:
                        raise ItemFormatError(f'Missing {key} from {item}')
            else:
                raise ItemFormatError('Items should only have name and amount_cents')

    def _validate_mandatory_data(self):
        """
        Should make sure that the must-include data are included.
        :return:
        """
        for key in self._MUST_INCLUDE_IN_ORDER_DATA:
            if key not in self.kwargs:
                raise OrderError(f'Missing {key} in order_data')

    def get_must_only_include_in_items_data(self):
        return self._MUST_AND_ONLY_INCLUDE_IN_ITEM_DATA

    def get_must_include_in_order_data(self):
        return self._MUST_INCLUDE_IN_ORDER_DATA

    def start(self):

        auth = self.kwargs.pop('auth')

        self.kwargs.setdefault('currency', 'EGP')
        self.kwargs.setdefault('delivery_needed', False)

        self.kwargs['auth_token'] = auth.auth_token
        self.kwargs['merchant_id'] = auth.merchant_id

        self._validate_mandatory_data()

        if self.kwargs.get('items', None) is not None:
            self._validate_items()

        try:
            self.request = self.http_pool.request('POST',
                                                  f'{WeAcceptConsts.ORDERS_URL}?token={self.kwargs["auth_token"]}',
                                                  body=json.dumps(self.kwargs),
                                                  headers=self.get_headers())
        except ConnectionError as e:
            return logging.error(f'Connection error, {e}')

        self.response = json.loads(self.request.data)

        if self.request.status == HTTP_CODES.CREATED:
            self.order_id = self.response['id']

        else:
            raise OrderError(self.response)

    def __getattribute__(self, item):
        if object.__getattribute__(self, item) is None:
            raise DirectAccessError(f"{self.__class__.__name__} is not meant to be instantiated.")

        return object.__getattribute__(self, item)


class WeAcceptPayment(WeAcceptSharedDataMixin, BaseSignatureMixin, NetworkingClassMixin):
    _allowed_kwargs = [
        'amount_cents', 'expiration', 'billing_data', 'currency', 'integration_id',
        'lock_order_when_paid', 'auth', 'order',
    ]

    _MUST_INCLUDE_IN_PAYMENT_DATA = [
        'order_id', 'currency', 'integration_id', 'billing_data', 'amount_cents',
    ]

    _MUST_INCLUDE_KWARGS = [
        'order', *_MUST_INCLUDE_IN_PAYMENT_DATA[2:]
    ]

    def start(self):

        order = self.kwargs.pop('order')
        auth = self.kwargs.pop('auth')

        self.kwargs['auth_token'] = auth.auth_token
        self.kwargs['order_id'] = order.order_id

        self.kwargs.setdefault('currency', 'EGP')
        self.kwargs.setdefault('lock_order_when_paid', False)

        for item in self._MUST_INCLUDE_IN_PAYMENT_DATA:
            if item not in self.kwargs:
                raise PaymentError(f'Missing {item} in payment_data')

        self.request = self.http_pool.request('POST',
                                              f"{WeAcceptConsts.PAYMENT_KEY_URL}?token={self.kwargs['auth_token']}",
                                              body=json.dumps(self.kwargs),
                                              headers=self.get_headers())

        self.response = json.loads(self.request.data)
        print(self.response)
        if 'token' in self.response:
            self.token = self.response['token']

        else:
            return PaymentError(self.response)
