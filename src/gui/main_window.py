import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from .form_panel import FormPanel
from .class_list_panel import ClassListPanel

class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Oferta Académica SIIAU")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Layout general: dos columnas
        self.columnconfigure(0, weight=35)
        self.columnconfigure(1, weight=65)

        self.form_panel = FormPanel(self)
        self.form_panel.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)

        self.class_list_panel = ClassListPanel(self)
        self.class_list_panel.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
