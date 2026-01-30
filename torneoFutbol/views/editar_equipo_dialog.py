from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.equipo_controller import actualizar_equipo


class EditarEquipoDialog(QDialog):
    def __init__(self, equipo_id, nombre, curso, color):
        super().__init__()

        self.equipo_id = equipo_id

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "editar_equipo_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.ui.txt_nombre.setText(nombre)
        self.ui.txt_curso.setText(curso)
        self.ui.txt_color.setText(color)

        self.ui.btn_guardar.clicked.connect(self.guardar)


    def guardar(self):
        nombre = self.ui.txt_nombre.text().strip()
        curso = self.ui.txt_curso.text().strip()
        color = self.ui.txt_color.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        actualizar_equipo(self.equipo_id, nombre, curso, color)
        self.accept()
