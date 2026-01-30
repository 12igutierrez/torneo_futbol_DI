import sys
from PySide6.QtCore import QCoreApplication
from models.database import conectar_bd

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    conectar_bd()
    print("Base de datos creada correctamente")
