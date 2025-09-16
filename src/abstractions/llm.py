from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel
class LLM(ABC):
    @abstractmethod
    def getLLM(self) -> BaseChatModel:
        pass
