"""wfapi base endpoint utilities module"""
from parat.enums.http_request_methods import HttpRequestMethod
from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins.common_utils import validate_max_retry
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.request_retry import request_retry


def get_job_name_and_run_count(
        request_settings: JenkinsRequestSettings,
        job_name: str,
):
    """Obtains job name and run count from job name"""
    validate_max_retry(request_settings.max_retry)
    response: dict = request_retry(HttpRequestMethod.GET,
                                   f'{request_settings.url}/job/{job_name}/wfapi/',
                                   request_settings.max_retry,
                                   HttpRequestSettings(None,
                                                       None,
                                                       False,
                                                       request_settings.auth)
                                   ).json()
    return {'name': job_name, 'runCount': response['runCount']}
