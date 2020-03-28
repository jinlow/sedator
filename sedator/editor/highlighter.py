import tkinter as tk
from tkinter.font import Font
from pygments import lex
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name
from typing import List


class Highlighter:
    def __init__(self, text, text_theme: str = "monokai", font: Font = None):
        self.text = text
        self.style = get_style_by_name(text_theme)
        self.fmt_list: List[str] = []

        # Make Fonts
        hfont = font if font else Font(font="{Lucida Console}")
        self.bold_font = hfont.copy()
        self.bold_font.configure(weight="bold")
        self.italic_font = hfont.copy()
        self.italic_font.configure(slant="italic")

        # Prep style tags
        self.prep_style_tags()

        # Bind events
        self.text.bind("<KeyRelease>", self.edit_highlighter)

    def prep_style_tags(self):
        """
        Prepare all tags to use for highlighting
        """
        for fmt, style_args in self.style:
            color = f"#{style_args['color']}" if style_args["color"] else None
            if style_args["bold"]:
                self.text.tag_config(
                    str(fmt), None, foreground=color, font=self.bold_font,
                )
            elif style_args["italic"]:
                self.text.tag_config(
                    str(fmt), foreground=color, font=self.italic_font,
                )
            else:
                self.text.tag_config(str(fmt), foreground=color)
            self.fmt_list.append(str(fmt))

    def edit_highlighter(self, event=None):
        """
        Syntax highlighting while editing.
        """
        self.text.mark_set("range_start", tk.INSERT + " linestart")
        data = self.text.get("range_start", "range_start lineend")
        for fmt, token in lex(data, PythonLexer()):
            self.text.mark_set("range_end", f"range_start+{len(token)}c")
            for tag in self.fmt_list:
                self.text.tag_remove(tag, "range_start", "range_end")
            self.text.tag_add(str(fmt), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")
