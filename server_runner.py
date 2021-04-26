from server import Server
from util.model_util import BERT_MODEL_PATH

REPO_DIR = "../razdolbai-chat"
SRC_DIR_SUFFIX = "src/main/java/com/razdolbai"

print("Starting the application")

server = Server(
    repo_dir=REPO_DIR,
    src_dir_suffix=SRC_DIR_SUFFIX,
    bert_model=BERT_MODEL_PATH
)

app = server.app


@app.route('/')
def main_page():
    return server.main_page()


@app.route('/', methods=['POST'])
def process_query():
    return server.process_query()


server.run()
