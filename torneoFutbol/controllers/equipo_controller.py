from PySide6.QtSql import QSqlQuery


# =========================
# INSERTAR EQUIPO
# =========================
def insertar_equipo(nombre, curso, color, escudo=None):
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO equipo (nombre, curso, color, escudo)
        VALUES (?, ?, ?, ?)
    """)
    query.addBindValue(nombre)
    query.addBindValue(curso)
    query.addBindValue(color)
    query.addBindValue(escudo)
    return query.exec()


# =========================
# OBTENER EQUIPOS (TABLA)
# =========================
def obtener_equipos_tabla():
    query = QSqlQuery("""
        SELECT id, nombre, curso, color, escudo
        FROM equipo
    """)

    equipos = []
    while query.next():
        equipos.append((
            query.value(0),
            query.value(1),
            query.value(2),
            query.value(3),
            query.value(4)
        ))
    return equipos


# =========================
# OBTENER EQUIPOS (ID + NOMBRE)
# =========================
def obtener_equipos():
    query = QSqlQuery("""
        SELECT id, nombre
        FROM equipo
    """)

    equipos = []
    while query.next():
        equipos.append((query.value(0), query.value(1)))
    return equipos


# =========================
# ACTUALIZAR EQUIPO
# =========================
def actualizar_equipo(equipo_id, nombre, curso, color):
    query = QSqlQuery()
    query.prepare("""
        UPDATE equipo
        SET nombre = ?, curso = ?, color = ?
        WHERE id = ?
    """)
    query.addBindValue(nombre)
    query.addBindValue(curso)
    query.addBindValue(color)
    query.addBindValue(equipo_id)
    return query.exec()


# =========================
# ACTUALIZAR ESCUDO
# =========================
def actualizar_escudo(equipo_id, ruta_escudo):
    query = QSqlQuery()
    query.prepare("""
        UPDATE equipo
        SET escudo = ?
        WHERE id = ?
    """)
    query.addBindValue(ruta_escudo)
    query.addBindValue(equipo_id)
    return query.exec()


# =========================
# OBTENER ESCUDO POR NOMBRE
# =========================
def obtener_escudo_equipo(nombre_equipo):
    query = QSqlQuery()
    query.prepare("""
        SELECT escudo FROM equipo WHERE nombre = ?
    """)
    query.addBindValue(nombre_equipo)
    query.exec()

    if query.next():
        return query.value(0)
    return None


# =========================
# DEPENDENCIAS
# =========================
def equipo_tiene_dependencias(equipo_id):
    q1 = QSqlQuery("""
        SELECT COUNT(*) FROM participante WHERE equipo_id = ?
    """)
    q1.addBindValue(equipo_id)
    q1.exec()
    q1.next()

    if q1.value(0) > 0:
        return True

    q2 = QSqlQuery("""
        SELECT COUNT(*) FROM partido
        WHERE equipo_local = ? OR equipo_visitante = ?
    """)
    q2.addBindValue(equipo_id)
    q2.addBindValue(equipo_id)
    q2.exec()
    q2.next()

    return q2.value(0) > 0


# =========================
# ELIMINAR EQUIPO
# =========================
def eliminar_equipo(equipo_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM equipo WHERE id = ?")
    query.addBindValue(equipo_id)
    return query.exec()

