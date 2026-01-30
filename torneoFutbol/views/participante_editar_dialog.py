from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.participante_controller import obtener_participante_por_id,actualizar_participante


class EditarParticipanteDialog(QDialog):
    def __init__(self, participante_id):
        super().__init__()
        self.participante_id = participante_id

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "participante_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.ui.combo_tipo.currentTextChanged.connect(self.actualizar_posicion)
        self.ui.btn_guardar.clicked.connect(self.guardar)

        self.cargar_datos()


    def actualizar_posicion(self):
        es_jugador = self.ui.combo_tipo.currentText() == "Jugador"
        self.ui.combo_posicion.setEnabled(es_jugador)


    def cargar_datos(self):
        datos = obtener_participante_por_id(self.participante_id)
        if not datos:
            QMessageBox.critical(self, "Error", "Participante no encontrado")
            self.reject()
            return

        nombre, fecha, curso, tipo, posicion = datos

        self.ui.txt_nombre.setText(nombre)
        self.ui.txt_fecha.setText(fecha)
        self.ui.txt_curso.setText(curso)

        self.ui.combo_tipo.setCurrentText(
            "Árbitro" if tipo == "arbitro" else "Jugador"
        )

        if posicion:
            self.ui.combo_posicion.setCurrentText(posicion)

        self.actualizar_posicion()


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

        ok = actualizar_participante(
            self.participante_id,
            nombre,
            fecha,
            curso,
            tipo,
            posicion
        )

        if not ok:
            QMessageBox.critical(self, "Error", "No se pudo actualizar")
            return

        self.accept()
