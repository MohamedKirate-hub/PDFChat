from rag_system.retrieval import HybridSearch
from rag_system.generation import Generation
from rag_system.chunking import DocsChunking

class RagManager:
    def __init__(self, model_name:str, files_path):
        self.chunks = DocsChunking(files_path).get_documents()
        self.retriever = HybridSearch(self.chunks)
        self.model = Generation(model_name)

    def generate(self, query, top_k=5):
        data = self.retriever.search(query, top_k)
        self.model.set_documents(data)
        return self.model.generate(query)
