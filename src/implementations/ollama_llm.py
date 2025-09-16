from abstractions.llm import LLM
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.chat_models import ChatOllama

class OllamaLLM(LLM):
    def __init__(self, model: str, host: str, temperature: float, max_tokens: int):
        self.llm = ChatOllama(
            model=model,
            base_url=host,
            temperature=temperature,
            max_tokens=max_tokens
        )
    def getLLM(self) -> BaseChatModel:
        return self.llm
