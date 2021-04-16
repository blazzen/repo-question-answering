from source_method import SourceMethod

MAIN_METHOD_PURPOSE_PREFIX = "running "
MAIN_METHOD_NAME = "main"


class MainMethod(SourceMethod):
    def __init__(self, name, is_abstract, surrounding_class):
        super().__init__(name, is_abstract, surrounding_class)

    @property
    def purpose(self):
        return MAIN_METHOD_PURPOSE_PREFIX + self.surrounding_class.purpose
