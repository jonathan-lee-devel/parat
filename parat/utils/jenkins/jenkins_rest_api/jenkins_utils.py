"""Jenkins utilities module"""
from parat.enums.http_request_methods import HttpRequestMethod
from parat.exceptions.request_retry_exception import RequestRetryException
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins.common_utils import validate_max_retry
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.request_retry import request_retry


def get_jenkins_console_output(
        jenkins_request_settings: JenkinsRequestSettings,
        job_name: str,
        build_number: int):
    """Jenkins utility function which gets console output for a specific job's build"""
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_request_settings.url}/job/{job_name}/{build_number}'
                         '/logText/progressiveText?start=0',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(auth=jenkins_request_settings.auth)).text


def get_jenkins_console_output_url_end(
        jenkins_request_settings: JenkinsRequestSettings,
        url_end: str):
    """Gets console output for a specific job's build based on URL ending"""
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_request_settings.url}/{url_end}'
                         '/logText/progressiveText?start=0',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(auth=jenkins_request_settings.auth)
                         ).text


def get_jenkins_job_dict(
        jenkins_request_settings: JenkinsRequestSettings,
        job_name: str,
        build_number: int):
    """Gets Jenkins job JSON data for a specific job's build"""
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_request_settings.url}/job/{job_name}/{build_number}/api/json',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(auth=jenkins_request_settings.auth)
                         ).json()


def get_jenkins_job_dict_url_end(jenkins_request_settings: JenkinsRequestSettings, url_end: str):
    """Gets Jenkins job JSON data for a specific job's build based on URL ending"""
    validate_max_retry(jenkins_request_settings.max_retry)
    try:
        response_dict = (request_retry(HttpRequestMethod.GET,
                                       f'{jenkins_request_settings.url}/{url_end}/api/json',
                                       jenkins_request_settings.max_retry,
                                       HttpRequestSettings(auth=jenkins_request_settings.auth))
                         .json())
        return response_dict
    except RequestRetryException:
        return None


def get_jenkins_job_dict_url_end_build_number(
        jenkins_request_settings: JenkinsRequestSettings,
        url_end: str,
        build_number: int):
    """Gets Jenkins job JSON data based on URL end and build number"""
    validate_max_retry(jenkins_request_settings.max_retry)
    try:
        response_dict = (request_retry(HttpRequestMethod.GET,
                                       f'{jenkins_request_settings.url}/{url_end}/{build_number}'
                                       '/api/json',
                                       jenkins_request_settings.max_retry,
                                       HttpRequestSettings(auth=jenkins_request_settings.auth))
                         .json())
        return response_dict
    except RequestRetryException:
        return None


def start_jenkins_build(jenkins_request_settings: JenkinsRequestSettings, job_name: str):
    """Kicks off a build for specified Jenkins job based on job name"""
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.POST,
                         f'{jenkins_request_settings.url}/job/{job_name}/build?delay=0sec',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(auth=jenkins_request_settings.auth))


def start_jenkins_build_url_end(jenkins_request_settings: JenkinsRequestSettings, url_end: str):
    """Kicks off a build for a specified Jenkins job based on URL ending"""
    validate_max_retry(jenkins_request_settings.max_retry)
    try:
        status_code = request_retry(HttpRequestMethod.POST,
                                    f'{jenkins_request_settings.url}/{url_end}/build?delay=0sec',
                                    jenkins_request_settings.max_retry,
                                    HttpRequestSettings(auth=jenkins_request_settings.auth)
                                    ).status_code
        return status_code
    except RequestRetryException:
        return 500
