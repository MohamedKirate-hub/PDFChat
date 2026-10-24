from rag_system.retrieval import HybridSearch, SemanticSearch, BM25Search
from rag_system.generation import Generation
from rag_system.chunking import DocsChunking

class RagManager:
    def __init__(self, model_name:str, files_path, data):
        chunk_cofig = data.get("chunk_conf")
        retriever_conf = data.get("retriever_conf")

        chunk_size = chunk_cofig.get("chunk_size")
        overlap_size = chunk_cofig.get("overlap_size")
        self.retriever_type = data.get("type", "hybrid")

        self.chunks = DocsChunking(files_path,
                                   chunk_size=chunk_size,
                                   chunk_overlap=overlap_size).get_documents()
        if self.retriever_type == "semantic":
            self.retriever = SemanticSearch(self.chunks)
        else:
            b = retriever_conf.get("b", 0.75)
            k1 = retriever_conf.get("k1", 1.25)
            if self.retriever_type == "hybrid":
                self.retriever = HybridSearch(self.chunks, k1=k1, b=b)
            else:
                self.retriever = BM25Search(self.chunks, k1=k1, b=b)

        self.top_k = retriever_conf.get("top_k", 5)
        self.model = Generation(model_name)

    def generate(self, query):
        data = self.retriever.search(query, self.top_k)
        self.model.set_documents(data)
        return self.model.generate(query)
