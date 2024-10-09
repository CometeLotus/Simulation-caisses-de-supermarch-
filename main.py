import matplotlib.pyplot as plt
from scipy.stats import sem, t
from Simulateur import simulateur
import numpy as np
from tqdm import tqdm

def main():
    cout = [1,3,5,7,10]
    tmp = 17
    _lambda = [i for i in range(1, tmp)]
    politique = [0, 2, 4, 6]
    nb_simulations = 20

    for C in cout:
        i_0, i_2, i_4, i_6 = [], [], [], []
        
        for lam in tqdm(_lambda, desc=f"Preparation du graphe avec C={C}"):
            for i in range(nb_simulations):
                i_0.append(simulateur(lam, politique[0], C))
                i_2.append(simulateur(lam, politique[1], C))
                i_4.append(simulateur(lam, politique[2], C))
                i_6.append(simulateur(lam, politique[3], C))

        i_0 = [sum(i_0[j*nb_simulations: j*nb_simulations + nb_simulations])/nb_simulations for j in range(tmp-1)]
        i_2 = [sum(i_2[j*nb_simulations: j*nb_simulations + nb_simulations])/nb_simulations for j in range(tmp-1)]
        i_4 = [sum(i_4[j*nb_simulations: j*nb_simulations + nb_simulations])/nb_simulations for j in range(tmp-1)]
        i_6 = [sum(i_6[j*nb_simulations: j*nb_simulations + nb_simulations])/nb_simulations for j in range(tmp-1)]

        # Calcul des intervalles de confiance à 95%
        confidence = 0.95
        ci_factor = t.ppf((1 + confidence) / 2, len(_lambda) - 1)  # Facteur pour l'intervalle de confiance
        sem_i_0 = sem(i_0)
        sem_i_2 = sem(i_2)
        sem_i_4 = sem(i_4)
        sem_i_6 = sem(i_6)
        ci_i_0 = sem_i_0 * ci_factor
        ci_i_2 = sem_i_2 * ci_factor
        ci_i_4 = sem_i_4 * ci_factor
        ci_i_6 = sem_i_6 * ci_factor

        # Tracé des courbes avec les intervalles de confiance
        plt.figure(figsize=(11, 7))

        # Tracer la première courbe avec intervalle de confiance
        plt.plot(_lambda, i_0, label='Politique 0', color='black', linestyle='-')
        plt.fill_between(_lambda, np.array(i_0) - ci_i_0, np.array(i_0) + ci_i_0, color='black', alpha=0.1)

        # Tracer la deuxième courbe avec intervalle de confiance
        plt.plot(_lambda, i_2, label='Politique 2', color='yellow', linestyle='--')
        plt.fill_between(_lambda, np.array(i_2) - ci_i_2, np.array(i_2) + ci_i_2, color='yellow', alpha=0.1)

        # Tracer la troisième courbe avec intervalle de confiance
        plt.plot(_lambda, i_4, label='Politique 4', color='green', linestyle='-.')
        plt.fill_between(_lambda, np.array(i_4) - ci_i_4, np.array(i_4) + ci_i_4, color='green', alpha=0.1)

        # Tracer la quatrième courbe avec intervalle de confiance
        plt.plot(_lambda, i_6, label='Politique 6', color='red', linestyle='-')
        plt.fill_between(_lambda, np.array(i_6) - ci_i_6, np.array(i_6) + ci_i_6, color='red', alpha=0.1)

        plt.xlabel('Lambda')
        plt.ylabel('Gain moyen du supermarché')
        plt.title('Gain moyen en fonction du paramètre lambda avec C = {} '.format(C))

        plt.legend()
        plt.axis('auto')
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    main()
