import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Fonction appelée lorsqu'une dent est cliquée
def show_tooth_number(tooth_number):
    messagebox.showinfo("Dent", f"Vous avez cliqué sur la dent {tooth_number}")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Modèle d'anatomie dentaire")

# Charger l'image du schéma dentaire
image_path = "images\\dents-machoire-superieure-inferieure-pour-clinique-dentaire_268834-147.png"  # Remplacer avec le chemin vers l'image
image = Image.open(image_path)
image = image.resize((600, 600))  # Ajuster la taille de l'image si nécessaire
photo = ImageTk.PhotoImage(image)



# Créer un canevas pour afficher l'image
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

# Afficher l'image sur le canevas
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Positions des boutons (tu devras ajuster les coordonnées en fonction de l'image)
teeth_positions = {
    1: (150, 250),
    2: (160, 210),
    3: (170, 170),
    4: (175, 135),
    5: (185, 105),
    6: (200, 75),
    7: (230, 55),
    8: (265, 45),
    9: ()
}

# Créer des boutons pour chaque dent
for tooth_number, (x, y) in teeth_positions.items():
    button = tk.Button(root, text=f"{tooth_number}", command=lambda t=tooth_number: show_tooth_number(t))
    # Positionner chaque bouton au-dessus de la dent
    button.place(x=x, y=y, width=30, height=30)

# Lancer la fenêtre principale
root.mainloop()
