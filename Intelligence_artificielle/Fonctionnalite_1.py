import csv
from copy import deepcopy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.cluster import KMeans, Birch, BisectingKMeans
import plotly.express as px
import pickle


#--------------------Lecture des données--------------------
data_arbres = pd.read_csv('Data_Arbre.csv')
data = deepcopy(data_arbres)


#--------------------Préparation des données--------------------
#Mise des valeurs en numériques
enc = OrdinalEncoder()
categorical_columns = data.select_dtypes(include=['object']).columns
data[categorical_columns] = enc.fit_transform(data[categorical_columns])

#Préparation et division des données
y = data['haut_tot']
x = data.drop(columns='haut_tot')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#Entraîner le modèle RandomForestClassifier
model_forest = RandomForestRegressor()
model_forest.fit(x_train, y_train)

#Choisit les caractéristiques importantes pour le modèle
feature_importances = pd.Series(model_forest.feature_importances_, index=x_train.columns).sort_values(ascending=False)
important_features = feature_importances[feature_importances > 0.08].index
remove_features = ['fk_nomtech', 'clc_nbr_diag']
important_features = important_features.difference(remove_features)
add_features = ['age_estim']
important_features = important_features.union(add_features)
data_reduced = data[important_features]

#--------------------Fonctions des différents modèles--------------------
def methode_kmeans(data, data_reduced, nbr_cluster):
    #Application du modèle
    kmeans = KMeans(n_clusters=nbr_cluster, random_state=42)
    y_pred_kmeans = kmeans.fit_predict(data_reduced)

    #Calculs des métriques
    print("------------- résultats k-means -------------")
    silhouette_kmeans = silhouette_score(data_reduced, y_pred_kmeans)
    silhouette_kmeans = round(silhouette_kmeans,2)
    print(silhouette_kmeans)
    calinski_harabasz_kmeans = calinski_harabasz_score(data_reduced, y_pred_kmeans)
    calinski_harabasz_kmeans = round(calinski_harabasz_kmeans,2)
    print(calinski_harabasz_kmeans)
    davies_bouldin_kmeans = davies_bouldin_score(data_reduced, y_pred_kmeans)
    davies_bouldin_kmeans = round(davies_bouldin_kmeans,2)
    print(davies_bouldin_kmeans)

    #Ajoute dans data une colonne avec le cluster de chaque arbre
    data['cluster'] = y_pred_kmeans

    #Visualisation sur une carte
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="cluster", hover_name="cluster",
                            zoom=2, center={"lat": data['latitude'].mean(), "lon": data['longitude'].mean()},
                            mapbox_style="open-street-map")
    fig.update_layout(title='KMeans Clustering with Plotly')
    fig.show()

    # Sauvegarder les centroides dans un csv
    centroides = kmeans.cluster_centers_
    with open('kmeans_' + str(nbr_cluster) + '.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for i in range(len(centroides)):
            writer.writerows([centroides[i]])

    return silhouette_kmeans, calinski_harabasz_kmeans, davies_bouldin_kmeans

def methode_birch(data, data_reduced, nbr_cluster):
    #Apllication du modèle
    birch = Birch(n_clusters=nbr_cluster)
    y_pred_birch = birch.fit_predict(data_reduced)

    #Calculs métriques
    print("------------- résultats Birch -------------")
    silhouette_birch = silhouette_score(data_reduced, y_pred_birch)
    silhouette_birch = round(silhouette_birch,2)
    print(silhouette_birch)
    calinski_harabasz_birch = calinski_harabasz_score(data_reduced, y_pred_birch)
    calinski_harabasz_birch = round(calinski_harabasz_birch,2)
    print(calinski_harabasz_birch)
    davies_bouldin_birch = davies_bouldin_score(data_reduced, y_pred_birch)
    davies_bouldin_birch = round(davies_bouldin_birch,2)
    print(davies_bouldin_birch)

    #Ajoute dans data une colonne avec le cluster de chaque arbre
    data['cluster'] = y_pred_birch

    #Visualisation sur une carte
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="cluster", hover_name="cluster",
                            zoom=2, center={"lat": data['latitude'].mean(), "lon": data['longitude'].mean()},
                            mapbox_style="open-street-map")
    fig.update_layout(title='Birch Clustering with Plotly')
    fig.show()

    # Sauvegarder les centroides dans un csv
    cluster_descriptions = data.groupby('cluster').mean()
    moy_age_estim = cluster_descriptions['age_estim']
    moy_haut_tronc = cluster_descriptions['haut_tronc']
    moy_tronc_diam = cluster_descriptions['tronc_diam']
    with open('birch_' + str(nbr_cluster) + '.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for i in range(nbr_cluster):
            writer.writerows([[moy_age_estim[i], moy_haut_tronc[i], moy_tronc_diam[i]]])

    return silhouette_birch, calinski_harabasz_birch, davies_bouldin_birch


def methode_bisectionKMeans(data, data_reduced, nbr_cluster):
    #Application du modèle
    bisect_means = BisectingKMeans(n_clusters=nbr_cluster, random_state=42)
    y_pred_bisect = bisect_means.fit_predict(data_reduced)

    #Calculs métriques
    print("------------- résultats BisectionKMeans -------------")
    silhouette_bisect = silhouette_score(data_reduced, y_pred_bisect)
    silhouette_bisect = round(silhouette_bisect,2)
    print(silhouette_bisect)
    calinski_harabasz_bisect = calinski_harabasz_score(data_reduced, y_pred_bisect)
    calinski_harabasz_bisect = round(calinski_harabasz_bisect,2)
    print(calinski_harabasz_bisect)
    davies_bouldin_bisect = davies_bouldin_score(data_reduced, y_pred_bisect)
    davies_bouldin_bisect = round(davies_bouldin_bisect,2)
    print(davies_bouldin_bisect)

    #Ajoute dans data une colonne avec le cluster de chaque arbre
    data['cluster'] = y_pred_bisect

    # Visualisation sur une carte
    fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", color="cluster", hover_name="cluster",
                            zoom=2, center={"lat": data['latitude'].mean(), "lon": data['longitude'].mean()},
                            mapbox_style="open-street-map")
    fig.update_layout(title='Bisection KMeans Clustering with Plotly')
    fig.show()

    # Sauvegarder les centroides dans un csv
    centroides = bisect_means.cluster_centers_
    with open('bisect_' + str(nbr_cluster) + '.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for i in range(len(centroides)):
            writer.writerows([centroides[i]])

    return silhouette_bisect, calinski_harabasz_bisect, davies_bouldin_bisect


methode_kmeans(data, data_reduced, 3)
methode_birch(data, data_reduced, 3)
methode_bisectionKMeans(data, data_reduced, 3)


def graphique_score():
    coef_silhouette_kmeans = []
    coef_silhouette_birch = []
    coef_silhouette_bisec = []
    indice_calinski_kmeans = []
    indice_calinski_birch = []
    indice_calinski_bisec = []
    indice_davies_kmeans = []
    indice_davies_birch = []
    indice_davies_bisec = []

    for i in range (2, 11):
        #Calcul les valeurs pour KMeans
        coef_silhouette_kmeans.append(methode_kmeans(data, data_reduced, i)[0])
        indice_calinski_kmeans.append(methode_kmeans(data, data_reduced, i)[1])
        indice_davies_kmeans.append(methode_kmeans(data, data_reduced, i)[2])

        #Calcul les valeurs pour bisection KMeans
        coef_silhouette_bisec.append(methode_bisectionKMeans(data, data_reduced, i)[0])
        indice_calinski_bisec.append(methode_bisectionKMeans(data, data_reduced, i)[1])
        indice_davies_bisec.append(methode_bisectionKMeans(data, data_reduced, i)[2])

        #Calcul les valeurs pour Birch
        coef_silhouette_birch.append(methode_birch(data, data_reduced, i)[0])
        indice_calinski_birch.append(methode_birch(data, data_reduced, i)[1])
        indice_davies_birch.append(methode_birch(data, data_reduced, i)[2])

    #Affiche le graphique pour le coefficient de silhouette
    plt.plot(range(2, 11), coef_silhouette_kmeans, label="KMeans")
    plt.plot(range(2, 11), coef_silhouette_birch, label="Birch")
    plt.plot(range(2, 11), coef_silhouette_bisec, label="Bisection KMeans")
    plt.xlabel("Nombre de clusters")
    plt.ylabel("Score")
    plt.title("Coefficient silhouette")
    plt.legend()
    plt.show()

    #Affiche le graphique pour l'indice de Calinski
    plt.plot(range(2, 11), indice_calinski_kmeans, label="KMeans")
    plt.plot(range(2, 11), indice_calinski_birch, label="Birch")
    plt.plot(range(2, 11), indice_calinski_bisec, label="Bisection KMeans")
    plt.xlabel("Nombre de clusters")
    plt.ylabel("Indice")
    plt.title("Indice Calinski-Harabasz")
    plt.legend()
    plt.show()

    #Affiche le graphique pour l'indice de Davies
    plt.plot(range(2, 11), indice_davies_kmeans, label="KMeans")
    plt.plot(range(2, 11), indice_davies_birch, label="Birch")
    plt.plot(range(2, 11), indice_davies_bisec, label="Bisection KMeans")
    plt.xlabel("Nombre de clusters")
    plt.ylabel("Indice")
    plt.title("Indice Davies-Bouldin")
    plt.legend()
    plt.show()

#graphique_score()

