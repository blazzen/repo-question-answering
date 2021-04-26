from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok

from pipeline_runner.bm25_pipeline_runner import BM25PipelineRunner
from pipeline_runner.fasttext_pipeline_runner import FasttextPipelineRunner
from prediction import Prediction
from util.model_util import download_bert_model

DEFAULT_TOP_N = 5
DEFAULT_RETRIEVER_SCORE_WEIGHT = 1.0
DEFAULT_RUNNER = "bm25"
DEFAULT_USE_NGROK = False
RUNNERS = {"bm25": BM25PipelineRunner, "fasttext": FasttextPipelineRunner}


class Server:

    def __init__(
            self,
            repo_dir,
            src_dir_suffix,
            bert_model,
            top_n=DEFAULT_TOP_N,
            retriever_score_weight=DEFAULT_RETRIEVER_SCORE_WEIGHT,
            runner_id=DEFAULT_RUNNER,
            use_ngrok=DEFAULT_USE_NGROK
    ):
        print("Starting the application")

        self.repo_dir = repo_dir
        self.src_dir_suffix = src_dir_suffix
        self.bert_model = bert_model
        self.top_n = top_n
        self.retriever_score_weight = retriever_score_weight

        download_bert_model()

        if runner_id in RUNNERS:
            self.__init_runner(runner_id)
        else:
            raise ValueError(f"Unknown pipeline runner name: {runner_id}")

        self.app = Flask(__name__)
        if use_ngrok:
            run_with_ngrok(self.app)

    def run(self):
        self.app.run()

    def main_page(self):
        return render_template("main.html")

    def process_query(self):
        query = request.form['text']
        print(f"Got query: {query}")

        print("Predicting...")
        raw_predictions = self.runner.query(query)
        print("Finished prediction")

        predictions = [Prediction(x) for x in raw_predictions]
        return render_template("main_with_answers.html", predictions=predictions, answered_question=query)

    def __init_runner(self, runner_id):
        print("Initializing the pipeline...")
        self.runner = RUNNERS[runner_id](self.repo_dir, self.src_dir_suffix, self.bert_model, top_n=self.top_n,
                                         retriever_score_weight=self.retriever_score_weight)
        print("Finished pipeline initialization")
