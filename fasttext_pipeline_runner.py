import fasttext

from fast_text_vectorizer import FasttextVectorizer
from model_util import download_fasttext_model, FASTTEXT_MODEL_PATH
from pipeline_runner import PipelineRunner


class FasttextPipelineRunner(PipelineRunner):
    def __init__(self, repo_dir, src_dir_suffix, bert_model):
        print("Initializing fastText pipeline")
        super().__init__(repo_dir, src_dir_suffix, bert_model)

        download_fasttext_model()

        print("Fitting the pipeline")
        self.vectorizer = FasttextVectorizer(self.model)
        self.model = fasttext.load_model(FASTTEXT_MODEL_PATH)
        self.fit_retriever()

    def fit_retriever(self):
        pass

