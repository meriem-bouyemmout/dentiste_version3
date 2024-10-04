from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as mb
from openpyxl import Workbook
from openpyxl import load_workbook
import Liste_consulation as ls
import Seance as sc
from tkinter import filedialog

class Seance_payement:
    def __init__(self, mast, user):
        self.master = mast
        self.master.title("Reglement")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width, h=self.height))
        self.master.state("zoomed")

        self.user = user
        
        # self.autorisation = autorisation
        ####################################################################################################
        
        self.frametop = ctk.CTkFrame(self.master, fg_color="#BCD2EE", height=200)
        self.frametop.pack(fill=X)

        image_path = "images\\Dental Health Board Background, Teeth, Healthy, Dashboard Background Image And Wallpaper for Free Download.jpg"
        self.image = Image.open(image_path)
        self.image = self.image.resize((800, 200))    
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.imgDent = Label(self.frametop, image=self.photo_image)
        self.imgDent.pack(padx=0, pady=0)

        self.framebody = ctk.CTkFrame(self.master, fg_color="#BCD2EE", height=200)
        self.framebody.pack(fill="both", expand=True)
           

        image_path_list_patient = "images\\seance.png"
        image_list_patient = Image.open(image_path_list_patient)    
        image_list_patient = image_list_patient.resize((100, 100))
        photo_image_list_patient = ImageTk.PhotoImage(image_list_patient)

        image_path_calendrier = "images\\paiement-a-la-livraison.png"
        image_calendrier = Image.open(image_path_calendrier)    
        image_calendrier = image_calendrier.resize((100, 100))
        photo_image_calendrier = ImageTk.PhotoImage(image_calendrier)



        self.buttonListePatient = ctk.CTkButton(self.framebody, image=photo_image_list_patient, compound="top", text='Seance', command=self.patient, height=35, width=200,  font=('Helvetica', 18), cursor='cross')
        self.buttonListePatient.grid(row=0, column=0,padx=5, pady=150)
        
        self.buttonListJour = ctk.CTkButton(self.framebody, text='Payement', image=photo_image_calendrier, compound="top", command=self.jour, height=35, width=200,  font=('Helvetica', 18), cursor='cross')
        self.buttonListJour.grid(row=0, column=1,padx=5, pady=150)

        

        # Réglage pour que les colonnes et lignes remplissent l'espace
        self.framebody.grid_columnconfigure(0, weight=1)
        self.framebody.grid_columnconfigure(1, weight=1)
        

    # Fonction pour gérer le clic sur le bouton "Liste Patients"
    def patient(self):
        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = sc.Seance(win, self.user)

    # Fonction pour gérer le clic sur le bouton "List jour et rendez-vous"
    def jour(self):
        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = ls.List_consultation(win)      

        



if __name__ == '__main__':
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Seance_payement(window)
    mainloop()
