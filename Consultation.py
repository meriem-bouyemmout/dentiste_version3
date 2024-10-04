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

        self.user = 1
        
        # Variables pour calcul automatique
        self.operations = []
        self.seances = []
        self.operations_payement = []
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

        self.table_operations = ttk.Treeview(frame_operations, columns=("Operation", "Prix", "Seance"), show='headings')
        self.table_operations.heading("Operation", text="Opération")
        self.table_operations.heading("Prix", text="Prix")
        self.table_operations.heading("Seance", text="Séance")

        self.table_operations.column("Operation", width=300)
        self.table_operations.column("Prix", width=100)
        self.table_operations.column("Seance", width=100)
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
            "Extraction DDS" : 5000,
            "Extraction Adulte Difficile": 5000,
            "Extraction Temporaire": 1500,
            "Détartrage": 6000,
            "Blanchiment": 3500,
            "Traitement Radiculaire Pluriradiculaire": 8000,
            "Traitement Canalaire Adulte": 7000,
            "Traitement Canalaire Temporaire": 7000,
            "Gouttière": 6000,
            "Alvéolite": 4000,
            "Réparation de facette": 4000,
            "Scellement de bridge": 3000, 
            "Prothèse Amovible Partielle Flexible Haut": 30000,
            "Prothèse Amovible Partielle Flexible Bas": 30000,
            "Prothèse Amovible Partielle Résinée Dent Résinée Haut": 25000,
            "Prothèse Amovible Partielle Résinée Dent Résinée Bas": 25000,
            "Prothèse Amovible Partielle Résinée Dent Composite Haut": 30000,
            "Prothèse Amovible Partielle Résinée Dent Composite Bas": 30000,
            "Prothèse Amovible Totale Simple Haut": 25000,
            "Prothèse Amovible Totale Simple Bas": 25000,
            "Prothèse Amovible Totale Piezographie Haut": 30000,
            "Prothèse Amovible Totale Piezographie Bas": 30000,
            "Prothèses Fixes" : 0,
            "Soin Composite Dent Antérieure Adulte": 0,
            "Soin Composite Dent Postérieure Adulte": 0,
            "Soin Composite Dent Antérieure Temporaire": 0,
            "Soin Composite Dent Postérieure Temporaire": 0,   
            "Autre": 0
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
        # self.operation_var = tk.StringVar()
        # operation_menu = tk.OptionMenu(new_window, self.operation_var, *self.prix_operations.keys())
        # operation_menu.grid(row=0, column=1, padx=10, pady=5)

        btn_confirm = tk.Button(new_window, text="Ajouter", command=lambda: self.show_menu(new_window))
        btn_confirm.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def show_menu(self, window):
        # Créer un menu déroulant
        menu_operations = Menu(window, tearoff=0)
        menu_operations.add_command(label="Consultation", command=lambda: self.confirm_add_operation("Consultation")) 
        menu_recent = Menu(menu_operations, tearoff=0)
        menu_recent.add_command(label="Adulte", command=lambda: self.confirm_add_operation("Extraction Adulte"))
        menu_recent.add_command(label="DDS", command=lambda: self.confirm_add_operation("Extraction DDS"))
        menu_recent.add_command(label="Adulte Difficile", command=lambda: self.confirm_add_operation("Extraction Adulte Difficile"))
        menu_recent.add_command(label="Temporaire", command=lambda: self.confirm_add_operation("Extraction Temporaire"))
        menu_operations.add_cascade(label="Extraction", underline=0, menu=menu_recent)
        menu_operations.add_command(label="Détartrage", command=lambda: self.confirm_add_operation("Détartrage"))
        menu_operations.add_command(label="Blanchiment", command=lambda: self.confirm_add_operation("Blanchiment"))
        menu_operations.add_command(label="Traitement Radiculaire Pluriradiculaire", command=lambda: self.confirm_add_operation("Traitement Radiculaire Pluriradiculaire"))
        menu_recent2 = Menu(menu_operations, tearoff=0)
        menu_recent2.add_command(label="Adulte", command=lambda: self.confirm_add_operation("Traitement Canalaire Adulte"))
        menu_recent2.add_command(label="Temporaire", command=lambda: self.confirm_add_operation("Traitement Canalaire Temporaire"))
        menu_operations.add_cascade(label="Traitement Canalaire", underline=0, menu=menu_recent2)
        menu_operations.add_command(label="Gouttière", command=lambda: self.confirm_add_operation("Gouttière"))
        menu_operations.add_command(label="Alvéolite", command=lambda: self.confirm_add_operation("Alvéolite"))
        menu_operations.add_command(label="Réparation de facette", command=lambda: self.confirm_add_operation("Réparation de facette"))
        menu_operations.add_command(label="Scellement de bridge", command=lambda: self.confirm_add_operation("Scellement de bridge"))
        ################################################################################################################
        menu_recent_petit_petit_petit = Menu(menu_operations, tearoff=0)
        menu_recent_petit_petit_petit.add_command(label="Haut", command=lambda: self.confirm_add_operation("Prothèse Amovible Partielle Résinée Dent Résinée Haut"))
        menu_recent_petit_petit_petit.add_command(label="Bas", command=lambda: self.confirm_add_operation("Prothèse Amovible Partielle Résinée Dent Résinée Bas"))
        menu_recent_petit_petit_petit2 = Menu(menu_operations, tearoff=0)
        menu_recent_petit_petit_petit2.add_command(label="Haut", command=lambda: self.confirm_add_operation("Prothèse Amovible Partielle Résinée Dent Composite Haut"))
        menu_recent_petit_petit_petit2.add_command(label="Bas", command=lambda: self.confirm_add_operation("Prothèse Amovible Partielle Résinée Dent Composite Bas"))

        menu_recent_petit_petit = Menu(menu_operations, tearoff=0)
        menu_recent_petit_petit.add_command(label="Haut", command=lambda: self.confirm_add_operation("Prothèse Amovible Partielle Flexible Haut"))
        menu_recent_petit_petit.add_command(label="Bas", command=lambda: self.confirm_add_operation("Prothèse Amovible Partielle Flexible Bas"))       
        menu_recent_petit_petit2 = Menu(menu_operations, tearoff=0)
        menu_recent_petit_petit2.add_cascade(label="Dent Résinée", underline=0, menu=menu_recent_petit_petit_petit)
        menu_recent_petit_petit2.add_cascade(label="Dent Composite", underline=0, menu=menu_recent_petit_petit_petit2)
        menu_recent_petit_petit3 = Menu(menu_operations, tearoff=0)
        menu_recent_petit_petit3.add_command(label="Haut", command=lambda: self.confirm_add_operation("Prothèse Amovible Totale Simple Haut"))
        menu_recent_petit_petit3.add_command(label="Bas", command=lambda: self.confirm_add_operation("Prothèse Amovible Totale Simple Bas"))
        menu_recent_petit_petit4 = Menu(menu_operations, tearoff=0)
        menu_recent_petit_petit4.add_command(label="Haut", command=lambda: self.confirm_add_operation("Prothèse Amovible Totale Piezographie Haut"))
        menu_recent_petit_petit4.add_command(label="Bas", command=lambda: self.confirm_add_operation("Prothèse Amovible Totale Piezographie Bas")) 

        menu_recent_petit = Menu(menu_operations, tearoff=0)
        menu_recent_petit.add_cascade(label="Flexible", underline=0, menu=menu_recent_petit_petit)
        menu_recent_petit.add_cascade(label="Résinée", underline=0, menu=menu_recent_petit_petit2)
        menu_recent_petit2 = Menu(menu_operations, tearoff=0)
        menu_recent_petit2.add_cascade(label="Simple", underline=0, menu=menu_recent_petit_petit3)
        menu_recent_petit2.add_cascade(label="Piezographie", underline=0, menu=menu_recent_petit_petit4)

        menu_recent3 = Menu(menu_operations, tearoff=0)
        menu_recent3.add_cascade(label="Partielle", underline=0, menu=menu_recent_petit)
        menu_recent3.add_cascade(label="Totale",  underline=0, menu=menu_recent_petit2)
        menu_operations.add_cascade(label="Prothèse Amovible", underline=0, menu=menu_recent3)

        menu_operations.add_command(label="Prothèses Fixes", command=lambda: self.confirm_add_operation("Prothèses Fixes"))
        ###############################################################################################################################################
        menu_recent3 = Menu(menu_operations, tearoff=0)
        menu_recent3.add_command(label="Adulte", command=lambda: self.confirm_add_operation("Soin Composite Dent Antérieure Adulte"))
        menu_recent3.add_command(label="Temporaire", command=lambda: self.confirm_add_operation("Soin Composite Dent Antérieure Temporaire"))
        menu_recent4 = Menu(menu_operations, tearoff=0)
        menu_recent4.add_command(label="Adulte", command=lambda: self.confirm_add_operation("Soin Composite Dent Postérieure Adulte"))
        menu_recent4.add_command(label="Temporaire", command=lambda: self.confirm_add_operation("Soin Composite Dent Postérieure Temporaire"))

        menu_operations.add_cascade(label="Soin Composite Dent Antérieure", underline=0, menu=menu_recent3)
        menu_operations.add_cascade(label="Soin Composite Dent Postérieure", underline=0, menu=menu_recent4)

        menu_operations.add_command(label="Autre", command=lambda: self.confirm_add_operation("Autre"))

        # Afficher le menu déroulant à la position actuelle du pointeur de la souris
        menu_operations.post(window.winfo_pointerx(), window.winfo_pointery())    

    def confirm_add_operation(self, o):

        operation = o
        ID_patient = self.entry_id_patient.get()

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

        val = [operation, ID_patient]

        cursor.execute("""
            SELECT MAX(S.NUM_SEANCE) FROM SEANCE S
            JOIN DETAILLE_CONSULTATION D ON S.ID_DETAILLE_CONSULTATION = D.ID_DETAILLE_CONSULTATION
            JOIN CONSULTATION C ON D.ID_CONSULTATION = C.ID_CONSULTATION
            JOIN PATIENT P ON C.ID_PATIENT = P.ID
            WHERE D.OPERATION = ? AND P.ID = ?                                 

        """, val)

        num_seance = cursor.fetchone()[0]
        print(num_seance)
        if num_seance is None:
        # Si aucune séance n'existe encore pour cette consultation, démarrer à 1
            seance = 1
        else:
            # Incrémenter le numéro de séance
            seance = num_seance + 1
        
        
        if operation == "Autre" :
            self.manual_entry_window()
        else:
            if operation == "Soin Composite Dent Antérieure Adulte" or operation == "Soin Composite Dent Postérieure Adulte" :
                self.modele_dentaire(operation)
            else:
                if operation == "Prothèses Fixes" :
                    self.prothse_fixi()
                else:    
                    if operation :
                            
                        prix = self.prix_operations[operation]
                        # self.open_seance_window(prix, operation)
                        self.table_operations.insert("", "end", values=(operation, prix, seance))
                        self.operations.append((operation, prix))
                        self.seances.append(seance)
                        if seance == 1:
                            self.operations_payement.append(prix)
                        
                        self.update_total()

    def open_seance_window(self, p, o):
        # Créer une fenêtre Toplevel
        toplevel = tk.Toplevel()
        toplevel.title("Saisie Séance")
        
        # Texte d'instruction
        label = ttk.Label(toplevel, text="Sélectionnez le numéro de la séance (1 à 5) :")
        label.pack(pady=10)

        # Combobox pour la sélection du numéro de séance
        combobox_seance = ttk.Combobox(toplevel, values=[1, 2, 3, 4, 5], state="readonly")
        combobox_seance.pack(pady=10)

        # Bouton pour valider la sélection
        def valider_seance():
            selected_seance = combobox_seance.get()
            self.table_operations.insert("", "end", values=(o, p, selected_seance))
            self.operations.append((o, p))
            self.update_total()

            toplevel.destroy()

        bouton_valider = ttk.Button(toplevel, text="Valider", command=valider_seance)
        bouton_valider.pack(pady=10)                    

    def manual_entry_window(self):
        # Créer une nouvelle fenêtre
        manual_window = Toplevel(self.master)
        manual_window.title("Saisie Manuelle")
        manual_window.config(bg="#f0f0f0")  # Fond de la fenêtre

        # Définir une police personnalisée
        # custom_font = font.Font(family="Arial", size=12)

        Label(manual_window, text="Nom de l'opération:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
        manual_operation = Entry(manual_window, font="Arial", bd=2, relief="solid", width=30)
        manual_operation.pack(pady=10)

        Label(manual_window, text="Prix:", bg="#f0f0f0", font="Arial").pack(pady=10)
        manual_price = Entry(manual_window, font="Arial", bd=2, relief="solid", width=30)
        manual_price.pack(pady=10)

        # Bouton pour soumettre les données
        submit_button = Button(manual_window, text="Soumettre", command=lambda: self.submit(manual_operation.get(), manual_price.get(), manual_window), bg="lightblue", fg="white", font="Arial")
        submit_button.pack(pady=15)
        submit_button.config(width=20)

    def submit(self,operation, prix, manual_window):
        seance = 1
        manual_window.destroy()
        prix = float(prix)
        self.open_seance_window(prix, operation)
        self.table_operations.insert("", "end", values=(operation, prix, seance))
        self.operations.append((operation, prix, seance))
        self.update_total()
        

    def modele_dentaire(self, operation):
        # Créer la fenêtre principale
        def show_tooth_number(operation,tooth_number):
            ID_patient = self.entry_id_patient.get()
            operation = f"{operation} {tooth_number}" 

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

            val = [operation, ID_patient]

            cursor.execute("""
                SELECT MAX(S.NUM_SEANCE) FROM SEANCE S
                JOIN DETAILLE_CONSULTATION D ON S.ID_DETAILLE_CONSULTATION = D.ID_DETAILLE_CONSULTATION
                JOIN CONSULTATION C ON D.ID_CONSULTATION = C.ID_CONSULTATION
                JOIN PATIENT P ON C.ID_PATIENT = P.ID
                WHERE D.OPERATION = ? AND P.ID = ?                                 

            """, val)

            num_seance = cursor.fetchone()[0]
            if num_seance is None:
            # Si aucune séance n'existe encore pour cette consultation, démarrer à 1
                seance = 1
            else:
                # Incrémenter le numéro de séance
                seance = num_seance + 1
            
            prix = "5000"
            prix = float(prix)
            self.table_operations.insert("", "end", values=(operation, prix, seance))
            self.operations.append((operation, prix))
            self.seances.append(seance)
            if seance == 1:
                self.operations_payement.append(prix)            
            self.update_total()

        root = Toplevel(self.master)
        root.title("Modèle d'anatomie dentaire")
        root.resizable(False, False)

        # Charger l'image du schéma dentaire
        image_path = "images/dents-machoire-superieure-inferieure-pour-clinique-dentaire_268834-147.png"  # Remplacer avec le chemin vers l'image
        image = Image.open(image_path)
        image = image.resize((600, 600))  # Ajuster la taille de l'image si nécessaire
        self.photo = ImageTk.PhotoImage(image)



        # Créer un canevas pour afficher l'image
        canvas = tk.Canvas(root, width=600, height=600)
        canvas.pack()

        # Afficher l'image sur le canevas
        canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Positions des boutons (tu devras ajuster les coordonnées en fonction de l'image)
        teeth_positions = {
            # HAUT
            18: (155, 255),
            17: (160, 217),
            16: (170, 175),
            15: (180, 140),
            14: (190, 110),
            13: (210, 80),
            12: (235, 60),
            11: (270, 55),
            21: (310, 55),
            22: (345, 60),
            23: (370, 80),
            24: (385, 110),
            25: (400, 140),
            26: (410, 175),
            27: (420, 217),
            28: (425, 255),
            # BAS
            48: (165, 345),
            47: (170, 385),
            46: (175, 425),
            45: (190, 455),
            44: (200, 485),
            43: (225, 510),
            42: (250, 525),
            41: (275, 535),
            31: (305, 535),
            32: (330, 525),
            33: (357, 510),
            34: (380, 485),
            35: (390, 455),
            36: (407, 425),
            37: (412, 385),
            38: (417, 345)
            
        }

        # Créer des boutons pour chaque dent
        for self.tooth_number, (x, y) in teeth_positions.items():
            button = tk.Button(root, text=f"{self.tooth_number}", command=lambda t=self.tooth_number: show_tooth_number(operation,t))
            # Positionner chaque bouton au-dessus de la dent
            button.place(x=x, y=y, width=20, height=20)


    def prothse_fixi(self):
        protheses_fixees = {
            "résine": 10000,
            "céramique": 20000,
            "zircone": 40000
        }
            
        toplevel = tk.Toplevel(self.master)
        toplevel.title("Gestion des Prothèses Fixes")

        label_prothese = tk.Label(toplevel, text="Type de prothèse:")
        label_prothese.pack()

        combobox_prothese = ttk.Combobox(toplevel, values=list(protheses_fixees.keys()), state="readonly")
        combobox_prothese.pack()

        label_nombre = tk.Label(toplevel, text="Nombre d'éléments:")
        label_nombre.pack()

        entry_nombre = tk.Entry(toplevel)
        entry_nombre.pack()

        

        def ajouter_prothese():
        # Permet d'utiliser la variable totale définie dans la fonction englobante
            type_prothese = combobox_prothese.get().strip().lower()
            try:
                nombre_elements = int(entry_nombre.get())
                if type_prothese in protheses_fixees:
                    # Calculer le coût et mettre à jour le total
                    cout = protheses_fixees[type_prothese] * nombre_elements
                    

                    # Afficher le coût total
                    operation = f"{type_prothese} de {nombre_elements} elements"
                    prix = float(cout)

                    self.operations.append((operation, prix))
                    self.table_operations.insert("", "end", values=(operation, prix))            
                    self.update_total() 



                    # Réinitialiser les champs
                    combobox_prothese.delete(0, tk.END)
                    entry_nombre.delete(0, tk.END)
                else:
                    mb.showerror("Erreur", "Type de prothèse invalide.", parent=self.master)
            except ValueError:
                mb.showerror("Erreur", "Veuillez entrer un nombre valide d'éléments.", parent=self.master)

        bouton_ajouter = tk.Button(toplevel, text="Ajouter Prothèse", command=ajouter_prothese)
        bouton_ajouter.pack()
    

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
        total = sum(float(prix) for prix in self.operations_payement)
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
            id_dentiste = self.user  # Par exemple, tu peux définir l'ID du dentiste
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
                mb.showerror("Erreur", "Ce patient a déjà une consultation pour cette date.", parent=self.master)
                conn.close()
                return  



            cursor.execute("""
                INSERT INTO CONSULTATION (ID_PATIENT, ID_DENTISTE, JOUR) 
                VALUES (?, ?, ?)
            """, (id_patient, id_dentiste, jour))

            # Récupérer l'ID de la consultation nouvellement créée
            cursor.execute("SELECT ID_CONSULTATION FROM CONSULTATION ORDER BY ID_CONSULTATION DESC ROWS 1")
            id_consultation = cursor.fetchone()[0]
            detaille_ids = []
            # 2. Insertion dans la table DETAILLE_CONSULTATION pour chaque opération
            for operation, prix in self.operations:
                cursor.execute("""
                    INSERT INTO DETAILLE_CONSULTATION (ID_CONSULTATION, OPERATION, PRIX) 
                    VALUES (?, ?, ?) RETURNING ID_DETAILLE_CONSULTATION
                """, (id_consultation, operation, prix))
                # Récupérer l'ID_DETAILLE_CONSULTATION retourné par la requête
                inserted_id = cursor.fetchone()[0]
                
                # Ajouter cet ID à la liste
                detaille_ids.append(inserted_id)

            cursor.execute("SELECT ID_CONSULTATION FROM CONSULTATION ORDER BY ID_CONSULTATION DESC ROWS 1")
            id_consultation = cursor.fetchone()[0]    

            # 3. Insertion dans la table PAYEMENT
            montant_total = self.total.get()
            versement = self.versement.get()
            reste = self.reste.get()

            cursor.execute("""
                INSERT INTO PAYEMENT (ID_CONSULTATION, MONTANT_TOTAL, VERSEMENT, RESTE)
                VALUES (?, ?, ?, ?)
            """, (id_consultation, montant_total, versement, reste))

            for  id_detaille_consultation ,seance  in zip(detaille_ids, self.seances) :

                cursor.execute("""
                    INSERT INTO SEANCE (ID_DETAILLE_CONSULTATION, NUM_SEANCE, DATE_SEANCE)
                    VALUES (?, ?, ?)
                """, (id_detaille_consultation, seance, jour))

            # Commit des transactions
            conn.commit()

            # Confirmation de la validation
            mb.showinfo('Succès',"Consultation valider", parent=self.master)

            self.operations = []
            self.seances = []
            self.operations_payement = []
            

            self.entry_id_patient.delete(0, 'end')
            self.label_nom.configure(text="")
            self.label_prenom.configure(text="")
            self.label_age.configure(text="")
            self.table_operations.delete(*self.table_operations.get_children())  # Supprime toutes les lignes du tableau
            self.total.set(0)
            self.versement.set(0)
            self.reste.set(0)

            # Fermer la connexion
            conn.close()

        except fdb.DatabaseError as e:
            print(f"Erreur lors de la validation : {e}")

        # Nettoyer tous les champs après validation
            



if __name__ == "__main__":
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Consultation(window)
    mainloop()
