import tkinter as tk
import tkinter.messagebox
import random

version = "0.2.0" #Version du jeu

# Création de la fenêtre principale
root = tk.Tk()
root.title("À prendre ou à laisser v. " + version)

objets = [
    "une tasse",
    "un stylo",
    "un parapluie",
    "un coussin",
    "un tapis",
    "un rideau"
]

n_objet_choisi = random.randrange(len(objets))

# Liste des numéros de boîtes et des sommes d'argent correspondantes
sommes_ordre = [
    objets[n_objet_choisi].split()[1], 0.05, 0.10, 0.50, 1, 5, 10, 25, 50, 100, 250, 500,
    1000, 1500, 3000, 4000, 5000, 10000, 15000, 20000, 30000, 50000, 100000, 250000
]
n_boites = len(sommes_ordre) # Nombre de boîtes
boites = list(range(1, n_boites+1))  # 24 boîtes numérotées de 1 à 24

# Répartition des sommes
sommes = sommes_ordre[:]
random.shuffle(sommes) # Répartition aléatoire des sommes dans les boîtes
contenu_boite_25 = random.randrange(4) # Contenu de la 25ème boîte (fin du jeu)
jackpot = 1000 # Montant du jackpot

sommes_restantes = [] # Sommes restantes (seulement des int ou float)
for somme in sommes_ordre:
    if type(somme) is str:
        sommes_restantes.append(0.01)
    else:
        sommes_restantes.append(somme)
boutons_boites = []
boite_joueur = -1
boites_a_ouvrir = 6
boites_tour_ouvertes = 0
boites_restantes = n_boites
offre = None
offre_acceptee = None
offres_banque = []
gains_gagnes = 0
jackpot_remporte = 0

def appel_banque(): # Appel de la banque
    global offre, offres_banque, boites_a_ouvrir, boites_tour_ouvertes
    if boites_a_ouvrir > 1:
        boites_a_ouvrir -= 1
    boites_tour_ouvertes = 0
    r = random.randrange(3)
    if r == 0 and offre_acceptee == None: #échange
        offre = "échange"
        bouton_refuser.config(state=tk.ACTIVE)
    elif r == 0 and offre_acceptee != None and min(sommes_restantes) <= offre_acceptee and max(sommes_restantes) >= offre_acceptee: #Comeback
        offre = "comeback"
        bouton_accepter.config(state=tk.ACTIVE)
        bouton_refuser.config(state=tk.ACTIVE)
    else: #Argent
        moyenne = sum(sommes_restantes)/len(sommes_restantes)
        offre = moyenne*random.uniform(0.08, 0.12)
        if offre < min(sommes_restantes):
            offre = moyenne
        offre = round(offre, 2)
        offres_banque.append(offre)
        if offre_acceptee == None:
            bouton_accepter.config(state=tk.ACTIVE)
        bouton_refuser.config(state=tk.ACTIVE)

def accepter(): #Acceptation d'une offre
    global gains_gagnes, offre, offre_acceptee
    bouton_accepter.config(state=tk.DISABLED)
    bouton_refuser.config(state=tk.DISABLED)
    if offre == "comeback":
        label_resultat.config(text=f"Vous avez accepté le comeback !\r\nLa boîte {boite_num} vous réappartient et vous avez abandonné l'offre de {offre_acceptee} €.")
        offre_acceptee = None
    elif offre == "boite 25":
        if contenu_boite_25 == 0:
            gains_gagnes = 0
            label_resultat.config(text=f"La 25ème boîte contient malheuresement banqueroute !\r\nVous avez tout perdu !")
        elif contenu_boite_25 == 1:
            if type(gains_gagnes) is str:
                gain_str = gains_gagnes = "la moitié de " + gains_gagnes
            else:
                gains_gagnes = gains_gagnes/2
                gain_str = str(gains_gagnes) + " €"
            label_resultat.config(text=f"La 25ème boîte contient divisé par 2 !\r\nVous avez divisé vos gains par 2 !\r\nVous gagnez donc {gain_str} !")
        elif contenu_boite_25 == 2:
            if type(gains_gagnes) is str:
                gains_gagnes = 1000
            else:
                gains_gagnes += 1000
            gain_str = str(gains_gagnes) + " €"
            label_resultat.config(text=f"La 25ème boîte contient plus 1000 € !\r\nVous avez ajouté 1000 € à vos gains !\r\nVous gagnez donc {gain_str} !")
        else:
            if type(gains_gagnes) is str:
                gain_str = gains_gagnes = "2 " + gains_gagnes + "s"
            else:
                gains_gagnes = gains_gagnes*2
                gain_str = str(gains_gagnes) + " €"
            label_resultat.config(text=f"La 25ème boîte contient multiplié par 2 !\r\nVous avez multiplié vos gains par 2 !\r\nVous gagnez donc {gain_str} !")
        gains()
    else:
        offre_acceptee = offre
        label_resultat.config(text=f"Vous avez accepté {offre} € !\r\nQuelle boîte auriez-vous ouverte si vous n'auriez pas accepté ?\r\nIl reste {boites_a_ouvrir} boîtes à ouvrir avant l'offre du banquier.")
    offre = None

