import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox

class HistoriqueConsultationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Historique des Consultations")
        self.root.geometry("900x600")

        # Couleur de fond
        root.configure(bg="#F0F8FF")

        # Section Patient
        frame_patient = ctk.CTkFrame(self.root, fg_color="#E6E6FA")
        frame_patient.pack(padx=10, pady=10, fill="x")

        label_patient = ctk.CTkLabel(frame_patient, text="ID du Patient:", font=("Arial", 14))
        label_patient.grid(row=0, column=0, padx=10, pady=5)

        self.entry_id_patient = ctk.CTkEntry(frame_patient, width=200)
        self.entry_id_patient.grid(row=0, column=1, padx=10, pady=5)

        btn_search_patient = ctk.CTkButton(frame_patient, text="Chercher", command=self.search_consultations)
        btn_search_patient.grid(row=0, column=2, padx=10, pady=5)

        # Section Historique des Consultations
        frame_historique = ctk.CTkFrame(self.root, fg_color="#FAF0E6")
        frame_historique.pack(padx=10, pady=10, fill="both", expand=True)

        label_historique = ctk.CTkLabel(frame_historique, text="Historique des Consultations:", font=("Arial", 14))
        label_historique.grid(row=0, column=0, padx=10, pady=5)

        self.table_historique = ttk.Treeview(frame_historique, columns=("Date", "Operations", "Total", "Versement", "Reste"), show='headings')
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
        btn_modify_payment = ctk.CTkButton(self.root, text="Modifier Versement", command=self.modify_payment)
        btn_modify_payment.pack(padx=10, pady=5)

    def search_consultations(self):
        # Fonction pour rechercher et afficher l'historique des consultations à partir de l'ID du patient
        patient_id = self.entry_id_patient.get()

        # Supposons que nous récupérions ces données à partir de la base de données
        self.consultations = [
            {"date": "2023-09-01", "operations": "Consultation, Extraction", "total": 3000, "versement": 2000, "reste": 1000},
            {"date": "2023-08-15", "operations": "Détartrage, Blanchiment", "total": 9500, "versement": 6000, "reste": 3500}
        ]

        # Clear existing rows
        for item in self.table_historique.get_children():
            self.table_historique.delete(item)

        # Populate table with consultation data
        for consultation in self.consultations:
            self.table_historique.insert('', 'end', values=(
                consultation["date"], consultation["operations"], f"{consultation['total']:.2f}",
                f"{consultation['versement']:.2f}", f"{consultation['reste']:.2f}"))

    def modify_payment(self):
        selected_item = self.table_historique.selection()

        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une consultation pour modifier le versement.")
            return

        # Récupérer les informations de la consultation sélectionnée
        consultation_values = self.table_historique.item(selected_item[0], 'values')
        current_versement = float(consultation_values[3])
        total_amount = float(consultation_values[2])

        # Créer une nouvelle fenêtre pour modifier le versement
        new_window = tk.Toplevel(self.root)
        new_window.title("Modifier le Versement")

        label_new_payment = tk.Label(new_window, text="Nouveau Versement:")
        label_new_payment.grid(row=0, column=0, padx=10, pady=5)

        new_payment_entry = tk.Entry(new_window)
        new_payment_entry.grid(row=0, column=1, padx=10, pady=5)
        new_payment_entry.insert(0, current_versement)

        btn_save_payment = tk.Button(new_window, text="Sauvegarder", command=lambda: self.save_new_payment(new_payment_entry.get(), total_amount, selected_item, new_window))
        btn_save_payment.grid(row=1, column=1, padx=10, pady=5)

    def save_new_payment(self, new_versement, total_amount, selected_item, window):
        try:
            new_versement = float(new_versement)
            reste = total_amount - new_versement

            # Mise à jour dans l'interface
            self.table_historique.item(selected_item[0], values=(
                self.table_historique.item(selected_item[0], 'values')[0],  # Date
                self.table_historique.item(selected_item[0], 'values')[1],  # Operations
                f"{total_amount:.2f}",                                      # Total
                f"{new_versement:.2f}",                                     # Versement
                f"{reste:.2f}"                                              # Reste
            ))

            window.destroy()

        except ValueError:
            messagebox.showerror("Erreur", "Le versement doit être un nombre valide.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = HistoriqueConsultationApp(root)
    root.mainloop()
