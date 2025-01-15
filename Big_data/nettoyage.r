#install.packages("stringi")
library(stringi)

######################### Definitions fonctions ##########################################

#Decale des variables dans une liste, from > to
slide <- function(from, to, list2Slide){
   i <- from
  while (i < to){
      list2Slide <- ifelse(list2Slide == i+1, i, list2Slide)
      i <- i+1
  }
  return(list2Slide)
}

# Fonction pour calculer l'âge à partir de la date de plantation
calculate_age <- function(date_str) {
  date <- as.Date(strsplit(date_str, "\\+")[[1]][1], format="%Y/%m/%d %H:%M:%S")
  floor(as.numeric(difftime(Sys.Date(), date, units = "weeks")) / 52.25)
}

#Fonction pour mettre des moyennes cohérentes là où des valeurs manquent
remplir_hauteur_diametre <- function(df) {
  # Remplacer les valeurs manquantes dans la colonne hauteur
  for (i in 1:nrow(df)) {
    #Verifie si des hauteurs totales sont vides
    if (is.na(df$haut_tot[i])) {
      #calcul la moyenne des hauteurs totales par apport au meme diametre des troncs
      moyenne_hauteur <- mean(df$haut_tot[df$tronc_diam == df$tronc_diam[i]], na.rm = TRUE)
      df$haut_tot[i] <- floor(moyenne_hauteur)
    }
    #Verifie si des hauteurs de troncs sont vides
    if (is.na(df$haut_tronc[i])){
      #calcul la moyenne des hauteurs de tronc par apport au meme diametre des troncs
      moyenne_haut_tronc <- mean(df$haut_tronc[df$tronc_diam == df$tronc_diam[i]], na.rm = TRUE)
      df$haut_tronc[i] <- floor(moyenne_haut_tronc)
    }
    #Verifie si des diametres de troncs sont vides
    if (is.na(df$tronc_diam[i])){
      #calcul la moyenne des diametres par apport à la meme hauteur des arbres
      moyenne_tronc_diam <- mean(df$tronc_diam[df$haut_tot == df$haut_tot[i]], na.rm = TRUE)
      df$tronc_diam[i] <- floor(moyenne_tronc_diam)
    }
  }
  
  return(df)
}

isEmpty <- function(test){
  return(is.na(test) | test == "")
}

remplir_stade_dev <- function(df){
  
  #Calcul le quantile à 0.9 de l'age pour chaque stade de developpement 
  q_jeune = quantile(df$age_estim[df$fk_stadedev == 1],0.9,na.rm = TRUE)
  print(q_jeune)
  q_adulte = quantile(df$age_estim[df$fk_stadedev == 2],0.9,na.rm = TRUE)
  print(q_adulte)
  q_vieux = quantile(df$age_estim[df$fk_stadedev == 4],0.9,na.rm = TRUE) 
  print(q_vieux)
  
  if (is.na(q_jeune) | is.na(q_adulte) | is.na(q_vieux)) {
    stop("Erreur : Un ou plusieurs quantiles sont NA.")
  }
  
  for (i in 1:nrow(df)){
    if (!isEmpty(df$age_estim[i]) & isEmpty(df$fk_stadedev[i])) {
      #si l'age est inf au quantile de jeune
      if(df$age_estim[i] <= q_jeune){
        df$fk_stadedev[i] <- 1
      }
      #si l'age est inf au quantile de adulte
      else if(df$age_estim[i] <= q_adulte){
        df$fk_stadedev[i] <- 2
      }
      #si age est inf au quantile de vieux
      else if(df$age_estim[i] <= q_vieux){
        df$fk_stadedev[i] <- 4
      }
      #si age est sup à tous alors senescent
      else {
        df$fk_stadedev[i] <- 3
      }
    }
  }
  return(df)
}

remplir_nom_quartier <- function(df){
  
  for (i in 1:nrow(df)){
    if(is.na(df$clc_quartier[i]) & !is.na(df$clc_secteur[i])){
      noms <- unique(na.omit(df$clc_quartier[df$clc_secteur == df$clc_secteur[i]]))
      if (length(noms) == 1) {
        df$clc_quartier[i] <- noms
      }
    }
  }
  
  return(df)
}

#####################################################################################################

#Lire le fichier
f = read.table("/home/bap/cours/postbac/CIR3/projet_A3/BigData/Patrimoine_Arboré_(RO).csv", header = TRUE, sep = ",", quote = "\"", stringsAsFactors = FALSE)

#Données à convertir au format numérique
data2Convert = c("created_user", "src_geo", "clc_quartier", "fk_arb_etat", "fk_stadedev", "fk_port", "fk_pied", "fk_situation", "fk_revetement", "last_edited_user", "villeca", "Creator", "Editor", "feuillage", "remarquable")

