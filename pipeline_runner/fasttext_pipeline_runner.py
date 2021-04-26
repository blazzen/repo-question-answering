from collections import OrderedDict

import fasttext
import numpy as np
from cdqa.utils.converters import generate_squad_examples
from sklearn.metrics.pairwise import cosine_similarity

from pipeline_runner.fasttext_vectorizer import FasttextVectorizer
from pipeline_runner.pipeline_runner import PipelineRunner
from util.model_util import download_fasttext_model, FASTTEXT_MODEL_PATH
from util.util import flatten_list, to_df


class FasttextPipelineRunner(PipelineRunner):
    def __init__(self, repo_dir, src_dir_suffix, bert_model, top_n, retriever_score_weight):
        print("Initializing fastText pipeline")
        super().__init__(repo_dir, src_dir_suffix, bert_model, top_n, retriever_score_weight)

        download_fasttext_model()

        print("Fitting the pipeline")
        self.model = fasttext.load_model(FASTTEXT_MODEL_PATH)
        self.vectorizer = FasttextVectorizer(self.model)
        self.__fit_retriever()

    def __fit_retriever(self):
        self.flattened_paragraphs = flatten_list(self.prediction_data)
        self.paragraphs_embedding = np.concatenate(
            [self.vectorizer.get_sentence_vector(x) for x in self.flattened_paragraphs]
        )

    def get_predictions(self, query):
        query_embedding = self.vectorizer.get_sentence_vector(query)
        result = np.concatenate(
            (
                cosine_similarity(query_embedding, self.paragraphs_embedding),
                np.array([self.flattened_paragraphs])
            )
        ).T
        return self.get_bert_predictions(query, result)

    def get_bert_predictions(self, query, retriever_result):
        metadata = self.cdqa_pipeline._expand_paragraphs(to_df(self.prediction_data))
        indexed_top_scores = self.get_indexed_top_scores(retriever_result)

        squad_examples = generate_squad_examples(
            question=query,
            best_idx_scores=indexed_top_scores,
            metadata=metadata,
            retrieve_by_doc=False
        )
        examples, features = self.cdqa_pipeline.processor_predict.fit_transform(X=squad_examples)

        return self.cdqa_pipeline.reader.predict(
            X=(examples, features),
            n_predictions=None,
            retriever_score_weight=self.retriever_score_weight,
            return_all_preds=True
        )

    def get_indexed_top_scores(self, result):
        indexed_result = np.insert(result, 0, np.arange(result.shape[0]), axis=1)
        indexed_top_n_results = indexed_result[indexed_result[:, 1].argsort(-1)[::-1]][0:self.top_n, :-1]

        indexed_top_scores = OrderedDict()
        for row in indexed_top_n_results:
            indexed_top_scores[int(row[0])] = np.array([float(row[1])])
        return indexed_top_scores
