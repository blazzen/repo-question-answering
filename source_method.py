from source_object import SourceObject
from util import DEFAULT_OUTPUT_VALUE, datetime_str

METHOD_FULL_NAME_SEPARATOR = "::"


class SourceMethod(SourceObject):
    def __init__(self, name, is_abstract, surrounding_class):
        super().__init__(name)
        self.is_abstract = is_abstract
        self.params = []
        self.surrounding_class = surrounding_class
        self.initial_commit = None
        self.last_modification_commit = None

    def to_printable_dict(self):
        return {
            "Name": self.name,
            "Signature": self.get_signature(),
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
                self.last_modification_commit.msg if self.last_modification_commit else DEFAULT_OUTPUT_VALUE
        }

    def add_param(self, param):
        self.params.append(param)

    def get_signature(self):
        return self.name + "(" + ", ".join([x.type + " " + x.name for x in self.params]) + ")"

    def get_full_name(self):
        return METHOD_FULL_NAME_SEPARATOR.join([self.surrounding_class.name, self.name])

    def enrich_with_initial_commit_data(self, commit):
        self.initial_commit = commit

    def enrich_with_last_modification_commit_data(self, commit):
        self.last_modification_commit = commit
