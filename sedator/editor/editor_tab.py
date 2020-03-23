import ntpath
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class EditorTab(ScrolledText):
    def __init__(self, root, *args, **kwargs):
        super().__init__(
            # Set defaults for ScrolledText
            root,
            padx=10,
            pady=10,
            bd=0,
            relief=tk.FLAT,
            bg="#270217",
            fg="#FFFDE7",
            insertbackground="#add8e6",
            *args,
            **kwargs
        )
        self.tab_saved = False
        self._tab_name = None

    @property
    def tab_name(self):
        return self._tab_name

    @tab_name.setter
    def tab_name(self, value):
        value = ntpath.basename(value)
        self._tab_name = value
