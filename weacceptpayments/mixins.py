import urllib3
import inspect
from weacceptpayments.decorators import classonlymethod


class NetworkingClassMixin:
    response = None
    request = None

    http_pool = urllib3.PoolManager()

    def get_headers(self):
        """
        Override this if you want more headers
        """
        return {
            'Content-Type': 'application/json'
        }

    def __getitem__(self, item):
        """
        Delegate the [] operator to the response.
        """

        if self.response:
            return self.response.get(item, {'Error': 'Trying to access a non-existant key.'})

    def __str__(self):
        return f'{self.response}'


class BaseSignatureMixin:
    def __init__(self, **kwargs):
        """
        Make all kwarg keys as attributes with value same as the kwarg value
        """

        for (k, v) in kwargs.items():
            setattr(self, k, v)

    @classonlymethod
    def as_instance(cls, **kwargs):
        """
        Creates the instance based on kwargs, If someone tried to pass an existing method name as a parameter, Raise an explosion.
        """
        for key in cls._MUST_INCLUDE_KWARGS:
            if key not in kwargs:
                raise AttributeError(f'You must include f{self._MUST_INCLUDE_KWARGS}')

        for k, v in kwargs.items():
            if k not in cls._allowed_kwargs:
                raise KeyError(f'An unknown key {k} was specified.')

        instance = cls(**kwargs)
        instance.kwargs = kwargs
        instance.start()

        return instance

    def start(self):
        return {
            "Error": "You've not implemented the start method"
        }


class WeAcceptSharedDataMixin:
    auth_token = None


