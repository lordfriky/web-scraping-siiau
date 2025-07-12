# src/gui/form_panel.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, BooleanVar
from ..siiau import SiiauOferta


class FormPanel(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.ciclos = SiiauOferta.obtener_ciclos()
        self.centros = SiiauOferta.obtener_centros()

        self._crear_widgets()

    def _crear_widgets(self):
        # Variables
        self.var_ciclo = StringVar()
        self.var_centro = StringVar()
        self.var_clave_carrera = StringVar()
        self.var_clave_materia = StringVar()
        self.var_nombre_materia = StringVar()
        self.var_hora_inicio = StringVar()
        self.var_hora_fin = StringVar()
        self.var_edificio = StringVar()
        self.var_aula = StringVar()
        self.var_disponibilidad = BooleanVar()
        self.var_orden_materia = BooleanVar()
        self.var_orden_clave = BooleanVar()
        self.var_orden_nrc = BooleanVar()

        # Fila 1: Ciclo
        ttk.Label(self, text="Ciclo:").grid(row=0, column=0, sticky=W)
        ciclo_options = [c.descripcion for c in self.ciclos]
        self.ciclo_dropdown = ttk.Combobox(self, textvariable=self.var_ciclo, values=ciclo_options, state="readonly")
        self.ciclo_dropdown.grid(row=0, column=1, columnspan=3, sticky=EW)

        # Fila 2: Centro
        ttk.Label(self, text="Centro:").grid(row=1, column=0, sticky=W)
        centro_options = [c.descripcion for c in self.centros]
        self.centro_dropdown = ttk.Combobox(self, textvariable=self.var_centro, values=centro_options, state="readonly")
        self.centro_dropdown.grid(row=1, column=1, columnspan=3, sticky=EW)

        # Fila 3: Carrera
        ttk.Label(self, text="Clave Carrera:").grid(row=2, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.var_clave_carrera, width=5).grid(row=2, column=1, sticky=EW)

        # Fila 4: Materia (clave y nombre en la misma fila)
        ttk.Label(self, text="Clave Materia:").grid(row=3, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.var_clave_materia, width=6).grid(row=3, column=1, sticky=EW)
        ttk.Label(self, text="Nombre Materia:").grid(row=3, column=2, sticky=W)
        ttk.Entry(self, textvariable=self.var_nombre_materia, width=30).grid(row=3, column=3, sticky=EW)

        # Fila 5: Horario (hora inicio y fin, días, edificio y aula)
        ttk.Label(self, text="Hora Inicio:").grid(row=4, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.var_hora_inicio, width=5).grid(row=4, column=1, sticky=W)
        ttk.Label(self, text="Hora Fin:").grid(row=4, column=2, sticky=W)
        ttk.Entry(self, textvariable=self.var_hora_fin, width=5).grid(row=4, column=3, sticky=W)

        # Días (LU, MA, MI, JU)
        dias = ["LU", "MA", "MI", "JU"]
        self.var_dias = {dia: BooleanVar() for dia in dias}
        ttk.Label(self, text="Días:").grid(row=5, column=0, sticky=W)
        for i, dia in enumerate(dias):
            ttk.Checkbutton(self, text=dia, variable=self.var_dias[dia]).grid(row=5, column=1+i, sticky=W)

        # Lugar: edificio y aula
        ttk.Label(self, text="Edificio:").grid(row=6, column=0, sticky=W)
        ttk.Entry(self, textvariable=self.var_edificio, width=6).grid(row=6, column=1, sticky=EW)
        ttk.Label(self, text="Aula:").grid(row=6, column=2, sticky=W)
        ttk.Entry(self, textvariable=self.var_aula, width=6).grid(row=6, column=3, sticky=EW)

        # Fila 6: Check Disponibilidad
        ttk.Checkbutton(self, text="Sólo con lugares disponibles", variable=self.var_disponibilidad).grid(row=7, column=0, columnspan=4, sticky=W)

        # Fila 7: Orden
        ttk.Label(self, text="Ordenar por:").grid(row=8, column=0, sticky=W)
        ttk.Checkbutton(self, text="Materia", variable=self.var_orden_materia).grid(row=8, column=1, sticky=W)
        ttk.Checkbutton(self, text="Clave", variable=self.var_orden_clave).grid(row=8, column=2, sticky=W)
        ttk.Checkbutton(self, text="NRC", variable=self.var_orden_nrc).grid(row=8, column=3, sticky=W)

        # Botón de enviar
        ttk.Button(self, text="Consultar").grid(row=9, column=0, columnspan=4, pady=10)

        # Label de estado
        ttk.Label(self, text="placeholder", bootstyle="info").grid(row=10, column=0, columnspan=4)

        # Expandir columnas
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
