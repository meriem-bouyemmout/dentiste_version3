import fdb  # Assurez-vous que le module fdb est installé
import tkinter as tk
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

class List_Impayee:
    def __init__(self, mast):
        self.master = mast
        self.master.title("Gestion des Impayees")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")
        self.master.configure(bg="white")  # Exemple pour un fond blanc
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")

        

        # Section Historique des Consultations
        frame_historique = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_historique.pack(padx=10, pady=10, fill="both", expand=True)

        label_historique = ctk.CTkLabel(frame_historique, text="Liste Des Patient Impayees:", font=("Arial", 14))
        label_historique.grid(row=0, column=0, padx=10, pady=5)

        self.table_historique = ttk.Treeview(frame_historique, columns=("ID_patient", "Nom", "Prenom", "Num_tel", "Date", "Operations", "Total", "Versement", "Reste"), show='headings', height=20)
        self.table_historique.heading("ID_patient", text="ID de patient")
        self.table_historique.heading("Nom", text="Nom")
        self.table_historique.heading("Prenom", text="Prenom")
        self.table_historique.heading("Num_tel", text="Numero de telephone")
        self.table_historique.heading("Date", text="Date de Consultation")
        self.table_historique.heading("Operations", text="Opérations")
        self.table_historique.heading("Total", text="Montant Total")
        self.table_historique.heading("Versement", text="Versement")
        self.table_historique.heading("Reste", text="Reste à Payer")

        self.table_historique.column("ID_patient", width=50)
        self.table_historique.column("Nom", width=75)
        self.table_historique.column("Prenom", width=75)
        self.table_historique.column("Num_tel", width=130) 
        self.table_historique.column("Date", width=150)
        self.table_historique.column("Operations", width=200)
        self.table_historique.column("Total", width=100)
        self.table_historique.column("Versement", width=100)
        self.table_historique.column("Reste", width=100)
        self.table_historique.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        self.table_historique.bind("<Double-1>", self.on_double_click)

        
        self.read()
        # Ajouter l'image en bas à droite
        self.add_image_bottom_right()
        

    def add_image_bottom_right(self):
        # Charger l'image
        image_path = "images\\tooth-1015409_640000.jpg"  # Assurez-vous que le chemin est correct
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200))  # Redimensionner l'image selon les besoins
        self.photo_image = ImageTk.PhotoImage(self.image)

        # Utiliser CTkImage à la place de PhotoImage
        self.ctk_image = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(200, 200))

        # Créer un label pour afficher l'image
        self.img_label = ctk.CTkLabel(self.master, image=self.ctk_image, text="", bg_color="white")
        self.img_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def on_double_click(self, event):
        # Récupérer l'élément sélectionné
        selected_item = self.table_historique.selection()
        if selected_item:
            patient_info = self.table_historique.item(selected_item, 'values')
            
            # Créer un message avec les informations du patient
            info_message = (
                f"ID Patient: {patient_info[0]}\n"
                f"Nom: {patient_info[1]}\n"
                f"Prenom: {patient_info[2]}\n"
                f"Numéro de Téléphone: {patient_info[3]}\n"
                f"Date de Consultation: {patient_info[4]}\n"
                f"Opérations: {patient_info[5]}\n"
                f"Montant Total: {patient_info[6]}\n"
                f"Versement: {patient_info[7]}\n"
                f"Reste à Payer: {patient_info[8]}\n"
            )
            
            # Afficher les informations dans une boîte de dialogue
            messagebox.showinfo("Informations du Patient", info_message)
        

    def read(self):
        
            def read_database_path(file_path='data_base.txt'):
                with open(file_path, 'r') as file:
                    return file.read().strip()

            def read_fbclient_path(file_path='fb_client.txt'):
                with open(file_path, 'r') as file:
                    return file.read().strip()

            database_path = read_database_path()
            fbclient_path = read_fbclient_path()

            conn = fdb.connect(
                dsn=database_path,
                user='SYSDBA',
                password='1234',
                charset='UTF8',
                fb_library_name=fbclient_path
            )
            cursor = conn.cursor()

            cursor.execute("""
                            SELECT 
                PAT.ID, 
                PAT.NOM, 
                PAT.PRENOM, 
                PAT.NUM_TEL, 
                C.JOUR AS DATE_CONSULTATION, 
                LIST(D.OPERATION, ', ') AS OPERATIONS, 
                P.MONTANT_TOTAL, 
                P.VERSEMENT, 
                P.RESTE
            FROM 
                CONSULTATION C
            JOIN 
                DETAILLE_CONSULTATION D ON C.ID_CONSULTATION = D.ID_CONSULTATION
            JOIN 
                PAYEMENT P ON C.ID_CONSULTATION = P.ID_CONSULTATION
            JOIN 
                PATIENT PAT ON C.ID_PATIENT = PAT.ID
            WHERE 
                P.RESTE > 0 
            GROUP BY 
                PAT.ID, 
                PAT.NOM, 
                PAT.PRENOM, 
                PAT.NUM_TEL, 
                C.JOUR, 
                P.MONTANT_TOTAL, 
                P.VERSEMENT, 
                P.RESTE;

            """)

            # Récupérer toutes les consultations
            consultations = cursor.fetchall()

            # Vider la table existante
            for item in self.table_historique.get_children():
                self.table_historique.delete(item)

            # Remplir la table avec les données de la base
            for consultation in consultations:
                id_patient = consultation[0]
                nom = consultation[1]
                prenom = consultation[2]
                num_tel = consultation[3]
                date_consultation = consultation[4]
                operations = consultation[5]
                total = consultation[6]
                versement = consultation[7]
                reste = consultation[8]

                self.table_historique.insert('', 'end', values=(id_patient, nom, prenom, num_tel,
                    date_consultation, operations, f"{total:.2f}",
                    f"{versement:.2f}", f"{reste:.2f}"))

            conn.close()

        

    




if __name__ == "__main__":
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = List_Impayee(window)
    mainloop()
