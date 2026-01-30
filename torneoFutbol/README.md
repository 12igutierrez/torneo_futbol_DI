
# TORNEO DE FÚTBOL


## Gestión de Torneo de Fútbol

Aplicación de escritorio desarrollada en **Python + PySide6** para la gestión completa de un torneo de fútbol, incluyendo:
- Gestión de equipos y participantes
- Gestión de partidos
- Inicio automático de partidos según fecha y hora programada
- Actualización automática del resultado al finalizar el partido
- Clasificación automática
- Eliminatorias (octavos, cuartos, semifinal y final)
- Visualización gráfica del cuadro de eliminatorias
- Base de datos persistente mediante SQLite



##  Tecnologías utilizadas

- Python 3.10+
- PySide6 (Qt for Python)
- SQLite
- Qt Designer
- QSS (Qt Style Sheets)



## Estructura torneo

TORNEOFUTBOL/
│
├── .venv/
│
├── controllers/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── clasificacion_controller.py
│   ├── equipo_controller.py
│   ├── estadistica_controller.py
│   ├── participante_controller.py
│   └── partido_controller.py
│
├── data/
│   ├── __init__.py
│   └── torneoFutbol_sqlite.db
│
├── docs/
│   ├── __init__.py
│   ├── pyside6+sqlite_tarea3_torneoFutbol.pdf
│   └── Tarea3.pdf
│
├── models/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── database.py
│   ├── equipo.py
│   ├── participante.py
│   └── partido.py
│
├── resources/
│   ├── icons/
│   │   ├── help.png
│   │   └── info.png
│   │
│   ├── img/
│   │   ├── escudo_athletic_bilbao.png
│   │   ├── escudo_atletico_madrid.png
│   │   ├── escudo_barcelona.png
│   │   ├── escudo_betis.png
│   │   ├── escudo_cadiz.png
│   │   ├── escudo_deportivo_la_coruña.png
│   │   ├── escudo_getafe.png
│   │   ├── escudo_granada.png
│   │   ├── escudo_guadalajara.png
│   │   ├── escudo_malaga.png
│   │   ├── escudo_osasuna.png
│   │   ├── escudo_oviedo.png
│   │   ├── escudo_real_madrid.png
│   │   ├── escudo_sevilla.png
│   │   ├── escudo_talavera.png
│   │   └── escudo_villarreal.png
│   │
│   └── qss/
│       ├── __init__.py
│       └── style.qss
│
├── views/
│   ├── __pycache__/
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── asignar_equipo_dialog.ui
│   │   ├── editar_equipo_dialog.ui
│   │   ├── eliminatorias_dialog.ui
│   │   ├── estadistica_dialog.ui
│   │   ├── mainwindow.ui
│   │   ├── match_window.ui
│   │   ├── participante_dialog.ui
│   │   ├── partido_dialog.ui
│   │   └── resultado_dialog.ui
│   │
│   ├── __init__.py
│   ├── asignar_equipo_dialog.py
│   ├── ayuda_dialog.py
│   ├── creditos_dialog.py
│   ├── editar_equipo_dialog.py
│   ├── eliminatorias_dialog.py
│   ├── estadistica_dialog.py
│   ├── mainwindow.py
│   ├── participante_dialog.py
│   ├── participante_editar_dialog.py
│   ├── partido_dialog.py
│   ├── partido_editar_dialog.py
│   ├── partido_en_vivio_dialog.py
│   └── resultado_dialog.py
│
├── main.py
├── README.md
├── requirements.txt
└── setup_db.py



## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
