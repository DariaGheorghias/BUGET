# baza_date.py - tot ce tine de baza de date (SQLite, un singur fisier: buget.db)

import hashlib
import sqlite3

FISIER_BD = "buget.db"

CATEGORII = [
    "Chirie", "Utilitati", "Alimente", "Consumabile casa",
    "Sanatate", "Educatie", "Divertisment", "Dorinte",
]


def conectare():
    return sqlite3.connect(FISIER_BD)


def creeaza_tabele():
    con = conectare()
    con.execute("""CREATE TABLE IF NOT EXISTS utilizatori (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT UNIQUE NOT NULL,
        parola TEXT NOT NULL)""")
    con.execute("""CREATE TABLE IF NOT EXISTS bugete (
        utilizator_id INTEGER, categorie TEXT, tinta REAL,
        PRIMARY KEY (utilizator_id, categorie))""")
    con.execute("""CREATE TABLE IF NOT EXISTS tranzactii (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilizator_id INTEGER, tip TEXT, categorie TEXT, suma REAL)""")
    con.commit()
    con.close()


def cripteaza(parola):
    # nu salvam parola in clar, ci un "hash" (amprenta) al ei
    return hashlib.sha256(parola.encode()).hexdigest()


# ---------------- LOGIN ----------------

def creeaza_cont(nume, parola):
    """Intoarce True daca s-a creat contul, False daca numele e deja luat."""
    con = conectare()
    try:
        con.execute("INSERT INTO utilizatori (nume, parola) VALUES (?, ?)",
                    (nume, cripteaza(parola)))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()


def login(nume, parola):
    """Intoarce id-ul utilizatorului daca datele sunt corecte, altfel None."""
    con = conectare()
    rand = con.execute("SELECT id FROM utilizatori WHERE nume = ? AND parola = ?",
                       (nume, cripteaza(parola))).fetchone()
    con.close()
    return rand[0] if rand else None


# ---------------- BUGETE PE CATEGORII ----------------

def seteaza_tinta(utilizator_id, categorie, suma):
    con = conectare()
    con.execute("INSERT OR REPLACE INTO bugete VALUES (?, ?, ?)",
                (utilizator_id, categorie, suma))
    con.commit()
    con.close()


def adauga_cheltuiala(utilizator_id, categorie, suma):
    con = conectare()
    con.execute("INSERT INTO tranzactii (utilizator_id, tip, categorie, suma) "
                "VALUES (?, 'cheltuiala', ?, ?)", (utilizator_id, categorie, suma))
    con.commit()
    con.close()


def situatie_bugete(utilizator_id):
    """Pentru fiecare categorie intoarce (categorie, tinta, cheltuit, ramas)."""
    con = conectare()
    rezultat = []
    for cat in CATEGORII:
        rand = con.execute("SELECT tinta FROM bugete WHERE utilizator_id = ? AND categorie = ?",
                           (utilizator_id, cat)).fetchone()
        tinta = rand[0] if rand else 0
        cheltuit = con.execute("SELECT COALESCE(SUM(suma), 0) FROM tranzactii "
                               "WHERE utilizator_id = ? AND categorie = ? AND tip = 'cheltuiala'",
                               (utilizator_id, cat)).fetchone()[0]
        rezultat.append((cat, tinta, cheltuit, tinta - cheltuit))
    con.close()
    return rezultat
