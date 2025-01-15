#!/usr/bin/python3
################### Importation des bibliothèques ###################


import pandas as pd
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.model_selection import cross_val_score, cross_val_predict, train_test_split, GridSearchCV
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, recall_score, precision_score, f1_score, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from numpy import nan
from matplotlib import pyplot as plt
import pickle


################### Définition des différentes fonctions ###################


def figure_matrice_confusion(disp, model):
    #Création de la figure et de l'axe
    fig, ax = plt.subplots()
    disp.plot(cmap=plt.cm.Blues, ax=ax)
    ax.set_xlabel("Prédiction")
    ax.set_ylabel("Vraie valeur")
    ax.set_title("Matrice de confusion pour 3 fold avec la méthode " + str(model).split("(")[0])
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_roc_courbes(model, datas_train, labels_train):
    #On calcul les scores de décision pour chaque fold
    """    if model == clf_sgd or model == sgd:
        y_scores = cross_val_predict(model, datas_train, labels_train, cv=3, method='decision_function')
    else:"""
    if model == sgd :#or model == clf_sgd:
        y_scores = cross_val_predict(model, datas_train, labels_train, cv=3, method='decision_function')
    else:
        y_scores = cross_val_predict(model, datas_train, labels_train, cv=3, method='predict_proba')

    #On calcul la courbe ROC et l'AUC pour la classe 1 par rapport à toutes les autres
    if y_scores.ndim == 1:
        fpr, tpr, _ = roc_curve(labels_train, y_scores)
    else:
        fpr, tpr, _ = roc_curve(labels_train, y_scores[:, 1])
    roc_auc = auc(fpr, tpr)

    # Tracez la courbe ROC
    plt.figure()
    plt.plot(fpr, tpr, color='navy', lw=2, label='Courbe ROC (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='black', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Taux de faux positifs')
    plt.ylabel('Taux de vrais positifs')
    plt.title('Courbe ROC pour la méthode ' + str(model).split("(")[0])
    plt.legend(loc="lower right")
    plt.show()

def metrique_classification(model, datas, labels):

    print("Méthode utilisée:", str(model).split("(")[0])

    #Calcul du taux de classification pour chaque fold
    accuracy_scores = cross_val_score(model, datas, labels, cv=3, scoring="accuracy")
    print("Taux de classification (accuracy) pour chaque fold:", accuracy_scores)

    #Moyenne des taux de classification
    print("Moyenne des taux de classification : {:.1f}%".format(100*accuracy_scores.mean()))

    #Prédiction croisée
    fold_3_prediction = cross_val_predict(model, datas, labels, cv=3)

    #Matrice de confusion normalisée
    cm_matrix = confusion_matrix(labels, fold_3_prediction, normalize="true")

    disp = ConfusionMatrixDisplay(cm_matrix, display_labels=["1", "0"])

    figure_matrice_confusion(disp, model)

    model_precision_score = precision_score(labels, fold_3_prediction, average="weighted")
    print("Précision : {:.1f}%".format(100*model_precision_score))

    model_recall_score = recall_score(labels, fold_3_prediction, average="weighted")
    print("Rappel : {:.1f}%".format(100*model_recall_score))

    model_f1_score = f1_score(labels, fold_3_prediction, average="weighted")
    print("Score F1 : {:.1f}%".format(100*model_f1_score))

    #plot_roc_courbes(model, datas, labels)


################### Filtrage des données et création des données d'apprentissage/test ###################


#Import du fichier csv
trees = pd.read_csv("/home/bap/cours/postbac/CIR3/projet_A3/IA/Data_Arbre.csv")

# Transformation de la colonne 'fk_arb_etat' et suppression après transformation
trees['fk_arb_etat_transformed'] = nan
i = 0
for elem in trees["fk_arb_etat"]:
    if elem in ['Essouché', 'Non essouché']:
        trees.loc[i, "fk_arb_etat_transformed"] = 1
    else:
        trees.loc[i, "fk_arb_etat_transformed"] = 0
    i+=1
trees = trees.drop("fk_arb_etat", axis=1)
#Séléction des colonnes
trees = trees[["fk_revetement", "fk_situation", "clc_nbr_diag", "longitude", "fk_arb_etat_transformed"]]#Pour log_reg
# Encodage des données textuelles
enc = OrdinalEncoder()
categorical_columns = trees.select_dtypes(include=['object']).columns
trees[categorical_columns] = enc.fit_transform(trees[categorical_columns])

