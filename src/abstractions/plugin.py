from abc import ABC, abstractmethod
from langchain_core.tools import Tool as LCTool

class Plugin(ABC): 
    prefix: str
    name: str
    prompt: str

    @property
    def Promt(self) -> str:  # noqa: N802
        return self.prompt
    
    @abstractmethod
    def run(self, text: str) -> str:
        pass

    def full_name(self) -> str:
        return self.name

    def to_langchain(self, *, return_direct: bool = False):
        tool = LCTool.from_function(
            name=self.full_name(),
            func=self.run,            
            description=self.prompt,
        )

        tool.return_direct = return_direct
        return tool
        
    def __call__(self, text: str) -> str:
        return self.run(text)