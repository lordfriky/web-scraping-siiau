import requests
from typing import Optional

from .models import Consulta
from .exceptions import SiiauDown

class SiiauRequester:
    @staticmethod
    def create(type: str):
        match type:
            case 'oferta':
                return OfertaRequester()
            case _:
                raise ValueError(f"Tipo de requester desconocido: {type}")

class BaseRequester:
    @staticmethod
    def _request(method: str, url: str, payload: Optional[dict] = None) -> str:
        response: requests.Response | None = None

        try:
            response = requests.request(method, url, data=payload)
        except requests.ConnectionError:
            raise SiiauDown("error de conexión con el servidor")
        except requests.Timeout:
            raise SiiauDown("tiempo límite alcanzado")
        except requests.RequestException as e:
            raise SiiauDown(f"error desconocido - {e}")

        if not response.ok:
            raise SiiauDown("error en la respuesta del servidor", response)

        return response.text

class OfertaRequester(BaseRequester):
    BASE_URL = "http://consulta.siiau.udg.mx/wco"
    URL_FORMULARIO = BASE_URL + "/sspseca.forma_consulta"
    URL_CONSULTA = BASE_URL + "/sspseca.consulta_oferta"

    _formulario_cache: str | None = None

    @classmethod
    def limpiar_cache(cls) -> None:
        cls._formulario_cache = None

    @classmethod
    def _set_formulario_cache(cls, formulario: str) -> None:
        cls._formulario_cache = formulario

    @classmethod
    def get_html_formulario(cls) -> str:
        if cls._formulario_cache is not None:
            return cls._formulario_cache

        cls._formulario_cache = cls._request('GET', cls.URL_FORMULARIO)
        return cls._formulario_cache

    @classmethod
    def get_html_consulta(cls, payload: Consulta) -> str:
        proper_payload = cls._create_dict_payload(payload)
        return cls._request('POST', cls.URL_CONSULTA, proper_payload)

    @staticmethod
    def _create_dict_payload(payload: Consulta) -> dict[str, str]:
        VALORES_ORDEN = {
            'materia': '0',
            'clave': '1',
            'nrc': '2'
        }

        return {
            'ciclop': payload.ciclo.clave,
            'cup': payload.centro.clave,

            'majrp': (payload.clave_carrera or '').upper(),

            'crsep': ((payload.materia.clave or '').upper()) if payload.materia else '',
            'materiap': ((payload.materia.descripcion or '').upper()) if payload.materia else '',

            'horaip': (payload.horario.hora_inicio or '') if payload.horario else '',
            'horafp': (payload.horario.hora_fin or '') if payload.horario else '',

            'lup': 'M' if payload.dias.lunes else '',
            'map': 'T' if payload.dias.martes else '',
            'mip': 'W' if payload.dias.miercoles else '',
            'jup': 'R' if payload.dias.jueves else '',
            'vip': 'F' if payload.dias.viernes else '',
            'sap': 'S' if payload.dias.sabado else '',

            'edifp': ((payload.lugar.edificio or '').upper()) if payload.lugar else '',
            'aulap': ((payload.lugar.aula or '').upper()) if payload.lugar else '',

            'dispp': 'D' if payload.solo_secciones_disponibles else '',
            'ordenp': VALORES_ORDEN[payload.ordenado_por],
            'mostrarp': str(payload.cantidad),
            'p_start': str(payload.offset)
        }
