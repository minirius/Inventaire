import customtkinter
from customtkinter import filedialog as fd
from tkinter.messagebox import askokcancel, showerror
import sqlite3
import json
from os.path import exists
import os
from pathlib import Path
import cv2 
import qrcode
from playsound import playsound
from tkinter.ttk import Combobox
from tkinter import Label
from tkinter import Listbox, END, StringVar, IntVar
from functools import reduce
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno

import pickle

def checkJsonFormat(jsonFile):
    """
    checkJsonFormat est une fonctione qui permet de valider la conformité d'un fichier JSON
    il parcour la list de listes pour vérifier si les enfants sont corrects et vérifier les
    types associés

    Arg: jsonFile (2d Array)
    Return : Bool : if the Json is valid
    """
    for i, row in enumerate(jsonFile):
        if (len(row) == 7 and 
            "id" in row and 
            "name" in row and 
            "amount" in row and 
            "price" in row and 
            "category" in row and 
            "masse" in row and 
            "dimensions" in row
        ):
            if not (type(row["id"]) == int and 
                    type(row["name"]) == str and 
                    type(row["amount"]) == int and 
                    type(row["price"]) == int and 
                    type(row["category"]) == str and 
                    type(row["masse"]) == int and 
                    type(row["dimensions"]) == str
                ):
                return False
        else:
            return False
    return True

def ensureDatabase():
    """
    EnsureData est une fonctione qui crée la base de donnée et la table dans le 
    répertoire res/database.db s'ils n'existe pas

    Arg: No
    Return : No
    """
    global CON, CUR

    # Création du dossier /res s'il n'existe pas
    Path(os.getcwd()+"/ressources").mkdir(parents=True, exist_ok=True)

    # Création du fichier database.db s'il n'existe pas
    if(not exists("ressources/database.db")):
        f = open("ressources/database.db", "x")
        f.close()

    # Création de la connection a la base de données en variable GLOBALE (tout le long du programme)
    CON = sqlite3.connect("ressources/database.db")
    CUR = CON.cursor()

    # Recherche de la table matable, qui stockera les données
    CUR.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='matable';")
    rows = CUR.fetchall()

    if(len(rows) == 0):
        # Création de la table si inexistante
        CUR.execute("CREATE TABLE matable(id INTEGER PRIMARY KEY NOT NULL, name MEDIUMTEXT, amount INTEGER, price INTEGER, category MEDIUMTEXT, masse INTEGER, dimensions MEDIUMTEXT);")

def getInfo():
    """
    getInfo est une fonction qui calcul la sommes des prix de tous les éléments dans la base de donnée json

    Arg: fichierjson
    Return : Tuple contenant la somme des prix de tous les éléments et le nombre total d'articles.
    """
    CUR.execute('SELECT * FROM matable')
    rows = CUR.fetchall()
    prixtotal=0

    for article in rows:
            prixtotal += article[3]*article[2]

    return prixtotal, len(rows)

class AddWindow(customtkinter.CTkToplevel):
    """
    AddWindow est la sous-fenetre graphique qui permet d'ajouter des items dans la base de données

    Entrée Utillisateurs:
        - Nom (string)
        - Prix (int)
        - Quantité (int)
        - Catégorie (string) 
    """
    def __init__(self, parent_self):
        super().__init__()

        # Création de la fenêtre de base non-resisable et du titre
        self.geometry("500x400")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.title("Ajouter")

        # Input texte pour le Nom ainsi que sa StringVar
        self.name_string = customtkinter.StringVar()
        self.name_label = customtkinter.CTkLabel(self, text="Nom", fg_color="transparent")
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : Banane", textvariable=self.name_string)
        self.name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # Input texte pour le Prix ainsi que sa StringVar
        self.price_string = customtkinter.StringVar()
        self.price_label = customtkinter.CTkLabel(self, text="Prix en €", fg_color="transparent")
        self.price_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : 2", textvariable=self.price_string)
        self.price_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.price_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        # Input texte pour la Quantité ainsi que sa StringVar
        self.amount_string = customtkinter.StringVar()
        self.amount_label = customtkinter.CTkLabel(self, text="Quantité", fg_color="transparent")
        self.amount_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : 500", textvariable=self.amount_string)
        self.amount_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.amount_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        # Input texte pour la Catégorie ainsi que sa StringVar
        self.category_string = customtkinter.StringVar()
        self.category_label = customtkinter.CTkLabel(self, text="Catégorie", fg_color="transparent")
        self.category_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : Fruits et Légumes", textvariable=self.category_string)
        self.category_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.category_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

        # Input texte pour la Masse ainsi que sa StringVar
        self.masse_string = customtkinter.StringVar()
        self.masse_label = customtkinter.CTkLabel(self, text="Masse", fg_color="transparent")
        self.masse_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : 1.2", textvariable=self.masse_string)
        self.masse_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.masse_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=10)

        # Input texte pour la Masse ainsi que sa StringVar
        self.dimensions_string = customtkinter.StringVar()
        self.dimensions_label = customtkinter.CTkLabel(self, text="Dimensions", fg_color="transparent")
        self.dimensions_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : 150x45x30", textvariable=self.dimensions_string)
        self.dimensions_label.grid(row=5, column=0, sticky="w", padx=10, pady=10)
        self.dimensions_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=10)

        # Bouton enregister qui appelle la fonction locale save()
        self.save_button = customtkinter.CTkButton(self, text="Ajouter", command=self.save)
        self.save_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=20, padx=10)

        # Configuration de la taille des lignes et des colonnes
        self.grid_columnconfigure(0, minsize=150)
        self.grid_columnconfigure(1, minsize=350)
        self.grid_rowconfigure([0, 1, 2, 3, 4, 5], minsize=50)

    def save(self):
        """
        Enregistre les valeurs des champs d'entrée dans la base de données.
        """
        # Requête SQL pour ajouter les valeur des inputs (via les StringVar) dans notre table matable
        if(
            self.amount_string.get().isnumeric() and 
           self.price_string.get().isnumeric() and 
           self.masse_string.get().isnumeric()
        ):
            CON.executemany(
                "INSERT INTO matable (name, amount, price, category, masse, dimensions) VALUES(?, ?, ?, ?, ?, ?)",
                [
                    (
                        self.name_string.get(), 
                        self.amount_string.get(), 
                        self.price_string.get(), 
                        self.category_string.get(), 
                        self.masse_string.get(), 
                        self.dimensions_string.get()
                    )
                ]
            )
            CON.commit()
            # Actualisation du tableau de la Fenêter Parent
            app.update_tableau()
            # Destrucion de la sous-fenêtre
            self.destroy()
        else:
            showerror("Type Erreur", "Veuillez rentrer des valeurs chiffrées pour : Prix, Quantité et Masse")

