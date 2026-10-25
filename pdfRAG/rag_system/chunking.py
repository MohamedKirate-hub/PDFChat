from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from typing import List

class DocsChunking:
    def __init__(self, file_paths: List, chunk_size, chunk_overlap) -> None:
        self.file_paths = file_paths
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                            chunk_overlap=chunk_overlap)
        self.documents = self._load_docs()

    def _load_docs(self):
        documents = []
        for file_path in self.file_paths:
            path = Path(file_path)
            suffix = path.suffix.lower()

            if suffix == ".pdf":
                loader = PyPDFLoader(str(path), encoding="utf-8")
                documents.extend(loader.load())

            elif suffix in [".txt", ".md"]:
                loader = TextLoader(str(path), encoding="utf-8")
                documents.extend(loader.load())

            elif suffix == ".csv":
                loader = CSVLoader(file_path=str(path), encoding="utf-8")
                documents.extend(loader.load())

        return self.text_splitter.split_documents(documents)

    def _load_docs_django(self):
        pass

    def get_documents(self) -> List:
        return self.documents
