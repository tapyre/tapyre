import gi
import threading

from implementations.plugin_agent import PluginAgent

gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")
from gi.repository import Gtk, Gdk
from gi.repository import GtkLayerShell  # type: ignore


class MyWindow(Gtk.Window):
    def __init__(self, agent: PluginAgent):
        Gtk.Window.__init__(self, title="tapyre")
        self.set_size_request(1000, 100)
        self.connect("key-press-event", self.on_key_press)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./src/style/main.css")
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

        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.box.pack_start(input_box, False, False, 10)

        self.prompt_label = Gtk.Label(label=" > ")
        self.prompt_label.set_name("prompt-label")
        input_box.pack_start(self.prompt_label, False, False, 0)

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


def start_gtk(agent: PluginAgent):
    win = MyWindow(agent=agent)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
