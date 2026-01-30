from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from controllers.partido_controller import (
    actualizar_resultado,
    generar_siguiente_fase_por_resultados,
    fase_completa
)

class ResultadoDialog(QDialog):
    def __init__(self, partido_id, texto_partido, goles_local, goles_visitante, fase):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "resultado_dialog.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        self.partido_id = partido_id
        self.fase = fase

        self.ui.lbl_partido.setText(texto_partido)
        self.ui.spin_local.setValue(goles_local)
        self.ui.spin_visitante.setValue(goles_visitante)
        self.ui.btn_guardar.clicked.connect(self.guardar)


    def guardar(self):
        gl = self.ui.spin_local.value()
        gv = self.ui.spin_visitante.value()
        actualizar_resultado(self.partido_id, gl, gv)

        # Solo generar la siguiente fase si la fase actual está completa
        if fase_completa(self.fase):

            if self.fase == "Octavos":
                generar_siguiente_fase_por_resultados("Octavos", "Cuartos")
            elif self.fase == "Cuartos":
                generar_siguiente_fase_por_resultados("Cuartos", "Semifinal")
            elif self.fase == "Semifinal":
                generar_siguiente_fase_por_resultados("Semifinal", "Final")

        self.accept()
