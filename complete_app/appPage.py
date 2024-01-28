import json
import sqlite3
import customtkinter
from customtkinter import filedialog as fd
from tkinter.messagebox import askokcancel, showerror

import cv2

from addPage import AddWindow
from editPage import EditWindow
from jsonPage import JsonWindow

def checkJsonFormat(jsonFile):
    """
    checkJsonFormat est une fonctione qui permet de valider la conformité d'un fichier JSON
    il parcour la list de listes pour vérifier si les enfants sont corrects et vérifier les
    types associés

    Arg: jsonFile (2d Array)
    Return : Bool : if the Json is valid
    """
    for i, row in enumerate(jsonFile):
        if (len(row) == 5 and "id" in row and "name" in row and "amount" in row and "price" in row and "category" in row):
            if not (type(row["id"]) == int and type(row["name"]) == str and type(row["amount"]) == int and type(row["price"]) == int and type(row["category"]) == str):
                return False
        else:
            return False
    return True

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
        self.navigation_frame.grid_rowconfigure(6, weight=1)

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
        self.scanner_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Scanner", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.readQRCode)
        self.scanner_button.grid(row=4, column=0, sticky="ew")

        # Bouton Effacer
        self.effacer_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Effacer", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.deleteDatabase)
        self.effacer_button.grid(row=5, column=0, sticky="ew")

        # Dropdown pour le thème 
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

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

        self.filter_frame.columnconfigure(0, minsize=645)
        self.filter_frame.columnconfigure(1, minsize=100)

        # Widget Scrollable pour afficher les items de la DB
        self.list_view = customtkinter.CTkScrollableFrame(self.home_frame, height=590, fg_color="transparent")
        self.list_view.pack(fill=customtkinter.BOTH)
    
    def find_categories(self):
        CON = sqlite3.connect("res/database.db")
        CUR = CON.cursor()
        # Cette fonction parcour les catégories et les retourne dans une liste
        temp_categories = ["(Catégorie)"]
        # On selectionne toute les catégorie
        CUR.execute('SELECT category FROM matable')
        rows = CUR.fetchall()
        for row in rows:
            # On fait attention qu'elle ne soit pas déjà dans la liste
            if not(row[0] in temp_categories):
                temp_categories.append(row[0])
        CON.close()
        return temp_categories

    def categorieMenuHandle(self, categorie):
        # On modifie la Variable selected_categorie de self.
        self.selected_categorie = categorie
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
            file = fd.askopenfile(title="Ouvrir le JSON", filetypes=[("JSON Files", "*.json")])
            jsonFile = json.load(file)
            if(file != None):
                if(checkJsonFormat(jsonFile)):
                    self.json_window = JsonWindow(self, jsonFile)
                else:
                    showerror("Erreur JSON", "Le Fichier JSON n'est pas conforme")
        else:
            self.json_window.focus() 
        
    def exportJson(self):
        CON = sqlite3.connect("res/database.db")
        CUR = CON.cursor()
        # Ouvre un explorateur de fichier pour stocker le fichier JSON
        filename = fd.asksaveasfile(mode="w", title="Enregistrer un JSON", initialfile="Inventaire_Donnees.json", filetypes=[("JSON Files", "*.json")])
        if(filename):
            # Parcourir tout les elements de la DB
            CUR.execute('SELECT * FROM matable')
            donnees_db = CUR.fetchall()
            donnees_format = []
            for row in donnees_db:
                #Associer à chaque element sa clef : converit une liste en dictionnaire
                donnees_format.append({"id":row[0], "name":row[1], "amount":row[2], "price":row[3], "category":row[4]})

            # Converti une array en string JSON indenté
            dataDump = json.dumps(donnees_format, indent=4)

            # L'écrit les données dans le fichier
            filename.write(dataDump)
        CON.close()

    def readQRCode(self):
        """
        Cette fonction permet de lire les codes QR et changer les variables dans la DB
        Peut lire des codes QR sous la forme : Index;Nbr
        avec: - Index = Id de l'element à modifier dans la DB
              - Nbr = nombre de quantité à soustraire
    
        Cette fonctione utilise la camera de l'utilisateur
        """
        CON = sqlite3.connect("res/database.db")
        CUR = CON.cursor()

        # Ouvre un flux de réception Vidéo
        cap = cv2.VideoCapture(0) 
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

        # Mise à jour de la BD
        CON.close()
        self.update_tableau()

    def deleteDatabase(self):
        CON = sqlite3.connect("res/database.db")
        if askokcancel(title="Suppression de la Base de Données", message="Etes-vous sûr de vouloir supprimer tous les élements de la base de données, cette action est irreversible. Si c'est le cas, il est recommendé d'exporter d'abord la base de données à l'aide du bouton exporter"):
            CON.execute("DELETE FROM matable")
            CON.commit()
        CON.close()

    def update_tableau(self, e=None, i=None, a=None):
        """
        Cette fonction permet de mettre à jour les elements du tableau
        par rapport à la base de donnée
        """
        CON = sqlite3.connect("res/database.db")
        CUR = CON.cursor()
        # Vide la liste de ses items
        for child in self.list_view.winfo_children():
            child.destroy()
        liste = []
        self.elementListe = []

        self.find_categories()

        # Parcour la liste lorsqu'il corresponde à la recherche
        if(self.selected_categorie == "(Catégorie)"):
            CUR.execute('SELECT * FROM matable WHERE name LIKE ?', (str("%")+self.search_bar.get()+str("%"), ))
        else:
            CUR.execute('SELECT * FROM matable WHERE name LIKE ? and category=?', (str("%")+self.search_bar.get()+str("%"), self.selected_categorie, ))

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

        CON.close()

    #Permet de changer l'apparence de l'application
    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)