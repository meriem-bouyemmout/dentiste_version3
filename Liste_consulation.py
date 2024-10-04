import fdb  # Assurez-vous que le module fdb est installé
import tkinter as tk
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

class List_consultation:
    def __init__(self, mast):
        self.master = mast
        self.master.title("Payement")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")
        self.master.configure(bg="white")  # Exemple pour un fond blanc
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")

        self.user = 1

        # Section Patient
        frame_patient = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_patient.pack(padx=10, pady=10, fill="x")

        label_patient = ctk.CTkLabel(frame_patient, text="ID du Patient:", font=("Arial", 14))
        label_patient.grid(row=0, column=0, padx=10, pady=5)

        self.entry_id_patient = ctk.CTkEntry(frame_patient, width=200)
        self.entry_id_patient.grid(row=0, column=1, padx=10, pady=5)

        # state = ''
        # if (autorisation == 0):
        #     state = DISABLED
        # else:
        #     if (autorisation == 1):
        #         state = NORMAL

        btn_search_patient = ctk.CTkButton(frame_patient, text="Chercher", command=self.search_consultations)
        btn_search_patient.grid(row=0, column=2, padx=10, pady=5)

        # Section Historique des Consultations
        frame_historique = ctk.CTkFrame(self.master, fg_color="#BCD2EE")
        frame_historique.pack(padx=10, pady=10, fill="both", expand=True)

        label_historique = ctk.CTkLabel(frame_historique, text="Historique des Consultations:", font=("Arial", 14))
        label_historique.grid(row=0, column=0, padx=10, pady=5)

        self.table_historique = ttk.Treeview(frame_historique, columns=("Date", "Operations", "Total", "Versement", "Reste"), show='headings', height=15)
        self.table_historique.heading("Date", text="Date de Consultation")
        self.table_historique.heading("Operations", text="Opérations")
        self.table_historique.heading("Total", text="Montant Total")
        self.table_historique.heading("Versement", text="Versement")
        self.table_historique.heading("Reste", text="Reste à Payer")

        self.table_historique.column("Date", width=150)
        self.table_historique.column("Operations", width=300)
        self.table_historique.column("Total", width=100)
        self.table_historique.column("Versement", width=100)
        self.table_historique.column("Reste", width=100)
        self.table_historique.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Bouton pour modifier le versement
        btn_modify_payment = ctk.CTkButton(frame_historique, text="Modifier Versement", command=self.modify_payment)
        btn_modify_payment.grid(row = 0,column = 1,padx=0, pady=20)

        # Ajouter l'image en bas à droite
        self.add_image_bottom_right()

    def add_image_bottom_right(self):
        # Charger l'image
        image_path = "images\\tooth-1015425_640.jpg"  # Assurez-vous que le chemin est correct
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200))  # Redimensionner l'image selon les besoins
        self.photo_image = ImageTk.PhotoImage(self.image)

        # Utiliser CTkImage à la place de PhotoImage
        self.ctk_image = ctk.CTkImage(light_image=self.image, dark_image=self.image, size=(200, 200))

        # Créer un label pour afficher l'image
        self.img_label = ctk.CTkLabel(self.master, image=self.ctk_image, text="", bg_color="white")
        self.img_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def search_consultations(self):
        # Fonction pour rechercher et afficher l'historique des consultations à partir de l'ID du patient
        patient_id = self.entry_id_patient.get()

        if not patient_id:
            messagebox.showerror("Erreur", "Veuillez entrer l'ID du patient.", parent=self.master)
            return

        # Connexion à la base de données Firebird
        try:
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

            cursor.execute("""
                SELECT C.JOUR, LIST(D.OPERATION, ', ') AS operations, P.MONTANT_TOTAL, P.VERSEMENT, P.RESTE
                FROM CONSULTATION C
                JOIN DETAILLE_CONSULTATION D ON C.ID_CONSULTATION = D.ID_CONSULTATION
                JOIN PAYEMENT P ON C.ID_CONSULTATION = P.ID_CONSULTATION
                WHERE C.ID_PATIENT = ? AND C.ID_DENTISTE = ?
                GROUP BY C.JOUR, P.MONTANT_TOTAL, P.VERSEMENT, P.RESTE
            """, val)

            # Récupérer toutes les consultations
            consultations = cursor.fetchall()

            # Vider la table existante
            for item in self.table_historique.get_children():
                self.table_historique.delete(item)

            # Remplir la table avec les données de la base
            for consultation in consultations:
                date_consultation = consultation[0]
                operations = consultation[1]
                total = consultation[2]
                versement = consultation[3]
                reste = consultation[4]

                self.table_historique.insert('', 'end', values=(
                    date_consultation, operations, f"{total:.2f}",
                    f"{versement:.2f}", f"{reste:.2f}"))

            conn.close()

        except fdb.Error as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de la connexion à la base de données : {str(e)}")

    def modify_payment(self):
        selected_item = self.table_historique.selection()

        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une consultation pour modifier le versement.", parent=self.master)
            return

        # Récupérer les informations de la consultation sélectionnée
        consultation_values = self.table_historique.item(selected_item[0], 'values')
        current_versement = float(consultation_values[3])
        total_amount = float(consultation_values[2])

        # Créer une nouvelle fenêtre pour modifier le versement
        new_window = tk.Toplevel(self.master)
        new_window.title("Modifier le Versement")

        label_new_payment = tk.Label(new_window, text="Nouveau Versement:")
        label_new_payment.grid(row=0, column=0, padx=10, pady=5)

        new_payment_entry = tk.Entry(new_window)
        new_payment_entry.grid(row=0, column=1, padx=10, pady=5)
        new_payment_entry.insert(0, current_versement)

        btn_save_payment = tk.Button(new_window, text="Sauvegarder", command=lambda: self.save_new_payment(new_payment_entry.get(), total_amount, selected_item, new_window))
        btn_save_payment.grid(row=1, column=1, padx=10, pady=5)

        return new_payment_entry.get()

    def save_new_payment(self, new_versement, total_amount, selected_item, window):
        try:
            new_versement = float(new_versement)
            reste = total_amount - new_versement

            patient_id = self.entry_id_patient.get()

            # Récupération des informations de la consultation sélectionnée
            consultation_date = self.table_historique.item(selected_item[0], 'values')[0]

            # Connexion à la base de données Firebird
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

            # Mise à jour dans la base de données (table PAYEMENT)
            cursor.execute("""
            UPDATE PAYEMENT P
            SET P.VERSEMENT = ?, P.RESTE = ?
            WHERE P.ID_CONSULTATION = (
                SELECT C.ID_CONSULTATION
                FROM CONSULTATION C
                WHERE C.JOUR = ? AND C.ID_PATIENT = ?
            )
        """, (new_versement, reste, consultation_date, patient_id))

            conn.commit()  # Valide les modifications dans la base de données
            conn.close()

            # Mise à jour dans l'interface
            self.table_historique.item(selected_item[0], values=(
                consultation_date,  # Date
                self.table_historique.item(selected_item[0], 'values')[1],  # Operations
                f"{total_amount:.2f}",                                      # Total
                f"{new_versement:.2f}",                                     # Versement
                f"{reste:.2f}"                                              # Reste
            ))

            window.destroy()

        except ValueError:
            messagebox.showerror("Erreur", "Le versement doit être un nombre valide.", parent= self.master)
        except fdb.Error as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de la mise à jour de la base de données : {str(e)}")




if __name__ == "__main__":
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = List_consultation(window)
    mainloop()
