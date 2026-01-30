from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.participante_controller import insertar_participante


class ParticipanteDialog(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "participante_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.ui.combo_tipo.currentTextChanged.connect(self.actualizar_posicion)
        self.ui.btn_guardar.clicked.connect(self.guardar)

        self.actualizar_posicion()


    def actualizar_posicion(self):
        es_jugador = self.ui.combo_tipo.currentText() == "Jugador"
        self.ui.combo_posicion.setEnabled(es_jugador)


    def guardar(self):
        nombre = self.ui.txt_nombre.text().strip()
        fecha = self.ui.txt_fecha.text().strip()
        curso = self.ui.txt_curso.text().strip()
        texto_tipo = self.ui.combo_tipo.currentText()

        tipo = "arbitro" if texto_tipo == "Árbitro" else "jugador"
        posicion = (
            self.ui.combo_posicion.currentText()
            if tipo == "jugador"
            else None
        )

        if not nombre or not fecha:
            QMessageBox.warning(self, "Error", "Datos incompletos")
            return

        ok = insertar_participante(
            nombre,
            fecha,
            curso,
            tipo,
            posicion
        )

        if not ok:
            QMessageBox.critical(
                self,
                "Error",
                "No se pudo guardar el participante.\nRevisa la base de datos."
            )
            return

        self.accept()
