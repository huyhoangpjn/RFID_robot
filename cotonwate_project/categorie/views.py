from tkinter import *
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.ttk import *
import customtkinter

from .models import  Categorie

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

class CategorieView(Frame):

    def __init__(self, root):
        super().__init__(root)

        # appel des methode pour le formulaire et le tableau
        self.formulaire(root)
        self.tableau(root)
        
    def formulaire(self, root):# rechercher les vetements par date
        snom = StringVar()

        def save(): # pour la date
            n = snom.get().split(",")
            if n != None and n != '':
                #gọi thẳng mà ko cần tạo đối tượng
                ligne = Categorie.create(n) # appel de la fonction qui permet de faire l'insertion dans la base de donnees
                if ligne == 1:
                    snom.set('') # supprimer le contenu de la zone de saisi
                    showinfo('Succes', 'Enregistrement effectué avec succès')

                else:
                    showerror('Erreur', "Une erreur est survenue lors de l'enregistrement")
            else:
                showwarning("Attention", "Vous devez saisir avant d'enregistrer")

        Label(root, text='Gestion des catégoires').pack()
        frame = Frame(root)
        lnom = Label(frame, text='Nom')
        lnom.grid(row=1, column=1)
        
        # recherche par date
        nom = Entry(frame, textvariable=snom)
        nom.grid(row=1, column=1)
        button = Button(frame, text='Enregistrer', command=save)
        button.grid(row=1, column=2)

        # boutton sotie
        button = Button(frame, text='sortie', command=lambda:root.grid_forget())
        button.grid(row=1, column=5, padx=10)
        
        # boutton mettre à jour stock
        frame.pack(side=TOP)


    def tableau(self, root):
        frame = customtkinter.CTkFrame(root, fg_color="transparent")
        Label(frame, text='Liste des article').grid(row=0, column=0, sticky='nesw', pady=40)
        tree = Treeview(frame)
        tree['columns'] = ('un', 'deux','trois','quatre','cinq','six','sept','huit','neuf') 
        # listes les index des colonnes du tableau

    # parametrer les colonnes
        tree.column('#0',width=50, minwidth=50,  anchor=CENTER)
        tree.column("un", width=160, minwidth=150, stretch=NO)
        tree.column("deux", width=160, minwidth=150)
        tree.column("trois", width=160, minwidth=150)
        tree.column("quatre", width=160, minwidth=150)
        tree.column("cinq", width=160, minwidth=150)
        tree.column("six", width=160, minwidth=150)
        tree.column("sept", width=160, minwidth=150)
        tree.column("huit", width=160, minwidth=150)
        tree.column("neuf", width=160, minwidth=150)

    # ajout des entete du tableau
        tree.heading('#0', text='N°')
        tree.heading("un", text="Id ",anchor=W)
        tree.heading("deux", text="Nom",anchor=W)
        tree.heading('trois', text='couleur')
        tree.heading("quatre", text="taille",anchor=W)
        tree.heading("cinq", text="marque",anchor=W)
        tree.heading('six', text='prix')
        tree.heading("sept", text="enStock",anchor=W)
        tree.heading("huit", text="date_ajout",anchor=W)
        tree.heading("neuf", text="date_modif",anchor=W)
        
    # insertion des lignes du tableau
        
        categories = Categorie.getAll() # répération de toutes les categories dans la base de données
        for index, categorie in enumerate(categories, start=1):
             tree.insert('', index, text=index, values=(categorie['NUID'], categorie['intitule'],categorie['couleur'], categorie['taille'],categorie['marque'], categorie['prix'],categorie['enStock'], categorie['date_ajout'],categorie['date_modif']))
            
        tree.grid(row=0, column=0) # afficher le tableau sur le frame
        frame.pack(pady=0, padx=0) # affichage du frame sur la fenetre



