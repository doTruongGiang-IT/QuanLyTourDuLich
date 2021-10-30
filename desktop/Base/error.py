class Error:
    def __init__(
        self, 
        status: bool, 
        message: str | None
    ):
        self.status = status
        self.message = message
