from abstractions.plugin import Plugin
import subprocess
import os
import configparser
import shlex

class AppPlugin(Plugin):
    def __init__(self):
        self.prefix = "launch"
        self.name = "AppLauncher"
        self.prompt = "Opens a specified application, you got the following apps to choose" + self.get_all_apps() + "."

        self.app_map = self._build_app_map()

    def _build_app_map(self):
        desktop_dirs = [
            "/usr/share/applications",
            os.path.expanduser("~/.local/share/applications")
        ]

        app_map = {}
        for directory in desktop_dirs:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    if file.endswith(".desktop"):
                        file_path = os.path.join(directory, file)
                        try:
                            config = configparser.ConfigParser(interpolation=None)
                            config.read(file_path, encoding="utf-8")

                            if "Desktop Entry" in config:
                                de = config["Desktop Entry"]

                                if de.get("NoDisplay", "false").lower() == "true":
                                    continue
                                if de.get("Hidden", "false").lower() == "true":
                                    continue

                                name = de.get("Name")
                                exec_cmd = de.get("Exec")

                                if name and exec_cmd:
                                    exec_cmd = self._cleanup_exec(exec_cmd)
                                    app_map[name] = exec_cmd
                        except Exception:
                            pass
        return app_map

    def _cleanup_exec(self, exec_cmd: str) -> str:
        exec_cmd = exec_cmd.replace("%%", "%")
        for code in ("%f", "%F", "%u", "%U", "%i", "%c", "%k"):
            exec_cmd = exec_cmd.replace(code, "")
        return exec_cmd.strip()

    def get_all_apps(self) -> str:
        return ";" .join(sorted(self._build_app_map().keys()))

    def run(self, text: str):
        try:
            exec_cmd = self._find_exec_cmd(text)
            if not exec_cmd:
                return f"App '{text}' wurde nicht gefunden."

            parts = shlex.split(exec_cmd)
            subprocess.Popen(parts, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Sucsessfully started '{text}'"
        except Exception as e:
            return f"Error Starting '{text}': {e}"

    def _find_exec_cmd(self, text: str) -> str:
        if text in self.app_map:
            return self.app_map[text]

        for name, cmd in self.app_map.items():
            if name.lower() == text.lower():
                return cmd

        for name, cmd in self.app_map.items():
            if text.lower() in name.lower():
                return cmd

        return ""