"""wfapi base endpoint utilities module"""
from parat.enums.http_request_methods import HttpRequestMethod
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins.common_utils import validate_max_retry
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.request_retry import request_retry


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


def get_job_name_and_run_count(
        request_settings: JenkinsRequestSettings,
        job_name: str,
) -> dict:
    """Obtains job name and run count from job name"""
    response: dict = get_json_response_dict(f'{request_settings.url}/job/{job_name}/wfapi/',
                                            request_settings.max_retry,
                                            HttpRequestSettings(auth=request_settings.auth))
    return {'name': job_name, 'runCount': response['runCount']}
