import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class EditorTab(ScrolledText):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, padx=0, pady=0, relief=tk.FLAT, *args, **kwargs)
        self.tab_saved = False
        self.tab_name = None