def refuser(): #Refus d'une offre
    global gains_gagnes, offre
    bouton_accepter.config(state=tk.DISABLED)
    bouton_refuser.config(state=tk.DISABLED)
    if offre == "boite 25":
        if contenu_boite_25 == 0:
            label_resultat.config(text=f"La 25ème boîte contenait banqueroute !\r\nVous avez bien fait de ne pas l'ouvrir !\r\nVous gardez vos {gains_gagnes} € !")
        elif contenu_boite_25 == 1:
            label_resultat.config(text=f"La 25ème boîte contenait divisé par 2 !\r\nVous avez bien fait de ne pas l'ouvrir !\r\nVous gardez vos {gains_gagnes} € !")
        elif contenu_boite_25 == 2:
            label_resultat.config(text=f"La 25ème boîte contenait plus 1000 € !\r\nVous gardez cependant vos {gains_gagnes} € !")
        else:
            label_resultat.config(text=f"La 25ème boîte contenait multiplié par 2 !\r\nVous gardez cependant vos {gains_gagnes} € !")
        gains()
    else:
        label_resultat.config(text=f"Offre refusée.\r\nVous pouvez ouvrir une boîte.\r\nIl reste {boites_a_ouvrir} boîtes à ouvrir avant l'offre du banquier.")
    offre = None

# Fonction qui affiche la somme d'argent correspondant à une boîte sélectionnée
def ouvrir(boite_num):
    global boite_joueur, boites_tour_ouvertes, boites_restantes, offre, jackpot_remporte
    jackpot_boite = False
    if boite_joueur >= 1 and boite_joueur <= 24 and offre == None: #Ouverture d'une boîte
        somme = sommes[boite_num - 1]  # Soustraction de 1 pour indexer correctement
        if boites_restantes >= 21 and ((type(somme) is str and sommes_ordre.index(somme) == 0) or sommes_ordre.index(somme) == 0): # Jackpot
            jackpot_remporte = jackpot
            jackpot_boite = True
            label_resultat.config(text=f"Félicitations !\r\nVous avez remporté le jackpot de {jackpot} € en ouvrant la 1ère somme dans les 3 premières boîtes !")
        if type(somme) is str: # Récupération contenu boîte et suppression de la somme des sommes restantes
            contenu = objets[n_objet_choisi]
            sommes_restantes.remove(0.01)
        else:
            contenu = str(somme) + " €"
            sommes_restantes.remove(somme)
        boites_tour_ouvertes += 1
        boites_restantes -= 1
        if boites_restantes < 1: # S'il n'y a plus de boîte, fin du jeu
            fin()
        elif boites_a_ouvrir-boites_tour_ouvertes <= 0:
            appel_banque()
            if offre == "échange":
                label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} qui contenait {contenu}.\r\nLa banque vous propose un échange de boîte.\r\nCliquez sur une boîte pour changer de boîte ou cliquez sur refuser (votre boîte actuelle : {boite_joueur}).")
            elif offre == "comeback":
                label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} qui contenait {contenu}.\r\nLa banque vous propose un comeback (offre acceptée : {offre_acceptee} €).")
            else:
                if offre_acceptee is not None: # Une offre a déjà été acceptée
                    label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} qui contenait {contenu}.\r\nLa banque vous aurait proposé la somme de {offre} €.\r\nVous avez cependant accepté précédemment {offre_acceptee} €.")
                else: # Aucune offre acceptée
                    label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} qui contenait {contenu}.\r\nLa banque vous propose la somme de {offre} €.\r\nÀ prendre ou à laisser.")
        elif not jackpot_boite:
            label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} qui contenait {contenu}.\r\nIl reste {boites_a_ouvrir-boites_tour_ouvertes} boîtes à ouvrir avant l'offre du banquier.")
        listbox.itemconfig(sommes_ordre.index(somme), {'bg': 'black'})  # Cacher
        sommes[boite_num - 1] = None
        boutons_boites[boite_num - 1].config(state=tk.DISABLED)  # Désactiver le bouton après le clic
    elif offre == "échange" or boite_joueur == -1: #Choix d'une boîte (échange ou début du jeu)
        if boite_joueur >= 1 and boite_joueur <= 24: #échange
            boutons_boites[boite_joueur - 1].config(state=tk.ACTIVE, bg=bouton_accepter.cget("background"))
        else:
            boites_restantes -= 1
        boutons_boites[boite_num - 1].config(state=tk.DISABLED, bg='blue')
        boite_joueur = boite_num
        offre = None
        bouton_refuser.config(state=tk.DISABLED)
        label_resultat.config(text=f"Vous avez choisi la boîte {boite_joueur}.\r\nVous pouvez ouvrir une boîte.\r\nIl reste {boites_a_ouvrir} boîtes à ouvrir avant l'offre du banquier.")
    else:
        label_resultat.config(text=f"Vous devez accepter ou refuser l'offre du banquier ({offre} €).")

