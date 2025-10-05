class FileExtensionError(Exception):
    def __init__(self, message="Output file type should be .mp3") -> None:
        self.message = message
        super().__init__(self.message)

class InvalidTokenError(Exception):
    def __init__(self, message="Invalid AuthToken") -> None:
        self.message = message
        super().__init__(self.message)
