import sqlite3
import customtkinter
import qrcode
from customtkinter import filedialog as fd
from tkinter.messagebox import askokcancel

class EditWindow(customtkinter.CTkToplevel):
    def __init__(self, parent_self, id):
        super().__init__()
        
        # Ajout de la Variable ID dans les variables self
        self.id = id
        self.parent_self = parent_self

        CON = sqlite3.connect("res/database.db")
        CUR = CON.cursor()

        # Création de la fenêtre de base non-resisable et du titre
        self.geometry("500x330")
        self.minsize(500, 330)
        self.maxsize(500, 330)
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

        # Bouton enregistrer lié à la fonction save()
        self.save_button = customtkinter.CTkButton(self, text="Enregistrer", command=self.save)
        self.save_button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

        # Bouton QRCode lié à la fonction qrcode()
        self.qrcode_button = customtkinter.CTkButton(self, text="QRCode", command=self.qrcode)
        self.qrcode_button.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

        # Bouton supprimer lié à la fonction delete()
        self.delete_button = customtkinter.CTkButton(self, text="Supprimer", command=self.delete, fg_color="#dc143c", hover_color="#b22222")
        self.delete_button.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

        #Configuration des tailles du tableau (colonnes et lignes)
        self.grid_columnconfigure(0, minsize=150)
        self.grid_columnconfigure(1, minsize=350)
        self.grid_rowconfigure([0, 1, 2, 3], minsize=50)
        CON.close()
    def save(self):
        CON = sqlite3.connect("res/database.db")
        CUR = CON.cursor()
        if(self.amount_string.get().isdigit() and self.price_string.get().isdigit()):
            # Fonction Save, update dans la base de données à l'aide des stringVar
            CON.execute('UPDATE matable set name=?, amount=?, price=?, category=? WHERE id=?', (self.name_string.get(), self.amount_string.get(), self.price_string.get(), self.category_string.get(), self.id, ))
            CON.commit()

            self.parent_self.update_tableau()
            CON.close()
            self.destroy()
        else:
            showerror("Type Erreur", "Veuillez rentrer des valeurs chiffrées pour : Prix et Quantité")
            CON.close()
    def delete(self):
        CON = sqlite3.connect("res/database.db")
        CUR = CON.cursor()
        # Supprime l'items de la base de données
        CON.execute('DELETE FROM matable WHERE id=?', (self.id, ))
        CON.commit()

        self.parent_self.update_tableau()
        CON.close()
        self.destroy()
    
    def qrcode(self):
        # Crée un code QR
        filepath = fd.asksaveasfilename(title="Sauvegarder le QRCode", initialfile=str(self.row[1])+"_QRCode.png", filetypes=[("PNG Images", "*.png")])
        qr = qrcode.make(str(self.id)+";1")
        qr.save(filepath)

        self.parent_self.update_tableau()
        self.destroy()