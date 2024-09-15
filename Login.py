from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from PIL import Image,ImageTk
import sqlite3
import tkinter.messagebox as mb
import Accueil as Ac
import Profiles as Pro
import os




class Login :
    def __init__(self,mast):
        self.master = mast
        self.master.title("Page de connexion")
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")

        self.img = Image.open('images\\loginImage.png')
        self.img.thumbnail((200,200))
        self.new_img = ImageTk.PhotoImage(self.img)
        self.imgLogin = Label(self.master, image=self.new_img)
        self.imgLogin.pack(padx=50, pady = 50)

        self.frameLogin = ctk.CTkFrame(self.master,fg_color="#BCD2EE", width=100, height=100)
        self.frameLogin.pack()
        self.usernameLabel = ctk.CTkLabel(self.frameLogin, text = 'Username', pady=15, padx=25, font=('Helvetica',18))
        self.usernameLabel.grid(row=0, column=0)
        self.passwordLabel = ctk.CTkLabel(self.frameLogin, text = 'Password', pady=15, padx=25, font=('Helvetica',18))
        self.passwordLabel.grid(row=1, column=0)
        self.username = ctk.CTkEntry(self.frameLogin,  font=('tahoma',15,'bold'))
        self.username.configure(justify="center")
        self.username.grid(row=0, column=1, pady=15, padx=10)
        self.password = ctk.CTkEntry(self.frameLogin,  show='*', font=('tahoma',18,'bold'))
        self.password.configure(justify="center")
        self.password.grid(row=1, column=1, pady=15, padx=10)
        self.buttonLogin=ctk.CTkButton(self.frameLogin, text='Login', command=self.Login, height=35,  font=('Helvetica',18), cursor='cross')
        self.buttonLogin.grid(row=2, column=0, columnspan=2, sticky='snew', padx=10, pady=10)


    def Login(self):

        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Lire le chemin de la base de données depuis le fichier texte
        database_path = read_database_path()
        
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor() 

        req = " select * from Connexion where Nom = '"+self.username.get()+"' and Mot_de_passe = '"+self.password.get()+"' "
        cursor.execute(req)
        result = cursor.fetchone()

        def read_admin_path(file_path='admin.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()
            
        def read_password_path(file_path='password.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()    
        
        admin_path = read_admin_path()
        password_path = read_password_path()


        if(self.username.get() == admin_path and self.password.get() == password_path ) :
                win = Toplevel()
                win.iconbitmap('images\\download.ico')
                uni = Pro.Profiles(win)
                self.username.delete(0,'end')
                self.password.delete(0,'end')


        else:
            if (result == None) :
                mb.showerror('Erreur','nom ou mot de passe invalider')  
           
            
          

            else :         
                self.master.destroy()  
                win = ctk.CTk()
                win.iconbitmap('images\\download.ico')
                uni = Ac.Accueil(win)
                self.username.delete(0,'end')
                self.password.delete(0,'end')
                conn.close()
                                 


if (__name__ == '__main__'):
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Login(window)
    mainloop()