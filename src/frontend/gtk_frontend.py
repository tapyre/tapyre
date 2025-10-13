import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, Gdk
from gi.repository import GtkLayerShell  # type: ignore

from implementations.plugin_agent import PluginAgent
from runtime.plugin_loader import PluginLoader
from runtime.config_loader import ConfigLoader
from implementations.ollama_llm import OllamaLLM
import yaml
import threading


class MyWindow(Gtk.Window):
    def __init__(self, agent: PluginAgent):
        Gtk.Window.__init__(self, title="Simple GTK Frontend")
        self.set_size_request(1000, 100)
        self.connect("key-press-event", self.on_key_press)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style/main.css")
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        if screen:
            style_context.add_provider_for_screen(
                screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

        self.agent = agent

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.OVERLAY)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.EXCLUSIVE)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.box.set_name("main-box")
        self.add(self.box)

        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.box.pack_start(input_box, False, False, 10)

        prompt_label = Gtk.Label(label=" > ")
        input_box.pack_start(prompt_label, False, False, 0)

        self.entry = Gtk.Entry()
        self.entry.set_name("user-input")
        self.entry.connect("activate", self.on_entry_activate)
        input_box.pack_start(self.entry, True, True, 0)

    def on_entry_activate(self, entry):
        text = entry.get_text()
        entry.set_text("")
        self.hide()
        thread = threading.Thread(target=self.agent.ask, args=(text,))   
        thread.start()
        Gtk.main_quit()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()


def main():
    config_loader = ConfigLoader()
    plugin_loader = PluginLoader()

    with open("config/system.yaml", "r") as f:
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

    win = MyWindow(agent=agent)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