class JsonWindow(customtkinter.CTkToplevel):
    """
    JsonWindow est la sous-fenetre graphique qui permet d'importer de remplacer
    les items actuels par les items présent dans le JSON dans la base de données

    Entrée Utillisateurs:
        - Fichier JSON (file) 
    """
    def __init__(self, parent_self, file):
        super().__init__()

        # Création de la fenêtre de base non-resisable et du titre
        self.geometry("700x500")
        self.minsize(700, 300)
        self.maxsize(700, 300)
        self.title("Importer")

        # Definition d'une police gras
        self.bold = customtkinter.CTkFont(weight="bold")
        # Ajout du fichier JSON dans les variables self
        self.jsonFile = file

        # Bouton pour confirmer le remplacement de la base de données
        self.replace_button = customtkinter.CTkButton(self, text="Remplacer l'Inventaire", command=lambda: self.save(self.jsonFile))
        self.replace_button.pack(fill=customtkinter.X, side=customtkinter.BOTTOM, pady=5)

        # Vue des items du fichier (Widget Parent)
        self.list_view = customtkinter.CTkScrollableFrame(self, height=400, fg_color="transparent")
        self.list_view.pack(fill=customtkinter.BOTH)

        self.liste = []

        # Titre des colonnes du tableau d'affichage
        self.title_name = customtkinter.CTkLabel(self.list_view, text="ID", fg_color="transparent", font=self.bold)
        self.title_name.grid(row=0, column=0, sticky="w", padx=10)
        self.title_name = customtkinter.CTkLabel(self.list_view, text="Nom", fg_color="transparent", font=self.bold)
        self.title_name.grid(row=0, column=1, sticky="w", padx=10)
        self.title_price = customtkinter.CTkLabel(self.list_view, text="Quantité", fg_color="transparent", font=self.bold)
        self.title_price.grid(row=0, column=2, sticky="w")
        self.title_amount = customtkinter.CTkLabel(self.list_view, text="Prix", fg_color="transparent", font=self.bold)
        self.title_amount.grid(row=0, column=3, sticky="w")
        self.title_amount = customtkinter.CTkLabel(self.list_view, text="Catégorie", fg_color="transparent", font=self.bold)
        self.title_amount.grid(row=0, column=4, sticky="w")
        self.title_masse = customtkinter.CTkLabel(self.list_view, text="Masse", fg_color="transparent", font=self.bold)
        self.title_masse.grid(row=0, column=5, sticky="w")
        self.title_dimensions = customtkinter.CTkLabel(self.list_view, text="Dimensions", fg_color="transparent", font=self.bold)
        self.title_dimensions.grid(row=0, column=6, sticky="w")

        # Boucle itérant les items du fichier json
        for i, row in enumerate(self.jsonFile):
            # Ajout de chaque elements de la liste dans le tableau
            tempListe = []

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row["id"], fg_color="transparent"))
            tempListe[0].grid(row=i+1, column=0, sticky="w", padx=10)

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row["name"], fg_color="transparent"))
            tempListe[1].grid(row=i+1, column=1, sticky="w", padx=10)

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row["amount"], fg_color="transparent"))
            tempListe[2].grid(row=i+1, column=2, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row["price"], fg_color="transparent"))
            tempListe[3].grid(row=i+1, column=3, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row["category"], fg_color="transparent"))
            tempListe[4].grid(row=i+1, column=4, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row["masse"], fg_color="transparent"))
            tempListe[5].grid(row=i+1, column=5, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row["dimensions"], fg_color="transparent"))
            tempListe[6].grid(row=i+1, column=6, sticky="w")

            self.liste.append(tempListe)
        
        # Configuration des tailles des colonnes et des lignes dans le tableau
        self.list_view.grid_columnconfigure(0, minsize=50)
        self.list_view.grid_columnconfigure(1, minsize=150)
        self.list_view.grid_columnconfigure(2, minsize=100)
        self.list_view.grid_columnconfigure(3, minsize=100)
        self.list_view.grid_columnconfigure(4, minsize=100)
        self.list_view.grid_columnconfigure(5, minsize=100)
        self.list_view.grid_columnconfigure(6, minsize=100)


    def save(self, jsonData):
        """
        La fonction save permet de stocker des items dans la base de données en excluant l'ID
        car celui-ci d'autoincrémente tout seul

        Args :
            - jsonData (2D list)
        """
        # Suppression de la table actuelles
        CON.execute("DELETE FROM matable;")
        # Ajout de tout les items via la fonction executemany
        CON.executemany(
            "INSERT INTO matable (name, amount, price, category, masse, dimensions) VALUES(?, ?, ?, ?, ?, ?)",
            [(row["name"], 
              row["amount"], 
              row["price"], 
              row["category"], 
              row["masse"], 
              row["dimensions"]) for row in jsonData]
        )
        CON.commit()
        # Actualisation du tableau de la fenêtre Parent
        app.update_tableau()
        # Destruction de la sous-fenêtre
        self.destroy()

