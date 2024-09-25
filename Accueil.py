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
    def __init__(self, mast):
        self.master = mast
        self.master.title("Accueil")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width, h=self.height))
        self.master.state("zoomed")
        
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
        # print(autorisation)

        # state = ''
        # if (autorisation == 0):
        #     state = DISABLED
        # else:
        #     if (autorisation == 1):
        #         state = NORMAL    

        image_path_list_patient = "images\\patient.png"
        image_list_patient = Image.open(image_path_list_patient)    
        image_list_patient = image_list_patient.resize((100, 100))
        photo_image_list_patient = ImageTk.PhotoImage(image_list_patient)

        image_path_calendrier = "images\\2688ff5e-727f-465e-a0b3-0243e7e6c28f.jpg"
        image_calendrier = Image.open(image_path_calendrier)    
        image_calendrier = image_calendrier.resize((100, 100))
        photo_image_calendrier = ImageTk.PhotoImage(image_calendrier)

        image_path_liste_des_actes = "images\\liste-de-controle.png"
        image_liste_des_actes = Image.open(image_path_liste_des_actes)    
        image_liste_des_actes = image_liste_des_actes.resize((100, 100))
        photo_image_list_des_actes = ImageTk.PhotoImage(image_liste_des_actes)

        image_path_liste_des_reglement = "images\\patient_sdoi.png"
        image_liste_des_reglement = Image.open(image_path_liste_des_reglement)    
        image_liste_des_reglement = image_liste_des_reglement.resize((100, 100))
        photo_image_list_des_reglement = ImageTk.PhotoImage(image_liste_des_reglement)

        image_path_liste_des_impayees = "images\\liste-de-prix.png"
        image_liste_des_impayees = Image.open(image_path_liste_des_impayees)    
        image_liste_des_impayees = image_liste_des_impayees.resize((100, 100))
        photo_image_list_des_impayees = ImageTk.PhotoImage(image_liste_des_impayees)


        self.buttonListePatient = ctk.CTkButton(self.framebody, image=photo_image_list_patient, compound="top", text='Liste des Patients', command=self.patient, height=35, width=200,  font=('Helvetica', 18), cursor='cross')
        self.buttonListePatient.grid(row=0, column=0,padx=5, pady=5)
        
        self.buttonListJour = ctk.CTkButton(self.framebody, text='Calendrier', image=photo_image_calendrier, compound="top", command=self.jour, height=35, width=200,  font=('Helvetica', 18), cursor='cross')
        self.buttonListJour.grid(row=0, column=1,padx=5, pady=5)

        # Nouveau bouton 1 : Consultation
        self.buttonConsultation = ctk.CTkButton(self.framebody, text='Liste des actes', image=photo_image_list_des_actes, compound="top", command=self.consultation, height=35, width=200, font=('Helvetica', 18), cursor='cross')
        self.buttonConsultation.grid(row=0, column=2,padx=5, pady=5)

        # Nouveau bouton 2 : Historique des consultations
        self.buttonHistorique = ctk.CTkButton(self.framebody, text='Règlement', command=self.historique, image=photo_image_list_des_reglement, compound="top", height=35, width=200, font=('Helvetica', 18), cursor='cross')
        self.buttonHistorique.grid(row=1, column=0,columnspan=2, padx=5, pady=5)

        self.buttonHistorique = ctk.CTkButton(self.framebody, text='Liste des impayées', command=self.historique,image=photo_image_list_des_impayees, compound="top", height=35, width=200, font=('Helvetica', 18), cursor='cross')
        self.buttonHistorique.grid(row=1, column=1,padx=5,columnspan=2, pady=5)

        # Réglage pour que les colonnes et lignes remplissent l'espace
        self.framebody.grid_columnconfigure(0, weight=1)
        self.framebody.grid_columnconfigure(1, weight=1)
        self.framebody.grid_columnconfigure(2, weight=1)
        self.framebody.grid_rowconfigure(0, weight=1)
        self.framebody.grid_rowconfigure(1, weight=1)

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
        uni = ls.List_consultation(win)
    




if __name__ == '__main__':
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Accueil(window)
    mainloop()
