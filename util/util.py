import re

import pandas as pd

DEFAULT_OUTPUT_VALUE = "-"
DATE_TIME_FORMAT = "%B %d, %Y %H:%M:%S"
DATE_FORMAT = "%B %d, %Y"


def camel_str_to_sentence(str, lowercase=False):
    return " ".join(camel_case_split(str, lowercase))


def get_pure_filename(filename):
    return filename.rsplit(".", 1)[0]


def camel_case_split(identifier, lowercase=False):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0).lower() if lowercase else m.group(0) for m in matches]


def to_df(paragraph_like_view):
    return pd.DataFrame(paragraph_like_view, columns=['title', 'paragraphs'])


def datetime_str(datetime_obj):
    return datetime_obj.strftime(DATE_TIME_FORMAT)


def date_str(datetime_obj):
    return datetime_obj.strftime(DATE_FORMAT)


def flatten_list(li):
    return [x for sublist in li for x in sublist]
