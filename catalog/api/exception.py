class BusinessException(Exception):
    def __init__(self, message, *args: object) -> None:
        super().__init__(*args)
        self.message = message

    @property
    def error(self):
        raise NotImplementedError('Abstract Method')

    def __str__(self):
        return self.message
