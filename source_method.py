from source_object import SourceObject
from util import DEFAULT_OUTPUT_VALUE, datetime_str, camel_str_to_sentence

METHOD_FULL_NAME_SEPARATOR = "::"


class SourceMethod(SourceObject):
    def __init__(self, name, body, line, invocations, surrounding_class):
        super().__init__(name)
        self.body = body
        self.line = line
        self.invocations = invocations
        self.params = []
        self.surrounding_class = surrounding_class
        self.initial_commit = None
        self.last_modification_commit = None

    @property
    def is_abstract(self):
        return self.body is None

    def has_invocations(self):
        return len(self.invocations) != 0

    def tokenize(self):
        return " ".join([camel_str_to_sentence(x[1].member, True) for x in self.invocations])

    def to_printable_dict(self):
        return {
            "Name": self.name,
            "Signature": self.signature,
            "Class": self.surrounding_class.name,
            "Abstract?": self.is_abstract,
            "Created by (name)":
                self.initial_commit.author.name if self.initial_commit else DEFAULT_OUTPUT_VALUE,
            "Created by (email)":
                self.initial_commit.author.email if self.initial_commit else DEFAULT_OUTPUT_VALUE,
            "Created on":
                datetime_str(self.initial_commit.author_date) if self.initial_commit
                else DEFAULT_OUTPUT_VALUE,
            "Creation message":
                self.initial_commit.msg if self.initial_commit else DEFAULT_OUTPUT_VALUE,
            "Last modified by (name)":
                self.last_modification_commit.author.name if self.last_modification_commit else DEFAULT_OUTPUT_VALUE,
            "Last modified by (email)":
                self.last_modification_commit.author.email if self.last_modification_commit else DEFAULT_OUTPUT_VALUE,
            "Last modified on":
                datetime_str(self.last_modification_commit.author_date) if self.last_modification_commit
                else DEFAULT_OUTPUT_VALUE,
            "Last modification message":
                self.last_modification_commit.msg if self.last_modification_commit else DEFAULT_OUTPUT_VALUE,
            "Tokens": self.tokenize()
        }

    @property
    def signature(self):
        return self.name + "(" + ", ".join([x.type + " " + x.name for x in self.params]) + ")"

    @property
    def name_with_class(self):
        return METHOD_FULL_NAME_SEPARATOR.join([self.surrounding_class.name, self.name])

    @property
    def full_name(self):
        return METHOD_FULL_NAME_SEPARATOR.join([self.surrounding_class.name, self.signature])

    def add_param(self, param):
        self.params.append(param)

    def enrich_with_initial_commit_data(self, commit):
        self.initial_commit = commit

    def enrich_with_last_modification_commit_data(self, commit):
        self.last_modification_commit = commit
