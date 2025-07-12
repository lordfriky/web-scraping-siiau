from dataclasses import dataclass
from typing import Optional, Literal

@dataclass
class SimpleClaveDescripcion:
    clave: str
    descripcion: str
    _full_string: str

class Ciclo(SimpleClaveDescripcion): pass
class Centro(SimpleClaveDescripcion): pass

@dataclass
class MateriaConsulta:
    clave: Optional[str] = None
    descripcion: Optional[str] = None

@dataclass
class HorarioConsulta:
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None

@dataclass(frozen=True)
class DiasConsulta:
    lunes: bool = False
    martes: bool = False
    miercoles: bool = False
    jueves: bool = False
    viernes: bool = False
    sabado: bool = False

@dataclass
class LugarConsulta:
    edificio: Optional[str] = None
    aula: Optional[str] = None

@dataclass
class Consulta:
    ciclo: Ciclo
    centro: Centro

    # Opcionales
    clave_carrera: Optional[str] = None
    materia: Optional[MateriaConsulta] = None
    horario: Optional[HorarioConsulta] = None
    dias: DiasConsulta = DiasConsulta()
    lugar: Optional[LugarConsulta] = None
    solo_secciones_disponibles: bool = False
    ordenado_por: Literal['materia', 'clave', 'nrc'] = 'materia'

    # Paginación (no es necesario modificar esto)
    cantidad: int = 999_999_999_999
    offset: int = 0

@dataclass
class Horario:
    hora_inicio: str
    hora_fin: str
    dias: list[Literal['L', 'M', 'I', 'J', 'V', 'S']]

    edificio: str
    aula: str

    periodo: str

@dataclass
class Sesion:
    id: int
    profesor: str
    horarios: list[Horario]

@dataclass
class Clase:
    # Generales
    clave: str
    nombre: str
    creditos: int

    # Específicos
    nrc: str
    seccion: str
    cupo: int
    disponibles: int
    sesiones: list[Sesion]
