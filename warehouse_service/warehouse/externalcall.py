import requests

from django.conf import settings

from .circuitbreaker import CircuitBreaker, CircuitBreakerError


def health_order():
    import requests
    from django.conf import settings
    try:
        r = requests.get(f'{settings.ORDER_URL}ht')
        return True
    except Exception:
        return False

def health_warehouse():
    import requests
    from django.conf import settings
    try:
        r = requests.get(f'{settings.WAREHOUSE_URL}ht')
        return True
    except Exception:
        return False

def health_warranty():
    import requests
    from django.conf import settings
    try:
        r = requests.get(f'{settings.WARRANTY_URL}ht')
        print(r, f'{settings.WARRANTY_URL}ht')
        return True
    except Exception as e:
        return False


@CircuitBreaker(recovery_timeout=10, health_checker=health_order)
def call_order(method, url, data):
    return method(url, data=data)


@CircuitBreaker(recovery_timeout=10, health_checker=health_warehouse)
def call_warehouse(method, url, data):
    return method(url, data=data)


@CircuitBreaker(recovery_timeout=10, health_checker=health_warranty)
def call_warranty(method, url, data):
    return method(url, data=data)


def name_by_url(url):
    if url.startswith(settings.ORDER_URL): 
        return "Order"
    elif url.startswith(settings.WAREHOUSE_URL): 
        return "Warehouse"
    elif url.startswith(settings.WARRANTY_URL): 
        return "Warranty"
    return url


class ExternalCallException(Exception):
    pass


def external_call(method, url, data=None):
    try:
        if url.startswith(settings.ORDER_URL): 
            return call_order(method, url, data)
        elif url.startswith(settings.WAREHOUSE_URL): 
            return call_warehouse(method, url, data)
        elif url.startswith(settings.WARRANTY_URL): 
            return call_warranty(method, url, data)
    except CircuitBreakerError:
        raise ExternalCallException("CircuitBreaker error!")
    except requests.exceptions.RequestException:
        raise ExternalCallException(f"{name_by_url(url)} service is not available")
