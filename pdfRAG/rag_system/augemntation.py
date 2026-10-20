from typing import List, Dict
from transformers import PreTrainedTokenizer
from langchain_core.documents import Document

class Augment:
    def __init__(self, documents: List[Document], history: List[Dict]):
        self.documents = documents
        self.history = history or []
        self.instructions = self._set_instructions()

    def _set_instructions(self):
        return """
        answer the question from the context\nif there is no relation between question and context say just I do not know.
        """

    def _context_selection(self) -> str:
        context = []
        for i, doc in enumerate(self.documents, 1):
            if isinstance(doc, Document):
                content = doc.page_content
                metadata = doc.metadata
                chunk_id = f"Chunk: {i}"

                context.append(
                    f"{chunk_id}\n"
                    f"Metadata: {metadata}\n"
                    f"Content: {content}")

        return "\n\n".join(context)

    def build_prompt(self, query):
        context = self._context_selection()
        prompt = (
                f"Retrieved context:\n{context}\n\n"
                f"User question:\n{query}\n\n"
                "Answer the question using the instructions and context above."
            )
        return [
            {"role": "system", "content": self.instructions},
            *self.history,
            {"role": "user", "content": f"question: {query}\ncontext: {context}"}
        ]
