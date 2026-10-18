from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from rag_system.base import SearchBase
from typing import List
from langchain_core.runnables import RunnableLambda, RunnablePassthrough


class BM25Search(SearchBase):
    def __init__(self, documents: List, k1: float = 1.25, b: float = 0.75):
        super().__init__(documents)
        self.model = BM25Retriever.from_documents(
            self.documents,
            bm25_params={
                'k1': k1, 'b': b
            },
            preprocess_func= self.tokenizer
        )
    
    def search(self, query, top_k):
        self.model.k = top_k
        return self.model.invoke(query)

class SemanticSearch(SearchBase):
    def __init__(self, documents: List) -> None:
        super().__init__(documents)
        self.model_name = "all-MiniLM-L6-v2"
        self.embedding = HuggingFaceEmbeddings(model_name=self.model_name)
        self.vector_store = Chroma.from_documents(documents,
                                                  embedding=self.embedding)
    
    def search(self, query: str, top_k: int) -> List:
        model = self.vector_store.as_retriever(
            kwargs={"k": top_k}
            )
        return model.invoke(query)

class HybridSearch(SearchBase):
    def __init__(self, documents: List, k1: float = 1.25, b: float = 0.75):
        super().__init__(documents)
        self.bm25_retriever = BM25Search(documents, k1, b)
        self.sementic_retriever = SemanticSearch(documents)
        self.model = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.sementic_retriever],
            weights = [0.5, 0.5])
    
    def search(self, query, top_k):
        return self.model.invoke(query) | RunnableLambda(lambda docs: docs[:top_k])
