from re import S
from bs4 import BeautifulSoup, Tag
from typing import cast

from requests.models import parse_header_links

from . import models as SiiauModels

class SiiauParser:
    @staticmethod
    def create(type: str, html_content: str):
        match type:
            case 'formulario_consulta':
                return FormularioConsultaParser(html_content)
            case 'resultado_consulta':
                return ResultadoConsultaParser(html_content)
            case _:
                raise ValueError(f"Tipo de parser inválido: {type}")

class FormularioConsultaParser:
    def __init__(self, html_content: str):
        self._soup = BeautifulSoup(html_content, 'html5lib')

    def extraer_ciclos(self) -> list[SiiauModels.Ciclo]:
        select = self._soup.find('select', {'name': 'ciclop'})

        # Para que el type checker no se enoje
        # Podemos asumir que esto nunca será None
        select = cast(Tag, select)

        ciclos = []
        for option in select.find_all('option'):
            option = cast(Tag, option)
            clave = cast(str, option['value'])
            texto = option.get_text(strip=True)
            descripcion = texto.split(" - ", 1)[-1]
            ciclos.append(SiiauModels.Ciclo(clave, descripcion, texto))

        return ciclos

    def extraer_centros(self) -> list[SiiauModels.Centro]:
        select = self._soup.find('select', {'name': 'cup'})
        select = cast(Tag, select)

        centros = []
        for option in select.find_all("option"):
            option = cast(Tag, option)
            clave = cast(str, option['value'])
            texto = option.get_text(strip=True)
            descripcion = texto.split(" - ", 1)[-1]
            centros.append(SiiauModels.Centro(clave, descripcion, texto))

        return centros

class ResultadoConsultaParser:
    def __init__(self, html_content: str):
        self._soup = BeautifulSoup(html_content, 'html5lib')

    def extraer_clases(self) -> list[SiiauModels.Clase]:
        tabla = self._soup.find('tbody')
        tabla = cast(Tag, tabla)

        clases = []
        filas_clases = tabla.find_all('tr', recursive=False)[2:]
        for fila_clase in filas_clases:
            fila_clase = cast(Tag, fila_clase)
            clase = self._extraer_clase(fila_clase)
            clases.append(clase)

        return clases

    def _extraer_clase(self, fila_clase: Tag) -> SiiauModels.Clase:
        celdas = fila_clase.find_all('td', recursive=False)

        horarios = self._extraer_horarios(celdas[7])
        profesores = self._extraer_profesores(celdas[8])

        return SiiauModels.Clase(
            clave = self._extraer_texto_link(celdas[1]),
            nombre = self._extraer_texto_link(celdas[2]),
            creditos = int(celdas[4].get_text(strip=True)),

            nrc = celdas[0].get_text(strip=True),
            seccion = celdas[3].get_text(strip=True),
            cupo = int(celdas[5].get_text(strip=True)),
            disponibles = int(celdas[6].get_text(strip=True)),
            sesiones = self._vincular_sesiones(horarios, profesores)
        )

    @staticmethod
    def _extraer_texto_link(celda: Tag) -> str:
        link = cast(Tag, celda.find('a'))
        return link.get_text(strip=True)

    @staticmethod
    def _extraer_horarios(celda_horarios: Tag) -> list[tuple[int, SiiauModels.Horario]]:
        horarios = []
        tabla_horarios = celda_horarios.find('table')

        for fila in tabla_horarios.find_all('tr'):
            celdas = fila.find_all('td')
            hora_inicio, hora_fin = celdas[1].get_text(strip=True).split('-')

            id = int(celdas[0].get_text(strip=True))
            horario = SiiauModels.Horario(
                hora_inicio = hora_inicio,
                hora_fin = hora_fin,
                dias = [dia for dia in celdas[2].get_text(strip=True).split() if dia != '.'], # pyright: ignore
                edificio = celdas[3].get_text(strip=True),
                aula = celdas[4].get_text(strip=True),
                periodo = celdas[5].get_text(strip=True)
            )
            horarios.append((id, horario))

        return horarios

    @staticmethod
    def _extraer_profesores(celda_profesores: Tag) -> list[tuple[int, str]]:
        profesores = []
        tabla_profesores = celda_profesores.find('table')

        for fila in tabla_profesores.find_all('tr'):
            celdas = fila.find_all('td')
            id = int(celdas[0].get_text(strip=True))
            nombre = celdas[1].get_text(strip=True)
            profesores.append((id, nombre))

        return profesores

    @staticmethod
    def _vincular_sesiones(
        horarios: list[tuple[int, SiiauModels.Horario]],
        profesores: list[tuple[int, str]]
    ) -> list[SiiauModels.Sesion]:
        # Agrupar horarios por id
        horarios_por_id = {}
        for id_, horario in horarios:
            horarios_por_id.setdefault(id_, []).append(horario)

        # Agrupar profesores por id (solo uno por id)
        profesores_por_id = {id_: nombre for id_, nombre in profesores}

        # Unir todos los ids presentes en ambos
        ids = set(horarios_por_id.keys()) | set(profesores_por_id.keys())
        sesiones = []

        for id_ in sorted(ids):
            profesor = profesores_por_id.get(id_, "")
            horarios_sesion = horarios_por_id.get(id_, [])
            sesiones.append(SiiauModels.Sesion(id=id_, profesor=profesor, horarios=horarios_sesion))

        return sesiones
