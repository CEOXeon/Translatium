from typeguard import typechecked


@typechecked
class TranslationError(Exception):
    def __init__(self, message, value=""):
        self.message = message
        self.value = value
        super().__init__(self.message)
    def __str__(self) -> str:
        return f'{self.message} -> {self.value}'
