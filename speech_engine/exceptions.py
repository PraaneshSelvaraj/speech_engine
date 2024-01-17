class FileExtensionError(Exception):
    def __init__(self, message="Output file type should be .mp3"):
        self.message = message
        super().__init__(self.message)

class InvalidTokenError(Exception):
    def __init__(self, message="Invalid AuthToken"):
        self.message = message
        super().__init__(self.message)
