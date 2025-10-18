from frontend.gtk import start_gtk
from implementations.plugin_agent import PluginAgent
from runtime.plugin_loader import PluginLoader
from runtime.config_loader import ConfigLoader
from implementations.ollama_llm import OllamaLLM
import yaml


def main():
    config_loader = ConfigLoader()
    plugin_loader = PluginLoader()

    with open("./src/config/system.yaml", "r") as f:
        system_config = yaml.safe_load(f)

    llm = OllamaLLM(
        model=config_loader.get_llm_model(),
        host=config_loader.get_llm_host(),
        temperature=config_loader.get_llm_temperature(),
        max_tokens=config_loader.get_llm_max_tokens(),
    )

    plugins = plugin_loader.load()
    tools = []
    for plugin in plugins:
        tools.append(plugin.to_langchain())

    agent = PluginAgent(
        tools=tools,
        llm=llm,
        system_prompt=system_config.get("app_agent"),
        verbose=config_loader.get_llm_verbose(),
    )

    start_gtk(agent)


if __name__ == "__main__":
    main()
