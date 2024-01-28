import sqlite3
import customtkinter
from tkinter.messagebox import showerror

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
        self.geometry("500x270")
        self.minsize(500, 270)
        self.maxsize(500, 270)
        self.title("Ajouter")

        self.parent_self = parent_self

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

        # Bouton enregister qui appelle la fonction locale save()
        self.save_button = customtkinter.CTkButton(self, text="Ajouter", command=self.save)
        self.save_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=20, padx=10)

        # Configuration de la taille des lignes et des colonnes
        self.grid_columnconfigure(0, minsize=150)
        self.grid_columnconfigure(1, minsize=350)
        self.grid_rowconfigure([0, 1, 2, 3], minsize=50)

    def save(self):
        CON = sqlite3.connect("res/database.db")
        # Requête SQL pour ajouter les valeur des inputs (via les StringVar) dans notre table matable
        if(self.amount_string.get().isdigit() and self.price_string.get().isdigit()):
            CON.executemany("INSERT INTO matable (name, amount, price, category) VALUES(?, ?, ?, ?)",[(self.name_string.get(), self.amount_string.get(), self.price_string.get(), self.category_string.get())])
            CON.commit()
            # Actualisation du tableau de la Fenêter Parent
            self.parent_self.update_tableau()
            # Destrucion de la sous-fenêtre
            CON.close()
            self.destroy()
        else:
            showerror("Type Erreur", "Veuillez rentrer des valeurs chiffrées pour : Prix et Quantité")
            CON.close()
