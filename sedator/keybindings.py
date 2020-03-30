import sys
import tkinter as tk
from typing import Callable, List


class KeyBinder:
    """
    Class for creating keybindings and menu items.
    """

    def __init__(self):
        # Check base platform type
        if sys.platform[0:3] == "win":
            self.ctrl = "Control"
        elif sys.platform == "darwin":
            self.ctrl = "Command"

    def base_control_bind(
        self,
        root: tk.Tk,
        func: Callable,
        add_keys: List[str],
        filemenu: tk.Menu = None,
        label: str = None,
    ):
        """
        Create a base menu command and binding. This command cannot
        be overwritten.

        Parameters
        ----------
        root: Parent

        func: Callable
            The function the binding is being created for.

        add_keys: str
            Additional Keys to be called in addition to the
            Control/Command key.
        """
        root.bind(f"<{self.ctrl}-{'-'.join(add_keys)}>", func=func)
        if filemenu is not None:
            filemenu.add_command(
                label=label,
                command=func,
                accelerator=f"{self.ctrl}-{'-'.join(add_keys)}",
            )

    def control_add_command(
        self,
        root: tk.Tk,
        func: Callable,
        add_keys: List[str],
        filemenu: tk.Menu,
        label: str = None,
    ):
        filemenu.add_command(
            label=label,
            command=func,
            accelerator=f"{self.ctrl}-{'-'.join(add_keys)}",
        )
