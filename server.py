import os

from cdqa.utils.download import download_model
from flask import Flask, render_template, request

from pipeline_runner import PipelineRunner
from prediction import Prediction

REPO_DIR = "/Users/blazzen/Documents/Development/razdolbai-chat"
SRC_DIR_SUFFIX = "src/main/java/com/razdolbai"
DEFAULT_MODEL = "models/bert_qa.joblib"

print("Starting the application")

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

print("Checking the model existence")
if os.path.isfile(DEFAULT_MODEL):
    print(f"Found model: {DEFAULT_MODEL}")
else:
    print(f"Downloading model: {DEFAULT_MODEL}")
    download_model(model='bert-squad_1.1', dir='./models')

print("Initializing the pipeline...")

pipeline_runner = PipelineRunner(REPO_DIR, SRC_DIR_SUFFIX, DEFAULT_MODEL)

print("Finished pipeline initialization")


@app.route('/')
def main_page():
    return render_template("main.html")


@app.route('/', methods=['POST'])
def process_query():
    query = request.form['text']
    print(f"Got query: {query}")

    print("Predicting...")
    raw_predictions = pipeline_runner.query(query)
    print("Finished prediction")

    predictions = [Prediction(x) for x in raw_predictions]
    return render_template("main_with_answers.html", predictions=predictions, answered_question=query)
