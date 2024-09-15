import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import customtkinter as ctk

class ConsultationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Consultations")
        self.root.geometry("900x600")
        
        # Variables pour calcul automatique
        self.operations = []
        self.total = tk.DoubleVar(value=0)
        self.versement = tk.DoubleVar(value=0)
        self.reste = tk.DoubleVar(value=0)

        # Couleurs principales
        root.configure(bg="#F0F8FF")

        # Section Patient
        frame_patient = ctk.CTkFrame(self.root, fg_color="#E6E6FA")
        frame_patient.pack(padx=10, pady=10, fill="x")

        label_patient = ctk.CTkLabel(frame_patient, text="ID du Patient:", font=("Arial", 14))
        label_patient.grid(row=0, column=0, padx=10, pady=5)

        self.entry_id_patient = ctk.CTkEntry(frame_patient, width=200)
        self.entry_id_patient.grid(row=0, column=1, padx=10, pady=5)

        btn_search_patient = ctk.CTkButton(frame_patient, text="Chercher", command=self.search_patient)
        btn_search_patient.grid(row=0, column=2, padx=10, pady=5)

        # Section Date de Consultation
        frame_date = ctk.CTkFrame(self.root, fg_color="#FAF0E6")
        frame_date.pack(padx=10, pady=10, fill="x")

        label_date = ctk.CTkLabel(frame_date, text="Date de Consultation:", font=("Arial", 14))
        label_date.grid(row=0, column=0, padx=10, pady=5)

        self.date_entry = DateEntry(frame_date, width=15, background='darkblue', foreground='white', borderwidth=2, year=2024)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)

        # Section Opérations
        frame_operations = ctk.CTkFrame(self.root, fg_color="#FAF0E6")
        frame_operations.pack(padx=10, pady=10, fill="both", expand=True)

        label_operations = ctk.CTkLabel(frame_operations, text="Opérations effectuées:", font=("Arial", 14))
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

        # Section Paiement
        frame_paiement = ctk.CTkFrame(self.root, fg_color="#F5FFFA")
        frame_paiement.pack(padx=10, pady=10, fill="x")

        label_total = ctk.CTkLabel(frame_paiement, text="Montant Total:", font=("Arial", 14))
        label_total.grid(row=0, column=0, padx=10, pady=5)

        self.entry_total = ctk.CTkEntry(frame_paiement, width=100, textvariable=self.total, state='readonly')
        self.entry_total.grid(row=0, column=1, padx=10, pady=5)

        label_versement = ctk.CTkLabel(frame_paiement, text="Versement:", font=("Arial", 14))
        label_versement.grid(row=1, column=0, padx=10, pady=5)

        self.entry_versement = ctk.CTkEntry(frame_paiement, width=100, textvariable=self.versement)
        self.entry_versement.grid(row=1, column=1, padx=10, pady=5)
        self.entry_versement.bind("<KeyRelease>", self.update_reste)

        label_reste = ctk.CTkLabel(frame_paiement, text="Reste à payer:", font=("Arial", 14))
        label_reste.grid(row=2, column=0, padx=10, pady=5)

        self.entry_reste = ctk.CTkEntry(frame_paiement, width=100, textvariable=self.reste, state='readonly')
        self.entry_reste.grid(row=2, column=1, padx=10, pady=5)

        # Prix fixes des opérations
        self.prix_operations = {
            "Consultation": 1000,
            "Extraction": 2000,
            "Extraction Adulte": 5000,
            "Extraction Adulte Difficile": 5000,
            "Extraction Dent Temporaire": 1500,
            "Détartrage": 6000,
            "Blanchiment": 3500
        }

    def search_patient(self):
        # Fonction pour rechercher et afficher les informations du patient
        pass

    def add_operation(self):
        # Fonction pour ajouter une nouvelle opération
        new_window = tk.Toplevel(self.root)
        new_window.title("Ajouter une Opération")

        label_operation = tk.Label(new_window, text="Sélectionner une Opération:")
        label_operation.grid(row=0, column=0, padx=10, pady=5)

        # Dropdown pour les opérations fixes
        self.operation_var = tk.StringVar()
        operation_menu = tk.OptionMenu(new_window, self.operation_var, *self.prix_operations.keys())
        operation_menu.grid(row=0, column=1, padx=10, pady=5)

        btn_save = tk.Button(new_window, text="Ajouter", command=lambda: self.save_operation(self.operation_var.get(), new_window))
        btn_save.grid(row=1, column=1, padx=10, pady=5)

    def save_operation(self, operation, window):
        if operation:
            price = self.prix_operations[operation]
            self.operations.append((operation, price))
            self.table_operations.insert('', 'end', values=(operation, f"{price:.2f}"))
            self.update_total()
            window.destroy()

    def delete_operation(self):
        selected_item = self.table_operations.selection()
        if selected_item:
            for item in selected_item:
                values = self.table_operations.item(item, "values")
                self.operations.remove((values[0], float(values[1])))
                self.table_operations.delete(item)
            self.update_total()

    def update_total(self):
        total_price = sum(price for _, price in self.operations)
        self.total.set(total_price)
        self.update_reste()

    def update_reste(self, event=None):
        try:
            versement = float(self.versement.get())
            reste = self.total.get() - versement
            self.reste.set(reste)
        except ValueError:
            self.reste.set(self.total.get())

if __name__ == "__main__":
    root = ctk.CTk()
    app = ConsultationApp(root)
    root.mainloop()
