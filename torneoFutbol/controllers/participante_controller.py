from PySide6.QtSql import QSqlQuery


def insertar_participante(nombre, fecha, curso, tipo, posicion):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO participante (nombre, fecha, curso, tipo, posicion)
        VALUES (?, ?, ?, ?, ?)
    """)
    query.addBindValue(nombre)
    query.addBindValue(fecha)
    query.addBindValue(curso)
    query.addBindValue(tipo)
    query.addBindValue(posicion)

    if not query.exec():
        print("Error SQL insertar_participante:", query.lastError().text())
        return False
    return True


def obtener_participantes():
    query = QSqlQuery("""
        SELECT p.id,
               p.nombre,
               p.fecha,
               p.curso,
               p.tipo,
               IFNULL(p.posicion, ''),
               IFNULL(e.nombre, '')
        FROM participante p
        LEFT JOIN equipo e ON p.equipo_id = e.id
        ORDER BY p.nombre
    """)

    participantes = []
    while query.next():
        participantes.append((
            query.value(0),  # id
            query.value(1),  # nombre
            query.value(2),  # fecha nacimiento
            query.value(3),  # curso
            query.value(4),  # tipo
            query.value(5),  # posicion
            query.value(6)   # equipo
        ))
    return participantes


def obtener_participante_por_id(participante_id):
    query = QSqlQuery()
    query.prepare("""
        SELECT nombre, fecha, curso, tipo, posicion
        FROM participante
        WHERE id = ?
    """)
    query.addBindValue(participante_id)
    query.exec()

    if query.next():
        return (
            query.value(0),
            query.value(1),
            query.value(2),
            query.value(3),
            query.value(4)
        )
    return None


def actualizar_participante(participante_id, nombre, fecha, curso, tipo, posicion):
    query = QSqlQuery()
    query.prepare("""
        UPDATE participante
        SET nombre = ?, fecha = ?, curso = ?, tipo = ?, posicion = ?
        WHERE id = ?
    """)
    query.addBindValue(nombre)
    query.addBindValue(fecha)
    query.addBindValue(curso)
    query.addBindValue(tipo)
    query.addBindValue(posicion)
    query.addBindValue(participante_id)

    if not query.exec():
        print("Error SQL actualizar_participante:", query.lastError().text())
        return False
    return True


def eliminar_participante(participante_id):
    query = QSqlQuery()
    query.prepare("""
        DELETE FROM participante
        WHERE id = ?
    """)
    query.addBindValue(participante_id)

    if not query.exec():
        print("Error SQL eliminar_participante:", query.lastError().text())
        return False
    return True


def asignar_equipo(jugador_id, equipo_id):
    query = QSqlQuery()
    query.prepare("""
        UPDATE participante
        SET equipo_id = ?
        WHERE id = ? AND tipo = 'jugador'
    """)
    query.addBindValue(equipo_id)
    query.addBindValue(jugador_id)

    if not query.exec():
        print("Error SQL asignar_equipo:", query.lastError().text())
        return False
    return True

