class SizeError(Exception):
    def __init__(self, why):
        self.message = why
        super.__init__(self.message)
