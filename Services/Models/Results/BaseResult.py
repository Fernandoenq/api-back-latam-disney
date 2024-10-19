class BaseResult:
    def __init__(self):
        self.errors = []
        self.is_valid = True

    def add_errors(self, errors):
        self.errors.extend(errors)
        self.is_valid = False

    def add_error(self, errors):
        self.errors.append(errors)
        self.is_valid = False
