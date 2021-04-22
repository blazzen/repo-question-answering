from main_source_method import MainMethod, MAIN_METHOD_NAME
from source_method import SourceMethod


class MethodFactory:
    def __init__(self, name, body, line, invocations, surrounding_class):
        self.name = name
        self.body = body
        self.line = line
        self.invocations = invocations
        self.surrounding_class = surrounding_class

    def resolve(self):
        if MethodFactory.is_main(self.name):
            method = MainMethod
        else:
            method = SourceMethod
        return method(self.name, self.body, self.line, self.invocations, self.surrounding_class)

    @staticmethod
    def is_main(name):
        return name == MAIN_METHOD_NAME
