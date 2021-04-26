from util.util import camel_str_to_sentence


class SourceObject:
    def __init__(self, name):
        self.name = name

    @property
    def purpose(self):
        return camel_str_to_sentence(self.name, lowercase=True)
