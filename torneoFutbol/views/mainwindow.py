from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QFileDialog, QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtSql import QSqlQuery
from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap
from views.eliminatorias_dialog import EliminatoriasDialog
from views.partido_editar_dialog import EditarPartidoDialog
from views.ayuda_dialog import AyudaDialog
from views.creditos_dialog import CreditosDialog
from PySide6.QtCore import QTimer
from datetime import datetime
from controllers.partido_controller import (
    borrar_eliminatorias,
    generar_octavos,
    obtener_partidos,
    eliminar_partido
)
from controllers.equipo_controller import (
    insertar_equipo,
    obtener_equipos_tabla,
    eliminar_equipo,
    equipo_tiene_dependencias,
    actualizar_escudo
)
from controllers.participante_controller import (
    obtener_participantes,
    eliminar_participante
)
from controllers.clasificacion_controller import obtener_clasificacion
from views.participante_dialog import ParticipanteDialog
from views.participante_editar_dialog import EditarParticipanteDialog
from views.asignar_equipo_dialog import AsignarEquipoDialog
from views.partido_dialog import PartidoDialog
from views.estadistica_dialog import EstadisticaDialog
from views.editar_equipo_dialog import EditarEquipoDialog
from views.partido_en_vivo_dialog import PartidoEnVivoDialog
from utils.path_utils import resource_path



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_path = Path(__file__).parent / "ui" / "mainwindow.ui"
        self.ui = loader.load(str(ui_path))
        self.setLayout(self.ui.layout())

        # ================= ICONOS =================
        icon_help = resource_path("resources/icons/help.png")
        icon_info = resource_path("resources/icons/info.png")
        self.ui.btn_ayuda.setIcon(QIcon(str(icon_help)))
        self.ui.btn_creditos.setIcon(QIcon(str(icon_info)))

        # CONFIGURACIÓN DE TABLAS
        self._configurar_tablas()
        self.ui.table_clasificacion.setSelectionMode(QAbstractItemView.NoSelection)

        # CONEXIONES EQUIPOS
        self.ui.btn_add.clicked.connect(self.crear_equipo)
        self.ui.btn_edit_equipo.clicked.connect(self.editar_equipo)
        self.ui.btn_delete_equipo.clicked.connect(self.eliminar_equipo)
        self.ui.btn_escudo.clicked.connect(self.asignar_escudo)

        # CONEXIONES PARTICIPANTES
        self.ui.btn_add_participante.clicked.connect(self.crear_participante)
        self.ui.btn_edit_participante.clicked.connect(self.editar_participante)
        self.ui.btn_delete_participante.clicked.connect(self.eliminar_participante)
        self.ui.btn_asignar_equipo.clicked.connect(self.asignar_equipo)

        # CONEXIONES PARTIDOS
        self.ui.btn_crear_partido.clicked.connect(self.crear_partido)
        self.ui.btn_estadistica.clicked.connect(self.estadisticas_jugadores)
        self.ui.btn_edit_partido.clicked.connect(self.editar_partido)
        self.ui.btn_delete_partido.clicked.connect(self.eliminar_partido)
        self.ui.btn_generar_eliminatorias.clicked.connect(self.generar_eliminatorias)
        self.ui.btn_generar_eliminatorias.clicked.connect(self.mostrar_eliminatorias)

        self.ui.btn_ayuda.clicked.connect(self.mostrar_ayuda)
        self.ui.btn_creditos.clicked.connect(self.mostrar_creditos)

        # CARGA INICIAL
        self.cargar_equipos()
        self.cargar_participantes()
        self.cargar_partidos()
        self.cargar_clasificacion()

        # ================= CONTROL DE PARTIDOS EN VIVO =================
        self._partido_en_curso = False
        self._partido_notificado = None

        self._timer_partidos = QTimer(self)
        self._timer_partidos.timeout.connect(self._comprobar_inicio_partido)
        self._timer_partidos.start(1000)

        qss_path = resource_path("resources/qss/style.qss")
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    # ================= EQUIPOS =================
    def crear_equipo(self):
        nombre = self.ui.txt_nombre.text().strip()
        curso = self.ui.txt_curso.text().strip()
        color = self.ui.txt_color.text().strip()

        if not nombre:
            QMessageBox.warning(self, "Error", "Introduce el nombre del equipo")
            return

        insertar_equipo(nombre, curso, color)
        self.cargar_equipos()
        self.cargar_clasificacion()

        self.ui.txt_nombre.clear()
        self.ui.txt_curso.clear()
        self.ui.txt_color.clear()


    def editar_equipo(self):
        fila = self.ui.table_equipos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un equipo")
            return

        equipo_id, nombre, curso, color, _ = obtener_equipos_tabla()[fila]
        dialog = EditarEquipoDialog(equipo_id, nombre, curso, color)

        if dialog.exec():
            self.cargar_equipos()
            self.cargar_clasificacion()


    def eliminar_equipo(self):
        fila = self.ui.table_equipos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un equipo")
            return

        equipo_id = obtener_equipos_tabla()[fila][0]

        if equipo_tiene_dependencias(equipo_id):
            QMessageBox.warning(
                self,
                "No permitido",
                "El equipo tiene participantes o partidos"
            )
            return

        eliminar_equipo(equipo_id)
        self.cargar_equipos()
        self.cargar_clasificacion()


    def cargar_equipos(self):
        equipos = obtener_equipos_tabla()
        self.ui.table_equipos.setRowCount(len(equipos))
        self.ui.table_equipos.setColumnCount(4)

        self.ui.table_equipos.setHorizontalHeaderLabels([
            "Nombre del equipo",
            "Curso",
            "Color camiseta",
            "Escudo"
        ])

        for fila, (_, nombre, curso, color, escudo) in enumerate(equipos):
            self.ui.table_equipos.setItem(fila, 0, QTableWidgetItem(nombre))
            self.ui.table_equipos.setItem(fila, 1, QTableWidgetItem(curso))
            self.ui.table_equipos.setItem(fila, 2, QTableWidgetItem(color))

            item_escudo = QTableWidgetItem()
            if escudo:
                icono = QIcon(QPixmap(escudo).scaled(32, 32))
                item_escudo.setIcon(icono)

            self.ui.table_equipos.setItem(fila, 3, item_escudo)


    def asignar_escudo(self):
        fila = self.ui.table_equipos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un equipo")
            return

        equipo_id = obtener_equipos_tabla()[fila][0]

        ruta, _ = QFileDialog.getOpenFileName(self,
            "Seleccionar escudo del equipo","","Imágenes (*.png *.jpg *.jpeg)"
        )

        if not ruta:
            return

        actualizar_escudo(equipo_id, ruta)
        self.cargar_equipos()



    # ================= PARTICIPANTES =================
    def crear_participante(self):
        dialog = ParticipanteDialog()
        if dialog.exec():
            self.cargar_participantes()


    def editar_participante(self):
        fila = self.ui.table_participantes.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un participante")
            return

        participante_id = obtener_participantes()[fila][0]
        dialog = EditarParticipanteDialog(participante_id)

        if dialog.exec():
            self.cargar_participantes()


    def eliminar_participante(self):
        fila = self.ui.table_participantes.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un participante")
            return

        participante_id = obtener_participantes()[fila][0]

        if QMessageBox.question(self,"Confirmar","¿Eliminar participante?") != QMessageBox.Yes:
            return

        eliminar_participante(participante_id)
        self.cargar_participantes()


    def asignar_equipo(self):
        dialog = AsignarEquipoDialog()
        if dialog.exec():
            self.cargar_participantes()


    def cargar_participantes(self):
        participantes = obtener_participantes()
        self.ui.table_participantes.setRowCount(len(participantes))

        self.ui.table_participantes.setHorizontalHeaderLabels([
            "Nombre",
            "Fecha nacimiento",
            "Curso",
            "Tipo",
            "Posición",
            "Equipo"
        ])

        for fila, (_, nombre, fecha, curso, tipo, posicion, equipo) in enumerate(participantes):
            self.ui.table_participantes.setItem(fila, 0, QTableWidgetItem(nombre))
            self.ui.table_participantes.setItem(fila, 1, QTableWidgetItem(fecha))
            self.ui.table_participantes.setItem(fila, 2, QTableWidgetItem(curso))
            self.ui.table_participantes.setItem(fila, 3, QTableWidgetItem(tipo))
            self.ui.table_participantes.setItem(fila, 4, QTableWidgetItem(posicion))
            self.ui.table_participantes.setItem(fila, 5, QTableWidgetItem(equipo))



    # ================= PARTIDOS =================
    def crear_partido(self):
        dialog = PartidoDialog()
        if dialog.exec():
            self.cargar_partidos()
            self.cargar_clasificacion()


    def estadisticas_jugadores(self):
        fila = self.ui.table_partidos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un partido")
            return

        partido_id = self.ui.table_partidos.item(fila, 0).data(32)
        EstadisticaDialog(partido_id).exec()


    def cargar_partidos(self):
        partidos = obtener_partidos()
        self.ui.table_partidos.setRowCount(len(partidos))

        self.ui.table_partidos.setHorizontalHeaderLabels([
            "Equipo local",
            "Equipo visitante",
            "Fecha",
            "Árbitro",
            "Goles local",
            "Goles visitante"
        ])

        for fila, partido in enumerate(partidos):
            for col, valor in enumerate(partido["tabla"]):
                item = QTableWidgetItem(str(valor))
                if col == 0:
                    item.setData(32, partido["id"])
                self.ui.table_partidos.setItem(fila, col, item)


    def editar_partido(self):
        fila = self.ui.table_partidos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un partido")
            return

        partido_id = self.ui.table_partidos.item(fila, 0).data(32)
        dialog = EditarPartidoDialog(partido_id)

        if dialog.exec():
            self.cargar_partidos()
            self.cargar_clasificacion()


    def eliminar_partido(self):
        fila = self.ui.table_partidos.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Error", "Selecciona un partido")
            return

        partido_id = self.ui.table_partidos.item(fila, 0).data(32)

        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Seguro que quieres eliminar este partido?\n"
            "Se eliminará aunque tenga resultado.",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta != QMessageBox.Yes:
            return

        if not eliminar_partido(partido_id):
            QMessageBox.critical(self, "Error", "No se pudo eliminar el partido")
            return

        self.cargar_partidos()
        self.cargar_clasificacion()



    # ================= CLASIFICACIÓN =================
    def cargar_clasificacion(self):
        clasificacion = obtener_clasificacion()
        self.ui.table_clasificacion.setRowCount(len(clasificacion))

        self.ui.table_clasificacion.setHorizontalHeaderLabels([
            "Equipo",
            "PJ",
            "PG",
            "PE",
            "PP",
            "GF",
            "GC",
            "DG",
            "Puntos"
        ])

        for fila, fila_clasif in enumerate(clasificacion):
            for col, valor in enumerate(fila_clasif):
                self.ui.table_clasificacion.setItem(
                    fila, col, QTableWidgetItem(str(valor))
                )
    

    def generar_eliminatorias(self):
        clasificacion = obtener_clasificacion()

        if len(clasificacion) < 16:
            QMessageBox.warning(
                self,
                "No se puede generar",
                "Se necesitan al menos 16 equipos"
            )
            return

        if QMessageBox.question(
            self,
            "Confirmar",
            "Esto borrará las eliminatorias existentes.\n¿Continuar?"
        ) != QMessageBox.Yes:
            return

        borrar_eliminatorias()
        generar_octavos(clasificacion)

        self.cargar_partidos()

        QMessageBox.information(
            self,
            "Correcto",
            "Eliminatorias generadas a partir de la clasificación"
        )


    def mostrar_eliminatorias(self):
        dialog = EliminatoriasDialog()
        dialog.exec()


    def mostrar_ayuda(self):
        AyudaDialog().exec()


    def mostrar_creditos(self):
        CreditosDialog().exec()


    def _configurar_tablas(self):
        tablas = [
            self.ui.table_equipos,
            self.ui.table_participantes,
            self.ui.table_partidos,
            self.ui.table_clasificacion
        ]

        for tabla in tablas:
            tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
            tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
            tabla.setSelectionMode(QAbstractItemView.SingleSelection)

  
    def _comprobar_inicio_partido(self):
        if self._partido_en_curso:
            return

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M")

        for fila in range(self.ui.table_partidos.rowCount()):
            fecha = self.ui.table_partidos.item(fila, 2).text()
            partido_id = self.ui.table_partidos.item(fila, 0).data(32)

            if self._partido_notificado == partido_id:
                 continue

            if fecha == ahora:
                equipo_local = self.ui.table_partidos.item(fila, 0).text()
                equipo_visitante = self.ui.table_partidos.item(fila, 1).text()

                QMessageBox.information(
                    self,
                    "Empieza el partido",
                    f"Empieza el partido:\n\n{equipo_local} vs {equipo_visitante}"
                )

                self._partido_notificado = partido_id
                self._partido_en_curso = True
                self._jugar_partido(partido_id, equipo_local, equipo_visitante)
                break
            
    
    def _jugar_partido(self, partido_id, equipo_local, equipo_visitante):
        dialog = PartidoEnVivoDialog(equipo_local, equipo_visitante, self)
        dialog.exec()

        goles_local, goles_visitante = dialog.resultado

        self._guardar_resultado_partido(
            partido_id,
            goles_local,
            goles_visitante
        )

        self._partido_en_curso = False

    
    def _guardar_resultado_partido(self, partido_id, gl, gv):
        query = QSqlQuery()
        query.prepare("""
            UPDATE partido
            SET goles_local = ?, goles_visitante = ?
            WHERE id = ?
        """)
        query.addBindValue(gl)
        query.addBindValue(gv)
        query.addBindValue(partido_id)
        query.exec()

        self.cargar_partidos()
        self.cargar_clasificacion()
