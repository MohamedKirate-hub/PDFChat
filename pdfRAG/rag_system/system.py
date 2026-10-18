from rag_system.retrieval import HybridSearch
from rag_system.generation import Generation
from rag_system.chunking import DocsChunking

class RagManager:
    def __init__(self, documents):
        self.chunks = DocsChunking(documents).get_documents()
        self.retriever = HybridSearch(self.chunks)
        self.model = Generation()

    def generate(self, query, top_k=5):
        data = self.retriever.search(query, top_k)
        self.model.set_documents(data)
        return self.model.generate(query)