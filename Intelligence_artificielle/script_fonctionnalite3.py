#!/usr/bin/python3
import argparse
import pickle
import numpy as np
import pandas as pd
import json

if __name__ == "__main__":
    #Arguments pour le modèle
    parser = argparse.ArgumentParser(description="Fonctionnalité 3 : prédire si un arbre va être déraciné par la tempête")
    parser.add_argument('-r', '--fk_revetement', required=True, help='Inclure la colonne fk_revetement, mettre 1 pour oui et 0 pour non')
    parser.add_argument('-s', '--fk_situation', required=True, help='Inclure la colonne fk_situation, mettre 0 pour Alignement, 1 pour Groupe et 2 pour Alignement')
    parser.add_argument('-d', '--clc_nbr_diag', required=True, help='Inclure la colonne clc_nbr_diag')
    parser.add_argument('-l', '--longitude', required=True, help='Inclure la colonne longitude')
    parser.add_argument('-m', '--model', type=str, choices=['sgd', 'log_reg', 'forest'], required=True, help='Modèle à utiliser (sgd, log_reg, forest)')
    args = parser.parse_args()

    # Chargement du modèle d'IA choisit
    match (args.model):
        case 'sgd':
            model_name = "sgd.pkl"
        case 'log_reg':
            model_name = 'log_regr.pkl'
        case "forest":
            model_name = "rdm_forest.pkl"
    # Charger le modèle depuis le fichier .pkl
    try:
        with open(model_name, 'rb') as file:
            model = pickle.load(file)
    except Exception as e:
        print(f"Erreur lors du chargement du modèle : {e}")
        exit()

    # Prédiction sur les nouvelles données
    new_data = np.array([[args.fk_revetement, args.fk_situation, args.clc_nbr_diag, args.longitude]])
    new_data_df = pd.DataFrame(new_data, columns=["fk_revetement", "fk_situation", "clc_nbr_diag", "longitude"])
    with open('fonctionalite_3.json', 'w') as json_file:
        json.dump({"arbre_deracine:":model.predict(new_data_df)[0]}, json_file)