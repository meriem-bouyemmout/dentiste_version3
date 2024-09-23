from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry  # Importer DateEntry de tkcalendar
import customtkinter as ctk
import fdb
import tkinter.messagebox as mb
import babel.numbers

class List_Jour:
    def __init__(self, mast):
        self.master = mast
        self.master.title("Les rendez-vous")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")
        self.master.configure(bg="#BCD2EE")  # Exemple pour un fond blanc
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")

        self.frame_rdv = ctk.CTkFrame(self.master, fg_color ="white", width=400, height=400)
        self.frame_rdv.grid(row=0, column=0, padx=20, pady=20)

        self.label_date = ctk.CTkLabel(self.frame_rdv, text="Saisir la Date")
        self.label_date.grid(row=0, column=0, padx=10, pady=10)

        self.entry_date = DateEntry(self.frame_rdv, date_pattern="dd/mm/yyyy", width=15)
        self.entry_date.grid(row=0, column=1, padx=10, pady=10)

        self.valider_date_button = ctk.CTkButton(self.frame_rdv, text="Valider la Date", command=self.valider_date)
        self.valider_date_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.label_id = ctk.CTkLabel(self.frame_rdv, text="ID du Patient",font=('Helvetica',15))
        self.label_id.grid(row=2, column=0, padx=10, pady=10)

        # Combobox pour sélectionner l'ID du patient
        self.combo_id = ttk.Combobox(self.frame_rdv, values=self.get_patient_ids(), state="readonly")
        self.combo_id.grid(row=2, column=1, padx=10, pady=10)
        self.combo_id.bind("<<ComboboxSelected>>", self.afficher_patient)

        # Labels pour afficher les informations du patient
        self.label_nom = ctk.CTkLabel(self.frame_rdv, text="Nom :",font=('Helvetica',15))
        self.label_nom.grid(row=3, column=0, padx=10, pady=10)
        self.label_prenom = ctk.CTkLabel(self.frame_rdv, text="Prénom :",font=('Helvetica',15))
        self.label_prenom.grid(row=4, column=0, padx=10, pady=10)
        self.label_tel = ctk.CTkLabel(self.frame_rdv, text="Numéro de Téléphone :",font=('Helvetica',15))
        self.label_tel.grid(row=5, column=0, padx=10, pady=10)

        self.nom_value = ctk.CTkLabel(self.frame_rdv, text="",font=('Helvetica',15))
        self.nom_value.grid(row=3, column=1, padx=10, pady=10)
        self.prenom_value = ctk.CTkLabel(self.frame_rdv, text="",font=('Helvetica',15))
        self.prenom_value.grid(row=4, column=1, padx=10, pady=10)
        self.tel_value = ctk.CTkLabel(self.frame_rdv, text="",font=('Helvetica',15))
        self.tel_value.grid(row=5, column=1, padx=10, pady=10)

        self.ajouter_patient_button = ctk.CTkButton(self.frame_rdv, text="Ajouter Patient", command=self.ajouter_patient)
        self.ajouter_patient_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.supprimer_patient_button = ctk.CTkButton(self.frame_rdv, text="Supprimer Patient", command=self.supprimer_patient)
        self.supprimer_patient_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
 

     
        # Deuxième frame pour valider les patients qui passent
        self.frame_validation = ctk.CTkFrame(self.master,fg_color="#BCD2EE", width=800, height=800)
        self.frame_validation.grid(row=0, column=1, padx=20, pady=20)

        self.label_validation = ctk.CTkLabel(self.frame_validation, text="Valider les Patients",text_color="white", font=('Helvetica',25,'bold'))
        self.label_validation.grid(row=0, column=0, padx=10, pady=10)

        # Tableau des patients ajoutés
        self.table_patients = ttk.Treeview(self.frame_validation, columns=("ID","Nom","Prenom","Num_tel", "Valider"), show='headings', height=20)
        self.table_patients.heading("ID", text="ID du Patient")
        self.table_patients.heading("Nom", text="Nom")
        self.table_patients.heading("Prenom", text="Prenom")
        self.table_patients.heading("Num_tel", text="Numero de telephone")
        self.table_patients.heading("Valider", text="Valider")

        self.table_patients.column("ID", width=100)  # Ajuster la largeur pour la colonne ID
        self.table_patients.column("Nom", width=120)
        self.table_patients.column("Prenom", width=120)
        self.table_patients.column("Num_tel", width=150)
        self.table_patients.column("Valider", width=100)  # Ajuster la largeur pour la colonne Valider
        self.table_patients.grid(row=1, column=0, padx=10, pady=10)

        self.valider_patient_button = ctk.CTkButton(self.frame_validation, text="Valider Patients",font=('Helvetica',15,'bold'), command=self.valider_patients)
        self.valider_patient_button.grid(row=2, column=0, padx=10, pady=10)

        




        self.patients_list = []
        self.validation_status = {}  # Dictionnaire pour stocker l'état de validation des patients

    def get_patient_ids(self):
        """ Récupère la liste des IDs de patients depuis la base de données """
        
        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()
            

        # Connexion à la base de données Firebird
        def read_fbclient_path(file_path='fb_client.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        database_path = read_database_path()
        fbclient_path = read_fbclient_path()


        conn = fdb.connect(
                dsn=database_path,
                user='SYSDBA',  # ou l'utilisateur configuré
                password='1234',  # ou le mot de passe configuré
                charset='UTF8',  # Utilisez le charset correspondant à votre base de données
                fb_library_name = fbclient_path  # Spécifiez le chemin complet vers fbclient.dll
        )
        cursor = conn.cursor()




        cursor.execute("SELECT ID FROM PATIENT")
        ids = [str(row[0]) for row in cursor.fetchall()]
        return ids

    
    def afficher_patient(self, event):
        """ Récupère les informations du patient et les affiche """
        patient_id = self.combo_id.get()
        # Connexion à la base de données Firebird

        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Connexion à la base de données Firebird
        def read_fbclient_path(file_path='fb_client.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        database_path = read_database_path()
        fbclient_path = read_fbclient_path() 

        conn = fdb.connect(
            dsn=database_path,
            user='SYSDBA',  # ou l'utilisateur configuré
            password='1234',  # ou le mot de passe configuré
            charset='UTF8',  # Utilisez le charset correspondant à votre base de données
            fb_library_name = fbclient_path  # Spécifiez le chemin complet vers fbclient.dll
        )
        cursor = conn.cursor()
        # Requête pour obtenir les informations du patient
        cursor.execute("SELECT NOM, PRENOM, NUM_TEL FROM Patient WHERE ID = ?", (patient_id,))
        patient_data = cursor.fetchone()

        if patient_data:
            # Afficher les informations dans les labels
            self.nom_value.configure(text=patient_data[0])
            self.prenom_value.configure(text=patient_data[1])
            self.tel_value.configure(text=patient_data[2])



    def valider_date(self):

        jour = self.entry_date.get() 

        self.entry_date.configure(state="disabled")
          # Rend le champ de la date grisé après validation
        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Connexion à la base de données Firebird
        def read_fbclient_path(file_path='fb_client.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        database_path = read_database_path()
        fbclient_path = read_fbclient_path() 

        conn = fdb.connect(
            dsn=database_path,
            user='SYSDBA',  # ou l'utilisateur configuré
            password='1234',  # ou le mot de passe configuré
            charset='UTF8',  # Utilisez le charset correspondant à votre base de données
            fb_library_name = fbclient_path  # Spécifiez le chemin complet vers fbclient.dll
        )
        cursor = conn.cursor()
        

        # Requête SQL pour récupérer les patients qui ont un rendez-vous à la date sélectionnée
        query = """
            SELECT PATIENT.ID, PATIENT.NOM, PATIENT.PRENOM, PATIENT.NUM_TEL, RENDEZ_VOUS.ETAT
            FROM PATIENT
            JOIN RENDEZ_VOUS ON RENDEZ_VOUS.ID_PATIENT = PATIENT.ID
            WHERE RENDEZ_VOUS.JOUR = ?
        """

        cursor.execute(query, (jour,))
        resultats = cursor.fetchall()

        # Effacer les anciennes données dans le tableau
        for item in self.table_patients.get_children():
            self.table_patients.delete(item)

        # Insérer les résultats dans le tableau
        for row in resultats:
            self.table_patients.insert("", "end", values=row)

        conn.close()



    def ajouter_patient(self):

        jour = self.entry_date.get()
        patient_id = self.combo_id.get()
        etat = "Non"

        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Connexion à la base de données Firebird
        def read_fbclient_path(file_path='fb_client.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        database_path = read_database_path()
        fbclient_path = read_fbclient_path() 

        conn = fdb.connect(
            dsn=database_path,
            user='SYSDBA',  # ou l'utilisateur configuré
            password='1234',  # ou le mot de passe configuré
            charset='UTF8',  # Utilisez le charset correspondant à votre base de données
            fb_library_name=fbclient_path  # Spécifiez le chemin complet vers fbclient.dll
        )
        cursor = conn.cursor()

        # Vérifier si le patient a déjà un rendez-vous pour ce jour
        cursor.execute("SELECT COUNT(*) FROM RENDEZ_VOUS WHERE ID_PATIENT = ? AND JOUR = ?", (patient_id, jour))
        rdv_count = cursor.fetchone()[0]

        if rdv_count > 0:
            # Afficher un message d'erreur si le patient a déjà un rendez-vous pour cette date
            mb.showerror('Erreur', 'Ce patient a déjà un rendez-vous pour cette date.', parent=self.master)
            conn.close()
            return

        # Requête pour obtenir les informations du patient
        cursor.execute("SELECT NOM, PRENOM, NUM_TEL FROM Patient WHERE ID = ?", (patient_id,))
        patient_data = cursor.fetchone()        

        if patient_id and patient_data:
            # Ajouter le patient dans le tableau
            item_id = self.table_patients.insert("", "end", values=(patient_id, patient_data[0], patient_data[1], patient_data[2], etat))
            self.patients_list.append(patient_id)

            # Initialiser la validation à "Non"
            self.validation_status[item_id] = False

            # Réinitialiser le champ ID
            self.combo_id.set("")

            # Ajouter le rendez-vous à la base de données
            val = (patient_id, 1, etat, jour)
            req = "INSERT INTO RENDEZ_VOUS (ID_PATIENT, ID_DENTISTE, ETAT, JOUR) VALUES (?, ?, ?, ?)"
            cursor.execute(req, val)
            conn.commit()
        else:
            if not patient_id:
                mb.showerror('Erreur', 'Veuillez saisir le ID du patient', parent=self.master)

        conn.close()


    def valider_patients(self):
        selected_items = self.table_patients.selection()
        
        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Connexion à la base de données Firebird
        def read_fbclient_path(file_path='fb_client.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        database_path = read_database_path()
        fbclient_path = read_fbclient_path() 

        conn = fdb.connect(
            dsn=database_path,
            user='SYSDBA',  # ou l'utilisateur configuré
            password='1234',  # ou le mot de passe configuré
            charset='UTF8',  # Utilisez le charset correspondant à votre base de données
            fb_library_name = fbclient_path  # Spécifiez le chemin complet vers fbclient.dll
        )
        cursor = conn.cursor()

        for item_id in selected_items:
            # Récupère les informations du patient sélectionné
            patient_values = self.table_patients.item(item_id)["values"]
            patient_id = patient_values[0]

            # Mise à jour dans la base de données Firebird
            query = "UPDATE RENDEZ_VOUS  SET ETAT = 'Oui' WHERE ID_PATIENT = ? AND JOUR = ?"
            jour = self.entry_date.get()  # Récupère la date saisie
            cursor.execute(query, (patient_id, jour))

            # Mise à jour de l'état dans l'interface (afficher "Oui" dans la colonne "ETAT")
            self.table_patients.item(item_id, values=(patient_values[0], patient_values[1], patient_values[2], patient_values[3], "Oui"))

            # Marquer comme validé dans le dictionnaire de statut
            self.validation_status[item_id] = True

        # Commit des changements dans la base de données
        conn.commit()
        conn.close()

        # Affichage de la validation dans la console (facultatif)
        for item_id, is_valid in self.validation_status.items():
            if is_valid:
                print(f"Patient validé : {self.table_patients.item(item_id)['values']}")
            else:
                print(f"Patient non validé : {self.table_patients.item(item_id)['values']}")
    

    
    def supprimer_patient(self):
        selected_items = self.table_patients.selection()

        if not selected_items:
            mb.showerror('Erreur', 'Veuillez sélectionner un patient à supprimer', parent=self.master)
            return

        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Connexion à la base de données Firebird
        def read_fbclient_path(file_path='fb_client.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        database_path = read_database_path()
        fbclient_path = read_fbclient_path()

        conn = fdb.connect(
            dsn=database_path,
            user='SYSDBA',  # ou l'utilisateur configuré
            password='1234',  # ou le mot de passe configuré
            charset='UTF8',  # Utilisez le charset correspondant à votre base de données
            fb_library_name=fbclient_path  # Spécifiez le chemin complet vers fbclient.dll
        )
        cursor = conn.cursor()

        for item_id in selected_items:
            # Récupère les informations du patient sélectionné
            patient_values = self.table_patients.item(item_id)["values"]
            patient_id = patient_values[0]
            jour = self.entry_date.get()

            # Suppression du patient de la base de données
            query = "DELETE FROM RENDEZ_VOUS WHERE ID_PATIENT = ? AND JOUR = ?"
            cursor.execute(query, (patient_id, jour))

            # Suppression du patient de l'interface
            self.table_patients.delete(item_id)

        # Commit des changements dans la base de données
        conn.commit()
        conn.close()

        
 







if (__name__ == '__main__'):
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = List_Jour(window)
    mainloop()
