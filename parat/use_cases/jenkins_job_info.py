"""Jenkins Job Info Module"""
from typeguard import typechecked

from parat.enums.jenkins import JenkinsJobStatus
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins.jenkins_rest_api.jenkins_utils import (
    get_jenkins_build_dict_url_end_build_number,
)


@typechecked
def get_jenkins_job_result_status(
        jenkins_request_settings: JenkinsRequestSettings,
        url_end: str,
        build_number: int) -> JenkinsJobStatus:
    """Gets the result status of the Jenkins job run"""
    response_dict = get_jenkins_build_dict_url_end_build_number(
        jenkins_request_settings,
        url_end,
        build_number)
    if response_dict is not None:
        if response_dict['result'] == 'SUCCESS':
            return JenkinsJobStatus.SUCCESS
        if response_dict['result'] == 'UNSTABLE':
            return JenkinsJobStatus.UNSTABLE
    else:
        return JenkinsJobStatus.UNKNOWN

    return JenkinsJobStatus.FAILURE
