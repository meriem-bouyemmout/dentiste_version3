from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from PIL import Image,ImageTk
import tkinter.messagebox as mb
from openpyxl import Workbook
from openpyxl import load_workbook
import List_Patients as pt
import List_Jour as lj
from tkinter import filedialog 
  
class Accueil:
    def __init__(self,mast):
        self.master = mast
        self.master.title("Accueil")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")

    ####################################################################################################
        

        self.frametop = ctk.CTkFrame(self.master,fg_color="#BCD2EE",height=200)
        self.frametop.pack(fill=X)

        image_path = "images\\Dental Health Board Background, Teeth, Healthy, Dashboard Background Image And Wallpaper for Free Download.jpg"
        self.image = Image.open(image_path)
        self.image = self.image.resize((800, 200))    
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.imgDent = Label(self.frametop, image=self.photo_image)
        self.imgDent.pack( padx=0, pady =0)


        self.buttonListePatient=ctk.CTkButton(self.master, text='Liste Patients', command=self.patient, height=35, width=200,  font=('Helvetica',18), cursor='cross')
        self.buttonListePatient.place(x=200, y=300)
        self.buttonListJour=ctk.CTkButton(self.master, text='List jour et rendez-vous', command=self.jour,  height=35, width=200,  font=('Helvetica',18), cursor='cross')
        self.buttonListJour.place(x=200, y=450)

 
    def patient(self):

        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = pt.List_Patients(win)

    def jour(self):

        win = Toplevel()
        win.iconbitmap('images\\download.ico')
        uni = lj.List_Jour(win)      


if (__name__ == '__main__'):
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Accueil(window)
    mainloop()

        