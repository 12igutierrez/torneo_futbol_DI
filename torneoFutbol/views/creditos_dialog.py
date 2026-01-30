from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class CreditosDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créditos")
        self.resize(400, 250)

        layout = QVBoxLayout(self)

        label = QLabel("""
<h2>Gestión de Torneo de Fútbol</h2>

<b>Autor:</b> Íñigo Gutiérrez López<br>
<b>Curso:</b> 2º DAM<br>
<b>Asignatura:</b> Desarrollo de Interfaces<br>
<b>Año:</b> 2026<br><br>

Proyecto académico realizado con Python, PySide6 y SQLite.
""")

        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)

        layout.addWidget(label)
