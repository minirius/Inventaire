import customtkinter
import os
from tkinter.messagebox import showwarning
import sqlite3

CON = sqlite3.connect("database.sql")
CUR = CON.cursor()

#CUR.execute("CREATE DATABASE madatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
#CUR.execute("CREATE TABLE matable(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name MEDIUMTEXT, amount INT, price INT, category MEDIUMTEXT);")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("image_example.py")
        self.geometry("1000x650")
        self.checkBoxListe= []
        self.elementListe = []

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Inventaire",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Ajouter",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=lambda: print("Begu 1"))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Importer",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=lambda:print("Begu 2"))
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Exporter",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=lambda:print("Begu 3"))
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Modifier",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.edit)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # select default frame
        customtkinter.set_appearance_mode('Dark')
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        
        self.search_bar = customtkinter.CTkEntry(self.home_frame, placeholder_text="Rechercher...")
        self.search_bar.pack(pady=10, fill=customtkinter.X, padx=10)

        self.list_view = customtkinter.CTkScrollableFrame(self.home_frame, height=590)
        self.list_view.pack(fill=customtkinter.BOTH)
    
    def edit(self):
        tempListe = []
        for i in self.checkBoxListe:
            tempListe.append(i.get())
        if(tempListe.count('on') == 1):
            print(tempListe.index("on"))
        else:
            showwarning("Erreur", "Veuillez selectionner 1 élément")
            
    def fill_table(self):
        liste = []
        self.checkBoxListe = []
        self.elementListe = []
        for i in range(10):
            tempListe = []
            self.checkBoxListe.append(customtkinter.StringVar(value="off"))
            tempListe.append(customtkinter.CTkCheckBox(self.list_view, text="", variable=self.checkBoxListe[i], onvalue="on", offvalue="off"))
            tempListe[0].grid(row=i, column=0, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text="Bateau gonflable", fg_color="transparent"))
            tempListe[1].grid(row=i, column=1, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text="15 ", fg_color="transparent"))
            tempListe[2].grid(row=i, column=2, sticky="w")

            tempListe.append(customtkinter.CTkLabel(self.list_view, text="20€", fg_color="transparent"))
            tempListe[3].grid(row=i, column=3, sticky="w")

            liste.append(tempListe)
        
        self.list_view.grid_columnconfigure(0, minsize=20)
        self.list_view.grid_columnconfigure(1, minsize=380)
        self.list_view.grid_columnconfigure(2, minsize=200)
        self.list_view.grid_columnconfigure(3, minsize=200)

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.fill_table()
    app.mainloop()
