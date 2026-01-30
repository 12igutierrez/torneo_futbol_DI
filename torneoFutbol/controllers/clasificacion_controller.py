from PySide6.QtSql import QSqlQuery

def obtener_clasificacion():
    """
    Devuelve una lista con:
    equipo, PJ, PG, PE, PP, GF, GC, DG, PTS
    """
    # Inicializamos todos los equipos
    query = QSqlQuery("""
        SELECT id, nombre
        FROM equipo
    """)
    clasificacion = {}

    while query.next():
        equipo_id = query.value("id")
        clasificacion[equipo_id] = {
            "equipo": query.value("nombre"),
            "pj": 0,
            "pg": 0,
            "pe": 0,
            "pp": 0,
            "gf": 0,
            "gc": 0,
            "pts": 0
        }

    # Procesamos partidos con resultado
    query = QSqlQuery("""
        SELECT equipo_local, equipo_visitante,
               goles_local, goles_visitante
        FROM partido
        WHERE goles_local IS NOT NULL
          AND goles_visitante IS NOT NULL
    """)

    while query.next():
        local = query.value("equipo_local")
        visitante = query.value("equipo_visitante")
        gl = query.value("goles_local")
        gv = query.value("goles_visitante")

        # Partidos jugados
        clasificacion[local]["pj"] += 1
        clasificacion[visitante]["pj"] += 1

        # Goles
        clasificacion[local]["gf"] += gl
        clasificacion[local]["gc"] += gv
        clasificacion[visitante]["gf"] += gv
        clasificacion[visitante]["gc"] += gl

        if gl > gv:
            clasificacion[local]["pg"] += 1
            clasificacion[local]["pts"] += 3
            clasificacion[visitante]["pp"] += 1
        elif gl < gv:
            clasificacion[visitante]["pg"] += 1
            clasificacion[visitante]["pts"] += 3
            clasificacion[local]["pp"] += 1
        else:
            clasificacion[local]["pe"] += 1
            clasificacion[visitante]["pe"] += 1
            clasificacion[local]["pts"] += 1
            clasificacion[visitante]["pts"] += 1

    # Convertimos a lista ordenada
    tabla = []
    for e in clasificacion.values():
        tabla.append((
            e["equipo"],
            e["pj"],
            e["pg"],
            e["pe"],
            e["pp"],
            e["gf"],
            e["gc"],
            e["gf"] - e["gc"],
            e["pts"]
        ))

    # Orden oficial: puntos, diferencia, goles a favor
    tabla.sort(key=lambda x: (x[8], x[7], x[5]), reverse=True)
    return tabla
