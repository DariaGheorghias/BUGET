# interfata.py - ferestrele aplicatiei (Qt / PySide6)

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QComboBox, QDoubleSpinBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                               QMessageBox, QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget)

import baza_date


class FereastraLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buget - Login")

        self.camp_nume = QLineEdit()
        self.camp_nume.setPlaceholderText("Nume utilizator")
        self.camp_parola = QLineEdit()
        self.camp_parola.setPlaceholderText("Parola")
        self.camp_parola.setEchoMode(QLineEdit.Password)   # afiseaza ****

        buton_login = QPushButton("Login")
        buton_cont = QPushButton("Cont nou")
        buton_login.clicked.connect(self.login)
        buton_cont.clicked.connect(self.cont_nou)

        layout = QVBoxLayout(self)
        layout.addWidget(self.camp_nume)
        layout.addWidget(self.camp_parola)
        layout.addWidget(buton_login)
        layout.addWidget(buton_cont)

    def cont_nou(self):
        nume, parola = self.camp_nume.text().strip(), self.camp_parola.text()
        if not nume or not parola:
            QMessageBox.warning(self, "Eroare", "Completeaza numele si parola.")
        elif baza_date.creeaza_cont(nume, parola):
            QMessageBox.information(self, "OK", "Cont creat. Acum apasa Login.")
        else:
            QMessageBox.warning(self, "Eroare", "Numele exista deja.")

    def login(self):
        uid = baza_date.login(self.camp_nume.text().strip(), self.camp_parola.text())
        if uid is None:
            QMessageBox.warning(self, "Eroare", "Nume sau parola gresita.")
            return
        self.fereastra_buget = FereastraBuget(uid, self.camp_nume.text().strip())
        self.fereastra_buget.show()
        self.close()


class FereastraBuget(QWidget):
    def __init__(self, utilizator_id, nume):
        super().__init__()
        self.uid = utilizator_id
        self.setWindowTitle(f"Buget - {nume}")
        self.resize(550, 420)

        # tabelul cu cele 8 categorii
        self.tabel = QTableWidget(len(baza_date.CATEGORII), 4)
        self.tabel.setHorizontalHeaderLabels(["Categorie", "Tinta", "Cheltuit", "Ramas"])
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # coloane late

        # randul de jos: categorie + suma + 2 butoane
        self.alege_categorie = QComboBox()
        self.alege_categorie.addItems(baza_date.CATEGORII)
        self.suma = QDoubleSpinBox()
        self.suma.setMaximum(1_000_000)
        buton_tinta = QPushButton("Seteaza tinta")
        buton_cheltuiala = QPushButton("Adauga cheltuiala")
        buton_tinta.clicked.connect(self.seteaza_tinta)
        buton_cheltuiala.clicked.connect(self.adauga_cheltuiala)

        jos = QHBoxLayout()
        for w in (self.alege_categorie, self.suma, buton_tinta, buton_cheltuiala):
            jos.addWidget(w)

        self.total = QLabel()
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabel)
        layout.addWidget(self.total)
        layout.addLayout(jos)

        self.actualizeaza()

    def seteaza_tinta(self):
        baza_date.seteaza_tinta(self.uid, self.alege_categorie.currentText(), self.suma.value())
        self.actualizeaza()

    def adauga_cheltuiala(self):
        if self.suma.value() <= 0:
            QMessageBox.warning(self, "Eroare", "Suma trebuie sa fie mai mare ca 0.")
            return
        baza_date.adauga_cheltuiala(self.uid, self.alege_categorie.currentText(), self.suma.value())
        self.actualizeaza()

    def actualizeaza(self):
        """Reciteste datele din baza de date si le pune in tabel."""
        situatie = baza_date.situatie_bugete(self.uid)
        for rand, (cat, tinta, cheltuit, ramas) in enumerate(situatie):
            valori = [cat, f"{tinta:.2f}", f"{cheltuit:.2f}", f"{ramas:.2f}"]
            for coloana, text in enumerate(valori):
                self.tabel.setItem(rand, coloana, QTableWidgetItem(text))
            if ramas < 0:   # buget depasit -> rosu
                self.tabel.item(rand, 3).setForeground(QColor("red"))
        total_tinta = sum(r[1] for r in situatie)
        total_cheltuit = sum(r[2] for r in situatie)
        self.total.setText(f"Total tinta: {total_tinta:.2f} lei   |   "
                           f"Total cheltuit: {total_cheltuit:.2f} lei")
