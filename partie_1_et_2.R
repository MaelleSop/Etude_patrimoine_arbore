
#Appel des fichiers
data = Patrimoine_Arbore_final
data2 = Patrimoine_Arbore_final_caractere

#*------------------------------/ DEBUT CALCULS DES FREQUENCES \------------------------------*#

data2Filter = c("OBJECTID","created_user", "src_geo", "clc_quartier", "clc_secteur", "fk_arb_etat", "fk_stadedev", "fk_port", "fk_pied", "fk_situation", "fk_revetement", "commentaire_environnement", "dte_plantation", "age_estim", "fk_nomtech", "last_edited_user", "villeca", "nomfrancais", "nomlatin", "Creator", "Editor", "feuillage", "remarquable")
frequency_tables <- list()
for (column in data2Filter) {
  frequency_tables[[column]] <- table(data[[column]])
}

arbres_total = length(frequency_tables$OBJECTID)
arbres_total

#*------------------------------/ FIN CALCULS DES FREQUENCES \------------------------------*#



#*------------------------------/ DEBUT STATS DESCRIPTIVES UNIVARIEES \------------------------------*#

#Hauteur des arbres
moy_haut = mean(data$haut_tot, na.rm = TRUE)
moy_haut
moy_haut_reel = mean(data$haut_tot[data$fk_arb_etat == 3], na.rm = TRUE)
moy_haut_reel
ecart_type_haut = sd(data$haut_tot, na.rm = TRUE)
ecart_type_haut


#Hauteur des troncs 
moy_haut_tron = mean(data$haut_tronc, na.rm = TRUE)
moy_haut_tron
moy_haut_tronc_reel = mean(data$haut_tronc[data$fk_arb_etat == 3], na.rm = TRUE)
moy_haut_tronc_reel
ecart_type_tron = sd(data$haut_tronc, na.rm = TRUE)
ecart_type_tron


#Diamètre des troncs
moy_diam_tron = mean(data$tronc_diam, na.rm = TRUE)
moy_diam_tron
moy_diam_tron_reel = mean(data$tronc_diam[data$fk_arb_etat == 3], na.rm = TRUE)
moy_diam_tron_reel
ecart_type_diam_tron = sd(data$tronc_diam, na.rm = TRUE)
ecart_type_diam_tron


#Age
moy_age = mean(data$age_estim, na.rm = TRUE)
moy_age
min_age = min(data$age_estim, na.rm = TRUE)
min_age
max_age = max(data$age_estim, na.rm = TRUE)
max_age


#Stade dev
jeunes = frequency_tables$fk_stadedev[1]
adultes = frequency_tables$fk_stadedev[2]
senescents = frequency_tables$fk_stadedev[3]
vieux = frequency_tables$fk_stadedev[4]
total = jeunes + adultes + senescents + vieux
prc_jeunes = (jeunes/total)*100
prc_jeunes
prc_ad = (adultes/total)*100
prc_ad
prc_sen = (senescents/total)*100
prc_sen
prc_vi = (vieux/total)*100
prc_vi


#Arbres remarquables
oui = frequency_tables$remarquable[2]
oui
non = frequency_tables$remarquable[1]
non
total_remarq = oui + non
per_remarq = (oui/total_remarq)*100
per_remarq


#Feuillage
feuillu = frequency_tables$feuillage['1']
conifere = frequency_tables$feuillage['2']
inconnu = frequency_tables$feuillage['3']
total_feuillu = feuillu+conifere+inconnu
per_feuillu = (feuillu/total_feuillu)*100
per_feuillu


#Object id
all_unique_objectid <- length(data$OBJECTID) == length(unique(data$OBJECTID))
all_unique_objectid


#Moyenne latitude/longitude
moyX = mean(data$X, na.rm= TRUE)
moyY = mean(data$Y, na.rm = TRUE)
moyX
moyY


#Etat
per_etat_place = (10326/arbres_total)*100
per_etat_place


#Quartier
print(frequency_tables$clc_quartier)
quart_st_martin_o = (2048/arbres_total)*100
quart_st_martin_o
quart_remicourt = (1767/arbres_total)*100
quart_remicourt
quart_faubourg = (1749/arbres_total)*100
quart_faubourg


#Mode
mode_func <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}
mode_func(data$age_estim)
mode_func(data$fk_port)

