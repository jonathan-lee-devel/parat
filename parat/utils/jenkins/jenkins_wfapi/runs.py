"""wfapi runs endpoints utilities module"""
from typeguard import typechecked

from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins.common_utils import get_json_response_dict
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings


@typechecked
def get_job_runs_response_content(
        request_settings: JenkinsRequestSettings,
        job_name: str,
) -> list or dict:
    """Obtains run information from job name"""
    return get_json_response_dict(f'{request_settings.url}/job/{job_name}/wfapi/runs',
                                  request_settings.max_retry,
                                  HttpRequestSettings(auth=request_settings.auth))
