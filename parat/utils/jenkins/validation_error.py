class ValidationError:
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
