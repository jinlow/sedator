import ntpath
import tkinter as tk
from tkinter.font import Font
from .highlighter import Highlighter
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
            # fg="#FFFDE7",
            insertbackground="#add8e6",
            highlightthickness=0,
            *args,
            **kwargs,
        )
        self.tab_saved = False
        self._tab_name = None

        self.configure(undo=True, autoseparators=True, maxundo=-1)

        self.font = Font(font="Consolas")
        self.configure(font=self.font)
        self.config(wrap="none")

        self.highlighter = Highlighter(
            self, text_theme="fruity", font=self.font
        )

        # Bind Keys
        self.bind("<Tab>", self.tab_key)
        self.bind("<KeyRelease>", self.highlighter.edit_highlighter)
        self.bind("<<Paste>>", self.paste_w_info)

    @property
    def tab_name(self):
        return self._tab_name

    @tab_name.setter
    def tab_name(self, value):
        value = ntpath.basename(value)
        self._tab_name = value

    def tab_key(self, event):
        """
        Set tabs to be 4 spaces.
        """
        self.insert(tk.INSERT, " " * 4)
        return "break"

    def paste_w_info(self, event=None):
        """
        Paste from clipboard

        A function to overwrite the standard Cmd+V paste functionality
        that provides more information and can utalize the paste_highlighter
        function.
        """
        data = self.clipboard_get(type="STRING")
        sidx = self.index(tk.INSERT)

        try:
            self.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

        # insert the clipboard contents
        self.insert(tk.INSERT, data)

        self.highlighter.paste_highlighter(sidx, tk.INSERT)
        return "break"
