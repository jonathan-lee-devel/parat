from parat.enums.http_request_methods import HttpRequestMethod
from parat.exceptions.request_retry_exception import RequestRetryException
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins_rest_api.jekins_request_settings import JenkinsRequestSettings
from parat.utils.request_retry import request_retry


def validate_max_retry(max_retry: int):
    if max_retry < 1 or max_retry > 100_000:
        raise Exception('Max retry value invalid')


def get_jenkins_console_output(
        jenkins_request_settings: JenkinsRequestSettings,
        job_name: str,
        build_number: int):
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_request_settings.url}/job/{job_name}/{build_number}/logText/progressiveText?start=0',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                         ).text


def get_jenkins_console_output_url_end(jenkins_request_settings: JenkinsRequestSettings, url_end: str):
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_request_settings.url}/{url_end}/logText/progressiveText?start=0',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                         ).text


def get_jenkins_job_dict(jenkins_request_settings: JenkinsRequestSettings, job_name: str, build_number: int):
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_request_settings.url}/job/{job_name}/{build_number}/api/json',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                         ).json()


def get_jenkins_job_dict_url_end(jenkins_request_settings: JenkinsRequestSettings, url_end: str):
    validate_max_retry(jenkins_request_settings.max_retry)
    try:
        response_dict = request_retry(HttpRequestMethod.GET,
                                      f'{jenkins_request_settings.url}/{url_end}/api/json',
                                      jenkins_request_settings.max_retry,
                                      HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                                      ).json()
        return response_dict
    except RequestRetryException:
        return None


def get_jenkins_job_dict_url_end_build_number(jenkins_request_settings: JenkinsRequestSettings, url_end: str,
                                              build_number: int):
    validate_max_retry(jenkins_request_settings.max_retry)
    try:
        response_dict = request_retry(HttpRequestMethod.GET,
                                      f'{jenkins_request_settings.url}/{url_end}/{build_number}/api/json',
                                      jenkins_request_settings.max_retry,
                                      HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                                      ).json()
        return response_dict
    except RequestRetryException:
        return None


def start_jenkins_build(jenkins_request_settings: JenkinsRequestSettings, job_name: str):
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.POST,
                         f'{jenkins_request_settings.url}/job/{job_name}/build?delay=0sec',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                         )


def start_jenkins_build_url_end(jenkins_request_settings: JenkinsRequestSettings, url_end: str):
    validate_max_retry(jenkins_request_settings.max_retry)
    try:
        status_code = request_retry(HttpRequestMethod.POST,
                                    f'{jenkins_request_settings.url}/{url_end}/build?delay=0sec',
                                    jenkins_request_settings.max_retry,
                                    HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                                    ).status_code
        return status_code
    except RequestRetryException:
        return 500
