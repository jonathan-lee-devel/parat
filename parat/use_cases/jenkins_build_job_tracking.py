"""Module containing functions related to jenkins build job tracking"""
import yaml

from parat.constants.jenkins_yaml import BUILD, HOSTS, JOBS, END
from parat.utils.jenkins_rest_api.validation_error import ValidationError


def validate_jenkins_job_build_tracking_yaml(build_jobs_tracking_yaml_file_path: str) -> list:
    """Validates jenkins job build tracking YAML input data"""
    validation_errors = []
    with open(build_jobs_tracking_yaml_file_path, 'r', encoding='utf-8') as yaml_file_contents:
        build_jobs_tracking_dict = yaml.safe_load(yaml_file_contents)
        for build_host_index in range(len(build_jobs_tracking_dict[BUILD][HOSTS])):
            try:
                build_jobs_tracking_dict[BUILD][HOSTS][build_host_index]
            except KeyError:
                validation_errors.append(
                    ValidationError(
                        f'{BUILD}.{HOSTS}[{build_host_index}]',
                        'Missing URL')
                )
            for job_index in range(
                    len(build_jobs_tracking_dict[BUILD][HOSTS][build_host_index][JOBS])
            ):
                try:
                    build_host = build_jobs_tracking_dict[BUILD][HOSTS][build_host_index]
                    if build_host[JOBS][job_index]['build_index'] is None:
                        raise KeyError('Missing build index')
                except KeyError:
                    validation_errors.append(
                        ValidationError(
                            f'{BUILD}.{HOSTS}[{build_host_index}].{JOBS}[{job_index}].build_index',
                            'Missing build index')
                    )
                try:
                    build_jobs_tracking_dict[BUILD][HOSTS][build_host_index][JOBS][job_index][END]
                except KeyError:
                    validation_errors.append(
                        ValidationError(
                            f'{BUILD}.{HOSTS}[{build_host_index}].{JOBS}[{job_index}].{END}',
                            'Missing job URL end')
                    )
    return validation_errors
