import yaml

class SystemLoader:
    def __init__(self, path: str = "../config/system.yaml"):
        with open(path, "r") as f:
            self._config = yaml.safe_load(f)

    def get(self, query: str) -> str:
        return self._config.get(query)