class EditWindow(customtkinter.CTkToplevel):
    def __init__(self, parent_self, id):
        super().__init__()
        
        # Ajout de la Variable ID dans les variables self
        self.id = id

        # Création de la fenêtre de base non-resisable et du titre
        self.geometry("500x500")
        self.minsize(500, 500)
        self.maxsize(500, 500)
        self.title("Modifier")

        # Requêtre SQL pour prendre l'element unique correspondant à l'ID donné
        CUR.execute('SELECT * FROM matable WHERE id=?', (self.id, ))
        # Ajout de ce dictionnaire dans les variables self
        self.row = CUR.fetchall()[0]

        # Input text de la variable Nom
        self.name_string = customtkinter.StringVar()
        self.name_string.set(self.row[1])
        self.name_label = customtkinter.CTkLabel(self, text="Nom", fg_color="transparent")
        self.name_entry = customtkinter.CTkEntry(self, placeholder_text=self.row[1], textvariable=self.name_string)
        self.name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # Input text de la variable Prix
        self.price_string = customtkinter.StringVar()
        self.price_string.set(self.row[3])
        self.price_label = customtkinter.CTkLabel(self, text="Prix", fg_color="transparent")
        self.price_entry = customtkinter.CTkEntry(self, placeholder_text=self.row[3], textvariable=self.price_string)
        self.price_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.price_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        # Input text de la variable Quantité
        self.amount_string = customtkinter.StringVar()
        self.amount_string.set(self.row[2])
        self.amount_label = customtkinter.CTkLabel(self, text="Quantité", fg_color="transparent")
        self.amount_entry = customtkinter.CTkEntry(self, placeholder_text=self.row[2], textvariable=self.amount_string)
        self.amount_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.amount_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

        # Input text de la variable Catégorie
        self.category_string = customtkinter.StringVar()
        self.category_string.set(self.row[4])
        self.category_label = customtkinter.CTkLabel(self, text="Catégorie", fg_color="transparent")
        self.category_entry = customtkinter.CTkEntry(self, placeholder_text=self.row[4], textvariable=self.category_string)
        self.category_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.category_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=10)

        # Input texte pour la Masse ainsi que sa StringVar
        self.masse_string = customtkinter.StringVar()
        self.masse_string.set(self.row[5])
        self.masse_label = customtkinter.CTkLabel(self, text="Masse", fg_color="transparent")
        self.masse_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : 1.2", textvariable=self.masse_string)
        self.masse_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.masse_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=10)

        # Input texte pour la Masse ainsi que sa StringVar
        self.dimensions_string = customtkinter.StringVar()
        self.dimensions_string.set(self.row[6])
        self.dimensions_label = customtkinter.CTkLabel(self, text="Dimensions", fg_color="transparent")
        self.dimensions_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : 150x45x30", textvariable=self.dimensions_string)
        self.dimensions_label.grid(row=5, column=0, sticky="w", padx=10, pady=10)
        self.dimensions_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=10)

        # Bouton enregistrer lié à la fonction save()
        self.save_button = customtkinter.CTkButton(self, text="Enregistrer", command=self.save)
        self.save_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

        # Bouton QRCode lié à la fonction qrcode()
        self.qrcode_button = customtkinter.CTkButton(self, text="QRCode", command=self.qrcode)
        self.qrcode_button.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

        # Bouton supprimer lié à la fonction delete()
        self.delete_button = customtkinter.CTkButton(self, text="Supprimer", command=self.delete, fg_color="#dc143c", hover_color="#b22222")
        self.delete_button.grid(row=8, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

        #Configuration des tailles du tableau (colonnes et lignes)
        self.grid_columnconfigure(0, minsize=150)
        self.grid_columnconfigure(1, minsize=350)
        self.grid_rowconfigure([0, 1, 2, 3, 4, 5], minsize=50)

    def save(self):
        if(
            self.amount_string.get().isdigit() and 
           self.price_string.get().isdigit() and 
           self.masse_string.get().isdigit()
        ):
            # Fonction Save, update dans la base de données à l'aide des stringVar
            CON.execute(
                'UPDATE matable set name=?, amount=?, price=?, category=?, masse=?, dimensions=? WHERE id=?',
                (
                    self.name_string.get(), 
                    self.amount_string.get(), 
                    self.price_string.get(), 
                    self.category_string.get(), 
                    self.id,
                    self.masse_string.get(), 
                    self.dimensions_string.get(),
                )
            )
            CON.commit()

            app.update_tableau()
            self.destroy()
        else:
            showerror("Type Erreur", "Veuillez rentrer des valeurs chiffrées pour : Prix et Quantité")

    def delete(self):
        # Supprime l'items de la base de données
        CON.execute('DELETE FROM matable WHERE id=?', (self.id, ))
        CON.commit()

        app.update_tableau()
        self.destroy()
    
    def qrcode(self):
        # Crée un code QR
        filepath = fd.asksaveasfilename(
            title="Sauvegarder le QRCode", 
            initialfile=str(self.row[1])+"_QRCode.png", 
            filetypes=[("PNG Images", "*.png")]
        )
        if(filepath):
            qr = qrcode.make(str(self.id)+";1")
            qr.save(filepath)
        
class App(customtkinter.CTk):
    """
    La classe App est la classe principale de cette application, c'est la Fenêtre Graphique Parent
    """
    def __init__(self):
        super().__init__()

        # Paramêtre de la fenêtre (non-resizable) 
        self.title("Inventaire")
        self.geometry("1000x650")
        self.minsize(1000, 650)
        self.maxsize(1000, 650)
        self.elementListe = []

        # Police Gras dans les variables slef
        self.bold = customtkinter.CTkFont(weight="bold")

        # Etat des sous-fenêtre pour eviter de créer plusieurs fenêtre
        self.edit_window = None
        self.add_window = None
        self.scan_window = None
        self.json_window = None

        # Layout en 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Création de la Div Navigation
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(7, weight=1)

        # Logo Textuel de l'application
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Inventaire",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Bouton Ajouter
        self.add_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Ajouter", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.openAddWindow)
        self.add_button.grid(row=1, column=0, sticky="ew")

        # Bouton Importer
        self.import_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Importer", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.openJsonWindow)
        self.import_button.grid(row=2, column=0, sticky="ew")

        # Bouton Exporter
        self.export_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exporter", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.exportJson)
        self.export_button.grid(row=3, column=0, sticky="ew")

        # Bouton Scanner
        self.scanner_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Scanner", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.choosescan)
        self.scanner_button.grid(row=4, column=0, sticky="ew")

        # Bouton Effacer
        self.effacer_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Effacer", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.deleteDatabase)
        self.effacer_button.grid(row=5, column=0, sticky="ew")

        # Bouton Gérer le Conteneur
        self.container_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Gérer le Conteneur", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.openContainerWindow)
        self.container_button.grid(row=6, column=0, sticky="ew")

        # Dropdown pour le thème 
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=7, column=0, padx=20, pady=20, sticky="s")

        # Création du Home 
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        
        # Thème par defaut
        customtkinter.set_appearance_mode('System')

        # Filtre Frame pour afficher les filtres et faciliter les recherche sur des grandes données
        self.filter_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.filter_frame.pack(fill=customtkinter.X)

        # Barre de recherche, StringVar (pour l'event onChanged) 
        self.search_value = customtkinter.StringVar()
        self.search_value.trace_add("write", callback=self.update_tableau)
        self.search_bar = customtkinter.CTkEntry(self.filter_frame, placeholder_text="Rechercher...", textvariable=self.search_value)
        self.search_bar.grid(row=0, column=0, sticky="we", padx=10)

        # Dropdown pour les catégories
        self.categories = self.find_categories()
        self.selected_categorie = "(Catégorie)"
        self.categories_menu = customtkinter.CTkOptionMenu(self.filter_frame, values=self.categories, command=self.categorieMenuHandle)
        self.categories_menu.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        self.selected_tri = "(Trier par)"
        self.tri_translate = {"Date d'ajout DESC":"id DESC", "Date d'ajout ASC":"id ASC", "Prix DESC":"price DESC", "Quantité DESC":"amount DESC", "Prix ASC":"price ASC", "Quantité ASC":"amount ASC"}
        self.tri_menu = customtkinter.CTkOptionMenu(self.filter_frame, values=["(Trier par)", "Date d'ajout DESC", "Date d'ajout ASC", "Prix DESC", "Prix ASC",  "Quantité DESC", "Quantité ASC"], command=self.triMenuHandle)
        self.tri_menu.grid(row=0, column=2, padx=10, pady=10, sticky="we")

        self.filter_frame.columnconfigure(0, minsize=485)
        self.filter_frame.columnconfigure(1, minsize=100)
        self.filter_frame.columnconfigure(1, minsize=100)

        # Widget Scrollable pour afficher les items de la DB
        self.info_view = customtkinter.CTkFrame(self.home_frame, height=30, fg_color="transparent")
        self.info_view.pack(fill=customtkinter.X, side="bottom")

        self.info_total = getInfo()
        customtkinter.CTkLabel(self.info_view, text=f"Valeur Totale : {self.info_total[0]} €").grid(row=0, column=0)
        customtkinter.CTkLabel(self.info_view, text=f"Nbr Items : {self.info_total[1]}").grid(row=0, column=1)
        self.info_view.grid_columnconfigure(0, minsize=400)
        self.info_view.grid_columnconfigure(1, minsize=400)

        # Widget Scrollable pour afficher les items de la DB
        self.list_view = customtkinter.CTkScrollableFrame(self.home_frame, height=590, fg_color="transparent")
        self.list_view.pack(fill=customtkinter.BOTH)
    
    def choosescan(self):
        choose = customtkinter.CTkToplevel()
        choose.title("Scanner quoi")
        qrbutton = customtkinter.CTkButton(choose,text="QRcode", command=self.readQRCode)
        qrbutton.pack()
        barbutton = customtkinter.CTkButton(choose,text="Code barre", command=self.readbarcode)
        barbutton.pack()


    def find_categories(self):
        # Cette fonction parcour les catégories et les retourne dans une liste
        temp_categories = ["(Catégorie)"]
        # On selectionne toute les catégorie
        CUR.execute('SELECT category FROM matable')
        rows = CUR.fetchall()
        for row in rows:
            # On fait attention qu'elle ne soit pas déjà dans la liste
            if not(row[0] in temp_categories):
                temp_categories.append(row[0])
        return temp_categories

    def categorieMenuHandle(self, categorie):
        """
        Fonction appelée lorsque l'utilisateur sélectionne une catégorie dans le menu déroulant.

        Args: categorie (str): La catégorie sélectionnée par l'utilisateur.

        Returns: None
        """
        # On modifie la Variable selected_categorie de self.
        self.selected_categorie = categorie
        # On rafraichi l'affichage
        self.update_tableau()
    
    def triMenuHandle(self, tri):
        """
        Fonction appelée lorsque l'utilisateur sélectionne une option de tri dans le menu déroulant.

        Args: tri (str): L'option de tri sélectionnée par l'utilisateur.

        Returns: None
        """
        # On modifie la Variable selected_categorie de self.
        self.selected_tri = tri
        # On rafraichi l'affichage
        self.update_tableau()

    def openEditWindow(self, id=0):
        # Ouvre la sous-fenêtre si elle n'existe pas déjà
        if self.edit_window is None or not self.edit_window.winfo_exists():
            self.edit_window = EditWindow(self, id)
        else:
            self.edit_window.focus() 

    def openAddWindow(self):
        # Ouvre la sous-fenêtre si elle n'existe pas déjà
        if self.add_window is None or not self.add_window.winfo_exists():
            self.add_window = AddWindow(self)
        else:
            self.add_window.focus()   
            
    def openJsonWindow(self):
        # Ouvre la sous-fenêtre si elle n'existe pas déjà
        if self.json_window is None or not self.json_window.winfo_exists():
            # Ouvre un explorateur de fichier pour ouvrir le fichier JSON 
            # et le passer en argument pour JsonWindow
            filename = fd.askopenfile(title="Ouvrir le JSON", filetypes=[("JSON Files", "*.json")])
            if(filename):
                jsonFile = json.load(filename)
                if(filename != None):
                    if(checkJsonFormat(jsonFile)):
                        self.json_window = JsonWindow(self, jsonFile)
                    else:
                        showerror("Erreur JSON", "Le Fichier JSON n'est pas conforme")
        else:
            self.json_window.focus() 
        
    def exportJson(self):
        # Ouvre un explorateur de fichier pour stocker le fichier JSON
        filename = fd.asksaveasfile(mode="w", title="Enregistrer un JSON", initialfile="Inventaire_Donnees.json", filetypes=[("JSON Files", "*.json")])
        if(filename):
            # Parcourir tout les elements de la DB
            CUR.execute('SELECT * FROM matable')
            donnees_db = CUR.fetchall()
            donnees_format = []
            for row in donnees_db:
                #Associer à chaque element sa clef : converit une liste en dictionnaire
                donnees_format.append({"id":row[0], "name":row[1], "amount":row[2], "price":row[3], "category":row[4], "masse":row[5], "dimensions":row[6]})

            # Converti une array en string JSON indenté
            dataDump = json.dumps(donnees_format, indent=4)

            # L'écrit les données dans le fichier
            filename.write(dataDump)

    def readQRCode(self):
        """
        Cette fonction permet de lire les codes QR et changer les variables dans la DB
        Peut lire des codes QR sous la forme : Index;Nbr
        avec: - Index = Id de l'element à modifier dans la DB
              - Nbr = nombre de quantité à soustraire
    
        Cette fonctione utilise la camera de l'utilisateur
        """

        # Ouvre un flux de réception Vidéo
        cap = cv2.VideoCapture(0)
        if cap is None or not cap.isOpened():
            showerror("Erreur Video", "Aucun flux vidéo disponible !")
            return
        # initialise le cv2 QRCode detector 
        detector = cv2.QRCodeDetector()
        # variable contenant le message du QRCode
        temp_data=""
        while True: 
            _, img = cap.read()
            # detecte and decode un possible CodeQR
            data, bbox, _ = detector.detectAndDecode(img)
            # Teste si il y a bien un code QR sur l'image
            # Si oui stocke la valeur dans temp_data
            if data: 
                temp_data=data 
                break
        
            # Affiche le Stream Vidéo
            cv2.imshow("Scanner", img)     
            # Permet d'arrêter le stream vidéo à l'appuie de la barre espace
            if cv2.waitKey(1) == ord(" "): 
                break
        
        # Arrête le flux vidéo et ferme la fenêtre de flux
        cap.release() 
        cv2.destroyAllWindows()

        if(temp_data != ""):
            # Séparer l'ID du Nbr
            id=temp_data.split(";")[0]
            nbr=int(temp_data.split(";")[1])
            # Parcour et obtient la quantité liée à l'ID
            CUR.execute('SELECT * FROM matable WHERE id=?', (id, ))
            row = CUR.fetchall()[0]
            # Soutraction
            newAmount = int(row[2]) - nbr
            if(newAmount < 0): newAmount = 0
            # Update en DB
            CON.execute('UPDATE matable set amount=? WHERE id=?', (newAmount, id, ))
            CON.commit()
            playsound('sound.mp3')

        # Mise à jour du tableau
        self.update_tableau()

    def readbarcode(self):
        """
        Cette fonction permet de lire les codes barre et changer les variables dans la DB
        Peut lire des codes barres sous la forme : Index;Nbr
        avec: - Index = Id de l'element à modifier dans la DB
              - Nbr = nombre de quantité à soustraire
    
        Cette fonctione utilise la camera de l'utilisateur
        """

        # Ouvre un flux de réception Vidéo
        cap = cv2.VideoCapture(0)
        if cap is None or not cap.isOpened():
            showerror("Erreur Video", "Aucun flux vidéo disponible !")
            return
        # initialise le cv2 BarCode detector
        detector2 = cv2.barcode.BarcodeDetector()
        # variable contenant le message du BarCode
        temp_data=""
        while True: 
            _, img = cap.read()
            # detecte and decode un possible Code barres
            data, re, rt = detector2.detectAndDecode(img)
            # Teste si il y a bien un code barres sur l'image
            # Si oui stocke la valeur dans temp_data
            print(re, rt, data)
            if data: 
                temp_data=data 
                break
        
            # Affiche le Stream Vidéo
            cv2.imshow("Scanner", img)     
            # Permet d'arrêter le stream vidéo à l'appuie de la barre espace
            if cv2.waitKey(1) == ord(" "): 
                break
        
        # Arrête le flux vidéo et ferme la fenêtre de flux
        cap.release() 
        cv2.destroyAllWindows()

        if(temp_data != ""):
            # Séparer l'ID du Nbr
            id=temp_data
            # Parcour et obtient la quantité liée à l'ID
            CUR.execute('SELECT * FROM matable WHERE id=?', (id, ))
            row = CUR.fetchall()[0]
            # Soutraction
            newAmount = int(row[2]) - 1
            if(newAmount < 0): newAmount = 0
            # Update en DB
            CON.execute('UPDATE matable set amount=? WHERE id=?', (newAmount, id, ))
            CON.commit()
            playsound('sound.mp3')

        # Mise à jour du tableau
        self.update_tableau()


    def deleteDatabase(self):
        if askokcancel(title="Suppression de la Base de Données", message="Etes-vous sûr de vouloir supprimer tous les élements de la base de données, cette action est irreversible. Si c'est le cas, il est recommendé d'exporter d'abord la base de données à l'aide du bouton exporter"):
            CON.execute("DELETE FROM matable")
            CON.commit()

    def openContainerWindow(self):
        # Ouvre la fenêtre de gestion du conteneur
        ContainerWindow(self)

    def update_tableau(self, e=None, i=None, a=None):
        """
        Cette fonction permet de mettre à jour les elements du tableau
        par rapport à la base de donnée
        """
        # Vide la liste de ses items
        for child in self.list_view.winfo_children():
            child.destroy()
        liste = []
        self.elementListe = []

        self.categories = self.find_categories()
        self.categories_menu = customtkinter.CTkOptionMenu(self.filter_frame, values=self.categories, command=self.categorieMenuHandle)
        self.categories_menu.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        # Parcour la liste lorsqu'il corresponde à la recherche
        if(self.selected_categorie == "(Catégorie)"):
            if(self.selected_tri == "(Trier par)"):
                CUR.execute('SELECT * FROM matable WHERE name LIKE ?', (str("%")+self.search_bar.get()+str("%"), ))
            else:
                CUR.execute('SELECT * FROM matable WHERE name LIKE ? ORDER BY '+self.tri_translate[self.selected_tri], (str("%")+self.search_bar.get()+str("%"), ))
        else:
            if(self.selected_tri == "(Trier par)"):
                CUR.execute('SELECT * FROM matable WHERE name LIKE ? and category=?', (str("%")+self.search_bar.get()+str("%"), self.selected_categorie, ))
            else:
                CUR.execute('SELECT * FROM matable WHERE name LIKE ? and category=? ORDER BY '+self.tri_translate[self.selected_tri], (str("%")+self.search_bar.get()+str("%"), self.selected_categorie, ))

        rows = CUR.fetchall()

        # Création du tableau et des titres de colonne
        self.title_name = customtkinter.CTkLabel(self.list_view, text="Nom", fg_color="transparent", font=self.bold)
        self.title_name.grid(row=0, column=0, sticky="w", padx=10)
        self.title_price = customtkinter.CTkLabel(self.list_view, text="Prix", fg_color="transparent", font=self.bold)
        self.title_price.grid(row=0, column=1, sticky="w")
        self.title_amount = customtkinter.CTkLabel(self.list_view, text="Quantité", fg_color="transparent", font=self.bold)
        self.title_amount.grid(row=0, column=2, sticky="w")
        self.categorie_amount = customtkinter.CTkLabel(self.list_view, text="Catégorie", fg_color="transparent", font=self.bold)
        self.categorie_amount.grid(row=0, column=3, sticky="w")

        for i, row in enumerate(rows):
            # Ajout de chaque item dans la ligne et les colonnes du tableau
            tempListe = []

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row[1], fg_color="transparent"))
            tempListe[0].grid(row=i+1, column=0, sticky="w", padx=10)

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row[3], fg_color="transparent"))
            tempListe[1].grid(row=i+1, column=1, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row[2], fg_color="transparent"))
            tempListe[2].grid(row=i+1, column=2, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text=row[4], fg_color="transparent"))
            tempListe[3].grid(row=i+1, column=3, sticky="w")

            tempListe.append(customtkinter.CTkButton(self.list_view, text="Modifier", command=lambda id = row[0]: self.openEditWindow(id)))
            tempListe[4].grid(row=i+1, column=4, sticky="e", pady=5)

            liste.append(tempListe)
        
        # Mise en page du tableau (taille des colonnes et lignes)
        self.list_view.grid_columnconfigure(0, minsize=250)
        self.list_view.grid_columnconfigure(1, minsize=100)
        self.list_view.grid_columnconfigure(2, minsize=100)
        self.list_view.grid_columnconfigure(3, minsize=200)
        self.list_view.grid_columnconfigure(4, minsize=100)

    def change_appearance_mode_event(self, new_appearance_mode):
        #Permet de changer l'apparence de l'application
        customtkinter.set_appearance_mode(new_appearance_mode)

