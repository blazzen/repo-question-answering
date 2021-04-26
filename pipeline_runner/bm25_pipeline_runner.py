from pipeline_runner.pipeline_runner import PipelineRunner
from util.util import to_df


class BM25PipelineRunner(PipelineRunner):
    def __init__(self, repo_dir, src_dir_suffix, bert_model, top_n, retriever_score_weight):
        print("Initializing BM25 pipeline")
        super().__init__(repo_dir, src_dir_suffix, bert_model, top_n, retriever_score_weight)

        print("Fitting the pipeline")
        self.__fit_retriever()

    def __fit_retriever(self):
        self.cdqa_pipeline.fit_retriever(to_df(self.prediction_data))

    def get_predictions(self, query):
        return self.cdqa_pipeline.predict(query, return_all_preds=True)
