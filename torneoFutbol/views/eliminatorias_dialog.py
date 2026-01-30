from PySide6.QtWidgets import (QDialog, QTableWidgetItem, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem, QAbstractItemView, QHeaderView)
from PySide6.QtUiTools import QUiLoader
from pathlib import Path
from PySide6.QtGui import QPen, QPixmap
from PySide6.QtCore import Qt
from controllers.equipo_controller import obtener_escudo_equipo
from views.resultado_dialog import ResultadoDialog
from controllers.partido_controller import obtener_partidos_por_fase_con_id, generar_siguiente_fase_por_resultados
from utils.path_utils import resource_path

class EliminatoriasDialog(QDialog):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "eliminatorias_dialog.ui"
        self.ui = loader.load(str(ui_path), self)
        self.setLayout(self.ui.layout())


        # AJUSTES DE VENTANA
        self.setWindowTitle("Cuadro de Eliminatorias")
        self.resize(1200, 900)

        # CONFIGURAR TABLAS
        self._configurar_tablas()
        self._cargar_fase("octavos", self.ui.table_octavos)
        self._cargar_fase("cuartos", self.ui.table_cuartos)
        self._cargar_fase("semifinal", self.ui.table_semifinal)
        self._cargar_fase("final", self.ui.table_final)

        # ÁREA GRÁFICA
        if hasattr(self.ui, "graphicsView"):
            self.scene = QGraphicsScene()
            self.ui.graphicsView.setScene(self.scene)
        
        self._redibujar_cuadro_completo()


        self.ui.btn_resultado_octavos.clicked.connect(
            lambda: self._introducir_resultado(self.ui.table_octavos, "octavos")
        )
        self.ui.btn_resultado_cuartos.clicked.connect(
            lambda: self._introducir_resultado(self.ui.table_cuartos, "cuartos")
        )
        self.ui.btn_resultado_semifinal.clicked.connect(
            lambda: self._introducir_resultado(self.ui.table_semifinal, "semifinal")
        )
        self.ui.btn_resultado_final.clicked.connect(
            lambda: self._introducir_resultado(self.ui.table_final, "final")
        )

        self.ui.graphicsView.setMinimumWidth(550)
        self.ui.graphicsView.setMaximumWidth(700)

        qss_path = resource_path("resources/qss/style.qss")
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))


    # TABLAS
    def _configurar_tablas(self):
        tablas = [
            (self.ui.table_octavos, 6),
            (self.ui.table_cuartos, 4),
            (self.ui.table_semifinal, 2),
            (self.ui.table_final, 1),
        ]

        for tabla, filas in tablas:
            tabla.horizontalHeader().setStretchLastSection(True)
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabla.setColumnCount(4)
            tabla.setHorizontalHeaderLabels([
                "Equipo local",
                "Equipo visitante",
                "Goles local",
                "Goles visitante"
            ])
            # Desactivar edición de celdas
            tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # Permitir selección de filas completas
            tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
            tabla.setSelectionMode(QAbstractItemView.SingleSelection)
            # No permitir reordenar columnas
            tabla.horizontalHeader().setSectionsMovable(False)
            # Ajuste visual
            tabla.horizontalHeader().setStretchLastSection(True)
            # Ajuste de altura
            self._ajustar_altura_tabla(tabla, filas)


    def _cargar_fase(self, fase, tabla):
        partidos = obtener_partidos_por_fase_con_id(fase)
        tabla.setRowCount(len(partidos))

        for fila, p in enumerate(partidos):
            item_local = QTableWidgetItem(p["local"])
            item_local.setData(Qt.UserRole, p["id"])

            tabla.setItem(fila, 0, item_local)
            tabla.setItem(fila, 1, QTableWidgetItem(p["visitante"]))
            tabla.setItem(fila, 2, QTableWidgetItem(str(p["gl"])))
            tabla.setItem(fila, 3, QTableWidgetItem(str(p["gv"])))


    def _dibujar_octavos(self):
        self.scene.clear()

        partidos = obtener_partidos_por_fase_con_id("octavos")
        if not partidos:
            return

        x_equipo = 20
        x_goles = 250
        x_linea = 320
        y = 20
        alto_partido = 90

        pen = QPen(Qt.black, 2)

        for p in partidos:
            local = p["local"]
            visitante = p["visitante"]
            gl = p["gl"]
            gv = p["gv"]

            self._dibujar_equipo_con_escudo(local, x_equipo, y)

            txt_gl = QGraphicsTextItem(str(gl))
            txt_gl.setPos(x_goles, y)
            self.scene.addItem(txt_gl)

            self._dibujar_equipo_con_escudo(visitante, x_equipo, y + 45)

            txt_gv = QGraphicsTextItem(str(gv))
            txt_gv.setPos(x_goles, y + 25)
            self.scene.addItem(txt_gv)

            self.scene.addLine(
                x_linea,
                y + 12,
                x_linea,
                y + 37,
                pen
            )

            y += alto_partido


    def _ganadores_fase(self, fase):
        partidos = obtener_partidos_por_fase_con_id(fase)
        ganadores = []

        for p in partidos:
            if p["gl"] >= p["gv"]:
                ganadores.append(p["local"])
            else:
                ganadores.append(p["visitante"])
        return ganadores


    def _dibujar_cuartos(self):
        if not self._fase_existe("cuartos"):
            return

        ganadores = self._ganadores_fase("octavos")

        if len(ganadores) < 8:
            return

        x_equipo = 380
        x_linea = 650
        y = 120
        alto_partido = 130

        pen = QPen(Qt.black, 2)

        for i in range(0, 8, 2):
            equipo1 = ganadores[i]
            equipo2 = ganadores[i + 1]

            self._dibujar_equipo_con_escudo(equipo1, x_equipo, y)
            self._dibujar_equipo_con_escudo(equipo2, x_equipo, y + 45)

            self.scene.addLine(x_linea, y + 15,x_linea, y + 45,pen)
            self.scene.addLine(x_linea, y + 30, x_linea + 40, y + 30,pen)

            y += alto_partido


    def _dibujar_semifinales(self):
        if not self._fase_existe("cuartos"):
            return

        ganadores = self._ganadores_fase("cuartos")

        if len(ganadores) < 4:
            return

        x_equipo = 720
        x_linea = 980
        y = 180
        alto_partido = 240

        pen = QPen(Qt.black, 2)

        for i in range(0, 4, 2):
            equipo1 = ganadores[i]
            equipo2 = ganadores[i + 1]

            self._dibujar_equipo_con_escudo(equipo1, x_equipo, y)

            self._dibujar_equipo_con_escudo(equipo2, x_equipo, y + 45)

            self.scene.addLine(
                x_linea,
                y + 15,
                x_linea,
                y + 45,
                pen
            )

            self.scene.addLine(
                x_linea,
                y + 30,
                x_linea + 40,
                y + 30,
                pen
            )

            y += alto_partido


    def _dibujar_final(self):
        if not self._fase_existe("cuartos"):
            return

        ganadores = self._ganadores_fase("semifinal")

        if len(ganadores) < 2:
            return

        equipo1 = ganadores[0]
        equipo2 = ganadores[1]

        x_equipo = 1050
        x_linea = 1250
        y = 285

        pen = QPen(Qt.black, 2)

        self._dibujar_equipo_con_escudo(equipo1, x_equipo, y)

        self._dibujar_equipo_con_escudo(equipo2, x_equipo, y + 45)

        self.scene.addLine(
            x_linea,
            y + 15,
            x_linea,
            y + 45,
            pen
        )

        self.scene.addLine(
            x_linea,
            y + 30,
            x_linea + 50,
            y + 30,
            pen
        )


    def _introducir_resultado(self, tabla, fase):
        fila = tabla.currentRow()
        if fila < 0:
            return

        item = tabla.item(fila, 0)
        partido_id = item.data(Qt.UserRole)

        local = tabla.item(fila, 0).text()
        visitante = tabla.item(fila, 1).text()
        gl = int(tabla.item(fila, 2).text())
        gv = int(tabla.item(fila, 3).text())

        dialog = ResultadoDialog(
            partido_id,
            f"{local} vs {visitante}",
            gl,
            gv,
            fase
        )

        if dialog.exec():
            self._cargar_fase(fase, tabla)
            self._comprobar_siguiente_fase(fase)
            self._redibujar_cuadro_completo()

    
    def _comprobar_siguiente_fase(self, fase_actual):
        fases = ["octavos", "cuartos", "semifinal", "final"]

        if fase_actual not in fases:
             return

        idx = fases.index(fase_actual)
        if idx == len(fases) - 1:
            return  # ya es la final

        partidos = obtener_partidos_por_fase_con_id(fase_actual)

        for p in partidos:
            if p["gl"] == p["gv"]:
                return  # empate no se avanza

        generar_siguiente_fase_por_resultados(
            fase_actual,
            fases[idx + 1]
        )

        self._cargar_fase(
            fases[idx + 1],
            getattr(self.ui, f"table_{fases[idx + 1]}")
        )


    def _redibujar_cuadro(self):
        if hasattr(self, "scene"):
            self.scene.clear()
    

    def _redibujar_cuadro_completo(self):
        if not hasattr(self, "scene"):
            return

        self.scene.clear()

        if self._fase_existe("octavos"):
            self._dibujar_octavos()

        if self._fase_existe("cuartos"):
            self._dibujar_cuartos()

        if self._fase_existe("semifinal"):
            self._dibujar_semifinales()

        if self._fase_existe("final"):
            self._dibujar_final()
            self._dibujar_campeon()


    def _obtener_campeon(self):
        partidos = obtener_partidos_por_fase_con_id("final")

        if not partidos:
            return None

        p = partidos[0]

        if p["gl"] > p["gv"]:
            return p["local"]
        elif p["gv"] > p["gl"]:
            return p["visitante"]
        else:
            return None


    def _dibujar_campeon(self):
        campeon = self._obtener_campeon()
        if not campeon:
            return

        escudo = obtener_escudo_equipo(campeon)
        if escudo:
            pix = QPixmap(escudo).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img = QGraphicsPixmapItem(pix)
            img.setPos(1320, 290)
            self.scene.addItem(img)

        nombre = QGraphicsTextItem(campeon)
        nombre.setScale(1.4)
        nombre.setPos(1360, 290)
        self.scene.addItem(nombre)


    def _dibujar_equipo_con_escudo(self, nombre, x, y):
        escudo = obtener_escudo_equipo(nombre)

        if escudo:
            pixmap = QPixmap(escudo)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img = QGraphicsPixmapItem(pixmap)
                img.setPos(x, y)
                self.scene.addItem(img)
                x += 35  # espacio tras el escudo

        txt = QGraphicsTextItem(nombre)
        txt.setPos(x, y)
        self.scene.addItem(txt)


    def _ajustar_altura_tabla(self, tabla, filas):
        altura_fila = tabla.verticalHeader().defaultSectionSize()
        altura_cabecera = tabla.horizontalHeader().height()

        margen = 4
        altura_total = filas * altura_fila + altura_cabecera + margen

        tabla.setFixedHeight(altura_total)


    def _fase_existe(self, fase):
        return len(obtener_partidos_por_fase_con_id(fase)) > 0
