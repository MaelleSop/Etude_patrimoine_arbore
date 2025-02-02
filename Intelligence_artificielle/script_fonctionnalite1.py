#!/usr/bin/env python3

#Import
import argparse
import pandas as pd
import numpy as np
import json

#Script pour la méthode KMeans
def prediction(methode, nbr_cluster, tronc_diam, haut_tronc, age_estim):
    #Choisit le fichier selon la méthode et le nombre de cluster demandé par l'utilisateur
    if methode == 1 :
        filename = f'kmeans_{nbr_cluster}.csv'

    if methode == 2 :
        filename = f'birch_{nbr_cluster}.csv'

    if methode == 3 :
        filename = f'bisect_{nbr_cluster}.csv'

    #Calcul les centroides de notre modèle
    centroides = pd.read_csv(filename, header=None).values
    #Entre les valeurs de features donné par l'utilisateur
    new_features = np.array([[age_estim, haut_tronc, tronc_diam]])
    #Calcul la distance des valeurs par apport aux centroides
    dist = np.max(np.abs(centroides - new_features), axis=1)
    cluster_pred = int(np.argmin(dist))
    print("Le cluster le plus proche est le :", cluster_pred)
    print("Distances aux centroides :", dist)

    #Ecrit le cluster prédit dans le fichier json
    with open('fonctionalite_1.json', 'w') as json_file:
        json.dump(cluster_pred, json_file, indent=4)

def main():
    #Prépare les arguments de la fonction
    parser = argparse.ArgumentParser(description="Fonctionnalité 1 : prédire la taille d'un arbre")
    parser.add_argument('methode', type=int, help='Méthode (KMeans : 1, Birch : 2, Bisection KMeans : 3)')
    parser.add_argument('nbr_cluster', type=int, help='Nombre de cluster')
    parser.add_argument('age_estim', type=float, help="Age estimé de l'arbre")
    parser.add_argument('haut_tronc', type=float, help='Hauteur du tronc')
    parser.add_argument('tronc_diam', type=float, help='Diamètre du tronc')
    args = parser.parse_args()
    prediction(args.methode, args.nbr_cluster, args.age_estim, args.haut_tronc, args.tronc_diam)

if __name__ == '__main__':
    main()
