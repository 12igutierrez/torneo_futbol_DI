from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.estadistica_controller import (
    obtener_jugadores_de_partido,
    obtener_estadistica,
    guardar_estadistica
)

class EstadisticaDialog(QDialog):
    def __init__(self, partido_id):
        super().__init__()

        self.partido_id = partido_id

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "estadistica_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.cargar_jugadores()
        self.ui.combo_jugador.currentIndexChanged.connect(self.cargar_estadistica)
        self.ui.btn_guardar.clicked.connect(self.guardar)


    def cargar_jugadores(self):
        self.jugadores = obtener_jugadores_de_partido(self.partido_id)
        self.ui.combo_jugador.clear()

        for j in self.jugadores:
            self.ui.combo_jugador.addItem(j[1], j[0])

        if self.jugadores:
            self.cargar_estadistica()


    def cargar_estadistica(self):
        jugador_id = self.ui.combo_jugador.currentData()
        if jugador_id is None:
            return

        goles, amarillas, rojas = obtener_estadistica(self.partido_id, jugador_id)
        self.ui.spin_goles.setValue(goles)
        self.ui.spin_amarillas.setValue(amarillas)
        self.ui.spin_rojas.setValue(rojas)


    def guardar(self):
        jugador_id = self.ui.combo_jugador.currentData()
        guardar_estadistica(
            self.partido_id,
            jugador_id,
            self.ui.spin_goles.value(),
            self.ui.spin_amarillas.value(),
            self.ui.spin_rojas.value()
        )
        self.accept()
