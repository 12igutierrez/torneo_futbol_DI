from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.participante_controller import obtener_participantes, asignar_equipo
from controllers.equipo_controller import obtener_equipos


class AsignarEquipoDialog(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "asignar_equipo_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.cargar_datos()
        self.ui.btn_guardar.clicked.connect(self.guardar)


    def cargar_datos(self):
        self.ui.combo_jugador.clear()
        self.ui.combo_equipo.clear()

        participantes = obtener_participantes()

        # FILTRAMOS SOLO JUGADORES (tipo = índice 4)
        jugadores = [
            p for p in participantes
            if p[4] == "jugador"
        ]

        if not jugadores:
            QMessageBox.warning(
                self,
                "Sin jugadores",
                "No hay jugadores creados"
            )
            self.reject()
            return

        for p in jugadores:
            jugador_id = p[0]
            nombre = p[1]
            equipo = p[6]

            texto = nombre if not equipo else f"{nombre} ({equipo})"
            self.ui.combo_jugador.addItem(texto, jugador_id)

        equipos = obtener_equipos()
        if not equipos:
            QMessageBox.warning(
                self,
                "Sin equipos",
                "No hay equipos creados"
            )
            self.reject()
            return

        for equipo_id, nombre in equipos:
            self.ui.combo_equipo.addItem(nombre, equipo_id)


    def guardar(self):
        jugador_id = self.ui.combo_jugador.currentData()
        equipo_id = self.ui.combo_equipo.currentData()

        if jugador_id is None or equipo_id is None:
            QMessageBox.warning(
                self,
                "Error",
                "Selecciona jugador y equipo"
            )
            return

        if not asignar_equipo(jugador_id, equipo_id):
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo asignar el equipo"
            )
            return

        QMessageBox.information(
            self,
            "Correcto",
            "Equipo asignado correctamente"
        )
        self.accept()
