import { For, createState } from "ags";
import { Astal, Gtk, Gdk } from "ags/gtk4";
import { exec } from "ags/process";
import Graphene from "gi://Graphene";
import GLib from "gi://GLib";

const { TOP, BOTTOM, LEFT, RIGHT } = Astal.WindowAnchor;

export default function () {
  let contentbox: Gtk.Box;
  let searchentry: Gtk.Entry;
  let win: Astal.Window;

  const TAPYRE_CMD = GLib.getenv("TAPYRE_CMD") || "tapyre-cli";

  const [list, setList] = createState(new Array<string>());

  function search(text: string) {
    if (text === "") setList([]);
    else {
      try {
        const output = exec(`${TAPYRE_CMD} query test search "${text}"`);
        const data = JSON.parse(output);

        if (data.type === "list" && Array.isArray(data.data)) {
          const names = data.data.map((item: { name: string }) => item.name);
          setList(names);
        } else {
          console.warn("Unexpected tapyre output format:", data);
          setList([]);
        }
      } catch (error) {
        console.error("Error running tapyre query:", error);
        setList([]);
      }
    }
  }

  function launch(item: string) {
    win.hide();
    exec(`${TAPYRE_CMD} query test launch "${item}"`);
  }

  function onKey(_e: Gtk.EventControllerKey, keyval: number) {
    if (keyval === Gdk.KEY_Escape) {
      win.visible = false;
      return;
    }
  }

  function onClick(_e: Gtk.GestureClick, _: number, x: number, y: number) {
    const [, rect] = contentbox.compute_bounds(win);
    const position = new Graphene.Point({ x, y });

    if (!rect.contains_point(position)) {
      win.visible = false;
      return true;
    }
  }

  return (
    <window
      $={(ref) => (win = ref)}
      name="launcher"
      anchor={TOP | BOTTOM | LEFT | RIGHT}
      exclusivity={Astal.Exclusivity.IGNORE}
      keymode={Astal.Keymode.EXCLUSIVE}
      onNotifyVisible={({ visible }) => {
        if (visible) searchentry.grab_focus();
        else searchentry.set_text("");
      }}
    >
      <Gtk.EventControllerKey onKeyPressed={onKey} />
      <Gtk.GestureClick onPressed={onClick} />
      <box
        $={(ref) => (contentbox = ref)}
        name="launcher-content"
        valign={Gtk.Align.CENTER}
        halign={Gtk.Align.CENTER}
        orientation={Gtk.Orientation.VERTICAL}
      >
        <entry
          $={(ref) => (searchentry = ref)}
          onNotifyText={({ text }) => search(text)}
        />
        <Gtk.Separator visible={list((l) => l.length > 0)} />
        <box orientation={Gtk.Orientation.VERTICAL}>
          <For each={list}>
            {(item) => (
              <button onClicked={() => launch(item)}>
                <box>
                  <label label={item} maxWidthChars={40} wrap />
                </box>
              </button>
            )}
          </For>
        </box>
      </box>
    </window>
  );
}
