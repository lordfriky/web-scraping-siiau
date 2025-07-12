from .siiau import SiiauOferta, Ciclo, Centro, Consulta, MateriaConsulta

print("--- Demo de Web Scraping con Python (oferta académica SIIAU UdeG) ---")

ciclos = SiiauOferta.obtener_ciclos()
print(f"Ciclos obtenidos del formulario ({len(ciclos)}):")
for ciclo in ciclos:
    print(f"  - [{ciclo.clave}] {ciclo.descripcion}")
print()

centros = SiiauOferta.obtener_centros()
print(f"Centros obtenidos del formulario ({len(centros)}):")
for centro in centros:
    print(f"  - [{centro.clave}] {centro.descripcion}")
print()

payload = Consulta(
    ciclo = Ciclo('202520', '', ''),    # Semestre 2025 B
    centro = Centro('D', '', ''),       # CUCEI
    clave_carrera = 'INFO',             # Ingeniería en Informática
    materia = MateriaConsulta('IL361')  # Fundamentos de Inteligencia Artificial
)

clases = SiiauOferta.consultar_oferta(payload)

print(f"Clases obtenidas del formulario ({len(clases)}):")
for clase in clases:
    print(f"  - [{clase.clave}] {clase.nombre}")
    print(f"    NRC={clase.nrc} Sección={clase.seccion}")
    print(f"    Cupo: {clase.disponibles} de {clase.cupo}")
    print(f"    Sesiones ({len(clase.sesiones)})")
    for sesion in clase.sesiones:
        print(f"      + [{sesion.id}] Prof. {sesion.profesor}")
        print(f"        Horarios: {len(sesion.horarios)}")
        for horario in sesion.horarios:
            print(f"          * Inicia {horario.hora_inicio} y termina {horario.hora_fin}")
            print(f"            Aula: {horario.aula} de {horario.edificio}")
            print(f"            Dias: {horario.dias}")
    print()

# Hack pa ejecutarlo con poetry
def main():
    pass

if __name__ == "__main__":
    main()
