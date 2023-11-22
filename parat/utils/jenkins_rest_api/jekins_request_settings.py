class JenkinsRequestSettings:
    def __init__(self, url: str, auth: tuple, max_retry: int):
        self.url = url
        self.auth = auth
        self.max_retry = max_retry
