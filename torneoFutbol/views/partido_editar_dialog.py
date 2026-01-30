from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.partido_controller import obtener_partido_por_id_editar, actualizar_partido
from controllers.equipo_controller import obtener_equipos
from controllers.participante_controller import obtener_participantes


class EditarPartidoDialog(QDialog):
    def __init__(self, partido_id):
        super().__init__()
        self.partido_id = partido_id

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "partido_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.cargar_datos()
        self.ui.btn_guardar.clicked.connect(self.guardar)


    def cargar_datos(self):
        datos = obtener_partido_por_id_editar(self.partido_id)
        if not datos:
            QMessageBox.critical(self, "Error", "Partido no encontrado")
            self.reject()
            return

        equipo_local, equipo_visitante, fecha, arbitro_id = datos

        self.ui.combo_local.clear()
        self.ui.combo_visitante.clear()
        self.ui.combo_arbitro.clear()

        for eid, nombre in obtener_equipos():
            self.ui.combo_local.addItem(nombre, eid)
            self.ui.combo_visitante.addItem(nombre, eid)

        for pid, nombre, _, _, tipo, _, _ in obtener_participantes():
            if tipo == "arbitro":
                self.ui.combo_arbitro.addItem(nombre, pid)

        self.ui.combo_local.setCurrentIndex(
            self.ui.combo_local.findData(equipo_local)
        )
        self.ui.combo_visitante.setCurrentIndex(
            self.ui.combo_visitante.findData(equipo_visitante)
        )
        self.ui.combo_arbitro.setCurrentIndex(
            self.ui.combo_arbitro.findData(arbitro_id)
        )

        self.ui.txt_fecha.setText(fecha)


    def guardar(self):
        local = self.ui.combo_local.currentData()
        visitante = self.ui.combo_visitante.currentData()
        arbitro = self.ui.combo_arbitro.currentData()
        fecha = self.ui.txt_fecha.text().strip()

        if local == visitante:
            QMessageBox.warning(self, "Error", "Los equipos no pueden ser iguales")
            return
        
        if not fecha:
            QMessageBox.warning(self, "Error", "Introduce la fecha")
            return
        
        if not actualizar_partido(self.partido_id, local, visitante, fecha, arbitro):
            QMessageBox.critical(self, "Error", "No se pudo actualizar el partido")
            return

        self.accept()
