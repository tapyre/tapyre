import app from "ags/gtk4/app";
import style from "./style.scss";
import Tapyre from "./tapyre";
import GLib from "gi://GLib";
import Gtk from "gi://Gtk?version=4.0";

let tapyre: Gtk.Window;

app.start({
  instanceName: "tapyre",
  css: style,
  requestHandler(request, res) {
    const [, argv] = GLib.shell_parse_argv(request);
    if (!argv) return res("argv parse error");

    switch (argv[0]) {
      case "toggle":
        tapyre.visible = !tapyre.visible;
        return res("ok");
      default:
        return res("unknown command");
    }
  },
  main() {
    tapyre = Tapyre() as Gtk.Window;
    app.add_window(tapyre);
    tapyre.present();
  },
});
