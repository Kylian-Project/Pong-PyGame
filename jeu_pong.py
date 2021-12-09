#########################################
###### Copyright Kylian GERARD 1°3 ######
#########################################



import pygame
from pygame.locals import *
from pygame import *
import time
#import de tout les library requis

def detect_collision(ballerect,barrerect): #je garde cette fonction mais on pourrait trés bien l'enlever
    """
        fonction qui détecte si la balle entre en contacte avec un des bords de la barre
        et renvoie 'Nord' si le côté touché est celui du dessus et 'Sud' si c'est celui du dessous

        Je l'utilise uniquement pour les colision en haut et en bas des barres (fonctionnerais donc sans)
    """
    if barrerect.left<=ballerect.left and barrerect.right>=ballerect.right and barrerect.top<=ballerect.bottom and barrerect.bottom>=ballerect.bottom :
        return 'Nord'
    elif barrerect.left<=ballerect.left and barrerect.right>=ballerect.right and barrerect.bottom<=ballerect.top and barrerect.top>=ballerect.top :
        return 'Sud'
    else :return False


pygame.init() #début de la boucle Pygame

#Titre
pygame.display.set_caption("Jeu De Pong Version NBA by Kylian 1°3") #donner un titre à la fenêtre

#Ouverture de la fenêtre Pygame
taille = largeur, hauteur = 1024, 596 #taille de la fenêtre
fenetre = pygame.display.set_mode(taille) #def la taille avec la ligne juste au dessus

barrerect_gauche_y_position = 200 #defnis position barre gauche au centre en y
barrerect_droit_y_position = 200 #defnis position barre droite au centre en y

#Chargement et collage de la balle
balle = pygame.image.load("ballon.png").convert_alpha()
ballerect = balle.get_rect()

#Chargement et collage de la barre gauche
barre_gauche = pygame.image.load("barre.png").convert()
barrerect_gauche = barre_gauche.get_rect()
barrerect_gauche.x, barrerect_gauche.y = 0, barrerect_gauche_y_position

#Chargement et collage de la barre droite
barre_droit = pygame.image.load("barre.png").convert()
barrerect_droit = barre_droit.get_rect()
barrerect_droit.x, barrerect_droit.y = 994, barrerect_droit_y_position

#Chargement et collage de la barre qui sépare le terrain en deux
barre_centre = pygame.image.load("barre_centre.png").convert_alpha()
barrerect_centre = barre_centre.get_rect()
barrerect_centre.x, barrerect_centre.y = 501, 0

#Chargement et collage de l'image de fond
background = pygame.image.load("background.jpg").convert()
rect_back = background.get_rect()

#Chargement et collage de l'image pour le boutton mute le son
mute_button = pygame.image.load("sound-on.png").convert_alpha()
rect_mute = mute_button.get_rect()
rect_mute.x, rect_mute.y = 15, 510 #place l'image sur l'écran

#Chargement et collage de l'image pour le boutton 1vs1
vs_button = pygame.image.load("1vs1.png").convert_alpha()
rect_vs = vs_button.get_rect()
rect_vs.x, rect_vs.y = 596, 444 #place l'image sur l'écran

#Chargement et collage de l'image pour le boutton VSordi
vsordi_button = pygame.image.load("vs_ordi.png").convert_alpha()
rect_vsordi = vsordi_button.get_rect()
rect_vsordi.x, rect_vsordi.y = 152, 444 #place l'image sur l'écran

#Chargement et collage de l'image pour le menu pause
pause = pygame.image.load("pause.jpg").convert()
rect_pause = pause.get_rect()

#Chargement et collage de l'image pour le boutton reprendre dans menu pause
resume_button = pygame.image.load("reprendre.png").convert_alpha()
rect_resume = resume_button.get_rect()
rect_resume.x, rect_resume.y = 390, 240 #place l'image sur l'écran

#Chargement et collage de l'image pour le boutton menu principale dans menu pause
menu_button = pygame.image.load("menu_principale.png").convert_alpha()
rect_menu = menu_button.get_rect()
rect_menu.x, rect_menu.y = 390, 320 #place l'image sur l'écran

