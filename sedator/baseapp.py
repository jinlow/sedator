import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter.messagebox import showerror
from .editor import EditorTab
from typing import List


class TextApplication:
    """
    Allows for multiple Editor tabs under one notebook.
    """

    def __init__(self, root: tk.Tk = None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.filename = None

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
        # self.notebook.add(EditorTab(self.root), text="Untitled")

        # Create menu
        self.create_menu()
        self.notebook.pack()

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label="New File", command=self.new_file)
        self.filemenu.add_command(label="Close File", command=self.close_file)
        self.filemenu.add_command(label="Save As...", command=self.save_as)
        self.filemenu.add_command(label="Save File", command=self.save_file)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)

    def new_file(self):
        self.filename = "untitled"
        new_file = EditorTab(self.root)
        new_file.tab_name = "untitled"
        self.file_list.append(new_file)
        new_file.pack()
        self.notebook.add(new_file, text=self.filename)
        self.notebook.select(new_file)

    def close_file(self):
        idx = self.notebook.index("current")
        self.notebook.forget(self.notebook.select())
        del self.file_list[idx]

    def save_as(self):
        f = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        self.get_tab().tab_name = f.name
        tab = self.get_tab()
        t = tab.get(0.0, tk.END)
        try:
            f.write(t.rstrip())
        except:
            showerror("Error", "Unable to save file")

    def save_file(self):
        tab = self.get_tab()
        t = tab.get(0.0, tk.END)
        fname = tab.tab_name
        f = open(fname, "w")
        f.write(t)
        f.close()

    def get_tab(self):
        # return self.notebook.tab(self.notebook.select())
        idx = self.notebook.index("current")
        return self.file_list[idx]

    def set_tab_name(self, name):
        idx = self.notebook.index("current")
        self.file_list[idx].tab_name = name

    def runApplication(self):
        self.root.mainloop()


if __name__ == "__main__":
    editor = TextApplication()
    editor.runApplication()
