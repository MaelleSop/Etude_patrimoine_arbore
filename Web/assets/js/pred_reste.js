function predCallback(myJson){
    document.getElementById("corps").style.display = "none";
    document.getElementById("apres-ajax").style.display = "block";
    //Si on predit l'age ou l'enracinement
    switch(myJson["prediction"]){
        case "age":
            //insertion des predictions dans le tableau
            document.getElementById("super-titre").innerHTML = "Prédiction sur l'âge de l'arbre";
            document.getElementById("tab-titre-1").innerHTML = "RFC";
            document.getElementById("tab-titre-2").innerHTML = "MLP";
            document.getElementById("tab-titre-3").innerHTML = "SGD";
            document.getElementById("tab-l1-c1").innerHTML = myJson["rfc"];
            document.getElementById("tab-l1-c2").innerHTML = myJson["mlp"];
            document.getElementById("tab-l1-c3").innerHTML = myJson["sgd"];
            break;
        case "tempete":
            //transforme le binaire en phrase
            switch(myJson["sgd"]["arbre_deracine:"]){
                case 0:
                    $sgd = "Ne va pas être déraciné";
                    break;
                case 1:
                    $sgd = "Va être déraciné";
                    break;
            }
            switch(myJson["rfc"]["arbre_deracine:"]){
                case 0:
                    $rfc = "Ne va pas être déraciné";
                    break;
                case 1:
                    $rfc = "Va être déraciné";
                    break;
            }
            switch(myJson["log_reg"]["arbre_deracine:"]){
                case 0:
                    $log = "Ne va pas être déraciné";
                    break;
                case 1:
                    $log = "Va être déraciné";
                    break;
            }
            //insertion des predictions dans le tableau
            document.getElementById("super-titre").innerHTML = "Prédiction sur le deracinement de l'arbre en cas de tempête";
            document.getElementById("tab-titre-1").innerHTML = "RFC";
            document.getElementById("tab-titre-2").innerHTML = "log_reg";
            document.getElementById("tab-titre-3").innerHTML = "SGD";
            document.getElementById("tab-l1-c1").innerHTML = $rfc;
            document.getElementById("tab-l1-c2").innerHTML = $log;
            document.getElementById("tab-l1-c3").innerHTML = $sgd;
    }
}

//Récupere les valeurs des features pour prédire l'âge
document.getElementById("age").onclick = () => {
    longitude = document.getElementById("longitude").value;
    latitude = document.getElementById("latitude").value;
    haut_tronc = document.getElementById("haut_tronc").value;
    haut_tot = document.getElementById("haut_tot").value;
    type_situation = document.getElementById("type_situation").value;
    precision_estime = document.getElementById("precision_estime").value;
    type_revetement = document.getElementById("type_revetement").value;
    tronc_diam = document.getElementById("tronc_diam").value;
    clc_nbr_diag = document.getElementById("clc_nbr_diag").value;
    typ_dev = document.getElementById("typ_dev").value;
    type_pied = document.getElementById("type_pied").value;
    type_feuillage = document.getElementById("type_feuillage").value;
    nom = document.getElementById("nom").value;
    remarquabe = document.getElementById("remarq").value;
    port = document.getElementById("type_port").value;

    ajaxRequest("POST", "php/requests.php/pred_age", predCallback, "longitude="+longitude+"&latitude="+latitude+"&haut_tronc="+haut_tronc+"&haut_tot="+haut_tot+"&type_situation="+type_situation+"&precision_estime="+precision_estime+"&type_revetement="+type_revetement+"&tronc_diam="+tronc_diam+"&clc_nbr_diag="+clc_nbr_diag+"&typ_dev="+typ_dev+"&type_pied="+type_pied+"&type_feuillage="+type_feuillage+"&nom="+nom+"&remarquable="+remarquabe+"&port="+port);
}

//Récupere les valeurs des features pour prédire le deracinement
document.getElementById("deracine").onclick = () => {
    longitude = document.getElementById("longitude").value;
    latitude = document.getElementById("latitude").value;
    haut_tronc = document.getElementById("haut_tronc").value;
    haut_tot = document.getElementById("haut_tot").value;
    type_situation = document.getElementById("type_situation").value;
    precision_estime = document.getElementById("precision_estime").value;
    type_revetement = document.getElementById("type_revetement").value;
    tronc_diam = document.getElementById("tronc_diam").value;
    clc_nbr_diag = document.getElementById("clc_nbr_diag").value;
    typ_dev = document.getElementById("typ_dev").value;
    type_pied = document.getElementById("type_pied").value;
    type_feuillage = document.getElementById("type_feuillage").value;
    nom = document.getElementById("nom").value;
    remarquabe = document.getElementById("remarq").value;
    port = document.getElementById("type_port").value;

    ajaxRequest("POST", "php/requests.php/pred_racine", predCallback, "longitude="+longitude+"&latitude="+latitude+"&haut_tronc="+haut_tronc+"&haut_tot="+haut_tot+"&type_situation="+type_situation+"&precision_estime="+precision_estime+"&type_revetement="+type_revetement+"&tronc_diam="+tronc_diam+"&clc_nbr_diag="+clc_nbr_diag+"&typ_dev="+typ_dev+"&type_pied="+type_pied+"&type_feuillage="+type_feuillage+"&nom="+nom+"&remarquable="+remarquabe+"&port="+port);
}

//Si pas de token renvoie vers la connexion
if (typeof Cookies.get("token") == "undefined"){
    window.location.href = "sign_in.html";
}

//Affiche l'identifiant
document.getElementById("button-id").innerHTML = Cookies.get("username");