#Chargement et collage de l'image pour le boutton quitter dans menu pause
leave_button = pygame.image.load("quitter.png").convert_alpha()
rect_leave = leave_button.get_rect()
rect_leave.x, rect_leave.y = 390, 400 #place l'image sur l'écran

#Création des variables
font = pygame.font.Font("police.ttf",60) #import une police d'écriture
vitesse = [2,2]
noir = 0, 0, 0 #def de la couleur noir en RGB (RVB)
red = 100, 80, 60 #def de la couleur rouge en RGB (RVB)
GREY=200,200,200 #def de la couleur gris en RGB (RVB)
winner = 'aucun' #def joueur gagner, aucun pour l'instant
nbcurseur = 'curseur1.png' #import image pour le curseur personnalisé
mute = False #def button coupé le son sur False, désactiver au début
music_on = True #def music sur True car musique pas désactiver au début (ligne du dessus)
continuer = 0 #met la boucle continuer a 0 car on a d'abbord un menu avant de jouer
menu = 0 #met la boucle du menu sur 0 car on lui donne 1 quand la fonction est appellé pour éviter des bugs
play_mod = 1 #def mode de jeux sur 1, mais on pourais mettre 0 ou encore 2 car elle change plus loin
score_g=0 #score gauche à 0 
score_d=0 #score droit à 0

#Rafraîchissement de l'écran
pygame.display.flip()

#Son rebond et foulle
rebond_song = pygame.mixer.Sound("rebond.mp3")
pygame.mixer.music.load("foulle.mp3")


pygame.key.set_repeat(100, 30) ##pour pouvoir laisser les fleches enfoncées

#Image menu principale et menu gagner / perdu
background_menu = pygame.image.load("menu.png").convert()
rect_backmenu = background_menu.get_rect()

wing_g = pygame.image.load("win_g.png").convert()
rect_wing = wing_g.get_rect()

wing_d = pygame.image.load("win_d.png").convert()
rect_wind = wing_g.get_rect()


def pointer():
    """
        procédure qui place le nouveaux curseur sur celui de base en temps réel
    """
    curseur = pygame.image.load(nbcurseur).convert_alpha() #"convert_alpha()" permet d'importer l'image avec sa transparence (png)
    curseur_rect = curseur.get_rect()
    x,y = pygame.mouse.get_pos() #prend la position de la souris en temps réel
    curseur_rect.x, curseur_rect.y = x, y #applique les postions de la lignes au dessus au nouveaux curseur
    fenetre.blit(curseur, curseur_rect) #affiche le nouveau curseur
    pygame.display.flip() #raffraichit l'écran

def actu_score():
    """
        procédure qui actualise le score affiché a l'écran
    """
    global scoreg, scored, scoreg_win, scored_win
    scoreg = font.render(str(score_g), 1, (212, 68, 31)) #score gauche en jeu
    scored = font.render(str(score_d), 1, (212, 68, 31)) #score droit en jeu
    scoreg_win = font.render(str(score_g), 1, (70, 17, 26)) #score gauche dans menu de fin
    scored_win = font.render(str(score_d), 1, (70, 17, 26)) #score droit dans menu de fin

def fondu_sortant():
    """
        procédure qui permet de baisser progressivement le volume du son a la fin de la partie
    """
    for i in range (9,-1,-1): #boucle for qui descend de 1 en 1
        i /= 10
        pygame.mixer.music.set_volume(i) #applique i au volume du son
        time.sleep(0.2) #attend 0.2s entre chaque changement de volume
        print(i,"Volume son") #affiche dans la console (ne sert a rien)
    pygame.mixer.music.stop() #arrête la musique quand boucle terminer

