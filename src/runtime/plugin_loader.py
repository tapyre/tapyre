from __future__ import annotations

import inspect
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import List
from abstractions.plugin import Plugin


class PluginLoader:
    def __init__(self, plugins_dir: str | Path | None = None) -> None:
        if plugins_dir is None:
            plugins_dir = Path(__file__).parent / ".." / ".." / "plugins"
        self.plugins_dir = Path(plugins_dir).resolve()

    def load(self) -> List[Plugin]:
        if not self.plugins_dir.exists():
            print(f"[PluginLoader] Folder not Found: {self.plugins_dir}")
            return []

        plugins: List[Plugin] = []
        for file in sorted(self.plugins_dir.glob("*.py")):
            if file.name.startswith("_"):
                continue

            mod = self._import_module(file)
            if not mod:
                continue

            for _, cls in inspect.getmembers(mod, inspect.isclass):
                if cls.__module__ != mod.__name__:
                    continue
                if not issubclass(cls, Plugin) or cls is Plugin:
                    continue
                if inspect.isabstract(cls):
                    continue
                try:
                    instance = cls()
                    plugins.append(instance)
                except TypeError as e:
                    print(f"[PluginLoader] Couldn't load a instance of {cls.__name__}: {e}")

        return plugins

    def _import_module(self, file: Path):
        module_name = f"plugins_{file.stem}_{abs(hash(str(file)))}"
        spec = spec_from_file_location(module_name, file)
        if not spec or not spec.loader:
            print(f"[PluginLoader] Spec failed for: {file}")
            return None
        mod = module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)  # type: ignore[attr-defined]
            return mod
        except Exception as e:
            print(f"[PluginLoader] Error while importing  {file}: {e}")
            return None
