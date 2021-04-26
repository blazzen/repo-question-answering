import re

from source_objects.source_file import SourceFile
from util.util import date_str

METHOD_PARAGRAPH_START = "Method"


class SourceParagraphsTransformer:
    def __init__(self, src_files):
        self.methods_by_paragraph = {
            SourceParagraphsTransformer.build_paragraph_str(file=x.surrounding_class, method=x): x
            for x in [
                m for sublist in [
                    f.methods
                    for f in src_files
                    if not f.is_abstract
                ]
                for m in sublist
            ]
        }

    def from_prediction(self, prediction):
        paragraph = prediction["paragraph"]
        if str.startswith(paragraph, METHOD_PARAGRAPH_START):
            if paragraph in self.methods_by_paragraph:
                return self.methods_by_paragraph[paragraph]
            return None
        raise ValueError(f"Unknown paragraph type '{paragraph}'")

    @staticmethod
    def to_paragraph_like_view(files):
        return [[x.purpose, SourceParagraphsTransformer.to_paragraphs(x)] for x in files if not x.is_abstract]

    @staticmethod
    def to_paragraphs(src_obj):
        if isinstance(src_obj, SourceFile):
            return SourceParagraphsTransformer.file_to_paragraphs(src_obj)
        else:
            raise ValueError(f"Unknown source object type {type(src_obj)}")

    @staticmethod
    def file_to_paragraphs(src_file):
        return [[SourceParagraphsTransformer.build_paragraph_str(file=src_file, method=x), x]
                for x in src_file.methods
                if not x.is_abstract]

    @staticmethod
    def build_paragraph_str(file, method):
        author = f"{METHOD_PARAGRAPH_START} \"{method.name}\" was implemented by {method.initial_commit.author.name}."
        purpose = f"Its purpose is {method.purpose} for {file.purpose}."
        commit_msg = f"The method was created with message: \"{method.initial_commit.msg}\"."
        commit_date = f"The method was created on {date_str(method.initial_commit.committer_date)}."

        tokens = ""
        if method.has_invocations():
            tokens = f"The method tokens are: {method.tokenize()}."

        return " ".join([author, purpose, commit_msg, commit_date, tokens])
