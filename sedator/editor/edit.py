import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText


class Editor:
    def __init__(self, root: tk.Tk = None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root

        self.filename = None
        self.prepRoot()

        # Create Scrolled text
        self.text = ScrolledText(self.root, width=200, height=200)
        self.text.pack()
        self.createFilemenu()

        self.root.config(menu=self.menubar)

    def newFile(self):
        self.filename = "Untitled"
        self.text.delete(0.0, tk.END)

    def saveFile(self):
        t = self.text.get(0.0, tk.END)
        f = open(self.filename, "w")
        f.write(t)
        f.close()

    def saveAs(self):
        f = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        t = self.text.get(0.0, tk.END)
        try:
            f.write(t.rstrip())
        except:
            tk.messagebox.showerror("Error", "Unable to save file")
        self.filename = f.name

    def openFile(self):
        f = filedialog.askopenfile(mode="r")
        t = f.read()
        self.filename = f.name
        self.text.delete(0.0, tk.END)
        self.text.insert(0.0, t)

    def prepRoot(self):
        self.root.title("Sedator: a simple editor")
        # get screen max size
        scr_h = self.root.winfo_screenheight()
        scr_w = self.root.winfo_screenwidth()

        self.root.minsize(width=0, height=0)
        self.root.maxsize(width=scr_w, height=scr_h)
        self.root.geometry(f"{scr_w // 2}x{scr_h // 2}")

    def createFilemenu(self):
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar)
        self.filemenu.add_command(label="New", command=self.newFile)
        self.filemenu.add_command(label="Open", command=self.openFile)
        self.filemenu.add_command(label="Save", command=self.saveFile)
        self.filemenu.add_command(label="Save As...", command=self.saveAs)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

    def runApplication(self):
        self.root.mainloop()


if __name__ == "__main__":
    editor = Editor()
    editor.runApplication()
