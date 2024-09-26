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
    def __init__(self, mast, user):
        self.master = mast
        self.master.title("Gestion des Consultations")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")
        self.master.configure(bg="white")  # Exemple pour un fond blanc
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")

        self.user = user
        
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
            "Extraction DDS" : 5000,
            "Extraction Adulte Difficile": 5000,
            "Extraction Dent Temporaire": 1500,
            "Détartrage": 6000,
            "Blanchiment": 3500,
            "Traitement radiculaire pluriradiculaire": 8000,
            "Traitement canalaire": 7000,
            "Gouttière": 6000,
            "Alvéolite": 4000,
            "Réparation de facette": 4000,
            "Scellement de bridge": 3000, 
            "Prothèse Partielle Flexible Haut": 30000,
            "Prothèse Partielle Flexible Bas": 30000,
            "Prothèse Partielle Résinée Dent Résinée Haut": 25000,
            "Prothèse Partielle Résinée Dent Résinée Bas": 25000,
            "Prothèse Partielle Résinée Dent Composite Haut": 30000,
            "Prothèse Partielle Résinée Dent Composite Bas": 30000,
            "Prothèse Totale Simple Haut": 25000,
            "Prothèse Totale Simple Bas": 25000,
            "Prothèse Totale Piezographie Haut": 30000,
            "Prothèse Totale Piezographie Bas": 30000,
            "Soutien Composite Dent Antérieure": 0,
            "Soutien Composite Dent Postérieure": 0,
            "Prothèses Fixes" : 0,
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
        self.operation_var = tk.StringVar()
        operation_menu = tk.OptionMenu(new_window, self.operation_var, *self.prix_operations.keys())
        operation_menu.grid(row=0, column=1, padx=10, pady=5)

        btn_confirm = tk.Button(new_window, text="Ajouter", command=self.confirm_add_operation)
        btn_confirm.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def confirm_add_operation(self):
        # Ajoute l'opération sélectionnée à la table et met à jour le total
        operation = self.operation_var.get()
        if operation == "Autre" :
            self.manual_entry_window()
        else:
            if operation == "Soutien Composite Dent Antérieure" or operation == "Soutien Composite Dent Postérieure" :
                self.modele_dentaire(operation)
            else:
                if operation == "Prothèses Fixes" :
                    self.prothse_fixi()
                else:    
                    if operation :    
                        prix = self.prix_operations[operation]
                        self.table_operations.insert("", "end", values=(operation, prix))
                        self.operations.append((operation, prix))
                        self.update_total()

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
        submit_button = Button(manual_window, text="Soumettre", command=lambda: self.submit(manual_operation.get(), manual_price.get()), bg="lightblue", fg="white", font="Arial")
        submit_button.pack(pady=15)
        submit_button.config(width=20)

    def submit(self,operation, prix):
        # Traiter les données soumises
        prix = float(prix)
        self.operations.append((operation, prix))
        self.table_operations.insert("", "end", values=(operation, prix))            
        self.update_total()

    def modele_dentaire(self, operation):
        # Créer la fenêtre principale
        def show_tooth_number(operation,tooth_number):
            operation = f"{operation} {tooth_number}"
            prix = "5000"
            prix = float(prix)
            self.operations.append((operation, prix))
            self.table_operations.insert("", "end", values=(operation, prix))            
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
            1: (155, 255),
            2: (160, 217),
            3: (170, 175),
            4: (180, 140),
            5: (190, 110),
            6: (210, 80),
            7: (235, 60),
            8: (270, 55),
            9: (310, 55),
            10:(345, 60),
            11:(370, 80),
            12:(385, 110),
            13:(400, 140),
            14:(410, 175),
            15:(420, 217),
            16:(425, 255),
            # BAS
            32:(165, 345),
            31:(170, 385),
            30:(175, 425),
            29:(190, 455),
            28:(200, 485),
            27:(225, 510),
            26:(250, 525),
            25:(275, 535),
            24:(305, 535),
            23:(330, 525),
            22:(357, 510),
            21:(380, 485),
            20:(390, 455),
            19:(407, 425),
            18:(412, 385),
            17:(417, 345)
            
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

        combobox_prothese = ttk.Combobox(toplevel, values=list(protheses_fixees.keys()))
        combobox_prothese.pack()

        label_nombre = tk.Label(toplevel, text="Nombre d'éléments:")
        label_nombre.pack()

        entry_nombre = tk.Entry(toplevel)
        entry_nombre.pack()

        label_total = tk.Label(toplevel, text="Coût total: 0 DA")
        label_total.pack()

        total = 0  # Coût total

        def ajouter_prothese():
            nonlocal total  # Permet d'utiliser la variable totale définie dans la fonction englobante
            type_prothese = combobox_prothese.get().strip().lower()
            try:
                nombre_elements = int(entry_nombre.get())
                if type_prothese in protheses_fixees:
                    # Calculer le coût et mettre à jour le total
                    cout = protheses_fixees[type_prothese] * nombre_elements
                    total += cout

                    # Afficher le coût total
                    operation = f"{type_prothese} de {nombre_elements} elements"
                    prix = float(total)

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
        total = sum(float(prix) for _, prix in self.operations)
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

            cursor.execute("""
                INSERT INTO SEANCE (ID_CONSULTATION, NUM_SEANCE, DATE_SEANCE)
                VALUES (?, ?, ?)
            """, (id_consultation, 1, jour))

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
