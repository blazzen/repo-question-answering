from source_objects.source_method import SourceMethod

MAIN_METHOD_PURPOSE_PREFIX = "running "
MAIN_METHOD_NAME = "main"


class MainMethod(SourceMethod):
    def __init__(self, name, body, line, invocations, surrounding_class):
        super().__init__(name, body, line, invocations, surrounding_class)

    @property
    def purpose(self):
        return MAIN_METHOD_PURPOSE_PREFIX + self.surrounding_class.purpose
