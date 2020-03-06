class AuthError(Exception):
    """Raise for auth failure"""


class OrderError(Exception):
    """Raise for order creation failure"""


class PaymentError(Exception):
    """Raise for payment failure"""
