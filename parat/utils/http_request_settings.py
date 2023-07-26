class HttpRequestSettings:
    def __init__(self, body: dict = None, proxy: dict = None, ssl: bool = False, auth: tuple = None):
        self.body = body
        self.proxy = proxy
        self.ssl = ssl
        self.auth = auth
