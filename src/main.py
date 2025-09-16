from implementations.plugin_agent import PluginAgent
from implementations.ollama_llm import OllamaLLM
from runtime.config_loader import ConfigLoader
from runtime.system_loader import SystemLoader
from runtime.plugin_loader import PluginLoader


loader = PluginLoader()
plugins = loader.load() 
tools = []

for plugin in plugins:
    tools.append(plugin.to_langchain())

print(tools)
config = ConfigLoader() 
system = SystemLoader()
llm = OllamaLLM(
    config.get_llm_model(),
    config.get_llm_host(),
    config.get_llm_temperature(),
    config.get_llm_max_tokens()
)

plugin_agent = PluginAgent(tools, llm, system.get("app_agent"), config.get_llm_verbose())

print(plugin_agent.ask("Bitte starte die App Google Chrome"))