def fin(): #Fin de la partie
    global offre, gains_gagnes, offres_banque
    offre = "boite 25"
    if len(offres_banque) == 0:
        offres_banque.append(0)
    if offre_acceptee == None:
        gains_gagnes = sommes[boite_joueur-1]
        if type(gains_gagnes) is str:
            label_resultat.config(text=f"Vous avez dans votre boîte {gains_gagnes} !\r\nOffre du banquier la plus élevée : {max(offres_banque)} €.\r\nVous avez la possibilité d'ouvrir la 25ème boîte qui peut multiplier vos gains par 2 ou ajouter 1000 €.\r\nCependant, elle peut aussi vous faire tout perdre ou diviser vos gains par 2 !\r\nSouhaitez-vous prendre le risque de l'accepter ?")
        else:
            label_resultat.config(text=f"Vous avez dans votre boîte la somme de {gains_gagnes} € !\r\nVous avez donc gagné {gains_gagnes} € !\r\nOffre du banquier la plus élevée : {max(offres_banque)} €.\r\nVous avez la possibilité d'ouvrir la 25ème boîte qui peut multiplier vos gains par 2 ou ajouter 1000 €.\r\nCependant, elle peut aussi vous faire tout perdre ou diviser vos gains par 2 !\r\nSouhaitez-vous prendre le risque de l'accepter ?")
    else:
        label_resultat.config(text=f"Vous avez accepté {offre_acceptee} € !\r\nVous avez {sommes[boite_joueur-1]} € dans votre boîte.\r\nOffre du banquier la plus élevée : {max(offres_banque)} €.\r\nVous avez la possibilité d'ouvrir la 25ème boîte qui peut multiplier vos gains par 2 ou ajouter 1000 €.\r\nCependant, elle peut aussi vous faire tout perdre ou diviser vos gains par 2 !\r\nSouhaitez-vous prendre le risque de l'accepter ?")
        gains_gagnes = offre_acceptee
    bouton_accepter.config(state=tk.ACTIVE)
    bouton_refuser.config(state=tk.ACTIVE)

def gains(): #Rapport des gains
    tk.messagebox.showinfo(message = f"Gain du jeu : {gains_gagnes} €.\r\nGain du jackpot (si gagné) : {jackpot_remporte} €.\r\nGains totaux de la session : {gains_gagnes+jackpot_remporte} €.")
    exit()

# Création des boutons pour chaque boîte
for i, boite_num in enumerate(boites):
    bouton = tk.Button(root, text=f"Boîte {boite_num}", width=15, command=lambda i=i: ouvrir(boites[i]))
    bouton.grid(row=i // 4, column=i % 4, padx=10, pady=10)
    boutons_boites.append(bouton)
bouton_accepter = tk.Button(root, text="Accepter", width=15, state=tk.DISABLED, command=lambda: accepter())
bouton_accepter.grid(row=7, column=1, padx=10, pady=10)
bouton_refuser = tk.Button(root, text="Refuser", width=15, state=tk.DISABLED, command=lambda: refuser())
bouton_refuser.grid(row=7, column=2, padx=10, pady=10)

# Label pour afficher les instructions
label_resultat = tk.Label(root, text="Choisissez une boîte pour commencer le jeu.", font=("Helvetica", 7))
label_resultat.grid(row=6, column=0, columnspan=5, pady=20)

# Création d'une section à droite pour afficher la liste des sommes
frame_sommes = tk.Frame(root)
frame_sommes.grid(row=0, column=5, rowspan=5, padx=20)

# Création du Label de titre pour le panneau des sommes
label_sommes = tk.Label(frame_sommes, text="Sommes restantes", font=("Helvetica", 7))
label_sommes.pack(pady=10)

# Création de la Listbox pour afficher les sommes
listbox = tk.Listbox(frame_sommes, height=n_boites, width=15, font=("Helvetica", 12))
for somme in sommes_ordre:   # Ajouter chaque somme à la listbox
    if type(somme) is str:
        listbox.insert(tk.END, f"{somme}")
    else:
        listbox.insert(tk.END, f"{somme} €")
for i in range(len(sommes_ordre)):
    if i < len(sommes_ordre)/2:
        listbox.itemconfig(i, {'bg': 'red'})
    else:
        listbox.itemconfig(i, {'bg': 'yellow'})
listbox.pack()

# Lancement de la boucle principale de l'interface graphique
root.mainloop()
