import re

from source_file import SourceFile
from util import date_str

METHOD_PARAGRAPH_START = "Method"


class SourceParagraphsTransformer:
    def __init__(self, src_files):
        self.files_by_purpose = {x.purpose: x for x in src_files}

    def from_prediction(self, prediction):
        paragraph = prediction["paragraph"]
        if str.startswith(paragraph, METHOD_PARAGRAPH_START):
            # todo: re-use constants
            groups = re.search("\"(.+?)\" was implemented by (.+?)\\. .+? for (.+?)\\.", paragraph)
            method_name = groups.group(1)
            author = groups.group(2)
            file_purpose = groups.group(3)
            # todo: improve matching
            src_file = self.files_by_purpose[file_purpose]
            for method in src_file.methods:
                if method_name == method.name and method.initial_commit.author.name == author:
                    return method
            return None
        else:
            raise ValueError(f"Unknown paragraph type '{paragraph}'")

    @staticmethod
    def to_paragraph_like_view(files):
        return [[x.purpose, SourceParagraphsTransformer.to_paragraphs(x)] for x in files if not x.is_abstract]

    @staticmethod
    def to_paragraphs(src_obj):
        if isinstance(src_obj, SourceFile):
            return SourceParagraphsTransformer.__file_to_paragraphs(src_obj)
        else:
            raise ValueError(f"Unknown source object type {type(src_obj)}")

    @staticmethod
    def __file_to_paragraphs(src_file):
        return [SourceParagraphsTransformer.__build_paragraph_str(file=src_file, method=x)
                for x in src_file.methods
                if not x.is_abstract]

    @staticmethod
    def __build_paragraph_str(file, method):
        author = f"{METHOD_PARAGRAPH_START} \"{method.name}\" was implemented by {method.initial_commit.author.name}."
        purpose = f"Its purpose is {method.purpose} for {file.purpose}."
        commit_msg = f"The method was created with message: \"{method.initial_commit.msg}\"."
        commit_date = f"The method was created on {date_str(method.initial_commit.committer_date)}."

        tokens = ""
        if method.has_invocations():
            tokens = f"The method tokens are: {method.tokenize()}."

        return " ".join([author, purpose, commit_msg, commit_date, tokens])
