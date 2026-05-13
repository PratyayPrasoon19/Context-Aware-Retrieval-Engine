import unittest
from unittest.mock import patch, mock_open, MagicMock
import numpy as np

from pkg.services.rag_pipeline import (
    SemanticRAGPipeline,
    MockTextEmbeddingModel
)


class TestMockTextEmbeddingModel(unittest.TestCase):

    @patch('pkg.services.rag_pipeline.SentenceTransformer')
    def test_embedding_model_initialization(self, mock_sentence_transformer):

        mock_model = MagicMock()
        mock_sentence_transformer.return_value = mock_model

        embedding_model = MockTextEmbeddingModel()

        mock_sentence_transformer.assert_called_once_with(
            'all-MiniLM-L6-v2'
        )

        self.assertEqual(embedding_model.model, mock_model)

    @patch('pkg.services.rag_pipeline.SentenceTransformer')
    def test_get_embeddings(self, mock_sentence_transformer):

        mock_model = MagicMock()
        mock_model.encode.return_value = [[0.1, 0.2, 0.3]]

        mock_sentence_transformer.return_value = mock_model

        embedding_model = MockTextEmbeddingModel()

        texts = ["sample text"]

        embeddings = embedding_model.get_embeddings(texts)

        mock_model.encode.assert_called_once_with(texts)

        self.assertEqual(
            embeddings,
            [[0.1, 0.2, 0.3]]
        )


class TestSemanticRAGPipeline(unittest.TestCase):

    def setUp(self):

        self.pipeline = SemanticRAGPipeline(
            file_path='mock_file.txt'
        )

    @patch('builtins.open', new_callable=mock_open,
           read_data="This is logistics knowledge base content")
    @patch('pkg.services.rag_pipeline.RecursiveCharacterTextSplitter')
    @patch('pkg.services.rag_pipeline.faiss.IndexFlatIP')
    @patch('pkg.services.rag_pipeline.faiss.normalize_L2')
    def test_load_and_prepare_db(
        self,
        mock_normalize,
        mock_index_class,
        mock_splitter_class,
        mock_file
    ):

        mock_splitter = MagicMock()
        mock_splitter.split_text.return_value = [
            "chunk1",
            "chunk2"
        ]

        mock_splitter_class.return_value = mock_splitter

        mock_embeddings = np.array([
            [0.1, 0.2],
            [0.3, 0.4]
        ])

        self.pipeline.embedding_model.get_embeddings = MagicMock(
            return_value=mock_embeddings
        )

        mock_index = MagicMock()
        mock_index_class.return_value = mock_index

        self.pipeline.load_and_prepare_db()

        mock_file.assert_called_once_with(
            'mock_file.txt',
            'r',
            encoding='utf-8'
        )

        mock_splitter.split_text.assert_called_once()

        self.pipeline.embedding_model.get_embeddings.assert_called_once_with(
            ["chunk1", "chunk2"]
        )

        mock_normalize.assert_called_once()

        mock_index.add.assert_called_once()

        self.assertEqual(
            self.pipeline.chunks,
            ["chunk1", "chunk2"]
        )

        self.assertEqual(
            self.pipeline.index,
            mock_index
        )

    def test_retrieval_pipeline_without_index(self):

        with self.assertRaises(Exception) as context:

            self.pipeline.retrieval_pipeline(
                query="logistics query"
            )

        self.assertEqual(
            str(context.exception),
            "Vector database not initialized"
        )

    @patch('pkg.services.rag_pipeline.faiss.normalize_L2')
    def test_retrieval_pipeline_success(
        self,
        mock_normalize
    ):

        self.pipeline.chunks = [
            "chunk one",
            "chunk two",
            "chunk three"
        ]

        mock_index = MagicMock()

        mock_index.search.return_value = (
            np.array([[0.95, 0.90, 0.85]]),
            np.array([[0, 1, 2]])
        )

        self.pipeline.index = mock_index

        self.pipeline.embedding_model.get_embeddings = MagicMock(
            return_value=np.array([[0.5, 0.6]])
        )

        results = self.pipeline.retrieval_pipeline(
            query="supply chain",
            top_k=3
        )

        self.pipeline.embedding_model.get_embeddings.assert_called_once_with(
            ["supply chain"]
        )

        mock_normalize.assert_called_once()

        mock_index.search.assert_called_once()

        expected_results = [
            {
                "chunk": "chunk one",
                "score": 0.95,
                "rank": 1
            },
            {
                "chunk": "chunk two",
                "score": 0.90,
                "rank": 2
            },
            {
                "chunk": "chunk three",
                "score": 0.85,
                "rank": 3
            }
        ]

        self.assertEqual(
            results,
            expected_results
        )

    @patch('pkg.services.rag_pipeline.faiss.normalize_L2')
    def test_retrieval_pipeline_top_k(
        self,
        mock_normalize
    ):

        self.pipeline.chunks = [
            "chunk one",
            "chunk two"
        ]

        mock_index = MagicMock()

        mock_index.search.return_value = (
            np.array([[0.99]]),
            np.array([[1]])
        )

        self.pipeline.index = mock_index

        self.pipeline.embedding_model.get_embeddings = MagicMock(
            return_value=np.array([[0.2, 0.8]])
        )

        results = self.pipeline.retrieval_pipeline(
            query="warehouse",
            top_k=1
        )

        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]["chunk"],
            "chunk two"
        )

        self.assertEqual(
            results[0]["rank"],
            1
        )


if __name__ == '__main__':
    unittest.main()