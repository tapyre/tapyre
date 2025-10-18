from abstractions.plugin import Plugin
class EchoTool(Plugin):
    def __init__(self):
        self.prefix = "echo"
        self.name = "echo"
        self.prompt = "Gibt den eingegebenen Text unverändert zurück."

    def run(self, text: str) -> str:
        return text