from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt


class AyudaDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ayuda - Gestión del Torneo")
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        contenido = QLabel("""
<h2>Ayuda del Programa</h2><br>

<b>Equipos</b><br>
- Puedes crear, editar y eliminar equipos.<br>
- Un equipo no puede eliminarse si tiene partidos o jugadores asignados.<br><br><br>

<b>Participantes</b><br>
- Los participantes pueden ser jugadores o árbitros.<br>
- Los jugadores se asignan a equipos.<br>
- Los árbitros se asignan a los partidos.<br><br><br>


<b>Partidos</b><br>
- Se pueden crear partidos entre equipos.<br>
- Para introducir los goles, el partido debe de estar en juego.<br>
- Los goles solo se actualizan si el partido termina.<br>
- La clasificación solo se actualiza si el partido termina.<br>
- Si se cierra la aplicación sin terminar el partido, el resultado será 0-0.<br><br><br>

<b>Eliminatorias</b><br>
- Se generan automáticamente a partir de la clasificación.<br>
- Al introducir resultados, se avanza de fase automáticamente.<br>
- Para pasar de fase es necesario introducir resultados (no vale 0-0).<br><br><br>

<b>Final</b><br>
- Al introducir el resultado de la final se obtiene el campeón.<br><br>
""")

        contenido.setWordWrap(True)
        contenido.setAlignment(Qt.AlignTop)

        scroll.setWidget(contenido)
        layout.addWidget(scroll)
