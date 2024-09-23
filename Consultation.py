import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter.messagebox as mb
import customtkinter as ctk
from PIL import Image, ImageTk
import fdb
import babel.numbers  # Assure-toi d'utiliser le bon module pour accéder à ta base de données

class Consultation:
    def __init__(self, mast):
        self.master = mast
        self.master.title("Gestion des Consultations")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")
        self.master.configure(bg="white")  # Exemple pour un fond blanc
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")
        
        # Variables pour calcul automatique
        self.operations = []
        self.total = tk.DoubleVar(value=0)
        self.versement = tk.DoubleVar(value=0)
        self.reste = tk.DoubleVar(value=0)

        # Couleurs principales
        self.master.configure(bg="#F0F8FF")

        # Section Patient
        frame_patient = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_patient.pack(padx=10, pady=10, fill="x")

        label_patient = ctk.CTkLabel(frame_patient, text="ID du Patient:", font=("Arial", 15, 'bold'))
        label_patient.grid(row=0, column=0, padx=10, pady=5)

        self.entry_id_patient = ctk.CTkEntry(frame_patient, width=200)
        self.entry_id_patient.grid(row=0, column=1, padx=10, pady=5)

        btn_search_patient = ctk.CTkButton(frame_patient, text="Chercher", command=self.search_patient)
        btn_search_patient.grid(row=0, column=2, padx=10, pady=5)

        # Labels pour afficher les informations du patient
        self.label_nom = ctk.CTkLabel(frame_patient, text="", font=("Arial", 15, 'bold'))
        self.label_nom.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        self.label_prenom = ctk.CTkLabel(frame_patient, text="", font=("Arial", 15, 'bold'))
        self.label_prenom.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        self.label_age = ctk.CTkLabel(frame_patient, text="", font=("Arial", 15, 'bold'))
        self.label_age.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        # Section Date de Consultation
        frame_date = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_date.pack(padx=10, pady=10, fill="x")

        label_date = ctk.CTkLabel(frame_date, text="Date de Consultation:", font=("Arial", 15, 'bold'))
        label_date.grid(row=0, column=0, padx=10, pady=5)

        self.date_entry = DateEntry(frame_date, width=15, background='darkblue', foreground='white', borderwidth=2, year=2024)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        # Section Opérations
        frame_operations = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_operations.pack(padx=10, pady=10, fill="both", expand=True)

        label_operations = ctk.CTkLabel(frame_operations, text="Opérations effectuées:", font=("Arial", 15, 'bold'))
        label_operations.grid(row=0, column=0, padx=10, pady=5)

        self.table_operations = ttk.Treeview(frame_operations, columns=("Operation", "Prix"), show='headings')
        self.table_operations.heading("Operation", text="Opération")
        self.table_operations.heading("Prix", text="Prix")

        self.table_operations.column("Operation", width=300)
        self.table_operations.column("Prix", width=100)
        self.table_operations.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Boutons pour ajouter et supprimer des opérations
        btn_add_operation = ctk.CTkButton(frame_operations, text="Ajouter Opération", command=self.add_operation)
        btn_add_operation.grid(row=2, column=0, padx=10, pady=5)

        btn_delete_operation = ctk.CTkButton(frame_operations, text="Supprimer Opération", command=self.delete_operation)
        btn_delete_operation.grid(row=2, column=1, padx=10, pady=5)

 
        

       
        # Ajouter une image à droite de frame_operations
        self.image_path = "images\\tooth-1015404_640.jpg"  # Assure-toi que le chemin est correct
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((300, 317))
        self.photo_image = ImageTk.PhotoImage(self.image)





        label_image = tk.Label(frame_operations, image=self.photo_image, bg="#BCD2EE")
        label_image.grid(row=0, column=3, rowspan=3, padx=20, pady=10)        
        label_image.place(relx=1.0, rely=1.0, anchor="se", x=0, y=0)


        # Section Paiement
        frame_paiement = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_paiement.pack(padx=10, pady=10, fill="x")

        label_total = ctk.CTkLabel(frame_paiement, text="Montant Total:", font=("Arial", 15, 'bold'))
        label_total.grid(row=0, column=0, padx=10, pady=5)

        self.entry_total = ctk.CTkEntry(frame_paiement, width=100, textvariable=self.total, state='readonly')
        self.entry_total.grid(row=0, column=1, padx=10, pady=5)

        label_versement = ctk.CTkLabel(frame_paiement, text="Versement:", font=("Arial", 15, 'bold'))
        label_versement.grid(row=1, column=0, padx=10, pady=5)

        self.entry_versement = ctk.CTkEntry(frame_paiement, width=100, textvariable=self.versement)
        self.entry_versement.grid(row=1, column=1, padx=10, pady=5)
        self.entry_versement.bind("<KeyRelease>", self.update_reste)

        label_reste = ctk.CTkLabel(frame_paiement, text="Reste à payer:", font=("Arial", 15, 'bold'))
        label_reste.grid(row=2, column=0, padx=10, pady=5)

        self.entry_reste = ctk.CTkEntry(frame_paiement, width=100, textvariable=self.reste, state='readonly')
        self.entry_reste.grid(row=2, column=1, padx=10, pady=5)

        btn_confirm_consultation = ctk.CTkButton(frame_paiement, text="valider consultation", command=self.valider_consultation)
        btn_confirm_consultation.grid(row=1, column=3, padx=600, pady=5)

        # Prix fixes des opérations
        self.prix_operations = {
            "Consultation": 1000,
            "Extraction": 2000,
            "Extraction Adulte": 5000,
            "Extraction Adulte Difficile": 5000,
            "Extraction Dent Temporaire": 1500,
            "Détartrage": 6000,
            "Blanchiment": 3500,
            "Prothèse Partielle Flexible": 30000,
            "Prothèse Partielle Désinée": 25000,
            "Prothèse Flexible Haut": 30000,
            "Prothèse Flexible Bas": 30000,
            "Prothèse Désinée Haut": 25000,
            "Prothèse Désinée Bas": 25000,
            "Prothèse Composite Haut": 30000,
            "Prothèse Composite Bas": 30000
        }

    def search_patient(self):
        # Fonction pour rechercher et afficher les informations du patient
        patient_id = self.entry_id_patient.get()
        if patient_id:
            # Connexion à la base de données SQLite (à adapter selon ta base de données)
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
            
            # Requête pour récupérer les informations du patient
            cursor.execute("SELECT NOM, PRENOM, AGE FROM PATIENT WHERE ID = ?", (patient_id,))
            patient = cursor.fetchone()
            
            if patient:
                nom, prenom, age = patient
                self.label_nom.configure(text=f"Nom: {nom}")
                self.label_prenom.configure(text=f"Prénom: {prenom}")
                self.label_age.configure(text=f"Âge: {age}")
            else:
                self.label_nom.configure(text="Nom: Non trouvé")
                self.label_prenom.configure(text="Prénom: Non trouvé")
                self.label_age.configure(text="Âge: Non trouvé")
            
            conn.close()

    def add_operation(self):
        # Fonction pour ajouter une nouvelle opération
        new_window = tk.Toplevel(self.master)
        new_window.title("Ajouter une Opération")

        label_operation = tk.Label(new_window, text="Sélectionner une Opération:")
        label_operation.grid(row=0, column=0, padx=10, pady=5)

        # Dropdown pour les opérations fixes
        self.operation_var = tk.StringVar()
        operation_menu = tk.OptionMenu(new_window, self.operation_var, *self.prix_operations.keys())
        operation_menu.grid(row=0, column=1, padx=10, pady=5)

        btn_confirm = tk.Button(new_window, text="Ajouter", command=self.confirm_add_operation)
        btn_confirm.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def confirm_add_operation(self):
        # Ajoute l'opération sélectionnée à la table et met à jour le total
        operation = self.operation_var.get()
        if operation:
            prix = self.prix_operations[operation]
            self.table_operations.insert("", "end", values=(operation, prix))
            self.operations.append((operation, prix))
            self.update_total()

    def delete_operation(self):
        # Supprime l'opération sélectionnée et met à jour le total
        selected_item = self.table_operations.selection()
        if selected_item:
            # Récupérer les valeurs de l'opération sélectionnée (opération, prix)
            selected_values = self.table_operations.item(selected_item, 'values')
            operation = selected_values[0]
            prix = float(selected_values[1])

            # Supprime l'opération de la liste des opérations
            for i, (op, pr) in enumerate(self.operations):
                if op == operation and pr == prix:
                    del self.operations[i]
                    break

            # Supprime l'opération du tableau Treeview
            self.table_operations.delete(selected_item)

            # Met à jour le montant total et le reste à payer
            self.update_total()


    def update_total(self):
        # Met à jour le montant total en fonction des opérations ajoutées
        total = sum(prix for _, prix in self.operations)
        self.total.set(total)
        self.update_reste()

    def update_reste(self, *args):
        # Met à jour le reste à payer en fonction du versement
        reste = self.total.get() - self.versement.get()
        self.reste.set(reste)
 
    def valider_consultation(self):
        
        try:
            # Connexion à la base de données Firebird
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

            # 1. Insertion dans la table CONSULTATION
            id_patient = self.entry_id_patient.get()
            id_dentiste = 1  # Par exemple, tu peux définir l'ID du dentiste
            jour = self.date_entry.get_date()
            

            # Vérifie si le patient a déjà une consultation ce jour-là
            cursor.execute("""
                SELECT COUNT(*)
                FROM CONSULTATION
                WHERE ID_PATIENT = ? AND JOUR = ?
            """, (id_patient, jour))
            
            count = cursor.fetchone()[0]

            if count > 0:
                # Si le patient a déjà une consultation, afficher un message d'erreur
                mb.showerror("Erreur", "Ce patient a déjà une consultation pour cette date.")
                conn.close()
                return  



            cursor.execute("""
                INSERT INTO CONSULTATION (ID_PATIENT, ID_DENTISTE, JOUR) 
                VALUES (?, ?, ?)
            """, (id_patient, id_dentiste, jour))

            # Récupérer l'ID de la consultation nouvellement créée
            cursor.execute("SELECT ID_CONSULTATION FROM CONSULTATION ORDER BY ID_CONSULTATION DESC ROWS 1")
            id_consultation = cursor.fetchone()[0]

            # 2. Insertion dans la table DETAILLE_CONSULTATION pour chaque opération
            for operation, prix in self.operations:
                cursor.execute("""
                    INSERT INTO DETAILLE_CONSULTATION (ID_CONSULTATION, OPERATION, PRIX) 
                    VALUES (?, ?, ?)
                """, (id_consultation, operation, prix))

            # 3. Insertion dans la table PAYEMENT
            montant_total = self.total.get()
            versement = self.versement.get()
            reste = self.reste.get()

            cursor.execute("""
                INSERT INTO PAYEMENT (ID_CONSULTATION, MONTANT_TOTAL, VERSEMENT, RESTE)
                VALUES (?, ?, ?, ?)
            """, (id_consultation, montant_total, versement, reste))

            # Commit des transactions
            conn.commit()

            # Confirmation de la validation
            mb.showinfo('Succès',"Consultation valider", parent=self.master)

            # Fermer la connexion
            conn.close()

        except fdb.DatabaseError as e:
            print(f"Erreur lors de la validation : {e}")

        # Nettoyer tous les champs après validation
        self.entry_id_patient.delete(0, 'end')
        self.label_nom.configure(text="")
        self.label_prenom.configure(text="")
        self.label_age.configure(text="")
        self.table_operations.delete(*self.table_operations.get_children())  # Supprime toutes les lignes du tableau
        self.total.set(0)
        self.versement.set(0)
        self.reste.set(0)    



if __name__ == "__main__":
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Consultation(window)
    mainloop()
