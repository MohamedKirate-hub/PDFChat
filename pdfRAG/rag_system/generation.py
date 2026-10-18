from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from rag_system.augemntation import Augment

class Generation:
    def __init__(self, history=None):
        self.history = history or []
        self.model_name = "Qwen/Qwen3-0.6B"
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
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
            add_generation_prompt = True,
            tokenize = False, enable_thinking = False,
        )
        answer = prompt.invoke(query)
        self.history.extend(
            [
                {"role": "user", "content": query},
                {"role": "assistant", "content": answer}
            ]
        )
        return answer
