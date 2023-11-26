import unittest

from parat.utils.http_request_settings import HttpRequestSettings
from parat.utils.jenkins.jekins_request_settings import JenkinsRequestSettings
from parat.utils.jenkins.jenkins_rest_api.jenkins_utils import get_jenkins_build_dict


def return_valid_json_response(
        _: str,
        __: int,
        ___: HttpRequestSettings
) -> dict | list:
    return {}


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_get_jenkins_build_dict_when_invalid_max_retry_then_except(self):
        jenkins_request_settings: JenkinsRequestSettings = JenkinsRequestSettings(
            'http://localhost:8080',
            ('user', 'token'),
            0
        )
        job_name: str = 'TestJob'
        build_number: int = 2
        with self.assertRaises(ValueError):
            get_jenkins_build_dict(
                jenkins_request_settings,
                job_name,
                build_number,
                get_json_response=return_valid_json_response)



if __name__ == '__main__':
    unittest.main()
