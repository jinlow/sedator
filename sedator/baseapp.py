import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter.messagebox import showerror
from .editor import EditorTab
from .keybindings import KeyBinder
from typing import List


class TextApplication:
    """
    Allows for multiple Editor tabs under one notebook.
    """

    def __init__(self, root: tk.Tk = None, base_tab=True):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.keybinder = KeyBinder()

        self.style = ttk.Style()
        self.style.theme_use("clam")

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
        self.filemenu = tk.Menu(self.menubar)
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

    def new_file(self, event=None, name="untitled"):
        nfile = self._add_tab(name=name)
        self.notebook.add(nfile, text=nfile.tab_name)
        self.notebook.select(nfile)

    def open_file(self, event=None):
        f = filedialog.askopenfile(mode="r")
        if f is not None:
            t = f.read()
            self.new_file(name=f.name)
            self.get_tab().insert(0.0, t)

    def save_as(self, event=None):
        f = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        self.get_tab().tab_name = f.name
        tab = self.get_tab()
        t = tab.get(0.0, tk.END)
        try:
            f.write(t.rstrip())
        except:
            showerror("Error", "Unable to save file")

    def save_file(self, event=None):
        tab = self.get_tab()
        t = tab.get(0.0, tk.END)
        fname = tab.tab_name
        f = open(fname, "w")
        f.write(t)
        f.close()

    def close_file(self, event=None):
        idx = self.notebook.index("current")
        self.notebook.forget(self.notebook.select())
        del self.file_list[idx]

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
