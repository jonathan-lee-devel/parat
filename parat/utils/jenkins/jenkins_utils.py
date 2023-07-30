from parat.enums.http_request_methods import HttpRequestMethod
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.request_retry import request_retry


def validate_max_retry(max_retry: int):
    if max_retry < 1 or max_retry > 100_000:
        raise Exception('Max retry value invalid')


def get_jenkins_console_output(jenkins_request_settings: JenkinsRequestSettings, job_name: str, build_number: int):
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.GET,
                         f'{jenkins_request_settings.url}/job/{job_name}/{build_number}/logText/progressiveText?start=0',
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


def start_jenkins_build(jenkins_request_settings: JenkinsRequestSettings, job_name: str):
    validate_max_retry(jenkins_request_settings.max_retry)
    return request_retry(HttpRequestMethod.POST,
                         f'{jenkins_request_settings.url}/job/{job_name}/build?delay=0sec',
                         jenkins_request_settings.max_retry,
                         HttpRequestSettings(None, None, False, jenkins_request_settings.auth)
                         )
