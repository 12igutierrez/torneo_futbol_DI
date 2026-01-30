from PySide6.QtSql import QSqlQuery


def insertar_partido(equipo_local, equipo_visitante, fecha, arbitro_id):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO partido (
            equipo_local,
            equipo_visitante,
            fecha,
            arbitro_id,
            goles_local,
            goles_visitante,
            fase
        )
        VALUES (?, ?, ?, ?, 0, 0, NULL)
    """)

    query.addBindValue(equipo_local)
    query.addBindValue(equipo_visitante)
    query.addBindValue(fecha)
    query.addBindValue(arbitro_id)

    if not query.exec():
        print("Error SQL insertar_partido:", query.lastError().text())
        return False

    return True


def obtener_partidos():
    query = QSqlQuery("""
        SELECT 
            p.id,
            el.nombre AS local,
            ev.nombre AS visitante,
            p.fecha,
            pa.nombre AS arbitro,
            p.goles_local,
            p.goles_visitante
        FROM partido p
        JOIN equipo el ON p.equipo_local = el.id
        JOIN equipo ev ON p.equipo_visitante = ev.id
        LEFT JOIN participante pa ON p.arbitro_id = pa.id
        WHERE p.fase IS NULL OR p.fase = ''
        ORDER BY p.fecha
    """)

    partidos = []
    while query.next():
        partidos.append({
            "id": query.value("id"),
            "tabla": (
                query.value("local"),
                query.value("visitante"),
                query.value("fecha"),
                query.value("arbitro") if query.value("arbitro") else "",
                query.value("goles_local"),
                query.value("goles_visitante")
            )
        })
    return partidos


def obtener_partido_por_id(partido_id):
    query = QSqlQuery()
    query.prepare("""
        SELECT 
            p.id,
            el.nombre AS local,
            ev.nombre AS visitante,
            p.goles_local,
            p.goles_visitante
        FROM partido p
        JOIN equipo el ON p.equipo_local = el.id
        JOIN equipo ev ON p.equipo_visitante = ev.id
        WHERE p.id = ?
    """)
    query.addBindValue(partido_id)
    query.exec()

    if query.next():
        return {
            "id": query.value("id"),
            "texto": f"{query.value('local')} vs {query.value('visitante')}",
            "goles_local": query.value("goles_local"),
            "goles_visitante": query.value("goles_visitante")
        }

    return None


def actualizar_resultado(partido_id, goles_local, goles_visitante):
    query = QSqlQuery()
    query.prepare("""
        UPDATE partido
        SET goles_local = ?, goles_visitante = ?
        WHERE id = ?
    """)
    query.addBindValue(goles_local)
    query.addBindValue(goles_visitante)
    query.addBindValue(partido_id)

    if not query.exec():
        print("Error SQL actualizar_resultado:", query.lastError().text())
        return False

    return True

def obtener_partido_por_id_editar(partido_id):
    query = QSqlQuery()
    query.prepare("""
        SELECT equipo_local, equipo_visitante, fecha, arbitro_id
        FROM partido
        WHERE id = ?
    """)
    query.addBindValue(partido_id)
    query.exec()

    if query.next():
        return (
            query.value(0),
            query.value(1),
            query.value(2),
            query.value(3)
        )
    return None


def actualizar_partido(partido_id, equipo_local, equipo_visitante, fecha, arbitro_id):
    query = QSqlQuery()
    query.prepare("""
        UPDATE partido
        SET equipo_local = ?,
            equipo_visitante = ?,
            fecha = ?,
            arbitro_id = ?
        WHERE id = ?
    """)
    query.addBindValue(equipo_local)
    query.addBindValue(equipo_visitante)
    query.addBindValue(fecha)
    query.addBindValue(arbitro_id)
    query.addBindValue(partido_id)

    if not query.exec():
        print("Error SQL actualizar_partido:", query.lastError().text())
        return False

    return True


def eliminar_partido(partido_id):
    query = QSqlQuery()
    query.prepare("""
        DELETE FROM partido
        WHERE id = ?
    """)
    query.addBindValue(partido_id)

    if not query.exec():
        print("Error SQL eliminar_partido:", query.lastError().text())
        return False

    return True

def borrar_eliminatorias():
    query = QSqlQuery()
    query.exec("""
        DELETE FROM partido
        WHERE fase IN ('octavos', 'cuartos', 'semifinal', 'final')
    """)


from PySide6.QtSql import QSqlQuery

def generar_octavos(clasificacion):
    """
    Genera los octavos de final basándose en la clasificación:
    1º vs último, 2º vs penúltimo, etc.
    """

    query = QSqlQuery()

    # Nos quedamos solo con los 16 primeros clasificados
    equipos = clasificacion[:16]

    total = len(equipos)

    for i in range(8):
        local = equipos[i][0]          # Mejor clasificado
        visitante = equipos[total - 1 - i][0]  # Peor clasificado

        query.prepare("""
            INSERT INTO partido (
                equipo_local,
                equipo_visitante,
                goles_local,
                goles_visitante,
                fase
            ) VALUES (
                (SELECT id FROM equipo WHERE nombre = ?),
                (SELECT id FROM equipo WHERE nombre = ?),
                0,
                0,
                'octavos'
            )
        """)

        query.addBindValue(local)
        query.addBindValue(visitante)
        query.exec()



def obtener_equipo_id_por_nombre(nombre):
    query = QSqlQuery()
    query.prepare("""
        SELECT id FROM equipo WHERE nombre = ?
    """)
    query.addBindValue(nombre)
    query.exec()

    if query.next():
        return query.value(0)
    return None


def obtener_partidos_por_fase(fase):
    query = QSqlQuery()
    query.prepare("""
        SELECT 
            p.id,
            el.nombre AS local,
            ev.nombre AS visitante,
            p.goles_local,
            p.goles_visitante
        FROM partido p
        JOIN equipo el ON p.equipo_local = el.id
        JOIN equipo ev ON p.equipo_visitante = ev.id
        WHERE p.fase = ?
        ORDER BY p.id
    """)
    query.addBindValue(fase)
    query.exec()

    partidos = []
    while query.next():
        partidos.append({
            "id": query.value(0),
            "local": query.value(1),
            "visitante": query.value(2),
            "gl": query.value(3),
            "gv": query.value(4)
        })
    return partidos


def obtener_partidos_por_fase_con_id(fase):
    query = QSqlQuery()
    query.prepare("""
        SELECT 
            p.id,
            el.nombre AS local,
            ev.nombre AS visitante,
            p.goles_local,
            p.goles_visitante
        FROM partido p
        JOIN equipo el ON p.equipo_local = el.id
        JOIN equipo ev ON p.equipo_visitante = ev.id
        WHERE p.fase = ?
        ORDER BY p.id
    """)
    query.addBindValue(fase)
    query.exec()

    partidos = []
    while query.next():
        partidos.append({
            "id": query.value(0),
            "local": query.value(1),
            "visitante": query.value(2),
            "gl": query.value(3),
            "gv": query.value(4)
        })
    return partidos

def generar_siguiente_fase_por_resultados(fase_actual, fase_siguiente):
    """
    Genera la siguiente fase usando los ganadores de la fase actual.
    Solo si la fase actual está completa.
    Regla: si empatan, pasa el local.
    """
    if not fase_completa(fase_actual):
        return False

    query = QSqlQuery()
    query.prepare("""
        SELECT equipo_local, equipo_visitante, goles_local, goles_visitante
        FROM partido
        WHERE fase = ?
        ORDER BY id
    """)
    query.addBindValue(fase_actual)
    query.exec()

    ganadores = []

    while query.next():
        el = query.value(0)
        ev = query.value(1)
        gl = query.value(2)
        gv = query.value(3)

        if gl >= gv:   # pasa el local
            ganadores.append(el)
        else:
            ganadores.append(ev)

    # Emparejar de dos en dos
    for i in range(0, len(ganadores), 2):
        q = QSqlQuery()
        q.prepare("""
            INSERT INTO partido (
                equipo_local,
                equipo_visitante,
                fecha,
                fase,
                goles_local,
                goles_visitante
            )
            VALUES (?, ?, '', ?, 0, 0)
        """)
        q.addBindValue(ganadores[i])
        q.addBindValue(ganadores[i + 1])
        q.addBindValue(fase_siguiente)
        q.exec()
    
    return True

def fase_completa(fase):
    """
    Devuelve True si todos los partidos de una fase
    tienen resultado introducido
    """
    query = QSqlQuery("""
        SELECT COUNT(*)
        FROM partido
        WHERE fase = ?
          AND (goles_local IS NULL OR goles_visitante IS NULL)
    """)
    query.addBindValue(fase)
    query.exec()
    query.next()

    return query.value(0) == 0

def generar_eliminatorias_desde_clasificacion(clasificacion):
    borrar_eliminatorias()
    generar_octavos(clasificacion)

