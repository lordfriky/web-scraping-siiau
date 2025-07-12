from .requester import SiiauRequester
from .parsers import SiiauParser

from . import models as SiiauModels
from .models import Ciclo, Centro, Consulta, MateriaConsulta

__all__ = ['SiiauOferta', 'Ciclo', 'Centro', 'Consulta', 'MateriaConsulta']

class SiiauOferta:
    _requester = SiiauRequester.create('oferta')

    @classmethod
    def obtener_ciclos(cls) -> list[SiiauModels.Ciclo]:
        formulario_html = cls._requester.get_html_formulario()
        formulario_parser = SiiauParser.create('formulario_consulta', formulario_html)
        return formulario_parser.extraer_ciclos()

    @classmethod
    def obtener_centros(cls) -> list[SiiauModels.Centro]:
        formulario_html = cls._requester.get_html_formulario()
        formulario_parser = SiiauParser.create('formulario_consulta', formulario_html)
        return formulario_parser.extraer_centros()

    @classmethod
    def consultar_oferta(cls, consulta: SiiauModels.Consulta):
        consulta_html = cls._requester.get_html_consulta(consulta)
        consulta_parser = SiiauParser.create('resultado_consulta', consulta_html)
        return consulta_parser.extraer_clases()
