"""Common util/helper functions for Jenkins"""
from parat.enums.http_request_methods import HttpRequestMethod
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.request_retry import request_retry


def validate_max_retry(max_retry: int):
    """Validates max retry parameter"""
    if max_retry < 1 or max_retry > 100_000:
        raise ValueError('Max retry value invalid')


def get_json_response_dict(
        url: str,
        max_retry: int,
        http_request_settings: HttpRequestSettings,
) -> dict:
    """Common util function which gets JSON response as dict"""
    validate_max_retry(max_retry)
    return (request_retry(HttpRequestMethod.GET,
                          url,
                          max_retry,
                          http_request_settings)
            .json())
