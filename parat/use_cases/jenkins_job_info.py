from parat.enums.jenkins import JenkinsJobStatus
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins.jenkins_utils import get_jenkins_job_dict_url_end_build_number


def get_jenkins_job_result_status(jenkins_request_settings: JenkinsRequestSettings, url_end: str, build_number: int) -> JenkinsJobStatus:
    response_dict = get_jenkins_job_dict_url_end_build_number(jenkins_request_settings, url_end, build_number)
    if response_dict is None:
        return JenkinsJobStatus.UNKNOWN
    if response_dict['result'] == 'SUCCESS':
        return JenkinsJobStatus.SUCCESS
    if response_dict['result'] == 'UNSTABLE':
        return JenkinsJobStatus.UNSTABLE
    else:
        return JenkinsJobStatus.FAILURE