#Passage des cellules vide en NA
for (colonne in f){
  colonne <- ifelse(colonne == "", NA, colonne)
}

# Convertir le texte en chiffre
unique_values <- list()
value_mappings <- list()
for (colonne in data2Convert) {
  f[[colonne]] <- gsub("\\.", " ", tolower(stri_trans_general(trimws(f[[colonne]]), "Latin-ASCII")))

  # Obtenir les valeurs uniques
  unique_values <- unique(f[[colonne]])
  
  # Créer un vecteur de numéros associés
  value_mapping <- setNames(seq_along(unique_values), unique_values)
  
  # Stocker le mapping dans la liste
  value_mappings[[colonne]] <- value_mapping
  
  # Remplacer les valeurs dans la colonne par les numéros associés
  f[[colonne]] <- value_mapping[f[[colonne]]]
}

#Remplace "orthophoto plan" (5) par "plan ortho" (4)
f$src_geo <- ifelse(f$src_geo == 5, 4, f$src_geo)
#Remplace "plan ortho" (4) par "orthophoto" (1)
f$src_geo <- ifelse(f$src_geo == 4, 1, f$src_geo)

#Decalage d'incices, y en a qui correspondent à vide au milieu des listes
f$created_user <- slide(2, 4, f$created_user)
f$src_geo <- ifelse(f$src_geo == 3, 2, f$created_user)
f$clc_quartier <- ifelse(f$clc_quartier == 12, 11, f$clc_quartier )
f$fk_stadedev <- slide(1, 5, f$fk_stadedev)
f$fk_port <- slide(1, 14, f$fk_port)
f$fk_pied <- slide(1, 9, f$fk_pied)
f$fk_revetement <- slide(1, 3, f$fk_revetement)
f$Creator <- slide(2, 3, f$Creator)
f$Editor <- slide(2, 3, f$Editor)
f$feuillage <- slide(1, 3, f$feuillage)

# Supprimer les lignes avec des valeurs NA dans les colonnes X et Y
f <- f[!is.na(f$X) & !is.na(f$Y), ]

#Supprimer les lignes avec des valeurs NA dans fk_arb_etat (correspond aux lignes avec uniquement X et Y)
f <- f[!isEmpty(f$fk_arb_etat), ]

#Supprime un arbre pas trop possible
f <- f[f$OBJECTID != 6777, ]

#Supprime les arbres avec un age > 1000
f <- f[f$age_estim < 1000 | is.na(f$age_estim) | f$age_estim == "", ]

#Remplace l'etat des arbres ayant une date d'abatage et un etat "en place" par l'etat "abattu" (2)
f$fk_arb_etat <- ifelse(!(isEmpty(f$dte_abattage)), 2, f$fk_arb_etat)

#Changement d'une faute de frappe
f$clc_secteur <- ifelse(f$clc_secteur == "Griourt", "Gricourt", f$clc_secteur)

#Calcul de l'age s'il n'existe pas
f$age_estim <- mapply(function(age, date) {
  if ((isEmpty(age)) && !isEmpty(date)) {
    calculate_age(date)
  } else {
    age
  }
}, f$age_estim, f$dte_plantation)

#Remplire les hauteurs des arbres 
f = remplir_hauteur_diametre(f)

#Remplir la colonne fk_port par "inconnue" (14) si la cellule est vide
f$fk_port <- ifelse(isEmpty(f$fk_port), 14, f$fk_port)

#Remplir la colonne fk_pied par "inconnue" (9) si la cellule est vide
f$fk_pied <- ifelse(isEmpty(f$fk_pied), 9, f$fk_pied)

#Remplir la colonne fk_revetement par "inconnue" (3) si la cellule est vide
f$fk_revetement <- ifelse(isEmpty(f$fk_revetement), 3, f$fk_revetement)

#Remplir la colonne feuillage par "inconnue" (3) si la cellule est vide
f$feuillage <- ifelse(isEmpty(f$feuillage), 3, f$feuillage)

f = remplir_stade_dev(f)

f = remplir_nom_quartier(f)

#Valeure incohérente pour l'ordonnée d'un arbre => suppression
f <- subset(f, Y<8297500)

#Filtrage d'une colonne
f$clc_secteur <- tolower(stri_trans_general(trimws(f$clc_secteur), "Latin-ASCII"))

#Suppression de colonnes redondantes
f <- subset(f, select = -fk_nomtech)
f <- subset(f, select = -nomlatin)

write.csv(f, file = "Patrimoine_Arbore_final.csv", row.names = FALSE)
