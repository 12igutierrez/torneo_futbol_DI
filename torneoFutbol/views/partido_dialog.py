from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.partido_controller import insertar_partido
from controllers.equipo_controller import obtener_equipos
from controllers.participante_controller import obtener_participantes


class PartidoDialog(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "partido_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.cargar_datos()
        self.ui.btn_guardar.clicked.connect(self.guardar)


    def cargar_datos(self):
        self.ui.combo_local.clear()
        self.ui.combo_visitante.clear()
        self.ui.combo_arbitro.clear()

        # ================= EQUIPOS =================
        for equipo_id, nombre in obtener_equipos():
            self.ui.combo_local.addItem(nombre, equipo_id)
            self.ui.combo_visitante.addItem(nombre, equipo_id)

        # ================= ÁRBITROS =================
        participantes = obtener_participantes()

        for p in participantes:
            participante_id = p[0]
            nombre = p[1]
            tipo = p[4]

            if tipo == "arbitro":
                self.ui.combo_arbitro.addItem(nombre, participante_id)


    def guardar(self):
        local_id = self.ui.combo_local.currentData()
        visitante_id = self.ui.combo_visitante.currentData()
        arbitro_id = self.ui.combo_arbitro.currentData()
        fecha = self.ui.txt_fecha.text().strip()

        if local_id == visitante_id:
            QMessageBox.warning(self, "Error", "Los equipos no pueden ser iguales")
            return

        if not fecha:
            QMessageBox.warning(self, "Error", "Introduce la fecha")
            return

        if not insertar_partido(local_id, visitante_id, fecha, arbitro_id):
            QMessageBox.critical(self, "Error", "No se pudo crear el partido")
            return

        self.accept()