def main_menu():
    """
        fonction du menu principale du jeu
    """
    global menu, mute_button, music_on, nbcurseur, mute, barrerect_gauche_y_position, play_mod, ballerect
    pygame.mouse.set_visible(False) #cacher la souris de base pour mettre la nouvelle (personnalisé)
    menu = 1 #met la boucle du dessous sur 1
    while menu: #boucle du menu
        pointer() #appelle la fonction pour le nouveau pointeur
        for event in pygame.event.get():  # On parcourt la liste de tous les événements reçus
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                menu = 0  # On arrête la boucle
            if event.type == KEYDOWN: #si une touche pressé
                if event.key == K_ESCAPE: #si touche echap pressé
                    menu = 0 #quitte le menu, ferme donc la fenêtre
            if rect_mute.collidepoint(pygame.mouse.get_pos()) or rect_vs.collidepoint(pygame.mouse.get_pos()) or rect_vsordi.collidepoint(pygame.mouse.get_pos()):
                #si curseur passe sur le boutton mute ou 1vs1 ou VSordi
                nbcurseur = "curseur2.png" #affiche le curseur 2, la main
            else: #sinon, laisse le curseur 1
                nbcurseur = "curseur1.png"
            if event.type == pygame.MOUSEBUTTONDOWN: #si click souris pressé
                if rect_mute.collidepoint(event.pos): #si boutton mute clické
                    music_on = not music_on #music_on reçois sont inverse
                    if music_on: #si music_on, alors affiche image "sound-on"
                        mute_button = pygame.image.load("sound-on.png").convert_alpha()
                        mute = False #donc mute reçois False car sont activer 
                    else: #sinon afficher image "sound-off"
                        mute_button = pygame.image.load("sound-off.png").convert_alpha()
                        mute = True #donc mute reçois True car sont désactiver
                if rect_vsordi.collidepoint(event.pos): #si button VSordi clické
                    play_mod = 1 #met le mode de jeu sur 1
                    jouer() #appelle la fonction jouer pour démarer la partie
                    menu = 0 #termine la boucle menu (celle-ci) pour éviter les bugs
                if rect_vs.collidepoint(event.pos): #si button 1vs1 clické
                    play_mod = 2 #met le mode de jeu sur 2
                    jouer() #appelle la fonction jouer pour démarer la partie
                    menu = 0 #termine la boucle menu (celle-ci) pour éviter les bugs
            fenetre.blit(background_menu, rect_backmenu) #affiche image de fond menu
            fenetre.blit(vsordi_button, rect_vsordi) #affiche image button VSordi
            fenetre.blit(vs_button, rect_vs) #affiche image button 1vs1
            fenetre.blit(mute_button, rect_mute) #affiche image button mute


def inwin():
    """
        fonction appeler lors de la fin de partie
    """
    global continuer, score_d, score_g
    win = 1 #def boucle win sur 1
    if winner == 'gauche': #si le joueur gagnant est gauche
        fenetre.blit(wing_g, rect_wing) #affiche image pour le gagnant gauche
        pygame.display.flip() #rafraichit l'écran
    elif winner == 'droit': #si le joueur gagnant est droit
        fenetre.blit(wing_d, rect_wind) #affiche image pour le gagnant droit
        pygame.display.flip() #rafraichit l'écran
    fenetre.blit(scoreg_win, (190, 15)) #écrit le score des deux joueurs
    fenetre.blit(scored_win, (190, 65))
    pygame.display.flip() #rafraichit l'écran
    if mute == False: #si son pas désactiver, appeler la fonction pour descendre le volume du son progressivement
        fondu_sortant()
    while win: #boucle menu fin de la partie
        for event in pygame.event.get():  # On parcourt la liste de tous les événements reçus
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                win = 0  # On arrête la boucle
            if event.type == KEYDOWN: # Si touche pressé
                if event.key == K_ESCAPE: # Si touche échap pressé
                    win = 0 #On arrête la boucle, donc on ferme la fenêtre
                if event.key == K_RETURN:  # Si "Entrer" pressé
                    win = 0 #On arrête la boucle pour éviter les bugs
                    main_menu() #Puis on appelle le menu principale

