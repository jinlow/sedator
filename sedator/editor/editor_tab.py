import ntpath
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class EditorTab(ScrolledText):
    def __init__(self, root: tk.Tk, *args, **kwargs):
        super().__init__(
            root,
            padx=10,
            pady=10,
            bd=0,
            relief=tk.FLAT,
            bg="#272822",
            fg="#FFFDE7",
            insertbackground="#add8e6",
            highlightthickness=0,
            *args,
            **kwargs
        )
        self.tab_saved = False
        self._tab_name = None

        self.config(wrap="none")
        self.config(font=("Consolas", 13))

        # self.linenumbers = tk.Text(self, width=1, state="disabled")
        # self.linenumbers.pack(side=tk.LEFT, fill=tk.BOTH)

    @property
    def tab_name(self):
        return self._tab_name

    @tab_name.setter
    def tab_name(self, value):
        value = ntpath.basename(value)
        self._tab_name = value
