import gzip
import os
import shutil

import requests
from cdqa.utils.download import download_model

MODELS_DIR = "./models"

BERT_MODEL_FILENAME = "bert_qa.joblib"
BERT_MODEL_PATH = f"{MODELS_DIR}/{BERT_MODEL_FILENAME}"

FASTTEXT_MODEL_FILENAME = "cc.en.300.bin"
GZ_EXTENSION = "gz"
GZIPPED_FASTTEXT_MODEL_FILENAME = f"{FASTTEXT_MODEL_FILENAME}.{GZ_EXTENSION}"
GZIPPED_FASTTEXT_MODEL_URL = f"https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/{GZIPPED_FASTTEXT_MODEL_FILENAME}"
FASTTEXT_MODEL_PATH = f"{MODELS_DIR}/{FASTTEXT_MODEL_FILENAME}"


def download_bert_model():
    print("Checking BERT model existence")
    if os.path.isfile(BERT_MODEL_PATH):
        print(f"Found model: {BERT_MODEL_PATH}")
    else:
        print(f"Downloading model: {BERT_MODEL_PATH}")
        download_model(model='bert-squad_1.1', dir=MODELS_DIR)
    print("Finished checking BERT model")


def download_fasttext_model():
    print("Checking fastText model existence")
    if os.path.isfile(FASTTEXT_MODEL_PATH):
        print(f"Found model: {FASTTEXT_MODEL_PATH}")
    else:
        print(f"Downloading compressed fastText model from {GZIPPED_FASTTEXT_MODEL_URL}")
        r = requests.get(GZIPPED_FASTTEXT_MODEL_URL, allow_redirects=True)
        print(f"Finished downloading compressed fastText model")

        print("Decompressing fastText model")
        with open(GZIPPED_FASTTEXT_MODEL_FILENAME, 'wb') as f:
            f.write(r.content)
        with gzip.open(GZIPPED_FASTTEXT_MODEL_FILENAME, 'rb') as f_in:
            with open(FASTTEXT_MODEL_PATH, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("Finished decompression of fastText model")
