# Installation des dépendances
```
$ python3 -m pip install requirements.txt
```
# Script pour les modèles d'apprentissage non-supervisé
## Notice d'utilisation
```
usage: script_fonctionnalite1.py [-h] methode nbr_cluster age_estim haut_tronc tronc_diam

Fonctionnalité 1 : prédire la taille d'un arbre

positional arguments:
  methode      Méthode (KMeans : 1, Birch : 2, Bisection KMeans : 3)
  nbr_cluster  Nombre de cluster
  age_estim    Age estimé de l'arbre
  haut_tronc   Hauteur du tronc
  tronc_diam   Diamètre du tronc

options:
  -h, --help   show this help message and exit
```
## Exemple d'utilisation
```
$ python3 script_fonctionnalite1.py 1 3 15 2 37
```
# Script pour les modèles d'apprentissage supervisé
## Fonctionnalité 2
### Notice d'utilisation
```
usage: script_fonctionnalite2.py [-h] -td TRONC_DIAM -hto HAUT_TOT -htr HAUT_TRONC -fpe FK_PREC_ESTIM -fsd FK_STADEDEV -fpd FK_PIED
                                 -ff FEUILLAGE -fs FK_SITUATION -cnd CLC_NBR_DIAG -m {sgd,rfc,mlp}

Fonctionnalité 2 : prédire l'âge d'un arbre à partir de ses caractéristiques

options:
  -h, --help            show this help message and exit
  -td TRONC_DIAM, --tronc_diam TRONC_DIAM
                        Diamètre du tronc
  -hto HAUT_TOT, --haut_tot HAUT_TOT
                        Hauteur totale
  -htr HAUT_TRONC, --haut_tronc HAUT_TRONC
                        Hauteur du tronc
  -fpe FK_PREC_ESTIM, --fk_prec_estim FK_PREC_ESTIM
                        Estimation précédente
  -fsd FK_STADEDEV, --fk_stadedev FK_STADEDEV
                        Stade de développement
  -fpd FK_PIED, --fk_pied FK_PIED
                        Pied
  -ff FEUILLAGE, --feuillage FEUILLAGE
                        Feuillage
  -fs FK_SITUATION, --fk_situation FK_SITUATION
                        Situation
  -cnd CLC_NBR_DIAG, --clc_nbr_diag CLC_NBR_DIAG
                        Nombre de diagnostics
  -m {sgd,rfc,mlp}, --model {sgd,rfc,mlp}
                        Modèle à utiliser (sgd, rfc, mlp)
```
### Exemple
```
$ python3 script_fonctionnalite2.py -td 37.0 -hto 6.0 -htr 2.0 -fpe 5.0 -fsd 1.0 -fpd 4.0 -ff 1.0 -fs 0.0 -cnd 0.0 -m mlp
```
## Fonctionnalité 3
### Notice d'utilisation
```
usage: script_fonctionnalite3.py [-h] [-r] [-s] [-d] [-l] -m {sgd,log_reg,forest}

Fonctionnalité 3 : prédire si un arbre va être déraciné par la tempête

options:
  -h, --help            show this help message and exit
  -r, --fk_revetement   Inclure la colonne fk_revetement, mettre 1 pour oui et 0 pour non
  -s, --fk_situation    Inclure la colonne fk_situation, mettre 0 pour Alignement, 1 pour Groupe et 2 pour Alignement
  -d, --clc_nbr_diag    Inclure la colonne clc_nbr_diag
  -l, --longitude       Inclure la colonne longitude
  -m {sgd,log_reg,forest}, --model {sgd,log_reg,forest}
                        Modèle à utiliser (sgd, log_reg, forest)
```
### Exemple
```
$ python3 script_fonctionnalite3.py -r 0  -s 0 -d 0 -l 3.2932636093638927
```