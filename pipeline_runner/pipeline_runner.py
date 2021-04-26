from abc import abstractmethod

from cdqa.pipeline import QAPipeline

import miner
from source_paragraphs_transformer import SourceParagraphsTransformer

SRC_OBJ_ATTRIBUTE = "src_obj"


class PipelineRunner:
    def __init__(self, repo_dir, src_dir_suffix, model):
        print("Mining repository data")
        self.repository_miner = miner.Miner(repo_dir, src_dir_suffix)
        self.data = self.repository_miner.mine()

        print("Fitting the pipeline")
        self.cdqa_pipeline = QAPipeline(reader=model, min_df=0.0, max_df=1.0, top_n=5)

    def query(self, query):
        predictions = self.cdqa_pipeline.predict(query, return_all_preds=True)
        result_transformer = SourceParagraphsTransformer(self.repository_miner.files)
        for prediction in predictions:
            prediction[SRC_OBJ_ATTRIBUTE] = result_transformer.from_prediction(prediction)
        return predictions

    @abstractmethod
    def fit_retriever(self):
        pass
