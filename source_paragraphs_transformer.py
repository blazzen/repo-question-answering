import re

from source_file import SourceFile
from util import datetime_str

METHOD_PARAGRAPH_START = "Method"


class SourceParagraphsTransformer:
    def __init__(self, src_files):
        self.files_by_purpose = {x.purpose: x for x in src_files}

    def from_prediction(self, prediction):
        paragraph = prediction["paragraph"]
        if str.startswith(paragraph, METHOD_PARAGRAPH_START):
            # todo: re-use constants
            groups = re.search("\"(.+?)\" was implemented by (.+?)\\. .+ for (.+?)\\.", paragraph)
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
        return [f"{METHOD_PARAGRAPH_START} \"{x.name}\" was implemented by {x.initial_commit.author.name}. " +
                f"Its purpose is {x.purpose} for {src_file.purpose}. " +
                f"The method was created with message: \"{x.initial_commit.msg}\". " +
                f"The method was created on {datetime_str(x.initial_commit.committer_date)}."
                for x in src_file.methods
                if not x.is_abstract]