#*------------------------------/ FIN STATS DESCRIPTIVES UNIVARIEES \------------------------------*#



#*------------------------------/ DEBUT STATS DESCRIPTIVES BIVARIEES \------------------------------*#

#Quantitatives
#Circonference tronc et age
plot(data$age_estim, data$tronc_diam, main="Relation entre l'âge et la diamètre du tronc", xlab="Age", ylab="Diamètre du tronc", pch = 19, cex=0.5, col = "blue")


#Qualitative et quantitative
#Age et quartier
boxplot( age_estim ~ clc_quartier, data = data, main = "Relation entre le quartier et l'âge", xlab ="Quartier", ylab="Age",  col = c("red", "green"))

#Moyenne d'age des arbres par quartier
moy_age_q1 = mean(data$age_estim[data$clc_quartier == 1], na.rm = TRUE)
moy_age_q1
moy_age_q2 = mean(data$age_estim[data$clc_quartier == 2], na.rm = TRUE)
moy_age_q2
moy_age_q3 = mean(data$age_estim[data$clc_quartier == 3], na.rm = TRUE)
moy_age_q3
moy_age_q4 = mean(data$age_estim[data$clc_quartier == 4], na.rm = TRUE)
moy_age_q4
moy_age_q5 = mean(data$age_estim[data$clc_quartier == 5], na.rm = TRUE)
moy_age_q5
moy_age_q6 = mean(data$age_estim[data$clc_quartier == 6], na.rm = TRUE)
moy_age_q6
moy_age_q7 = mean(data$age_estim[data$clc_quartier == 7], na.rm = TRUE)
moy_age_q7
moy_age_q8 = mean(data$age_estim[data$clc_quartier == 8], na.rm = TRUE)
moy_age_q8
moy_age_q9 = mean(data$age_estim[data$clc_quartier == 9], na.rm = TRUE)
moy_age_q9
moy_age_q10 = mean(data$age_estim[data$clc_quartier == 10], na.rm = TRUE)
moy_age_q10
moy_age_q11 = mean(data$age_estim[data$clc_quartier == 11], na.rm = TRUE)
moy_age_q11
axe = c(1,2,3,4,5,6,7,8,9,10,11)
moy_age_q = c(moy_age_q1, moy_age_q2, moy_age_q3, moy_age_q4, moy_age_q5, moy_age_q6, moy_age_q7, moy_age_q8, moy_age_q9, moy_age_q10, moy_age_q11)
barplot(moy_age_q, main="Histogramme des moyennes d'age par quartier", xlab="Quartiers", ylab="Moyenne dâge", col="black")

#*------------------------------/ FIN STATS DESCRIPTIVES BIVARIEES \------------------------------*#



#*------------------------------/ DEBUT GRAPHIQUES UNIVARIEES \------------------------------*#

#Histogramme fréquence arbres par quartier
freq_clc_quartier <- frequency_tables$clc_quartier
barplot(freq_clc_quartier, main = "Histogramme représentant le nombre d'arbres par quartier", xlab = "Quartiers", ylab = "Fréquence", col = "red")


#Histogramme fréquence arbres par age
freq_age <- frequency_tables$age_estim
barplot(freq_age, main = "Histogramme des âges estimés", xlab = "Âge estimé", ylab = "Fréquence", col = "red")


#Histogramme fréquence arbres par état
freq_etat <- frequency_tables$fk_arb_etat
barplot(freq_etat, main="Répartition des arbres en fonction de leur état", xlab="Etat", ylab="Fréquence", col="black")


#Histogramme fréquence arbres par situation
freq_situation <- frequency_tables$fk_situation
barplot(freq_situation, main="Répartition des arbres en fonction de leur situation", xlab="Situation", ylab="Fréquence", col="black")


#Histogramme fréquence arbres par revetement
freq_revet <- frequency_tables$fk_revetement
barplot(freq_revet, main="Répartition des arbres en fonction de leur revêtement", xlab="Revêtement", ylab="Fréquence", col="red")


#Histogramme fréquence arbres par feuillage
freq_feuil <- frequency_tables$feuillage
barplot(freq_feuil, main="Répartition des arbres selon leur feuillage", xlab="Feuillage", ylab="Fréquence", col="black")

#*------------------------------/ FIN GRAPHIQUES UNIVARIEES \------------------------------*#
