"""
This is a payment library for WeAccept.co
It supports the basic operations there, Auth -> Order -> Pay.

The library takes a specific approach explained below.
- Each instance takes kwargs upon creation, We create instances by using a factory called as_instance(**kwargs)
- Kwargs are iterated and validated, They are set as an instance attribute after that, So instance.kwargs works.
- Upon validation, When everything is ready, The instance creates a POST request to the weaccept.co API and posts self.kwargs
- That's why there's a method called post_request_kwargs(url, body=None), It automatically posts the instance kwargs when they're ready.
"""