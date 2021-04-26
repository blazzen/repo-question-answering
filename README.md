How to prepare your environment:
```
pip install -r requirements.txt
```

How to run the server locally:

```
python server_runner.py
```

Example of running the code in Google Colab:
```
!git clone https://github.com/blazzen/razdolbai-chat.git
!git clone https://github.com/blazzen/repo-question-answering.git
%cd repo-question-answering
!pip install -r requirements.txt
```
```
from server import Server
from util.model_util import BERT_MODEL_PATH

REPO_DIR = "../razdolbai-chat"
SRC_DIR_SUFFIX = "src/main/java/com/razdolbai"

server = Server(
    repo_dir=REPO_DIR,
    src_dir_suffix=SRC_DIR_SUFFIX,
    bert_model=BERT_MODEL_PATH,
    runner_id="fasttext",
    use_ngrok=True
)
```
```
app = server.app


@app.route('/')
def main_page():
    return server.main_page()


@app.route('/', methods=['POST'])
def process_query():
    return server.process_query()


server.run()
```