def jouer():
    """
        Procédure du jeu principale, appelé donc lors du lancement d'une partie
    """
    global continuer, score_d, score_g, ballerect, barrerect_gauche_y_position, barrerect_droit_y_position, winner, nbcurseur, menu
    ballerect.x, ballerect.y = 474.5, 261 #place la balle au centre a chaque debut de partie
    barrerect_gauche_y_position = 200 #placer barre au centre a gauche (pour quand on relance une partie)
    barrerect_droit_y_position = 200 #placer barre au centre a droite (pour quand on relance une partie)
    score_g, score_d = 0, 0 #remet le score a zero a chaque debut de parti
    vitesse = [2,2] #remet la vitesse de base a chaque début
    if mute == False: #si son activer
        pygame.mixer.music.set_volume(1) #met le volume a 1
        pygame.mixer.music.play() #lance le son
    continuer = 1 #met la boucle "continuer" sur 1
    while continuer: #boucle du jeu principale
    #Création de la boucle de déplacement de la balle
        pygame.time.Clock().tick(144) #pour ralentir la boucle de jeu (144 fps)
        ballerect = ballerect.move(vitesse) #donne la vitesse a la balle

        if play_mod == 1: #si le mode de jeu est le 1 (VS ordi)
            barrerect_gauche.y = ballerect.y #la barre geuche prend la même hauteur que la balle en temps réel
            barrerect_droit.y = barrerect_droit_y_position #la barre gauche prend sa hauteur en temps réel 
        elif play_mod == 2: #si le mode de jeu est le 2 (1 vs 1)
            barrerect_gauche.y = barrerect_gauche_y_position #la barre gauche prend sa hauteur en temps réel
            barrerect_droit.y = barrerect_droit_y_position #la barre droite prend sa hauteur en temps réel
            

        if ballerect.left < 0 : #Ajouter score 
            score_d += 1 #ajoute 1 au score joueur droit
            ballerect.x, ballerect.y = 474.5, 261 #remet la balle au centre
            vitesse[0] = 2 #remet la vitesse de base
        if ballerect.right > largeur :
            score_g += 1 #ajoute 1 au score joueur gauche
            ballerect.x, ballerect.y = 474.5, 261 #remet la balle au centre
            vitesse[0] = 2 #remet la vitesse de base
            vitesse[0] = -vitesse[0] #change le sens au renvoi de la balle
        actu_score() #appelle cette procédure qui actualise le score a l'écran

        if ballerect.top < 0 or ballerect.bottom > hauteur: # changement de direction de la balle si atteint les bords bas ou ahut
            vitesse[1] = -vitesse[1] #vitesse reçoit l'opposer

        #Permet de ne pas faire sortir la barre de la fenêtre
        if barrerect_gauche_y_position >= 400 :
            barrerect_gauche_y_position -= 16.25
        if barrerect_gauche_y_position <= -10:
            barrerect_gauche_y_position += 16.25
        if barrerect_droit_y_position >= 400 :
            barrerect_droit_y_position -= 16.25
        if barrerect_droit_y_position <= -10:
            barrerect_droit_y_position += 16.25



        #Gestion de la fermeture :

        for event in pygame.event.get():   #On parcourt la liste de tous les événements reçus
            if event.type == KEYDOWN and event.key == K_ESCAPE: #détecte touche échap pour le menu pause
                print('en pause') #print pause dans la console (ne sert a rien)
                in_pause = 1 #met in_pause = 1
                while in_pause: #tant que "in_pause" est égal à 1
                    #si souris sur un des boutton du menu
                    if rect_resume.collidepoint(pygame.mouse.get_pos()) or rect_leave.collidepoint(pygame.mouse.get_pos()) or rect_menu.collidepoint(pygame.mouse.get_pos()):
                        nbcurseur = "curseur2.png" #change le curseur
                    else:
                        nbcurseur = "curseur1.png" #laisse le curseur 1
                    pointer() #apelle la procédure pour changer le curseur en temps réel
                    fenetre.blit(pause, rect_pause) #affiche l'image pause
                    fenetre.blit(resume_button, rect_resume) #affiche le button "reprendre"
                    fenetre.blit(menu_button, rect_menu) #affiche le button "menu principale"
                    fenetre.blit(leave_button, rect_leave) #affiche le button "quitter"
                    event = pygame.event.wait() #attendre
                    if event.type == QUIT:     #Si un de ces événements est de type QUIT
                        in_pause = 0 #quitte le menu pause et ferme la fenetre
                    if event.type == KEYDOWN and event.key == K_ESCAPE: #Si touche échap pressé
                        print('fin pause') #print fin "fin pause" dans la console (ne sert a rien)
                        in_pause = 0 #termine la boucle pause
                    if event.type == pygame.MOUSEBUTTONDOWN: #si button souris pressé
                        if rect_resume.collidepoint(event.pos): #si button "reprendre" pressé
                            print('fin pause')
                            in_pause = 0 #termine la boucle pause
                        if rect_menu.collidepoint(event.pos): #si button "menu principale" pressé
                            print('fin pause')
                            if mute == False: #si il y a de la musique
                                pygame.mixer.music.stop() #stopper la musique
                            main_menu() #appelle cette procédure et renvoi au menu principale
                            continuer = 0 #termine la boucle du jeu
                            in_pause = 0 #termine la boucle pause
                        if rect_leave.collidepoint(event.pos):
                            print('fin pause')
                            continuer = 0 #termine la boucle du jeu
                            in_pause = 0 #termine la boucle pause

                                
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
        # mouvement de la barre de gauche:
            if event.type == KEYDOWN:
                if event.key == K_DOWN: #Si "flèche bas"
                    barrerect_droit_y_position += 16.25  #On descend la barre de gauche de 16.25 pixels
                if event.key == K_UP:   #Si "flèche haut"
                    barrerect_droit_y_position -= 16.25 #On monte la barre de gauche de 16.25 pixels
                if event.key == K_z: #si touche "z"
                    barrerect_gauche_y_position -= 16.25 #On monte la barre de gauche de 16.25 pixels
                if event.key == K_s: #si touche "s"
                    barrerect_gauche_y_position += 16.25 #On descend la barre de gauche de 16.25 pixels

        if ballerect.colliderect(barrerect_gauche) : #si balle touche barre gauche
            vitesse[0]= -vitesse[0] #change direction balle
            rebond_song.play() #joue le song "rebond"
            vitesse[0] += 0.5 #augmenter légerement la vitesse de la balle
        elif detect_collision(ballerect,barrerect_gauche)=='Nord' or detect_collision(ballerect,barrerect_gauche)=='Sud': #si balle touche haut ou bas de la barre gauche
            vitesse[1]= -vitesse[1] #change la direction de la balle (en y)
        elif ballerect.colliderect(barrerect_droit) : #si balle touche barre droit
            vitesse[0]= -vitesse[0] #change direction balle
            rebond_song.play() #joue le song "rebond"
            vitesse[0] -= 0.5 #augmenter légerement la vitesse de la balle
        elif detect_collision(ballerect,barrerect_droit)=='Nord' or detect_collision(ballerect,barrerect_droit)=='Sud': #si balle touche haut ou bas de la barre droite
            vitesse[1]= -vitesse[1] #change la direction de la balle (en y)


        if score_g >= 10: #si score joueur gauche supérieur ou égal à 10
            winner = 'gauche' #gagnant reçoit "gauche"
            inwin() #appelle la procédure "inwin" qui ouvre le menu de fin de partie
            continuer = 0 #termine la boucle du jeu
        if score_d >= 10: #si score joueur droit supérieur ou égal à 10
            winner = 'droit' #gagnant reçoit "droit"
            inwin() #appelle la procédure "inwin" qui ouvre le menu de fin de partie
            continuer = 0 #termine la boucle du jeu

        fenetre.blit(background, rect_back) #affiche image arrière plan
        fenetre.blit(barre_centre, barrerect_centre) #affiche barre du centre "pointillé"

        fenetre.blit(balle, ballerect) #Dessin de la balle
        fenetre.blit(barre_gauche, barrerect_gauche) #Dessin de la barre
        fenetre.blit(barre_droit, barrerect_droit) #affiche la barre doit
        #affichage du score
        fenetre.blit(scoreg,(256,30))
        fenetre.blit(scored,(710,30))

        #Rafraîchissement de l'écran
        pygame.display.flip()

main_menu() #appelle le menu principale
pygame.quit() #fin de la boucle "PyGame"


#########################################
###### Copyright Kylian GERARD 1°3 ######
#########################################