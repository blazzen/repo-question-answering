from pipeline_runner.pipeline_runner import PipelineRunner
from util.util import to_df


class BM25PipelineRunner(PipelineRunner):
    def __init__(self, repo_dir, src_dir_suffix, bert_model):
        print("Initializing BM25 pipeline")
        super().__init__(repo_dir, src_dir_suffix, bert_model)

        print("Fitting the pipeline")
        self.fit_retriever()

    def fit_retriever(self):
        transformed_data = [[f[0], [m[0] for m in f[1]]] for f in self.data]
        self.cdqa_pipeline.fit_retriever(to_df(transformed_data))
