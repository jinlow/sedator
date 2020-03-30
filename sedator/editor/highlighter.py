import tkinter as tk
from tkinter.font import Font
from pygments import lex
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name
from typing import List


class Highlighter:
    """
    Class for Syntax highlighting and formatting
    
    This class implements functionality for syntax highlighting,
    and syntax formatting. Currently it is a class called within
    the EditorTab constructor. This may be implemented as a different
    way in the future as functionality is built out. It may be an
    easier design to have it as a class EditorTab inherits from.
    """

    def __init__(
        self, text: tk.Text, text_theme: str = "monokai", font: Font = None
    ):
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

    def block_highlighter(self, data, index1, remove_fmt=False):
        """
        Syntax highlighting a block of text
        """
        self.text.mark_set("range_start", index1)
        if remove_fmt:
            for tag in self.fmt_list:
                self.text.tag_remove(tag, "range_start", "end")
        for fmt, token in lex(data, PythonLexer()):
            self.text.mark_set("range_end", f"range_start+{len(token)}c")
            self.text.tag_add(str(fmt), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

    def edit_highlighter(self, event=None):
        """
        Syntax highlighting while editing.
        This will edit a single line. This does not deal with
        triple quotes.
        """
        self.text.mark_set("range_start", tk.INSERT + " linestart")
        data = self.text.get("range_start", "range_start lineend")
        for tag in self.fmt_list:
            self.text.tag_remove(tag, "range_start", "range_start lineend")
        for fmt, token in lex(data, PythonLexer()):
            self.text.mark_set("range_end", f"range_start+{len(token)}c")
            self.text.tag_add(str(fmt), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")

    def paste_highlighter(self, index1, index2, event=None):
        """
        Highlighter to use if text is pasted in.
            This highlighter is more efficient but does not have
            the same real time checks needed for overwriting the tags
            as are present in the edit_highlighter function.
        """
        self.text.mark_set("range_start", index1)
        data = self.text.get("range_start", index2)
        for fmt, token in lex(data, PythonLexer()):
            self.text.mark_set("range_end", f"range_start+{len(token)}c")
            self.text.tag_add(str(fmt), "range_start", "range_end")
            self.text.mark_set("range_start", "range_end")
