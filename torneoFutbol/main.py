import sys
from PySide6.QtWidgets import QApplication
from models.database import conectar_bd
from views.mainwindow import MainWindow
from pathlib import Path

if __name__ == "__main__":
    app = QApplication(sys.argv)

    qss_path = Path("resources/qss/style.qss")

    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    else:
        print("⚠️ No se encontró el archivo style.qss")

    conectar_bd()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
