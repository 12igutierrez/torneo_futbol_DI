from PySide6.QtSql import QSqlDatabase, QSqlQuery
from pathlib import Path
import sys
import shutil


def obtener_ruta_bd():
    """
    Devuelve la ruta donde se usará la base de datos.
    - En desarrollo: data/torneoFutbol_sqlite.db
    - En exe: junto al ejecutable
    """

    if hasattr(sys, "_MEIPASS"):
        # Estamos en el .exe
        exe_dir = Path(sys.executable).parent
        db_destino = exe_dir / "torneoFutbol_sqlite.db"

        # BD original empaquetada
        db_origen = Path(sys._MEIPASS) / "data" / "torneoFutbol_sqlite.db"

        if not db_destino.exists():
            shutil.copy(db_origen, db_destino)

        return db_destino

    else:
        # Modo desarrollo normal
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        return data_dir / "torneoFutbol_sqlite.db"


def conectar_bd():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(str(obtener_ruta_bd()))

    if not db.open():
        raise Exception("No se pudo abrir la base de datos")

    crear_tablas()
    return db


def crear_tablas():
    query = QSqlQuery()

    query.exec("""
        CREATE TABLE IF NOT EXISTS equipo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            curso TEXT,
            color TEXT,
            escudo TEXT
        )
    """)

    query.exec("""
        CREATE TABLE IF NOT EXISTS participante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha TEXT,
            curso TEXT,
            tipo TEXT,
            posicion TEXT,
            equipo_id INTEGER,
            FOREIGN KEY (equipo_id) REFERENCES equipo(id)
        )
    """)

    query.exec("""
        CREATE TABLE IF NOT EXISTS partido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_local INTEGER,
            equipo_visitante INTEGER,
            fecha TEXT,
            arbitro_id INTEGER,
            goles_local INTEGER DEFAULT 0,
            goles_visitante INTEGER DEFAULT 0,
            fase TEXT
        )
    """)

