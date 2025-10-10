import yaml

class ConfigLoader:
    def __init__(self, path: str = "./config/config.yaml"):
        with open(path, "r") as f:
            self._config = yaml.safe_load(f)

    def get_llm_provider(self) -> str:
        return self._config.get("llm", {}).get("provider")

    def get_llm_model(self) -> str:
        return self._config.get("llm", {}).get("model")

    def get_llm_temperature(self) -> float:
        return self._config.get("llm", {}).get("temperature", 0.0)

    def get_llm_max_tokens(self) -> int:
        return self._config.get("llm", {}).get("max_tokens", 512)

    def get_llm_verbose(self) -> bool:
        return self._config.get("llm", {}).get("verbose", False)
    
    def get_llm_host(self) -> bool:
        return self._config.get("llm", {}).get("host", "http://localhost:11434")

    def get(self, key: str, default=None):
        """Generic getter"""
        parts = key.split(".")
        value = self._config
        for p in parts:
            value = value.get(p, {})
        return value if value != {} else default
