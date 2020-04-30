import urllib3
from weacceptpayments.decorators import classonlymethod
import logging
import json


class NetworkingClassMixin:
    response = None
    request = None
    auth_token = None

    http_pool = urllib3.PoolManager()

    def get_headers(self):
        """
        Override this if you want more headers if the server needed them one day.

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

    def __repr__(self):
        """
        The representation of the inheriting classes should be their response.
        """
        return f'{self.response}'

    def post_request_kwargs(self, url, token=None, body=None):
        """
        This is mainly created to override this behavior if you want to use requests library or whatever if you want better
        flexibility when dealing with the request or the response.

        """

        if token is None:
            token = self.kwargs["auth_token"]

        if body is None:
            body = json.dumps(self.kwargs)

        request = self.http_pool.request('POST',
                                         f'{url}?token={token}',
                                         body=body,
                                         headers=self.get_headers())

        return request


class BaseSignatureMixin:
    """
    :param _MANDATORY_KWARGS: Those are the kwargs needed to create the object, Not necessarily the kwargs needed to request the server.
    :param _allowed_kwargs: Those are the kwargs allowed by the server.
    """
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
        Treat this as a factory, This creates the instance based on kwargs, If someone tried to pass an existing method name as a parameter, Raise an explosion.
        """
        for key in cls.get_mandatory_kwargs():
            if key not in kwargs:
                raise AttributeError(f'You must include f{cls.get_mandatory_kwargs()}')

        for k, v in kwargs.items():
            if k not in cls._allowed_kwargs:
                raise KeyError(f'An unknown key {k} was specified.')

        # create an instance
        instance = cls(**kwargs)

        # to allow the instances to alter kwargs in their __init__
        if not hasattr(instance, 'kwargs'):
            instance.kwargs = kwargs

        instance.start()

        return instance

    def start(self):
        """
        If this is not overridden, Raise an Exception.
        """

        raise NotImplementedError("You've not implemented the start method")

    @classonlymethod
    def get_mandatory_kwargs(cls):
        """
        To override mandatory kwargs.
        """

        return cls._MANDATORY_KWARGS

    def __getattribute__(self, item):
        """
        Trying to access a None attribute raises AttributeError
        mainly created for trying to access request, response before calling as_instance()
        """
        if object.__getattribute__(self, item) is None:
            raise AttributeError(f"{self.__class__.__name__} is not meant to be instantiated.")

        return object.__getattribute__(self, item)
