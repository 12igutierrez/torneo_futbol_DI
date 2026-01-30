from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import QTimer, Qt


def format_mm_ss(seconds):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


class PartidoEnVivoDialog(QDialog):
    DURACION_PARTIDO = 90 * 60

    def __init__(self, equipo_local, equipo_visitante, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Partido en curso")
        self.setModal(True)

        self._seconds = self.DURACION_PARTIDO
        self._running = False

        self.goles_local = 0
        self.goles_visitante = 0
        self.resultado = (0, 0)

        # UI
        self.lbl_equipos = QLabel(f"{equipo_local}  vs  {equipo_visitante}")
        self.lbl_equipos.setAlignment(Qt.AlignCenter)

        self.lbl_time = QLabel("90:00")
        self.lbl_time.setAlignment(Qt.AlignCenter)

        self.lbl_marcador = QLabel("0  -  0")
        self.lbl_marcador.setAlignment(Qt.AlignCenter)

        self.btn_start = QPushButton("Iniciar")
        self.btn_pause = QPushButton("Pausar")
        self.btn_reset = QPushButton("Reiniciar")

        self.btn_gol_local = QPushButton("+ Gol Local")
        self.btn_gol_visitante = QPushButton("+ Gol Visitante")
        self.btn_quitar_local = QPushButton("- Gol Local")
        self.btn_quitar_visitante = QPushButton("- Gol Visitante")

        layout = QVBoxLayout(self)
        layout.addWidget(self.lbl_equipos)
        layout.addWidget(self.lbl_time)
        layout.addWidget(self.lbl_marcador)

        botones = QHBoxLayout()
        botones.addWidget(self.btn_start)
        botones.addWidget(self.btn_pause)
        botones.addWidget(self.btn_reset)
        layout.addLayout(botones)

        goles = QHBoxLayout()
        goles.addWidget(self.btn_gol_local)
        goles.addWidget(self.btn_gol_visitante)
        goles.addWidget(self.btn_quitar_local)
        goles.addWidget(self.btn_quitar_visitante)
        layout.addLayout(goles)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)

        # Conexiones
        self.btn_start.clicked.connect(self.start)
        self.btn_pause.clicked.connect(self.pause)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_gol_local.clicked.connect(self.gol_local)
        self.btn_gol_visitante.clicked.connect(self.gol_visitante)
        self.btn_quitar_local.clicked.connect(self.quitar_gol_local)
        self.btn_quitar_visitante.clicked.connect(self.quitar_gol_visitante)

        self._update_display()

    def _tick(self):
        if not self._running:
            return

        if self._seconds > 0:
            self._seconds -= 1
            self._update_display()

        if self._seconds == 0:
            self._running = False
            self.resultado = (self.goles_local, self.goles_visitante)
            QMessageBox.information(self, "Final", "El partido ha terminado")
            self.accept()

    def _update_display(self):
        self.lbl_time.setText(format_mm_ss(self._seconds))
        self.lbl_marcador.setText(f"{self.goles_local}  -  {self.goles_visitante}")

    def start(self):
        self._running = True

    def pause(self):
        self._running = False

    def reset(self):
        self._running = False
        self._seconds = self.DURACION_PARTIDO
        self._update_display()

    def gol_local(self):
        if self._running:
            self.goles_local += 1
            self._update_display()

    def gol_visitante(self):
        if self._running:
            self.goles_visitante += 1
            self._update_display()

    def quitar_gol_local(self):
        if self._running and self.goles_local > 0:
            self.goles_local -= 1
            self._update_display()

    def quitar_gol_visitante(self):
        if self._running and self.goles_visitante > 0:
            self.goles_visitante -= 1
            self._update_display()

    def closeEvent(self, event):
        self.resultado = (self.goles_local, self.goles_visitante)
        event.accept()

