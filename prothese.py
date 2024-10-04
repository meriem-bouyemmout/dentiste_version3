from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk


class MyWindow:
    def __init__(self, mast):
        self.mast = mast
        self.mast.title("Fenêtre principale")
        self.mast.geometry("10x10")
        self.modele_dentaire()

    def modele_dentaire(self):
        # Créer la fenêtre principale
        def show_tooth_number(tooth_number):
            messagebox.showinfo("THOOTH",f"you put on {tooth_number}")

        root = tk.Toplevel(self.mast)
        root.title("Modèle d'anatomie dentaire")
        root.resizable(False, False)

        # Charger l'image du schéma dentaire
        image_path = "images/42484894-les-dents-primaires-modèle-de-la-bouche-avec-des-enfants-mâchoire-supérieure-et-inférieure-et-ses.jpg"  # Remplacer avec le chemin vers l'image
        image = Image.open(image_path)
        image = image.resize((400, 600))  # Ajuster la taille de l'image si nécessaire
        self.photo = ImageTk.PhotoImage(image)



        # Créer un canevas pour afficher l'image
        canvas = tk.Canvas(root, width=400, height=600)
        canvas.pack()

        # Afficher l'image sur le canevas
        canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Positions des boutons (tu devras ajuster les coordonnées en fonction de l'image)
        teeth_positions = {
            # HAUT
            
            4: (80, 245),
            5: (90, 200),
            6: (110,170),
            7: (135,145),
            8: (170,130),
            9: (210,130),
            10:(245,145),
            11:(270,170),
            12:(285,200),
            13:(300,245),
            
            # BAS
            
            29:(80, 355),
            28:(95, 395),
            27:(115,435),
            26:(145,460),
            25:(175,470),
            24:(205,470),
            23:(235,460),
            22:(265,435),
            21:(285,395),
            20:(300,355),
            
            
        }

        # Créer des boutons pour chaque dent
        for self.tooth_number, (x, y) in teeth_positions.items():
            button = tk.Button(root, text=f"{self.tooth_number}", command=lambda t=self.tooth_number: show_tooth_number(t))
            # Positionner chaque bouton au-dessus de la dent
            button.place(x=x, y=y, width=20, height=20)

# Créer et exécuter l'application
root = tk.Tk()
app = MyWindow(root)
root.mainloop()
