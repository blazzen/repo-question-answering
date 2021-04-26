from string import punctuation

import nltk
import numpy as np
from nltk.corpus import stopwords
from sklearn.preprocessing import normalize

nltk.download("stopwords")


class FasttextVectorizer:
    def __init__(self, model):
        self.model = model
        self.eng_stopwords = stopwords.words("english")
        self.translator = str.maketrans('', '', punctuation)

    def remove_punctuation(self, doc):
        return doc.translate(self.translator)

    def lemmatize(self, doc):
        return [
            x.strip()
            for x in self.remove_punctuation(doc).split()
            if x.strip() and x not in self.eng_stopwords
        ]

    def get_sentence_vector(self, sentence):
        return normalize(
            np.expand_dims(
                normalize(
                    np.array(
                        [self.model.get_word_vector(x) for x in self.lemmatize(sentence)]
                    )
                ).sum(axis=0),
                axis=0
            )
        )
