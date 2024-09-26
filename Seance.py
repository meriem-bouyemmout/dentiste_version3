import fdb  # Assurez-vous que le module fdb est installé
import tkinter as tk
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
import babel.numbers

class Seance:
    def __init__(self, master, user):
        self.master = master
        self.master.title("Liste des Consultations")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")
        self.master.configure(bg="white")
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width, h=self.height))
        self.master.state("zoomed")
        
        self.user = user

        # Section Patient
        frame_patient = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_patient.pack(padx=10, pady=10, fill="x")

        label_patient = ctk.CTkLabel(frame_patient, text="ID du Patient:", font=("Arial", 14))
        label_patient.grid(row=0, column=0, padx=10, pady=5)

        self.entry_id_patient = ctk.CTkEntry(frame_patient, width=200)
        self.entry_id_patient.grid(row=0, column=1, padx=10, pady=5)

        

        

        btn_search_patient = ctk.CTkButton(frame_patient, text="Chercher", command=self.list_consultations)
        btn_search_patient.grid(row=0, column=4, padx=10, pady=5)

        # Section Historique des Consultations
        frame_historique = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_historique.pack(padx=10, pady=10, fill="both", expand=True)

        label_historique = ctk.CTkLabel(frame_historique, text="Historique des Consultations:", font=("Arial", 14))
        label_historique.grid(row=0, column=0, padx=10, pady=5)
        # Champ de saisie pour la date
        label_date = ctk.CTkLabel(frame_historique, text="Date de Séance:", font=("Arial", 14))
        label_date.grid(row=0, column=1, padx=5, pady=5)

        self.entry_date_seance = DateEntry(frame_historique, width=15, background='darkblue', foreground='white', borderwidth=2, year=2024)
        self.entry_date_seance.grid(row=0, column=2, padx=5, pady=5)

        # Table avec colonnes : ID, Opération, Date, Numéro de Séance
        self.table_historique = ttk.Treeview(frame_historique, columns=("Date", "Operations", "Num_seance"), show='headings', height=15)
        self.table_historique.heading("Date", text="Date de Seance")
        self.table_historique.heading("Operations", text="Opérations")
        self.table_historique.heading("Num_seance", text="Numero de seance")
        

        self.table_historique.column("Date", width=200)
        self.table_historique.column("Operations", width=250)
        self.table_historique.column("Num_seance", width=150)
        
        self.table_historique.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        # Lier l'événement de sélection d'une ligne à la méthode de gestion
        self.table_historique.bind("<<TreeviewSelect>>", self.on_item_selected)

        # Ajouter l'image en bas à droite
        self.add_image_bottom_right()


        

    def add_image_bottom_right(self):
        # Charger l'image
        image_path = "images\\tooth-1015425_640.jpg"  # Assurez-vous que le chemin est correct
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200))  # Redimensionner l'image selon les besoins
        self.photo_image = ImageTk.PhotoImage(self.image)

        # Créer un label pour afficher l'image
        self.img_label = Label(self.master, image=self.photo_image, bg="white")
        self.img_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def list_consultations(self):
        patient_id = self.entry_id_patient.get()

        if not patient_id:
            messagebox.showerror("Erreur", "Veuillez entrer l'ID du patient.", parent=self.master)
            return

        else :
        
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
            val = [patient_id, self.user]
            # Requête pour obtenir les consultations du patient
            cursor.execute(""" 
                        SELECT 
                C.ID_CONSULTATION ,          
                S.DATE_SEANCE , 
                LIST(D.OPERATION, ', ') AS OPERATIONS,
                S.NUM_SEANCE 
            FROM 
                CONSULTATION C
            JOIN 
                DETAILLE_CONSULTATION D ON C.ID_CONSULTATION = D.ID_CONSULTATION
            JOIN 
                SEANCE S ON C.ID_CONSULTATION = S.ID_CONSULTATION
            WHERE 
                C.ID_PATIENT = ? AND C.ID_DENTISTE = ?
            GROUP BY
                           
                C.ID_CONSULTATION,S.DATE_SEANCE, S.NUM_SEANCE;

            """, val)

            # Vider la table existante
            for item in self.table_historique.get_children():
                self.table_historique.delete(item)

            # Remplir la table avec les consultations récupérées
            for consultation in cursor.fetchall():
                self.consultation_id = consultation[0]
                date_seance = consultation[1]
                operation = consultation[2]
                num_de_seance = consultation[3]
                # Ajout de l'entrée dans le tableau
                self.table_historique.insert('', 'end', values=(date_seance, operation, num_de_seance, "", 0))

            conn.close()

        

    def on_item_selected(self, event):
        # Récupérer l'élément sélectionné
        selected_item = self.table_historique.selection()
        if selected_item:
            # Récupérer l'opération de l'élément sélectionné
            operation_name = self.table_historique.item(selected_item, 'values')[1]
            date_seance = self.entry_date_seance.get_date()

            if not date_seance:
                messagebox.showerror("Erreur", "Veuillez saisir une date de séance.", parent=self.master)
                return

            # Incrémente le numéro de séance
            # Convertir la valeur du numéro de séance en entier avant d'incrémenter
            try:
                current_session_number = int(self.table_historique.item(selected_item, 'values')[2])
            except ValueError:
                # Si la conversion échoue, on initialise à 0
                current_session_number = 0

            session_number = current_session_number + 1

            # Ajout d'une nouvelle séance dans la base de données
            self.add_seance(self.consultation_id,  date_seance, session_number, operation_name)

            


    def add_seance(self, consultation_id,  date_seance, session_number, operation_name):
        # Ajouter la séance à la base de données
        
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
        # Vérification si la séance existe déjà
        cursor.execute("""
            SELECT COUNT(*) FROM SEANCE WHERE ID_CONSULTATION = ? AND NUM_SEANCE = ?
        """, (consultation_id, session_number))

        # Récupérer le résultat de la requête
        result = cursor.fetchone()

        if result[0] > 0:
            # Si la séance existe déjà, afficher un message d'erreur
            messagebox.showerror("Erreur", f"La séance numéro {session_number} existe déjà pour cette consultation.", parent=self.master)
            conn.close()
            return False  # Retourne False pour indiquer que la séance n'a pas été ajoutée

        else:
            # Insérer la nouvelle séance dans la base de données
            cursor.execute("""
                INSERT INTO SEANCE (ID_CONSULTATION,  NUM_SEANCE, DATE_SEANCE )
                VALUES (?, ?, ?)
            """, (consultation_id,  session_number, date_seance ))

        # Ajout de la nouvelle ligne dans le tableau
        self.table_historique.insert('', 'end', values=( date_seance, operation_name, session_number))    

        conn.commit()
        conn.close()

        

if __name__ == "__main__":
    root = tk.Tk()
    app = Seance(root)
    root.mainloop()
