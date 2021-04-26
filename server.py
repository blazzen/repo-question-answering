import os

from cdqa.utils.download import download_model
from flask import Flask, render_template, request

from pipeline_runner import PipelineRunner
from prediction import Prediction

REPO_DIR = "/Users/blazzen/Documents/Development/razdolbai-chat"
SRC_DIR_SUFFIX = "src/main/java/com/razdolbai"
BERT_MODEL = "models/bert_qa.joblib"

print("Starting the application")

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

print("Checking BERT model existence")
if os.path.isfile(BERT_MODEL):
    print(f"Found model: {BERT_MODEL}")
else:
    print(f"Downloading model: {BERT_MODEL}")
    download_model(model='bert-squad_1.1', dir='./models')
print("Finished checking BERT model")

print("Initializing the pipeline...")

pipeline_runner = PipelineRunner(REPO_DIR, SRC_DIR_SUFFIX, BERT_MODEL)

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


app.run()
