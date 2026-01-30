from PySide6.QtSql import QSqlQuery

def obtener_jugadores_de_partido(partido_id):
    query = QSqlQuery("""
        SELECT p.id, p.nombre
        FROM participante p
        JOIN partido pa ON 
            p.equipo_id = pa.equipo_local OR p.equipo_id = pa.equipo_visitante
        WHERE pa.id = ? AND p.tipo = 'jugador'
    """)
    query.addBindValue(partido_id)
    query.exec()

    jugadores = []
    while query.next():
        jugadores.append((query.value(0), query.value(1)))
    return jugadores


def obtener_estadistica(partido_id, jugador_id):
    query = QSqlQuery("""
        SELECT goles, amarillas, rojas
        FROM estadistica
        WHERE partido_id = ? AND participante_id = ?
    """)
    query.addBindValue(partido_id)
    query.addBindValue(jugador_id)
    query.exec()

    if query.next():
        return query.value(0), query.value(1), query.value(2)

    return 0, 0, 0


def guardar_estadistica(partido_id, jugador_id, goles, amarillas, rojas):
    query = QSqlQuery("""
        SELECT id FROM estadistica
        WHERE partido_id = ? AND participante_id = ?
    """)
    query.addBindValue(partido_id)
    query.addBindValue(jugador_id)
    query.exec()

    if query.next():
        q = QSqlQuery("""
            UPDATE estadistica
            SET goles=?, amarillas=?, rojas=?
            WHERE partido_id=? AND participante_id=?
        """)
        q.addBindValue(goles)
        q.addBindValue(amarillas)
        q.addBindValue(rojas)
        q.addBindValue(partido_id)
        q.addBindValue(jugador_id)
        return q.exec()

    q = QSqlQuery("""
        INSERT INTO estadistica
        (partido_id, participante_id, goles, amarillas, rojas)
        VALUES (?, ?, ?, ?, ?)
    """)
    q.addBindValue(partido_id)
    q.addBindValue(jugador_id)
    q.addBindValue(goles)
    q.addBindValue(amarillas)
    q.addBindValue(rojas)
    return q.exec()
