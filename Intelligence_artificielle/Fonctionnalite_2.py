import numpy as np
import pandas as pd
import warnings
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score, \
    roc_curve, auc
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
import pickle

warnings.filterwarnings("ignore")

#============================================================================================================================================#
#==============================================================Fonctions annexes=============================================================#
#============================================================================================================================================#

def age_class(age):
    if age <= 10:
        return 0
    elif age <= 40:
        return 1
    elif age <= 70:
        return 2
    elif age <= 100:
        return 3
    else:
        return 4

def metrique_classification(model, datas, labels, grid_searched=False):
    if grid_searched:
        print("\nMéthode utilisée après grid search:", str(model).split("(")[0])
    else:
        print("\nMéthode utilisée:", str(model).split("(")[0])

    #Calcul du taux de classification pour chaque fold
    accuracy_scores = cross_val_score(model, datas, labels, cv=3, scoring="accuracy")
    print("Taux de classification (accuracy) pour chaque fold:", accuracy_scores)

    #Moyenne des taux de classification
    print("Moyenne des taux de classification : {:.1f}%".format(100 * accuracy_scores.mean()))

    #Prédiction croisée
    fold_3_prediction = cross_val_predict(model, datas, labels, cv=3)

    #Matrice de confusion normalisée
    cm_matrix = confusion_matrix(labels, fold_3_prediction, normalize="true")

    disp = ConfusionMatrixDisplay(cm_matrix, display_labels=["0-10", "11-40", "41-70", "71-100", "+100"])

    if grid_searched:
        figure_matrice_confusion(disp, model, grid_searched=True)
    else:
        figure_matrice_confusion(disp, model)

    #Précision
    model_precision_score = precision_score(labels, fold_3_prediction, average="weighted")
    print("Précision : {:.1f}%".format(100 * model_precision_score))

    #Rappel
    model_recall_score = recall_score(labels, fold_3_prediction, average="weighted")
    print("Rappel : {:.1f}%".format(100 * model_recall_score))

    #Score F1
    model_f1_score = f1_score(labels, fold_3_prediction, average="weighted")
    print("Score F1 : {:.1f}%".format(100 * model_f1_score))

    #Courbe ROC
    if grid_searched:
        plot_roc_courbes(model, datas, labels, grid_searched=True)
    else:
        plot_roc_courbes(model, datas, labels)


def figure_matrice_confusion(disp, model, grid_searched=False):
    #Création de la figure et de l'axe
    fig, ax = plt.subplots()
    disp.plot(cmap=plt.cm.Blues, ax=ax)
    ax.set_xlabel("Prédiction")
    ax.set_ylabel("Vraie valeur")
    if grid_searched:
        ax.set_title("Matrice de confusion, 3 fold, méthode: " + str(model).split("(")[0] + " + grid search")
    else:
        ax.set_title("Matrice de confusion, 3 fold, méthode: " + str(model).split("(")[0])
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_roc_courbes(model, datas_train, labels_train, grid_searched=False):

    #On calcul les scores de décision pour chaque fold
    if hasattr(model, "decision_function"):
        y_scores = cross_val_predict(model, datas_train, labels_train, cv=3, method="decision_function")
    else:
        y_scores = cross_val_predict(model, datas_train, labels_train, cv=3, method="predict_proba")

    #On calcul la courbe ROC et l'AUC pour la classe 1 par rapport à toutes les autres
    false_positive_rate, true_positive_rate, _ = roc_curve(labels_train == 1, y_scores[:, 1])
    roc_auc = auc(false_positive_rate, true_positive_rate)

    #On trace la courbe ROC
    plt.figure()
    plt.plot(false_positive_rate, true_positive_rate, color="navy", lw=2, label="Courbe ROC (AUC = %0.2f)" % roc_auc)
    plt.plot([0, 1], [0, 1], color="black", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Taux de faux positifs")
    plt.ylabel("Taux de vrais positifs")
    if grid_searched:
        plt.title("Courbe ROC, méthode: " + str(model).split("(")[0] + " + grid search")
    else:
        plt.title("Courbe ROC, méthode: " + str(model).split("(")[0])
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()


def grid_search(model, datas, labels, param_grid=0):
    if isinstance(model, SGDClassifier):
        param_grid = {
            "loss": ["hinge", "log"],
            "penalty": ["l2", "l1"],
            "alpha": [0.0001, 0.001, 0.01],
            "max_iter": [2000, 3000],
            "tol": [1e-3, 1e-4]
        }
    elif isinstance(model, RandomForestClassifier):
        param_grid = {
            "n_estimators": [50, 100],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5],
            "min_samples_leaf": [1, 2],
            "max_features": ["sqrt", "log2"]
        }
    elif isinstance(model, MLPClassifier):
        param_grid = {
            "hidden_layer_sizes": [(50,), (100,)],
            "solver": ["adam", "sgd"],
            "max_iter": [1000, 2000],
            "learning_rate": ["constant", "adaptive"]
        }

    grid_search_model = GridSearchCV(model, param_grid, cv=3, scoring="accuracy")
    grid_search_model.fit(datas, labels)

    return grid_search_model.best_params_

