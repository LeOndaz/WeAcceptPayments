class WeAcceptConsts:
    MAIN_URL = 'https://accept.paymobsolutions.com/'
    AUTH_URL = f'{MAIN_URL}api/auth/tokens'
    ORDERS_URL = f'{MAIN_URL}api/ecommerce/orders'
    PAYMENT_KEY_URL = f'{MAIN_URL}api/acceptance/payment_keys'
    PROCESS_WALLET_PAYMENT_URL = f'{MAIN_URL}api/acceptance/pay'

    headers = {
        'Content-Type': 'application/json'
    }

# They are inside a class because I intend (not sure) to support multiple payments, but idk when
