from abc import ABC, abstractmethod
class Agent(ABC):
    @abstractmethod
    def ask(self, prompt: str) -> str:
        pass
