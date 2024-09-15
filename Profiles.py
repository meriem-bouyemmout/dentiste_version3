from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from PIL import Image,ImageTk
import tkinter.messagebox as mb
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
import pathlib
import sqlite3
from tkinter import filedialog


class Profiles:
    def __init__(self,mast):
        self.master = mast
        self.master.title("Page de gestion des profiles")
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("{w}x{h}+0+0".format(w=self.width,h=self.height))
        self.master.state("zoomed")


        #=========================university management system=======================================#
   
        self.Frameleft = ctk.CTkFrame(self.master,fg_color="#BCD2EE", width=300)
        self.Frameleft.pack(side=LEFT, fill=Y)
        ################################################################################################
       

        #############################################################################################
        self.Nom = ctk.CTkLabel(self.Frameleft,text="Nom d'utilisateur", font=('Helvetica',15))
        self.Nom.place(x=10,y=20 )
        self.Mot_de_passe = ctk.CTkLabel(self.Frameleft,text="Mot de passe", font=('Helvetica',15))
        self.Mot_de_passe.place(x=10,y=60 )
       
######################################################################
        
        self.nom = StringVar()
        self.prenom = StringVar()
      

    


    
########################################################
        self.nom_entry = ctk.CTkEntry(self.Frameleft, font=('tahoma',12), textvariable = self.nom)
        self.nom_entry.configure(justify="center")
        self.nom_entry.place(x=120,y=20)
        self.prenom_entry = ctk.CTkEntry(self.Frameleft, font=('tahoma',12), textvariable = self.prenom)
        self.prenom_entry.configure(justify="center")
        self.prenom_entry.place(x=120,y=60)
        


        self.buttonAdd=ctk.CTkButton(self.Frameleft,text='Ajouter', command=self.ajouter,  font=('Helvetica',15,'bold'))
        self.buttonAdd.place(x=10,y=450)
        self.buttonDELETE=ctk.CTkButton(self.Frameleft,text='Supprimer', command=self.delete,  font=('Helvetica',15,'bold'))
        self.buttonDELETE.place(x=155,y=450)
        self.buttonUP=ctk.CTkButton(self.Frameleft,text='Mise a jour', command=self.update,  font=('Helvetica',15,'bold'))
        self.buttonUP.place(x=10,y=485)
        self.buttonRESET=ctk.CTkButton(self.Frameleft,text='Nettoyer', command=self.netoyer,  font=('Helvetica',15,'bold'))
        self.buttonRESET.place(x=155,y=485)


        
        ####################################### RIGHT ####################################################
        self.Frameright = ctk.CTkFrame(self.master,fg_color="#BCD2EE", height=800)
        self.Frameright.pack(fill=BOTH, expand=True)
        ###########################################################################################################
        


        # ##################################################################################################
        self.Framerighttop = ctk.CTkFrame(self.Frameright,fg_color="#BCD2EE", height=70)
         
        self.rechercher_entry = ctk.CTkEntry(self.Framerighttop,  font=('Helvetica',18,'bold'), width=10)
        self.rechercher_entry.grid(row = 0, column = 0, sticky='nsew', pady=10, padx=5)
        self.rechercher_button = ctk.CTkButton(self.Framerighttop, text='Rechercher', command=self.rechercher_ligne_par_valeur, font=('Helvetica',16,'bold'), height=35)
        self.rechercher_button.grid(row = 0, column = 1, sticky='nsew', pady=10, padx=5)
        self.voir_button = ctk.CTkButton(self.Framerighttop, text='Voir', command=self.voir, font=('Helvetica',16,'bold'), height=35)
        self.voir_button.grid(row = 0, column = 2, sticky='nsew', pady=10, padx=5)
           
        self.Framerighttop.grid_columnconfigure(0, weight=1)
        self.Framerighttop.grid_columnconfigure(0, weight=1)  

        self.Framerighttop.pack(fill=X)

        ##################################################################################################
        
        


        self.frameView = ctk.CTkFrame(self.Frameright, height=400)
        self.frameView.pack(fill=BOTH)

        self.scrollbar = Scrollbar(self.frameView, orient = VERTICAL)

        style1 = ttk.Style()
        style1.layout('my.treeview.layout',
                    [('Header', {'sticky':'nswe'})] +
                    [('Separator', {'sticky':'ew'})] +
                    [('Item..focus', {'sticky':'nswe'})] +
                    [('Item', {'sticky':'nswe'})]
                    )
        style1.configure("Treeview",  background="#00C957")
        style1.configure("Treeview.Item", font=("Helvetica", 12))
        style1.configure("Treeview.Heading",  font=("tahoma", 10))

        

        self.table = ttk.Treeview(self.frameView, style='Treeview.Heading', column= ("ID","Nom","Mot_de_passe"), show='headings', height=17 , yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.table.yview())       
        self.table.pack(fill=BOTH)
         

        self.table.heading("ID",text="ID")
        self.table.heading("Nom",text="Nom")
        self.table.heading("Mot_de_passe",text="Mot de passe")
        
       
        self.table.column("ID", anchor=W, width=5)
        self.table.column("Nom", anchor=W, width=5)
        self.table.column("Mot_de_passe", anchor=W, width=6)
        
        


        
        self.lire()
        self.table.bind("<ButtonRelease>", self.show)
        


    def ajouter(self):
          nom = self.nom_entry.get()
          prenom = self.prenom_entry.get()
          

          # Connect to SQLite database
          def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Lire le chemin de la base de données depuis le fichier texte
          database_path = read_database_path()
          conn = sqlite3.connect(database_path)
          cursor = conn.cursor()

          # Fetch data from SQLite
          

          if (nom == '' or prenom == '' ) :
           mb.showerror('Erreur','Veuiller saisir le nom et le mot de passe', parent=self.master)
          else :
              req = "INSERT INTO Connexion(Nom, Mot_de_passe) values ( ?, ?)"  
              val = (nom, prenom)          
              cursor.execute(req, val)        
              conn.commit()
              conn.close() 
              mb.showinfo('Succes ajoute','Donnees inserees', parent=self.master)
              self.lire()          
              self.netoyer()

       
   
    def lire(self):
          
          # Connect to SQLite database
          def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Lire le chemin de la base de données depuis le fichier texte
          database_path = read_database_path()
          conn = sqlite3.connect(database_path)
          cursor = conn.cursor()

          # Fetch data from SQLite
          #req = "SELECT Nom, Prenom, Age, Motif, Jour, Rendez_vous, Montant_total, Versement, Reste, Num_de_tel FROM Patient" 
          cursor.execute("SELECT * FROM Connexion")
          data = cursor.fetchall()

  
          self.table.delete(*self.table.get_children())

          counter = 1  # Start from 1 or another appropriate value
          for i in data:
            self.table.insert('', 'end', iid=str(counter), values=i)
            counter += 1
 
          conn.close()  
              
    def show(self,ev): 
        selected_item = self.table.selection()
    
        # Extract the unique identifier (e.g., ID)
        self.row_id = self.table.item(selected_item, "values")[0]

        self.data = self.table.focus()
        alldata = self.table.item(self.data)
        print(self.row_id)
        val = alldata['values']
        self.nom.set(val[1])
        self.prenom.set(val[2])
        
    def voir(self):
        # Call your read function to refresh the table with all data
        self.lire()

        # Optionally, you can clear the search entry if you have one
        self.rechercher_entry.delete(0, 'end')

    def netoyer(self):
        self.nom_entry.delete(0,'end')
        self.prenom_entry.delete(0,'end')
        


    def delete(self):
    
        # Connect to SQLite database
        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Lire le chemin de la base de données depuis le fichier texte
        database_path = read_database_path()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        req = ("delete from Connexion where ID="+self.row_id)
        cursor.execute(req)
        conn.commit()
        conn.close()
        mb.showinfo("Supprimer", "L'utilisateur a été supprimé", parent=self.master)
        self.lire()
        self.netoyer() 

    def update(self):
      
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        

        # print(nom, prenom, age, motif, jour, rendez_vous, montant_total, versement, reste, tel )  
        
        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Lire le chemin de la base de données depuis le fichier texte
        database_path = read_database_path()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        if (nom == '' or prenom == '' ) :
           mb.showerror('Erreur',"Veuiller saisir le nom d'utlisateur et le mot de passe", parent=self.master)
        else :
              req = "UPDATE Connexion set ID=? ,Nom=?, Mot_de_passe=? WHERE ID=? "  
              val = (self.row_id, nom, prenom, self.row_id)          
              cursor.execute(req, val)        
              conn.commit()
              conn.close() 
              mb.showinfo('Mise a jour',"L'utlisateur a été mis à jour", parent=self.master)
              self.lire()          
              self.netoyer()
        

    def rechercher_ligne_par_valeur(self):

        rechercher_entry = self.rechercher_entry.get()
        def read_database_path(file_path='data_base.txt'):
            with open(file_path, 'r') as file:
                return file.read().strip()

        # Lire le chemin de la base de données depuis le fichier texte
        database_path = read_database_path()
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

    # Remplacez 'nom_de_la_table' par le nom réel de votre table et 'nom_colonne' par le nom de la colonne dans laquelle vous voulez rechercher.
        req = (f"SELECT * FROM Connexion WHERE Nom LIKE ?")
        cursor.execute(req, ('%' + rechercher_entry + '%',))

    # Utilisation du caractère joker '%' pour rechercher partiellement la valeur
        resultats = cursor.fetchall()
        print(resultats)
        if  not resultats: 
    
            mb.showerror("Erreur","L'utlisateur n'existe pas ", parent=self.master)  
        
        else :

            # Effacer les anciennes entrées dans le tableau
            for row in self.table.get_children():
                self.table.delete(row)

            # Afficher les résultats dans le tableau
            for resultat in resultats:
                self.table.insert("", "end", values=resultat)

        conn.commit()
        conn.close() 

if (__name__ == '__main__'):
    window = ctk.CTk()
    window.iconbitmap('images\\download.ico')
    std = Profiles(window)
    mainloop()