from pipeline_runner import PipelineRunner


class BM25PipelineRunner(PipelineRunner):
    def __init__(self, repo_dir, src_dir_suffix, bert_model):
        print("Initializing BM25 pipeline")
        super().__init__(repo_dir, src_dir_suffix, bert_model)

        print("Fitting the pipeline")
        self.fit_retriever()

    def fit_retriever(self):
        self.cdqa_pipeline.fit_retriever(self.data)
