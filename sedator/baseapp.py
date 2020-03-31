import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror
from .editor import EditorTab
from .keybindings import KeyBinder
from typing import List, Any, Optional


class TextApplication:
    """
    Allows for multiple Editor tabs under one notebook.
    """

    def __init__(self, root: Optional[tk.Tk] = None, base_tab: bool = True):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.keybinder = KeyBinder()

        _bg_color0 = "#272822"
        _bg_color1 = "#75715E"
        _fg_color0 = "#63604f"
        _fg_color1 = "#F8F8F2"

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=_bg_color0)
        self.style.configure(".", foreground=_fg_color0)
        self.style.map(
            ".", background=[("selected", "orange"), ("active", "orange")]
        )
        self.style.configure("TNotebook.Tab", background=_fg_color0)
        self.style.configure("TNotebook.Tab", foreground=_fg_color1)
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", _bg_color1), ("active", _bg_color1)],
        )

        self.root.title("Sedator: A simple editor")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create base notebook
        scr_h = self.root.winfo_screenheight()
        scr_w = self.root.winfo_screenwidth()
        self.notebook = ttk.Notebook(self.root, width=scr_w, height=scr_h)
        self.root.geometry(f"{scr_w // 2}x{scr_h // 2}")

        self.file_list: List[EditorTab] = []

        # Create base editor tab
        if base_tab:
            self.new_file()

        # Create menu
        self.menubar = tk.Menu(self.root)
        self.create_menu()
        self.notebook.pack()

    def create_menu(self):
        # filemenue
        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_separator()
        self.keybinder.base_control_bind(
            self.root,
            func=self.new_file,
            add_keys=["n"],
            filemenu=self.filemenu,
            label="New File",
        )
        self.filemenu.add_separator()
        self.keybinder.base_control_bind(
            self.root,
            func=self.open_file,
            add_keys=["o"],
            filemenu=self.filemenu,
            label="Open File",
        )
        self.filemenu.add_separator()
        self.keybinder.base_control_bind(
            self.root,
            func=self.save_as,
            add_keys=["Shift", "s"],
            filemenu=self.filemenu,
            label="Save As...",
        )
        self.keybinder.base_control_bind(
            self.root,
            func=self.save_file,
            add_keys=["s"],
            filemenu=self.filemenu,
            label="Save File",
        )
        self.filemenu.add_separator()
        self.keybinder.base_control_bind(
            self.root,
            func=self.close_file,
            add_keys=["w"],
            filemenu=self.filemenu,
            label="Close File",
        )
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)
        # Edit Menu
        self.editmenu = tk.Menu(self.menubar)
        self.editmenu.add_separator()
        self.keybinder.base_control_bind(
            self.root,
            func=self.undo_tab,
            add_keys=["z"],
            filemenu=self.editmenu,
            label="Undo",
        )
        self.keybinder.base_control_bind(
            self.root,
            func=self.redo_tab,
            add_keys=["Shift", "z"],
            filemenu=self.editmenu,
            label="Redo",
        )
        self.editmenu.add_separator()
        self.keybinder.control_add_command(
            self.root,
            func=lambda: self.get_tab().event_generate("<<Cut>>"),
            add_keys=["x"],
            filemenu=self.editmenu,
            label="Cut",
        )
        self.keybinder.control_add_command(
            self.root,
            func=lambda: self.get_tab().event_generate("<<Copy>>"),
            add_keys=["c"],
            filemenu=self.editmenu,
            label="Copy",
        )
        self.keybinder.control_add_command(
            self.root,
            func=self.get_tab().paste_w_info,
            add_keys=["v"],
            filemenu=self.editmenu,
            label="Paste",
        )
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        self.root.config(menu=self.menubar)

    def new_file(self, event: Optional[Any] = None, name: str = "untitled"):
        nfile = self._add_tab(name=name)
        self.notebook.add(nfile, text=nfile.tab_name)
        self.notebook.select(nfile)

    def open_file(self, event: Optional[Any] = None):
        f = filedialog.askopenfile(mode="r")
        if f is not None:
            t = f.read()
            self.new_file(name=f.name)
            self.get_tab().tab_saved = True
            self.get_tab().insert("1.0", t)
            self.get_tab().highlighter.block_highlighter(t, "1.0")

    def save_as(self, event: Optional[Any] = None):
        f = filedialog.asksaveasfile(mode="w", defaultextension=".py")
        if f is not None:
            self.get_tab().tab_name = f.name
            tab = self.get_tab()
            self.notebook.tab(tab, text=tab.tab_name)
            t = tab.get("1.0", tk.END)
            try:
                f.write(t.rstrip())
            except:
                showerror("Error", "Unable to save file")
            self.get_tab().tab_saved = True

    def save_file(self, event: Optional[Any] = None):
        tab = self.get_tab()
        if not tab.tab_saved:
            self.save_as()
        else:
            t = tab.get("1.0", tk.END)
            fname = tab.tab_name
            f = open(fname, "w")
            f.write(t)
            f.close()

    def close_file(self, event: Optional[Any] = None):
        idx = self.notebook.index("current")
        self.notebook.forget(self.notebook.select())
        del self.file_list[idx]

    def undo_tab(self, event: Optional[Any] = None):
        try:
            self.get_tab().edit_undo()
        except tk.TclError:
            pass

    def redo_tab(self, event: Optional[Any] = None):
        try:
            self.get_tab().edit_redo()
        except tk.TclError:
            pass

    def get_tab(self):
        idx = self.notebook.index("current")
        return self.file_list[idx]

    def _add_tab(self, name="untitled"):
        nfile = EditorTab(self.root)
        nfile.tab_name = name
        self.file_list.append(nfile)
        return nfile

    def runApplication(self):
        self.root.mainloop()


if __name__ == "__main__":
    editor = TextApplication()
    editor.runApplication()
