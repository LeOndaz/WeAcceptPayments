import urllib3
from weacceptpayments.decorators import classonlymethod
import logging


class NetworkingClassMixin:
    response = None
    request = None
    auth_token = None

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
            return self.response.get(item, {'Error': 'Trying to access a non-existent key.'})

    def __str__(self):
        return f'{self.response}'


class BaseSignatureMixin:
    _MANDATORY_KWARGS = None
    _allowed_kwargs = None

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
        for key in cls._MANDATORY_KWARGS:
            if key not in kwargs:
                raise AttributeError(f'You must include f{cls._MANDATORY_KWARGS}')

        for k, v in kwargs.items():
            if k not in cls._allowed_kwargs:
                raise KeyError(f'An unknown key {k} was specified.')

        instance = cls(**kwargs)
        instance.kwargs = kwargs
        instance.start()

        return instance

    def start(self):
        raise NotImplementedError("You've not implemented the start method")

    def __getattribute__(self, item):
        """
        Trying to access a None attribute raises AttributeError
        mainly created for trying to access request, response before calling as_instance()
        """
        if object.__getattribute__(self, item) is None:
            raise AttributeError(f"{self.__class__.__name__} is not meant to be instantiated.")

        return object.__getattribute__(self, item)

