class Prediction:
    def __init__(self, raw_prediction):
        self.raw_prediction = raw_prediction

    @property
    def answer(self):
        return self.raw_prediction["text"]

    @property
    def probability(self):
        return self.raw_prediction["probability"]

    @property
    def paragraph(self):
        return self.raw_prediction["paragraph"]

    @property
    def retriever_score(self):
        return self.raw_prediction["retriever_score"]

    @property
    def final_score(self):
        return self.raw_prediction["final_score"]

    @property
    def source_object(self):
        return self.raw_prediction["src_obj"]