from abc import ABC, abstractmethod
from typing import List
import regex

class SearchBase(ABC):
    def __init__(self, documents: List) -> None:
        self.documents = documents
        self.pattern = r'[a-zA-Z0-9]+'
    
    def tokenizer(self, text: str) -> List:
        return regex.findall(self.pattern, text)
    
    @abstractmethod
    def search(self, query: str, top_k: int) -> List:
        ...