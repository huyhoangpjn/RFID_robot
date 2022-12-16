from tkinter import *
import serial
from categorie.views import CategorieView
from categorie.models import Categorie
from tkinter.ttk import *
from PIL import Image, ImageTk
from random import randint
from time import time
import time
import customtkinter
from tkinter.messagebox import showerror, showinfo, showwarning

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

class Main:
    def __init__(self):
        #________________________ création de la fenetre générale _________________________
        self.root = customtkinter.CTk()
        self.root.geometry('1187x620')

        self.root.title('COTONWATE : GESTION DES STOCK')
        self.frame_categorie = None

        #________________________ création du frame acceuil _____________________________
        page_acceuil = customtkinter.CTkFrame(self.root, fg_color="transparent")
        page_acceuil.grid(row=0, column=0)

        image_fond = Image.open("Mod1.jpg")
        image_logo = Image.open("logo.png")
        image_fond.paste(image_logo,(593,150))
        photo_fond = ImageTk.PhotoImage(image_fond)
        bloc1 = Canvas(page_acceuil,  width = 1480, height = 500)
        bloc1.create_image(0,0, anchor = NW, image=photo_fond)
        bloc1.pack()



        bloc3 = Canvas(page_acceuil, width=1480, height=500,background='#ebebeb')
        l = Label(bloc3, text = "GESTION DES STOCKS DES VETEMENTS",foreground='#a7786a',background='#ebebeb')
        l.config(font =("Ariel", 30,"bold"))
        l.pack(padx=0, pady=0)
        bloc3.pack()
        
        b=customtkinter.CTkButton(self.root,corner_radius=30,text ='Suivre le robot',font=("Arial",25),
                                width=250,height=50,fg_color='#a7786a', hover_color='#873e23',
                                command=self.show_update).place(relx=0.3, rely=0.9, anchor=CENTER)

        b2=customtkinter.CTkButton(self.root,corner_radius=30,text ='Gérer les stocks',font=("Arial",25),
                                width=250,height=50, fg_color='#a7786a',hover_color='#873e23',
                                command=self.show_categorie).place(relx=0.7, rely=0.9, anchor=CENTER)

        self.old_data = ""
        with open("incomming_data.txt", 'w') as f:
            f.close()

        self.hide_update = True

        self.text_var = StringVar(value="")
        self.label_update = customtkinter.CTkLabel(master=self.root,
                                    textvariable=self.text_var,
                                    width=500,
                                    height=25,
                                    bg_color= '#ebebeb',
                                    corner_radius=8, font=("Ariel", 20),text_color='#a7786a')
        self.label_update.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.run()

    def show_categorie(self):
       if self.frame_categorie is not None: 
            self.frame_categorie.grid_forget()
            self.frame_categorie = None
       self.frame_categorie = Frame(self.root)
       self.frame_categorie.grid(row=0, column=0)
       CategorieView(self.frame_categorie)

    def show_update(self):
        if self.hide_update:
            self.hide_update = False
            self.label_update.configure(textvariable = StringVar(value="Prêt à recevoir des données"))
        else:
            self.hide_update = True
            self.label_update.configure(textvariable = StringVar(value=""))
    def run(self):
        while True:
            with open("incomming_data.txt", 'r') as f:
                self.data = f.readline()
                if len(self.data) != 0:
                    if self.old_data != self.data:

                        self.to_database = self.data.split('_')
                        ligne = Categorie.create(self.to_database)
                        if ligne == 1:
                            if self.hide_update == False:
                                self.text_var = f"Vetements ID:{self.to_database[0]} sont mis à jour"
                                self.label_update.configure(textvariable = StringVar(value = self.text_var))  
                            self.show_categorie()         
                        else:
                            if self.hide_update == False:
                                self.text_var = f"Données erronées"
                                self.label_update.configure(textvariable = StringVar(value = self.text_var))

                
                self.old_data = self.data
                f.close()         
            self.root.update_idletasks()
            self.root.update()

 
def connect_and_run():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM16'
    ser.timeout = None
    try:
        ser.open()
    except:
        print("Can't connect to the robot...")
    return ser


if __name__ == "__main__":
    Main()
    # method Categorie.create du fichier modèle pour inserer les données