#============================================================================================================================================#
#========================================================Import de la base de données========================================================#
#============================================================================================================================================#

data = pd.read_csv("Data_Arbre.csv", sep=",")

#============================================================================================================================================#
#=========================================================1. Préparation des données=========================================================#
#============================================================================================================================================#

#Extraction des données d’intérêt : Sélectionner les colonnes pertinentes de la base de données selon ce besoin
x = data[["tronc_diam", "haut_tot", "haut_tronc", "fk_prec_estim", "fk_stadedev", "fk_pied", "feuillage",
          "fk_situation", "clc_nbr_diag"]]

#Encodage des données catégorielles (type object en float)
for idx, col in enumerate(x.columns):
    if x.iloc[:, idx].dtype == "object":
        #On crée un DataFrame avec la colonne à encoder
        col_data = pd.DataFrame(x.iloc[:, idx])

        enc = OrdinalEncoder()
        x.iloc[:, idx] = enc.fit_transform(col_data)

        #Sauvegarde de l'encodeur
        with open("ordinal_encoder_" + col + ".pkl", "wb") as file:
            pickle.dump(enc, file)

#Normalisation des données
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# Sauvegarde du scaler
with open("scaler.pkl", "wb") as file:
    pickle.dump(scaler, file)

print("Encodeur et scaler sauvegardés avec succès.")

#On détermine notre cible
y = data["age_estim"]

#On divise les données en classe d'âge estimée
y = y.apply(age_class)


#============================================================================================================================================#
#===================== Sauvegarde de la base de données modifiée après encodage =====================#
#============================================================================================================================================#

#Ajout de la colonne cible
#x["age_estim"] = y.values

#Sauvegarde du DataFrame modifié
#x.to_csv("Data_Arbre_Modified_Encoded.csv", index=False)

#============================================================================================================================================#
#==============================================2. Apprentissage Supervisé pour la classification=============================================#
#============================================================================================================================================#

#Création des échantillons de test et d'apprentissage
trees_data_train, trees_data_test = train_test_split(x_scaled, test_size=0.2, random_state=42)
trees_labels_train, trees_labels_test = train_test_split(y, test_size=0.2, random_state=42)

#Création du modèle avec la méthode SGD
sgd_clf = SGDClassifier()
sgd_clf.fit(trees_data_train, trees_labels_train)

#Création du modèle avec la méthode RandomForestClassifier
rfc_clf = RandomForestClassifier()
rfc_clf.fit(trees_data_train, trees_labels_train)

#Création du modèle avec la méthode MLPClassifier
mlp_clf = MLPClassifier()
mlp_clf.fit(trees_data_train, trees_labels_train)

#============================================================================================================================================#
#====================================================3. Métriques pour la classification=====================================================#
#============================================================================================================================================#

#Métrique de classification pour la méthode SGD
metrique_classification(sgd_clf, trees_data_test, trees_labels_test)

#On applique grid_search pour trouver les meilleurs paramètres
grid_sgd_params = grid_search(sgd_clf, trees_data_train, trees_labels_train)
grid_sgd = SGDClassifier(**grid_sgd_params)
grid_sgd.fit(trees_data_train, trees_labels_train)
metrique_classification(grid_sgd, trees_data_test, trees_labels_test, grid_searched=True)
print("Meilleurs paramètres trouvés pour la méthode SGD après grid search :", grid_sgd_params)

# #Métrique de classification pour la méthode RandomForestClassifier
metrique_classification(rfc_clf, trees_data_test, trees_labels_test)

#On applique grid_search pour trouver les meilleurs paramètres
grid_rfc_params = grid_search(rfc_clf, trees_data_train, trees_labels_train)
grid_rfc = RandomForestClassifier(**grid_rfc_params)
grid_rfc.fit(trees_data_train, trees_labels_train)
metrique_classification(grid_rfc, trees_data_test, trees_labels_test, grid_searched=True)
print("Meilleurs paramètres trouvés pour la méthode RandomForestClassifier après grid search :", grid_rfc_params)

#Métrique de classification pour la méthode OneVsRestClassifier
metrique_classification(mlp_clf, trees_data_test, trees_labels_test)

#On applique grid_search pour trouver les meilleurs paramètres
grid_mlp_params = grid_search(mlp_clf, trees_data_train, trees_labels_train)
grid_mlp = MLPClassifier(**grid_mlp_params)
grid_mlp.fit(trees_data_train, trees_labels_train)
metrique_classification(grid_mlp, trees_data_test, trees_labels_test, grid_searched=True)
print("Meilleurs paramètres trouvés pour la méthode MLPClassifier après grid search :", grid_mlp_params)

#============================================================================================================================================#
#=========================================================Enregistrement des modèles=========================================================#
#============================================================================================================================================#

model_filename = "sgd_clf.pkl"
with open(model_filename, "wb") as file:
    pickle.dump(grid_sgd, file)

model_filename = "rfc_clf.pkl"
with open(model_filename, "wb") as file:
    pickle.dump(grid_rfc, file)

model_filename = "mlp_clf.pkl"
with open(model_filename, "wb") as file:
    pickle.dump(grid_mlp, file)
