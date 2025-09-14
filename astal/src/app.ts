import app from "ags/gtk4/app";
import style from "./style.scss";
import Tapyre from "./tapyre";
import GLib from "gi://GLib";
import Gtk from "gi://Gtk?version=4.0";

let tapyre: Gtk.Window;

app.start({
  instanceName: "tapyre",
  css: style,
  requestHandler(argv: string[], response: (response: string) => void) {
    const [, arg] = argv;
    switch (argv[0]) {
      case "toggle":
        tapyre.visible = !tapyre.visible;
        return response("ok");
      default:
        return response("unknown command");
    }
  },
  main() {
    tapyre = Tapyre() as Gtk.Window;
    app.add_window(tapyre);
    // tapyre.present();
  },
});
