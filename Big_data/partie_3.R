#======================================================================================#
#=================================FONCTIONNALITÉ 3=====================================#
#======================================================================================#

#------------------------------------------CARTE ARBRE DE LA VILLE--------------------------------#
#On charge les bibliothèques nécessaires
library(leaflet)
library(readr)
library(sf)

#On lit les données
data <- "Patrimoine_Arbore_final_caractere.csv"
data <- read_csv(data)

#On crée un objet sf avec les coordonnées Lambert CC Zone 49
coord_sf <- st_as_sf(data, coords = c("X", "Y"), crs = 3949)

#On transforme les coordonnées en WGS84
coord_wgs84 <- st_transform(coord_sf, crs = 4326)

#On extrait les nouvelles colonnes de longitude et latitude
data$lon <- st_coordinates(coord_wgs84)[,1]
data$lat <- st_coordinates(coord_wgs84)[,2]

#On crée une carte leaflet
map <- leaflet(data) %>%
  addTiles() %>%
  addCircleMarkers(~lon, ~lat, radius = 1, color = "green")

#On affiche la carte
map

#-------------------------------------------ARBRE PAR QUARTIER--------------------------------#
#On charge les bibliothèques nécessaires
library(leaflet)
library(readr)
library(sf)
library(RColorBrewer)

#On lit les données
data <- "Patrimoine_Arbore_final_caractere.csv"
data <- read_csv(data)

#On crée un objet sf avec les coordonnées Lambert CC Zone 49
coord_sf <- st_as_sf(data, coords = c("X", "Y"), crs = 3949)

#On transforme les coordonnées en WGS84
coord_wgs84 <- st_transform(coord_sf, crs = 4326)

#On extrait les nouvelles colonnes de longitude et latitude
data$lon <- st_coordinates(coord_wgs84)[,1]
data$lat <- st_coordinates(coord_wgs84)[,2]

#On crée une palette de couleurs basée sur les quartiers
unique_quartiers <- unique(data$clc_quartier)
palette <- brewer.pal(length(unique_quartiers), "Paired")

#On crée une fonction de couleur pour les quartiers
pal <- colorFactor(palette, domain = unique_quartiers)

#On crée une carte leaflet et une légende
map <- leaflet(data) %>%
  addTiles() %>%
  addCircleMarkers(~lon, ~lat, radius = 1, color = ~pal(clc_quartier)) %>%
  addLegend("bottomright", pal = pal, values = ~clc_quartier,title = "Quartiers",opacity = 1)

#On affiche la carte
map


#---------------------------------------ARBRE REMARQUABLE------------------------#
#On charge les bibliothèques nécessaires
library(leaflet)
library(readr)
library(sf)

#On lit les données
data <- "Patrimoine_Arbore_final_caractere.csv"
data <- read_csv(data)

#On garde seulement les arbres remarquable
data <- subset(data, remarquable == "oui")

#On crée un objet sf avec les coordonnées Lambert CC Zone 49
coord_sf <- st_as_sf(data, coords = c("X", "Y"), crs = 3949)

#On transforme les coordonnées en WGS84
coord_wgs84 <- st_transform(coord_sf, crs = 4326)

#On extrait les nouvelles colonnes de longitude et latitude
data$lon <- st_coordinates(coord_wgs84)[,1]
data$lat <- st_coordinates(coord_wgs84)[,2]

#On crée une carte leaflet
map <- leaflet(data) %>%
  addTiles() %>%
  addCircleMarkers(~lon, ~lat, radius = 2, color = "green")

#On affiche la carte
map


#-------------------------------------STADE DE DEVELOPPEMENT-----------------#
#On charge les bibliothèques nécessaires
library(leaflet)
library(readr)
library(sf)
library(RColorBrewer)

#On lit les données
data <- "Patrimoine_Arbore_final_caractere.csv"
data <- read_csv(data)

#On crée un objet sf avec les coordonnées Lambert CC Zone 49
coord_sf <- st_as_sf(data, coords = c("X", "Y"), crs = 3949)

#On transforme les coordonnées en WGS84
coord_wgs84 <- st_transform(coord_sf, crs = 4326)

#On extrait les nouvelles colonnes de longitude et latitude
data$lon <- st_coordinates(coord_wgs84)[,1]
data$lat <- st_coordinates(coord_wgs84)[,2]

#On défini dans l'ordre croissant le stade de développement
triee_stadedev <- c("jeune", "adulte", "vieux", "senescent")

#On réorganise correctement les valeurs dans notre base de donnée
data$fk_stadedev <- factor(data$fk_stadedev, levels = triee_stadedev)

#On crée notre palette de couleur
unique_couleurs <- brewer.pal(length(triee_stadedev), "YlOrRd")

#On met nos couleurs par ordre d'intensitée
couleurs <- unique_couleurs[c(2, 1, 4, 3)]
palette <- colorFactor(couleurs, domain = triee_stadedev)

#On crée une carte leaflet avec une légende
map <- leaflet(data) %>%
  addTiles() %>%
  addCircleMarkers(~lon, ~lat, radius = 1, color = ~palette(fk_stadedev)) %>%
  addLegend("bottomright", pal = palette, values = ~fk_stadedev, title = "Stade de développement", opacity = 1)

#On affiche la carte
map