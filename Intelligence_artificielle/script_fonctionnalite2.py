#!/usr/bin/env python

import json
import argparse
import pickle
import numpy as np
import pandas as pd
from sklearn.exceptions import NotFittedError

# Définir la fonction tranche_age
def tranche_age(age):
    if age == 0:
        return "0-10"
    elif age == 1:
        return "11-40"
    elif age == 2:
        return "41-70"
    elif age == 3:
        return "71-100"
    else:
        return "+100"

def main():
    parser = argparse.ArgumentParser(description="Fonctionnalité 2 : prédire l'âge d'un arbre à partir de ses caractéristiques")
    parser.add_argument("-td", "--tronc_diam", type=float, required=True, help="Diamètre du tronc")
    parser.add_argument("-hto", "--haut_tot", type=float, required=True, help="Hauteur totale")
    parser.add_argument("-htr", "--haut_tronc", type=float, required=True, help="Hauteur du tronc")
    parser.add_argument("-fpe", "--fk_prec_estim", type=float, required=True, help="Precision de l\'age")
    parser.add_argument("-fsd", "--fk_stadedev", type=float, required=True, help="Stade de développement")
    parser.add_argument("-fpd", "--fk_pied", type=float, required=True, help="Pied")
    parser.add_argument("-ff", "--feuillage", type=float, required=True, help="Feuillage")
    parser.add_argument("-fs", "--fk_situation", type=float, required=True, help="Situation")
    parser.add_argument("-cnd", "--clc_nbr_diag", type=float, required=True, help="Nombre de diagnostics")
    parser.add_argument("-m", "--model", type=str, choices=["sgd", "rfc", "mlp"], required=True, help="Modèle à utiliser (sgd, rfc, mlp)")
    args = parser.parse_args()

    if args.model == "sgd":
        model_name = "sgd_clf.pkl"
    elif args.model == "rfc":
        model_name = "rfc_clf.pkl"
    elif args.model == "mlp":
        model_name = "mlp_clf.pkl"
    else:
        print("Modèle non reconnu. Veuillez choisir parmi 'sgd', 'rfc', 'mlp'.")
        exit()

    # Charger le modèle depuis le fichier .pkl
    try:
        with open(model_name, "rb") as file:
            model = pickle.load(file)
    except Exception as e:
        print(f"Erreur lors du chargement du modèle : {e}")
        exit()

    # Charger les encodeurs depuis les fichiers .pkl
    encoder_files = {
        "fk_stadedev": "ordinal_encoder_fk_stadedev.pkl",
        "fk_pied": "ordinal_encoder_fk_pied.pkl",
        "feuillage": "ordinal_encoder_feuillage.pkl",
        "fk_situation": "ordinal_encoder_fk_situation.pkl"
    }

    encoders = {}

    try:
        for col, filename in encoder_files.items():
            with open(filename, 'rb') as file:
                enc = pickle.load(file)
                encoders[col] = enc
    except Exception as e:
        print(f"Erreur lors du chargement des encodeurs : {e}")
        exit()

    # Définir les nouvelles données à prédire
    new_data = np.array([[args.tronc_diam, args.haut_tot, args.haut_tronc, args.fk_prec_estim, args.fk_stadedev, args.fk_pied, args.feuillage, args.fk_situation, args.clc_nbr_diag]])
    new_data_df = pd.DataFrame(new_data, columns=["tronc_diam", "haut_tot", "haut_tronc", "fk_prec_estim", "fk_stadedev", "fk_pied", "feuillage", "fk_situation", "clc_nbr_diag"])

    # Vérifier et encoder les colonnes catégorielles
    categorical_columns = ["fk_stadedev", "fk_pied", "feuillage", "fk_situation"]

    for col in categorical_columns:
        if col in new_data_df.columns:
            try:
                enc = encoders[col]
                new_data_df[col] = new_data_df[col].apply(
                    lambda val: val if val in enc.categories_[0] else enc.categories_[0][0]
                )
            except ValueError:
                print(f"Colonne '{col}' non trouvée dans l'encodeur. Veuillez vérifier les noms des colonnes.")

    # Transformer les colonnes catégorielles avec les encodeurs chargés
    for col in categorical_columns:
        if col in encoders:
            new_data_df[col] = encoders[col].transform(new_data_df[[col]])

    # Charger le scaler depuis le fichier .pkl
    try:
        with open("scaler.pkl", "rb") as file:
            scaler = pickle.load(file)
    except Exception as e:
        print(f"Erreur lors du chargement du scaler : {e}")
        exit()

    # Normaliser les données numériques
    new_data_scaled = scaler.transform(new_data_df)

    try:
        # Faire la prédiction avec le modèle chargé
        prediction = model.predict(new_data_scaled)
        age_category = tranche_age(prediction[0])  # Convertir la prédiction en classe d'âge
        print(f"L'âge prédit de l'arbre (catégorie) est : {age_category}")
    except NotFittedError as e:
        print("Le modèle n'est pas encore entraîné. Veuillez entraîner le modèle avant de l'utiliser pour les prédictions.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la prédiction : {e}")

    #Ecrit l'âge prédit dans le fichier json
    with open(f"fonctionalite_2_{args.model}.json", "w") as json_file:
        json.dump(age_category, json_file, indent=4)

if __name__ == "__main__":
    main()
