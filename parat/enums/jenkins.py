from enum import Enum


class JenkinsJobStatus(Enum):
    UNKNOWN = 0
    SUCCESS = 1
    UNSTABLE = 2
    FAILURE = 3
