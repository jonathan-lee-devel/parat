"""Common util/helper functions for Jenkins"""
from typeguard import typechecked

from parat.enums.http_request_methods import HttpRequestMethod
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.request_retry import request_retry


@typechecked
def validate_max_retry(max_retry: int) -> None:
    """Validates max retry parameter"""
    if max_retry < 1 or max_retry > 100_000:
        raise ValueError('Max retry value invalid')


@typechecked
def get_json_response_dict(
        url: str,
        max_retry: int,
        http_request_settings: HttpRequestSettings,
) -> list or dict:
    """Common util function which gets JSON response as dict"""
    validate_max_retry(max_retry)
    return (request_retry(HttpRequestMethod.GET,
                          url,
                          max_retry,
                          http_request_settings)
            .json())
