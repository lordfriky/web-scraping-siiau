import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ClassListPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        label = ttk.Label(self, text="Clases encontradas", font=("Arial", 12, "bold"))
        label.pack(anchor=W)
        # Aquí va la lista
