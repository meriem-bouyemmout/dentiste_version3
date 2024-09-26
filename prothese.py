import tkinter as tk
from tkinter import ttk

def update_options(*args):
    prothese_type = prothese_combobox.get()
    if prothese_type == "Partielle":
        sous_options = ["Flexible", "Résine"]
    elif prothese_type == "Totale":
        sous_options = ["Simple", "Piezographie"]
    else:
        sous_options = []
    
    sous_combobox['values'] = sous_options
    sous_combobox.current(0) if sous_options else sous_combobox.set("")
    prix_label.config(text="")  # Réinitialise le prix à chaque changement

def update_sub_options(*args):
    sous_option = sous_combobox.get()
    if sous_option == "Flexible":
        choix_combobox['values'] = ["Haut (30 000)", "Bas (30 000)"]
    elif sous_option == "Résine":
        choix_combobox['values'] = ["Dent résine", "Dent composite"]
    else:
        choix_combobox['values'] = []
    
    choix_combobox.current(0) if choix_combobox['values'] else choix_combobox.set("")
    prix_label.config(text="")  # Réinitialise le prix à chaque changement

def update_resin_options(*args):
    resin_option = choix_combobox.get()
    if resin_option == "Dent résine":
        resin_combobox['values'] = ["Haut (25 000)", "Bas (25 000)"]
    elif resin_option == "Dent composite":
        resin_combobox['values'] = ["Haut (30 000)", "Bas (30 000)"]
    else:
        resin_combobox['values'] = []
    
    resin_combobox.current(0) if resin_combobox['values'] else resin_combobox.set("")
    prix_label.config(text="")  # Réinitialise le prix à chaque changement

def update_prix(*args):
    prothese_type = prothese_combobox.get()
    sous_option = sous_combobox.get()
    choix = choix_combobox.get()
    resin = resin_combobox.get()

    if choix == "Haut (30 000)" or choix == "Bas (30 000)":
        prix_label.config(text="Prix : 30 000")
    elif resin == "Haut (25 000)" or resin == "Bas (25 000)":
        prix_label.config(text="Prix : 25 000")
    elif resin == "Haut (30 000)" or resin == "Bas (30 000)":
        prix_label.config(text="Prix : 30 000")
    elif sous_option == "Simple":
        prix_label.config(text="Prix : 50 000")
    elif sous_option == "Piezographie":
        prix_label.config(text="Prix : 60 000")
    else:
        prix_label.config(text="")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Choix de la Prothèse")

# Label pour le type de prothèse
tk.Label(root, text="Prothèse Amovible :").grid(row=0, column=0)

# Menu déroulant pour le type de prothèse
prothese_combobox = ttk.Combobox(root, values=["Partielle", "Totale"])
prothese_combobox.grid(row=0, column=1)
prothese_combobox.bind("<<ComboboxSelected>>", update_options)

# Label pour sous-options
tk.Label(root, text="Type de Partielle / Totale :").grid(row=1, column=0)

# Menu déroulant pour les sous-options
sous_combobox = ttk.Combobox(root)
sous_combobox.grid(row=1, column=1)
sous_combobox.bind("<<ComboboxSelected>>", update_sub_options)

# Label pour les choix spécifiques
tk.Label(root, text="Choix Flexible / Résine :").grid(row=2, column=0)

# Menu déroulant pour les choix spécifiques
choix_combobox = ttk.Combobox(root)
choix_combobox.grid(row=2, column=1)
choix_combobox.bind("<<ComboboxSelected>>", update_resin_options)

# Label pour les options résine (Haut / Bas)
tk.Label(root, text="Options pour Résine :").grid(row=3, column=0)

# Menu déroulant pour les options résine
resin_combobox = ttk.Combobox(root)
resin_combobox.grid(row=3, column=1)
resin_combobox.bind("<<ComboboxSelected>>", update_prix)

# Label pour afficher le prix
prix_label = tk.Label(root, text="Prix : ")
prix_label.grid(row=4, column=1)

# Lancer la boucle principale
root.mainloop()