class ContainerWindow(customtkinter.CTkToplevel):
    dimensions_validated = False

    def __init__(self, parent):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Gérer le Conteneur")
        self.geometry("400x350")

        # Ajout des widgets pour les dimensions et les fonctionnalités de gestion du conteneur
        self.dimensions_label = customtkinter.CTkLabel(self, text="Dimensions du Conteneur", fg_color="transparent")
        self.dimensions_entry = customtkinter.CTkEntry(self, placeholder_text="Ex : 150x45x30")
        self.dimensions_label.pack()
        self.dimensions_entry.pack()

        self.validate_button = customtkinter.CTkButton(self, text="Valider les Dimensions", command=self.validateDimensions)
        self.validate_button.pack()

        self.add_item_button = customtkinter.CTkButton(self, text="Ajouter un Article", command=self.addArticle)
        self.add_item_button.pack()

        self.remove_item_button = customtkinter.CTkButton(self, text="Supprimer un Article", command=self.removeArticle)
        self.remove_item_button.pack()

        self.clear_container_button = customtkinter.CTkButton(self, text="Vider le Conteneur", command=self.clearContainer)
        self.clear_container_button.pack()

        # Liste des articles disponibles (vous devez remplacer cela par votre propre liste)
        self.available_articles = self.retrieveAvailableArticles()

        # Liste des articles ajoutés au conteneur
        self.container_articles = []

        # Dimensions du conteneur
        self.container_dimensions = None

        # Étiquette pour afficher l'espace restant dans le conteneur
        self.remaining_space_label = Label(self, text="Espace restant dans le conteneur :")
        self.remaining_space_label.pack()

        # Listebox pour afficher les articles dans le conteneur
        self.container_listbox = Listbox(self, selectmode="single", height=5, width=50)
        self.container_listbox.pack()

        self.updateContainerListbox()
        self.updateRemainingSpaceLabel()

    def retrieveAvailableArticles(self):
        # Récupérer les articles directement de la base de données matable
        CUR.execute('SELECT id, name, amount, dimensions FROM matable')
        rows = CUR.fetchall()
        available_articles = [{"id": row[0], "name": row[1], "amount": row[2], "dimensions": row[3].split('x')} for row in rows]
        return available_articles

    def validateDimensions(self):
        # Valider les dimensions du conteneur
        dimensions_input = self.dimensions_entry.get()
        try:
            self.container_dimensions = list(map(int, dimensions_input.split('x')))
            print(f"Dimensions du conteneur validées : {self.container_dimensions}")
    
            # Mettre à jour la variable de classe pour indiquer que les dimensions sont validées
            ContainerWindow.dimensions_validated = True
    
            # Désactiver le widget d'entrée des dimensions
            self.dimensions_entry.configure(state='disabled')
            
            # Désactiver le bouton de validation des dimensions
            self.validate_button.configure(state='disabled')
        except ValueError:
            showerror("Erreur de Dimensions", "Veuillez entrer des dimensions valides (séparées par 'x').")

    def addArticle(self):
        # Vérifier si les dimensions du conteneur ont été validées
        if self.container_dimensions is None:
            showerror("Erreur d'Opération", "Veuillez d'abord valider les dimensions du conteneur.")
            return

        # Ouvrir une fenêtre pour sélectionner un article
        selected_article = self.selectArticle()

        if selected_article:
            # Calculer l'espace restant dans le conteneur
            remaining_space = self.calculateRemainingSpace()

            # Calculer l'espace nécessaire pour la quantité demandée de l'article
            space_required = selected_article["quantity"] * self.calculateArticleVolume(selected_article)

            # Vérifier si l'espace restant est suffisant
            if remaining_space >= space_required:
                # Vérifier si l'article est déjà présent dans le conteneur
                existing_article = next((article for article in self.container_articles if article["id"] == selected_article["id"]), None)

                if existing_article:
                    # Si l'article existe déjà, augmenter la quantité
                    existing_article["quantity"] += selected_article["quantity"]
                else:
                    # Sinon, ajouter l'article au conteneur
                    self.container_articles.append(selected_article)

                # Mettre à jour l'affichage de la Listbox
                self.updateContainerListbox()

                # Mettre à jour l'espace restant dans le conteneur
                self.updateRemainingSpaceLabel()
            else:
                showerror("Erreur d'Espace", "Il n'y a pas assez d'espace disponible dans le conteneur pour cette quantité d'articles.")

    def removeArticle(self):
        # Vérifier si des articles sont présents dans le conteneur
        if not self.container_articles:
            showinfo("Information", "Le conteneur est vide.")
            return

        # Sélectionner l'article à supprimer
        selected_index = self.container_listbox.curselection()
        if not selected_index:
            showerror("Erreur de Sélection", "Veuillez sélectionner un article à supprimer.")
            return

        # Récupérer l'index de l'article sélectionné
        selected_index = selected_index[0]

        # Retirer l'article du conteneur
        removed_article = self.container_articles.pop(selected_index)

        # Mettre à jour l'affichage de la Listbox
        self.updateContainerListbox()

        # Mettre à jour l'espace restant dans le conteneur
        self.updateRemainingSpaceLabel()

        showinfo("Article Supprimé", f"L'article {removed_article['name']} a été retiré du conteneur.")
 
    def clearContainer(self):
        # Vérifier si des articles sont présents dans le conteneur
        if not self.container_articles:
            showinfo("Information", "Le conteneur est déjà vide.")
            return

        # Demander une confirmation à l'utilisateur
        confirmation = askyesno("Confirmation", "Voulez-vous vraiment vider le conteneur de tous les articles ?")

        if confirmation:
            # Vider le conteneur
            self.container_articles = []

            # Mettre à jour l'affichage de la Listbox
            self.updateContainerListbox()

            # Mettre à jour l'espace restant dans le conteneur
            self.updateRemainingSpaceLabel()

            showinfo("Conteneur Vidé", "Le conteneur a été vidé de tous les articles.")

    def updateRemainingSpaceLabel(self):
        # Calculer l'espace restant dans le conteneur
        remaining_space = self.calculateRemainingSpace()

        # Mettre à jour le texte de l'étiquette
        self.remaining_space_label.configure(text=f"Espace restant dans le conteneur : {remaining_space} cm3")

    def calculateRemainingSpace(self):
        # Vérifier si les dimensions du conteneur ont été validées
        if self.container_dimensions is None:
            print("Veuillez d'abord valider les dimensions du conteneur.")
            return 0  # Ou une autre valeur par défaut appropriée

        # Convertir les dimensions du conteneur en entiers
        container_dimensions = [int(dim) for dim in self.container_dimensions]

        # Calculer le volume total du conteneur
        total_volume = reduce(lambda x, y: x * y, container_dimensions)

        # Calculer le volume occupé par les articles dans le conteneur
        occupied_volume = 0
        for article in self.container_articles:
            # Convertir les dimensions de l'article en entiers
            article_dimensions = [int(dim) for dim in article['dimensions']]
            # Calculer le volume de l'article en tenant compte de la quantité
            article_volume = reduce(lambda x, y: x * y, article_dimensions) * article['quantity']
            occupied_volume += article_volume

        # Calculer l'espace restant
        remaining_space = total_volume - occupied_volume

        print(f"Volume total du conteneur : {total_volume}")
        print(f"Volume occupé par les articles : {occupied_volume}")
        print(f"Espace restant dans le conteneur : {remaining_space}")
        
        # Mettre à jour l'affichage de la Listbox
        self.updateContainerListbox()
        return remaining_space

    def calculateArticleVolume(self, article):
        # Convertir les dimensions de l'article en entiers
        article_dimensions = [int(dim) for dim in article['dimensions']]

        # Calculer le volume de l'article
        article_volume = reduce(lambda x, y: x * y, article_dimensions)

        return article_volume

    def updateContainerListbox(self):
        # Effacer le contenu actuel de la Listbox
        self.container_listbox.delete(0, END)

        # Ajouter les articles actuellement dans le conteneur à la Listbox
        for article in self.container_articles:
            article_info = f"{article['name']} - Quantité: {article['quantity']}"
            self.container_listbox.insert(END, article_info)

    def selectArticle(self):
        # Liste des noms d'articles disponibles
        available_articles = [article for article in self.available_articles if article["amount"] > 0]

        if not available_articles:
            showerror("Erreur de Sélection", "Aucun article disponible.")
            return None

        # Boîte de dialogue pour la sélection de l'article et de la quantité
        selected_article, quantity = self.createArticleDialog(available_articles)

        if selected_article:
            # Vérifier la quantité disponible
            if selected_article["amount"] >= quantity:
                # Décrémenter la quantité disponible de l'article
                selected_article["amount"] -= quantity

                # Ajouter l'article sélectionné à la liste des articles du conteneur avec la quantité
                selected_article_with_quantity = selected_article.copy()
                selected_article_with_quantity["quantity"] = quantity
                return selected_article_with_quantity

        # Mettre à jour l'affichage de la Listbox
        self.updateContainerListbox()
        # Si aucun article n'est sélectionné ou s'il n'y en a pas en quantité suffisante
        showerror("Erreur de Sélection", "Aucun article sélectionné ou quantité insuffisante.")
        return None

    def createArticleDialog(self, available_articles):
        dialog = customtkinter.CTkToplevel(self)

        # Ajouter une liste déroulante pour la sélection de l'article
        article_var = StringVar(dialog)
        article_var.set(available_articles[0]["name"])
        article_dropdown = Combobox(dialog, textvariable=article_var, values=[article["name"] for article in available_articles])
        article_dropdown.pack()

        # Ajouter une entrée pour la sélection de la quantité
        quantity_label = customtkinter.CTkLabel(dialog, text="Quantité :")
        quantity_label.pack()

        quantity_var = IntVar(dialog)
        quantity_var.set(1)
        quantity_entry = customtkinter.CTkEntry(dialog, textvariable=quantity_var)
        quantity_entry.pack()

        # Ajouter un bouton pour valider la sélection
        confirm_button = customtkinter.CTkButton(dialog, text="Confirmer", command=dialog.destroy)
        confirm_button.pack()

        # Attendre la fermeture de la fenêtre de dialogue
        dialog.wait_window()

        # Récupérer la valeur sélectionnée après que la boîte de dialogue est fermée
        selected_article_name = article_var.get()
        quantity = quantity_var.get()

        # Trouver l'article sélectionné dans la liste des articles disponibles
        selected_article = next((article for article in available_articles if article["name"] == selected_article_name), None)

        return selected_article, quantity

    def createArticleDropdown(self, article_names):
        # Créer une nouvelle fenêtre de dialogue
        dialog = customtkinter.CTkToplevel(self)

        # Ajouter une liste déroulante pour la sélection de l'article
        article_name_var = StringVar(dialog)
        article_name_var.set(article_names[0])
        article_dropdown = Combobox(dialog, textvariable=article_name_var, values=article_names)
        article_dropdown.pack()

        # Ajouter un bouton pour valider la sélection
        confirm_button = customtkinter.CTkButton(dialog, text="Confirmer", command=dialog.destroy)
        confirm_button.pack()

        # Attendre la fermeture de la fenêtre de dialogue
        dialog.wait_window()

        # Récupérer la valeur sélectionnée après que la boîte de dialogue est fermée
        selected_article_name = article_name_var.get()

        return selected_article_name

if __name__ == "__main__":
    ensureDatabase()
    app = App()
    app.update_tableau()
    app.mainloop()
