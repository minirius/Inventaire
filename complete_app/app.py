import sqlite3
from os.path import exists
import os
from pathlib import Path

from appPage import App

def ensureDatabase():
    """
    EnsureData est une fonctione qui crée la base de donnée et la table dans le 
    répertoire res/database.db s'ils n'existe pas

    Arg: No
    Return : No
    """

    # Création du dossier /res s'il n'existe pas
    Path(os.getcwd()+"/res").mkdir(parents=True, exist_ok=True)

    # Création du fichier database.db s'il n'existe pas
    if(not exists("res/database.db")):
        f = open("res/database.db", "x")
        f.close()

    # Création de la connection a la base de données en variable GLOBALE (tout le long du programme)
    CON = sqlite3.connect("res/database.db")
    CUR = CON.cursor()

    # Recherche de la table matable, qui stockera les données
    CUR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matable';")
    rows = CUR.fetchall()
    if(len(rows) == 0):
        # Création de la table si inexistante
        CUR.execute("CREATE TABLE matable(id INTEGER PRIMARY KEY NOT NULL, name MEDIUMTEXT, amount INTEGER, price INTEGER, category MEDIUMTEXT);")
    CON.close()

if __name__ == "__main__":
    os.chdir('complete_app/')
    ensureDatabase()
    app = App()
    app.update_tableau()
    app.mainloop()