# simple_agent.py
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from abstractions.agent import Agent
from abstractions.llm import LLM

class PluginAgent(Agent):
    def __init__(self, tools: list, llm: LLM, system_prompt: str, verbose: bool):

        self.llm = llm.getLLM()

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=2,                   
            early_stopping_method="generate"
        )

    def ask(self, prompt: str) -> str:
        return self.agent.run(prompt)
