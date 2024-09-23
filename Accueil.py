from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter.messagebox as mb
from openpyxl import Workbook
from openpyxl import load_workbook
import List_Patients as pt
import List_Jour as lj
import Consultation as cn
import Liste_consulation as ls
from tkinter import filedialog

class Accueil:
    def __init__(self, mast, autorisation):
        self.master = mast
        self.master.title("Accueil")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width, h=self.height))
        self.master.state("zoomed")
        
        self.autorisation = autorisation
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
        print(autorisation)

        state = ''
        if (autorisation == 0):
            state = DISABLED
        else:
            if (autorisation == 1):
                state = NORMAL    


        # Boutons existants
        self.buttonListePatient = ctk.CTkButton(self.framebody, text='Liste des Patients', command=self.patient, height=35, width=200,  font=('Helvetica', 18), cursor='cross')
        self.buttonListePatient.grid(row=0, column=0,padx=200, pady=100)
        
        self.buttonListJour = ctk.CTkButton(self.framebody, text='Listes des rendez-vous', command=self.jour, height=35, width=200,  font=('Helvetica', 18), cursor='cross', state=state)
        self.buttonListJour.grid(row=1, column=0,padx=200, pady=50)

        # Nouveau bouton 1 : Consultation
        self.buttonConsultation = ctk.CTkButton(self.framebody, text='Gestion des Consultations', command=self.consultation, height=35, width=200, font=('Helvetica', 18), cursor='cross', state=state)
        self.buttonConsultation.grid(row=0, column=1,padx=50, pady=100)

        # Nouveau bouton 2 : Historique des consultations
        self.buttonHistorique = ctk.CTkButton(self.framebody, text='Listes des Consultations', command=self.historique, height=35, width=200, font=('Helvetica', 18), cursor='cross')
        self.buttonHistorique.grid(row=1, column=1,padx=50, pady=50)

    # Fonction pour gérer le clic sur le bouton "Liste Patients"
    def patient(self):
        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = pt.List_Patients(win)

    # Fonction pour gérer le clic sur le bouton "List jour et rendez-vous"
    def jour(self):
        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = lj.List_Jour(win)      

    # Fonction pour gérer le clic sur le bouton "Consultations"
    def consultation(self):
        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = cn.Consultation(win)

    # Fonction pour gérer le clic sur le bouton "Historique Consultations"
    def historique(self):
        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = ls.List_consultation(win, autorisation=self.autorisation)
    




if __name__ == '__main__':
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Accueil(window)
    mainloop()
