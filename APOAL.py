import tkinter as tk
import random

# Création de la fenêtre principale
root = tk.Tk()
root.title("À prendre ou à laisser")

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

def appel_banque(): # Appel de la banque
    global offre, boites_a_ouvrir, boites_tour_ouvertes
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
        if len(sommes_restantes)%2 == 0:
            mediane = (sommes_restantes[len(sommes_restantes)//2-1]+sommes_restantes[len(sommes_restantes)//2])/2
        else:
            mediane = sommes_restantes[len(sommes_restantes)//2]
        offre = mediane*(random.random()+0.5)
        if offre < 1.1*min(sommes_restantes):
            offre = mediane
        elif offre > 0.9*max(sommes_restantes):
            offre = mediane
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
            gains_gagnes = gains_gagnes/2
            label_resultat.config(text=f"La 25ème boîte contient divisé par 2 !\r\nVous avez divisé vos gains par 2 !\r\nVous gagnez donc {gains_gagnes} € !")
        elif contenu_boite_25 == 2:
            gains_gagnes += 1000
            label_resultat.config(text=f"La 25ème boîte contient plus 1000 € !\r\nVous avez ajouté 1000 € à vos gains !\r\nVous gagnez donc {gains_gagnes} € !")
        else:
            gains_gagnes = gains_gagnes*2
            label_resultat.config(text=f"La 25ème boîte contient multiplié par 2 !\r\nVous avez multiplié vos gains par 2 !\r\nVous gagnez donc {gains_gagnes} € !")
    else:
        offre_acceptee = offre
        label_resultat.config(text=f"Vous avez accepté {offre} € !\r\nQuelle boîte auriez-vous ouverte si vous n'auriez pas accepté ?\r\nIl reste {boites_a_ouvrir} boîtes à ouvrir avant l'offre du banquier.")
        offres_banque.append(offre)
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
    else:
        label_resultat.config(text=f"Offre refusée.\r\nVous pouvez ouvrir une boîte.\r\nIl reste {boites_a_ouvrir} boîtes à ouvrir avant l'offre du banquier.")
        if type(offre) is not str:
            offres_banque.append(offre)
    offre = None

# Fonction qui affiche la somme d'argent correspondant à une boîte sélectionnée
def ouvrir(boite_num):
    global boite_joueur, boites_tour_ouvertes, boites_restantes, offre
    if boite_joueur >= 1 and boite_joueur <= 24 and offre == None: #Ouverture d'une boîte
        somme = sommes[boite_num - 1]  # Soustraction de 1 pour indexer correctement
        if type(somme) is str:
            contenu = objets[n_objet_choisi]
            sommes_restantes.remove(0.01)
        else:
            contenu = str(somme) + " €"
            sommes_restantes.remove(somme)
        boites_tour_ouvertes += 1
        if boites_a_ouvrir-boites_tour_ouvertes <= 0:
            appel_banque()
            if offre == "échange":
                label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} avec {contenu}.\r\nLa banque vous propose un échange de boîte.\r\nCliquez sur une boîte pour changer de boîte ou cliquez sur refuser (votre boîte actuelle : {boite_joueur}).")
            elif offre == "comeback":
                label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} avec {contenu}.\r\nLa banque vous propose un comeback (offre acceptée : {offre_acceptee} €).")
            else:
                if offre_acceptee is not None: # Une offre a déjà été acceptée
                    label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} avec {contenu}.\r\nLa banque vous aurait proposé la somme de {offre} €.\r\nVous avez cependant accepté précédemment {offre_acceptee} €.")
                else: # Aucune offre acceptée
                    label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} avec {contenu}.\r\nLa banque vous propose la somme de {offre} €.\r\nÀ prendre ou à laisser.")
        else:
            label_resultat.config(text=f"Vous avez ouvert la boîte {boite_num} avec {contenu}.\r\nIl reste {boites_a_ouvrir-boites_tour_ouvertes} boîtes à ouvrir avant l'offre du banquier.")
        listbox.itemconfig(sommes_ordre.index(somme), {'bg': 'black'})  # Cacher
        sommes[boite_num - 1] = None
        boites_restantes -= 1
        boutons_boites[boite_num - 1].config(state=tk.DISABLED)  # Désactiver le bouton après le clic
        if boites_restantes < 1:
            fin()
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
        label_resultat.config(text=f"Vous avez dans votre boîte la somme de {sommes[boite_joueur-1]} € !\r\nVous avez donc gagné {sommes[boite_joueur-1]} € !\r\nOffre du banquier la plus élevée : {max(offres_banque)} €.\r\nVous avez la possibilité d'ouvrir la 25ème boîte qui peut multiplier vos gains par 2 ou ajouter 1000 €.\r\nCependant, elle peut aussi vous faire tout perdre ou diviser vos gains par 2 !\r\nSouhaitez-vous prendre le risque de l'accepter ?")
        gains_gagnes = sommes[boite_joueur-1]
    else:
        label_resultat.config(text=f"Vous avez accepté {offre_acceptee} € !\r\nVous avez {sommes[boite_joueur-1]} € dans votre boîte.\r\nOffre du banquier la plus élevée : {max(offres_banque)} €.\r\nVous avez la possibilité d'ouvrir la 25ème boîte qui peut multiplier vos gains par 2 ou ajouter 1000 €.\r\nCependant, elle peut aussi vous faire tout perdre ou diviser vos gains par 2 !\r\nSouhaitez-vous prendre le risque de l'accepter ?")
        gains_gagnes = offre_acceptee
    bouton_accepter.config(state=tk.ACTIVE)
    bouton_refuser.config(state=tk.ACTIVE)

# Création des boutons pour chaque boîte
for i, boite_num in enumerate(boites):
    bouton = tk.Button(root, text=f"Boîte {boite_num}", width=15, command=lambda i=i: ouvrir(boites[i]))
    bouton.grid(row=i // 4, column=i % 4, padx=10, pady=10)
    boutons_boites.append(bouton)
bouton_accepter = tk.Button(root, text="Accepter", width=15, state=tk.DISABLED, command=lambda i=i: accepter())
bouton_accepter.grid(row=7, column=1, padx=10, pady=10)
bouton_refuser = tk.Button(root, text="Refuser", width=15, state=tk.DISABLED, command=lambda i=i: refuser())
bouton_refuser.grid(row=7, column=2, padx=10, pady=10)

# Label pour afficher les instructions
label_resultat = tk.Label(root, text="Choisir une boîte pour commencer le jeu", font=("Helvetica", 7))
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
