import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sms.log')),
        logging.StreamHandler(),
    ]
)

response_logger = logging.getLogger('response')
dec_logger = logging.getLogger('decorator')


def logged(func):
    def wrapper(request, *args, **kwargs):
        dec_logger.info(f'{func.__name__}: {request}')
        return func(request, *args, **kwargs)
    return wrapper
