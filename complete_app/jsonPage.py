import sqlite3
import customtkinter

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
        self.geometry("500x500")
        self.minsize(500, 300)
        self.maxsize(500, 300)
        self.title("Importer")

        self.parent_self = parent_self

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
        self.title_amount = customtkinter.CTkLabel(self.list_view, text="Prix", fg_color="transparent", font=self.bold)
        self.title_amount.grid(row=0, column=4, sticky="w")

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

            self.liste.append(tempListe)
        
        # Configuration des tailles des colonnes et des lignes dans le tableau
        self.list_view.grid_columnconfigure(0, minsize=50)
        self.list_view.grid_columnconfigure(1, minsize=150)
        self.list_view.grid_columnconfigure(2, minsize=100)
        self.list_view.grid_columnconfigure(3, minsize=100)
        self.list_view.grid_columnconfigure(4, minsize=100)


    def save(self, jsonData):
        """
        La fonction save permet de stocker des items dans la base de données en excluant l'ID
        car celui-ci d'autoincrémente tout seul

        Args :
            - jsonData (2D list)
        """
        CON = sqlite3.connect("res/database.db")

        temp_liste = [(row["name"], row["amount"], row["price"], row["category"]) for row in jsonData]
        # Suppression de la table actuelles
        CON.execute("DELETE FROM matable;")
        # Ajout de tout les items via la fonction executemany
        CON.executemany("INSERT INTO matable (name, amount, price, category) VALUES(?, ?, ?, ?)",temp_liste)
        CON.commit()
        # Actualisation du tableau de la fenêtre Parent
        self.parent_self.update_tableau()
        # Destruction de la sous-fenêtre
        CON.close()
        self.destroy()
