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
    17:(165, 345),
    18:(170, 385),
    19:(175, 425),
    20:(190, 455),
    21:(200, 485),
    22:(225, 510),
    23:(250, 525),
    24:(275, 535),
    25:(305, 535),
    26:(330, 525),
    27:(357, 510),
    28:(380, 485),
    29:(390, 455),
    30:(407, 425),
    31:(412, 385),
    32:(417, 345)
    
}

# Créer des boutons pour chaque dent
for tooth_number, (x, y) in teeth_positions.items():
    button = tk.Button(root, text=f"{tooth_number}", command=lambda t=tooth_number: show_tooth_number(t))
    # Positionner chaque bouton au-dessus de la dent
    button.place(x=x, y=y, width=20, height=20)

# Lancer la fenêtre principale
root.mainloop()
