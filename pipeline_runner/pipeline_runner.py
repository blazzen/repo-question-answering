from abc import abstractmethod

from cdqa.pipeline import QAPipeline

import miner
from source_paragraphs_transformer import SourceParagraphsTransformer

SRC_OBJ_ATTRIBUTE = "src_obj"


class PipelineRunner:
    def __init__(self, repo_dir, src_dir_suffix, model, top_n, retriever_score_weight):
        print("Mining repository data")
        self.top_n = top_n
        self.retriever_score_weight = retriever_score_weight
        self.repository_miner = miner.Miner(repo_dir, src_dir_suffix)
        self.miner_data = self.repository_miner.mine()
        self.prediction_data = [[f[0], [m[0] for m in f[1]]] for f in self.miner_data]
        self.result_transformer = SourceParagraphsTransformer(self.repository_miner.files)

        print("Fitting the pipeline")
        self.cdqa_pipeline = QAPipeline(reader=model, min_df=0.0, max_df=1.0, top_n=self.top_n,
                                        retriever_score_weight=retriever_score_weight)

    def query(self, query):
        predictions = self.get_predictions(query)
        self.enrich_predictions(predictions)
        return predictions

    @abstractmethod
    def get_predictions(self, query):
        pass

    @abstractmethod
    def __fit_retriever(self):
        pass

    def enrich_predictions(self, predictions):
        for prediction in predictions:
            prediction[SRC_OBJ_ATTRIBUTE] = self.result_transformer.from_prediction(prediction)
