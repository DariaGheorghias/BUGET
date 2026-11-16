# BUGET

Aplicație simplă în Python + Qt (PySide6): **login** și **buget pe categorii**.

## Ce face
1. **Login** – creezi cont (nume + parolă) și te autentifici. Parola se salvează criptată (hash SHA-256).
2. **Bugete pe categorii** – 8 categorii: Chirie, Utilități, Alimente, Consumabile casă, Sănătate, Educație, Divertisment, Dorințe.
   - alegi categoria + suma → **Setează ținta** (limita pe categorie);
   - alegi categoria + suma → **Adaugă cheltuială**;
   - tabelul arată pentru fiecare categorie: **Țintă / Cheltuit / Rămas** (roșu dacă s-a depășit).

## Fișiere
| Fișier | Ce conține |
|---|---|
| `main.py` | pornește aplicația |
| `baza_date.py` | baza de date SQLite (`buget.db`): tabelele `utilizatori`, `bugete`, `tranzactii` + funcțiile de login și bugete |
| `interfata.py` | cele 2 ferestre Qt: `FereastraLogin` și `FereastraBuget` |

## Instalare și pornire (terminal în VS Code, în folderul proiectului)
```
python -m venv .venv
.venv\Scripts\python -m pip install PySide6-Essentials
.venv\Scripts\python main.py
```
Fișierul `buget.db` se creează singur la prima pornire.
