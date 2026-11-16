# main.py - porneste aplicatia

import sys

from PySide6.QtWidgets import QApplication

import baza_date
from interfata import FereastraLogin

baza_date.creeaza_tabele()          # creeaza buget.db daca nu exista

app = QApplication(sys.argv)
fereastra = FereastraLogin()
fereastra.show()
sys.exit(app.exec())
