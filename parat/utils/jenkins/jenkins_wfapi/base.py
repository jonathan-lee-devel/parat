"""wfapi base endpoint utilities module"""
from typeguard import typechecked

from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins.common_utils import get_json_response_dict
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings


@typechecked
def get_job_name_and_run_count(
        request_settings: JenkinsRequestSettings,
        job_name: str,
) -> dict:
    """Obtains job name and run count from job name"""
    response: dict = get_json_response_dict(f'{request_settings.url}/job/{job_name}/wfapi/',
                                            request_settings.max_retry,
                                            HttpRequestSettings(auth=request_settings.auth))
    return {'name': job_name, 'runCount': response['runCount']}
