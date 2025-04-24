import tkinter as tk
from ui import build_ui

root = tk.Tk()
root.title("Propagation Model Calculator")
root.geometry("1024x768")

build_ui(root)
root.mainloop()
