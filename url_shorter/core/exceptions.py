class EmptyUrlException(Exception):
    def __init__(self, text):
        self.txt = text

class SubpartAlreadyExistsException(Exception):
    def __init__(self, text):
        self.txt = text