#Création des échantillons de test et d'apprentissage
train_set, test_set = train_test_split(trees, test_size=0.2, random_state=42)
trees_data_train = train_set.drop("fk_arb_etat_transformed", axis=1)
trees_data_test = test_set.drop("fk_arb_etat_transformed", axis=1)
trees_labels_train = train_set["fk_arb_etat_transformed"].copy()
trees_labels_test = test_set["fk_arb_etat_transformed"].copy()


################### Création des modèles d'IA et apprentissage ###################


#Création du modèle avec la méthode sgd
sgd = SGDClassifier(class_weight={0: 1, 1: 65}, alpha=0.00000001, max_iter=1000000, penalty="l2")
sgd.fit(trees_data_train, trees_labels_train)
param_grid_sgd = {
    'alpha': [0.0001, 0.001, 0.01],
    'penalty': ['l2', 'l1', 'elasticnet'],
    'max_iter': [1000, 2000, 3000],
}
clf_sgd = GridSearchCV(sgd, param_grid_sgd, cv=5, scoring="balanced_accuracy")
clf_sgd.fit(trees_data_train, trees_labels_train)
print(clf_sgd.best_params_)

# Création du modèle avec la régression logistique
log_reg = LogisticRegression(C=0.1, penalty="l2", solver="liblinear", class_weight={0:1, 1: 55})
log_reg.fit(trees_data_train, trees_labels_train)
# Evaluation des features
coefficients = log_reg.coef_[0]
coefficients_df = pd.DataFrame({'feature': trees_data_train.columns, 'coefficient': coefficients})
coefficients_df = coefficients_df.sort_values(by='coefficient', ascending=False)
print(coefficients_df)
# Utilisation de gridsearch
param_grid_log = {
    'C': [0.1, 1, 10],
    'penalty': ['l2', 'l1'],
    'solver': ['liblinear', 'saga'],
}
clf_log = GridSearchCV(log_reg, param_grid_log, cv=5, scoring="balanced_accuracy")
clf_log.fit(trees_data_train, trees_labels_train)


#Création du modèle avec les forets aléatoires
forest = RandomForestClassifier(class_weight={0:1, 1: 55})
forest.fit(trees_data_train, trees_labels_train)
# Evaluation des features
feature_importances = forest.feature_importances_
feature_importances_df = pd.DataFrame({'feature': trees_data_train.columns, 'importance': feature_importances})
feature_importances_df = feature_importances_df.sort_values(by='importance', ascending=False)
print(feature_importances_df)
# Utilisation de gridsearch
param_grid_forest = {"n_estimators": [3, 10, 30, 50, 100, 200], 
                     "max_features":[2, 4, 6, 8]
}
clf_forest = GridSearchCV(forest, param_grid_forest, cv=5, scoring="balanced_accuracy")
clf_forest.fit(trees_data_train, trees_labels_train)

################### Evaluation des modèles ###################

metrique_classification(sgd, trees_data_test, trees_labels_test)
metrique_classification(clf_sgd, trees_data_test, trees_labels_test)
metrique_classification(clf_log, trees_data_test, trees_labels_test)
metrique_classification(clf_forest, trees_data_test, trees_labels_test)


################### Enregistrement des modèles ###################


user_input = input("Enregistrer sgd ? (y/n) >> ")
if (user_input == "y"):
    user_input = input("Avec grid search (y/n) >> ")
    if (user_input == "y"):
        model = clf_sgd
    else:
        model = sgd
    model_filename = 'sgd.pkl'
    with open(model_filename, 'wb') as file:
        pickle.dump(model, file)

user_input = input("Enregistrer log ? (y/n) >> ")
if (user_input == "y"):
    model_filename = 'log_regr.pkl'
    with open(model_filename, 'wb') as file:
        pickle.dump(clf_log, file)

user_input = input("Enregistrer forest ? (y/n) >> ")
if (user_input == "y"):
    model_filename = 'rdm_forest.pkl'
    with open(model_filename, 'wb') as file:
        pickle.dump(clf_forest, file)

#Save scaled datas
scaler = StandardScaler()
data_scaled = scaler.fit_transform(trees.values)
with open("scaled_datas.pkl" , "wb") as file:
    pickle.dump(data_scaled, file)