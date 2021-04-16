import json

from flask import Flask, render_template, request, jsonify

from pipeline_runner import PipelineRunner

REPO_DIR = "/Users/blazzen/Documents/Development/razdolbai-chat"
SRC_DIR_SUFFIX = "src/main/java/com/razdolbai"
DEFAULT_MODEL = "models/bert_qa.joblib"

print("Starting the application")

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
    predictions = pipeline_runner.query(query)
    print("Finished prediction")

    return jsonify(predictions)
