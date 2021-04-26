import os

import javalang

from source_objects.method_factory import MethodFactory
from source_objects.source_method_param import SourceMethodParam
from source_objects.source_object import SourceObject
from util.util import get_pure_filename


class SourceFile(SourceObject):
    def __init__(self, path):
        self.methods = []
        self.is_abstract = True
        self.path = path
        self.filename = os.path.split(path)[-1]
        pure_filename = get_pure_filename(self.filename)
        super().__init__(pure_filename)

        source_code = self.read_file_source_code(path)
        self.__parse_source_code(source_code)

    def to_printable_dict(self):
        return {
            "Filename": self.filename,
            "Purpose": self.purpose,
            "Path": self.path,
            "Abstract?": self.is_abstract,
            "Methods": [x.to_printable_dict() for x in self.methods]
        }

    def __parse_source_code(self, source_code):
        tree = javalang.parse.parse(source_code)

        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            invocations = list(node.filter(javalang.tree.MethodInvocation))
            src_method = MethodFactory(
                name=node.name,
                body=node.body,
                line=node.position[0] // 2 + 1,
                invocations=invocations,
                surrounding_class=self
            ).resolve()

            for param in node.parameters:
                src_method.add_param(SourceMethodParam(param))

            self.__add_method(src_method)

    def __add_method(self, method):
        self.methods.append(method)

        if not method.is_abstract:
            self.is_abstract = False

    @staticmethod
    def read_file_source_code(path):
        with open(path, "r") as file:
            return "\n".join(file.readlines())
