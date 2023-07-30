from parat.enums.http_request_methods import HttpRequestMethod
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.request_retry import request_retry


def validate_max_retry(max_retry: int):
    if max_retry < 1 or max_retry > 100_000:
        raise Exception('Max retry value invalid')


def get_jenkins_console_output(jenkins_url: str, auth: tuple, max_retry: int, job_name: str, build_number: int):
    validate_max_retry(max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_url}/job/{job_name}/{build_number}/logText/progressiveText?start=0',
                         max_retry,
                         HttpRequestSettings(None, None, False, auth)
                         ).text


def get_jenkins_job_dict(jenkins_url: str, auth: tuple, max_retry: int, job_name: str, build_number: int):
    validate_max_retry(max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_url}/job/{job_name}/{build_number}/api/json',
                         1,
                         HttpRequestSettings(None, None, False, auth)
                         ).json()


def start_jenkins_build(jenkins_url: str, auth: tuple, max_retry: int, job_name: str):
    validate_max_retry(max_retry)
    return request_retry(HttpRequestMethod.POST,
                         f'{jenkins_url}/job/{job_name}/build?delay=0sec',
                         1,
                         HttpRequestSettings(None, None, False, auth)
                         )
