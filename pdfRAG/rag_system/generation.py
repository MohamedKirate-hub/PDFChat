from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from rag_system.augemntation import Augment
from django.conf import settings

class Generation:
    def __init__(self, history=None):
        self.history = history or []
        self.model_name = settings.MODEL_NAME
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.pipeline = pipeline(
            task = "text-generation",
            model = self.model, tokenizer = self.tokenizer,
            return_full_text = False,
            max_new_tokens = 200,
        )
        self.llm = HuggingFacePipeline(pipeline=self.pipeline)
    
    def set_documents(self, documents):
        self.documents = documents
        self.augment = Augment(self.documents, self.history)
    
    def generate(self, query):
        prompt_template = self.augment.build_prompt(query)
        prompt = self.tokenizer.apply_chat_template(
            prompt_template,
            tokenize=False,
            add_generation_prompt = True,
            enable_thinking = False,
        )
        answer = self.llm.invoke(prompt)
        self.history.extend(
            [
                {"role": "user", "content": query},
                {"role": "assistant", "content": answer}
            ]
        )
        return answer
