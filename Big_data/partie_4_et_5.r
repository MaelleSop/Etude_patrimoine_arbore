#fichier csv non vectorialisé
f <- read.csv("/home/bap/cours/postbac/CIR3/projet_A3/BigData/RProject/pete_smr.csv")

#*------------------------------/ Coefficient de corrélation Pearson et régression linéaire \------------------------------*#

# Sélectionner les colonnes numériques
numeric_columns <- sapply(f, is.numeric)
f_numeric <- f[, numeric_columns]


# Calculer la matrice de corrélation de Pearson
correlations <- cor(f_numeric, use="complete.obs", method = "pearson")

# Visualiser la matrice de corrélation
if (!require("corrplot")) {
  install.packages("corrplot")
  library(corrplot)
}
corrplot(correlations, method="circle")

# Visualiser les relations bivariées
pairs(f_numeric)

# Régression de age en fonction du diametre du tronc
coeff = coef(lm(f_numeric$age_estim ~ f_numeric$tronc_diam))
plot(x = f_numeric$tronc_diam, y = f_numeric$age_estim)
curve(expr = coeff[1] + coeff[2]*x, add=T)


#Regression de age en fonction du diamètre, du stadedev, de la precision, hauteur totale, hauteur tronc
modelAge = lm(f_numeric$age_estim ~ f_numeric$tronc_diam + f_numeric$haut_tot + f_numeric$haut_tronc + f_numeric$fk_stadedev + f_numeric$fk_prec_estim)

#*------------------------------/ Fin coefficient de corrélation Pearson et régression linéaire\------------------------------*#



#*------------------------------/ DEBUT ANALYSE BIVARIEES \------------------------------*#

#Covariance en ométtant les valeurs manquantes
"covariance age / hauteur tot"
cov(data$age_estim, data$haut_tot, use="complete.obs")

"covariance hauteur tronc / diametre tronc"
cov(data$haut_tronc, data$tronc_diam, use="complete.obs")


#Tableau de contingence 
table_contingence <- table(data2$feuillage, data2$fk_situation)
print("Tableau de contingence :")
print(table_contingence)

chi2_result <- chisq.test(table_contingence)

if (chi2_result$p.value < 0.05) {
  print("Les variables sont dépendantes (p < 0.05).")
} else {
  print("Les variables sont indépendantes (p >= 0.05).")
}


#Stade de dev et état
table_contingence1 <- table(data$fk_stadedev, data$fk_arb_etat)
chi2_result1 <- chisq.test(table_contingence1)
mosaicplot(table_contingence1, main = "Relation entre le stade de developpement et l'état de l'arbre", xlab = "Stade de developpement", ylab = "Etat",  color = TRUE)


#Feuillage et situation
table_contingence2 <- table(data2$feuillage, data2$fk_situation)
chi2_result2 <- chisq.test(table_contingence2)
mosaicplot(table_contingence2, main = "Relation entre le feuillage et la situation", xlab = "Feuillage", ylab = "Situation", color = TRUE)


#Quartier et stade de dev
table_contingence3 <- table(data$clc_quartier, data$fk_stadedev)
chi2_result3 <- chisq.test(table_contingence3)
mosaicplot(table_contingence3, main = "Relation entre le quartier et le stade de developpement", xlab = "Quartier", ylab = "Stade de developpement", color = TRUE)


#Pied et port 
table_contingence4 <- table(data$fk_pied, data$fk_port)
chi2_result4 <- chisq.test(table_contingence4)
mosaicplot(table_contingence4, main = "Relation entre le pied et le port", xlab = "Pied", ylab = "Port", color = TRUE)


#Feuillage et remarquables 
table_contingence5 <- table(data$feuillage, data$remarquable)
chi2_result5 <- chisq.test(table_contingence5)
mosaicplot(table_contingence5, main = "Relation entre le quartier et le port", xlab = "Quartier", ylab = "Port", color = TRUE)

#*------------------------------/ FIN ANALYSE BIVARIEES \------------------------------*#



#*------------------------------/ Regression logistique \------------------------------*#

############### Regression logistique ######################
# Créer la variable binaire fk_arb_etat_bin (1 pour 'en place', 0 pour les autres)
f_numeric$fk_arb_etat_bin <- ifelse(f$fk_arb_etat == 3, 1, 0)
# Créer le modèle de régression logistique
model_logistic <- glm(fk_arb_etat_bin ~ X + clc_quartier + haut_tronc + fk_stadedev + fk_prec_estim + clc_nbr_diag + remarquable, data = f_numeric)

#*------------------------------/ Fin regression logistique \------------------------------*#
