from heapq import heappush, heappop
import matplotlib.pyplot as plt
from scipy.stats import sem
from scipy.stats import t
import numpy as np


T_MAX = 100         # temps max de la simulation
CAPACITE_MAX = 5    # capacité maximum de la file


def duree_exp(p): 
   """
      - Génère une variable aléatoire exponentielle de paramètre p
   """
   return np.random.exponential(1/p)


def simulateur(_lambda, I, C):

   global T_MAX
   global CAPACITE_MAX
   gain_du_supermarche = 0
   demande_ouverture = False
   ouvert = False
   temps = 0
   echeancier = []
   # On initialise l'état des caisses a 4 caisses ouverte avec 0 client dans toutes les files 
   caisses = [0, 0, 0, 0, 0]
   # Représente l'indice de la caisse fermée sinon il vaut -1
   caisse_fermee = 4
   # On initialise l'échéancier en ajoutant un client
   heappush(echeancier, (0,"client"))

   while temps < T_MAX:
      evenement = heappop(echeancier)
      temps = evenement[0]

      # On traite l'evenement
      match evenement[1]:
         case "client":
            heappush(echeancier, (temps + duree_exp(_lambda), "client"))

            # Retrouver la caisse la moins encembrée
            long = 6
            for i in range(5):
               if i != caisse_fermee:
                  if caisses[i] <= long:
                     long = caisses[i]
                     num_caisse = i
            
            # Si y a de la place
            if long < CAPACITE_MAX:
               caisses[num_caisse] += 1

               # Si y a une caisse fermée, vérifier si y a besoin de l'ouvrir
               if I != 0:
                  if long + 1 == I and not demande_ouverture:
                     heappush(echeancier, (temps + 2, "ouverture"))
                     demande_ouverture = True
                     
               elif not demande_ouverture:
                  heappush(echeancier, (temps , "ouverture"))
                  demande_ouverture = True

            else:
               # Le client quitte le supermarché
               gain_du_supermarche -= 1

            # Si la file était vide, on commence un service
            if caisses[num_caisse] == 1:
               heappush(echeancier, (temps + duree_exp(1), "service", num_caisse))
               

         case "service":
            gain_du_supermarche += 10
            caisses[evenement[2]] -= 1
            
            
            if I != 0:
               # Fermeture de la caisse si elle est vide
               if caisses[evenement[2]] == 0: 
                     if caisse_fermee == -1:
                        caisse_fermee = evenement[2]
                        date_fermeture = temps
                        duree_ouverture = date_fermeture - date_ouverture
                        gain_du_supermarche -= duree_ouverture * C
            
               # Si il reste un client, il commence son service
               else:
                  heappush(echeancier, (temps + duree_exp(1), "service", evenement[2]))
            
            elif caisses[evenement[2]] != 0:
               heappush(echeancier, (temps + duree_exp(1), "service", evenement[2]))


         case "ouverture":
      
            if I != 0:
               date_ouverture = temps
               caisse_fermee = -1
               gain_du_supermarche -= 2*C
               demande_ouverture = False
            
            elif not ouvert:
               date_ouverture = temps
               caisse_fermee = -1
               ouvert = True
               
   if I == 0:
      gain_du_supermarche -= T_MAX * C
     


   return gain_du_supermarche
