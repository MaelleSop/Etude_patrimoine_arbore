function pred_taille_callback(json){
    //Réécriture de la page avec les nouveaux div
    let form = document.getElementById("corps");
    let prediction = document.getElementById("prediction_taille");
    let map = document.getElementById("map");
    let legende =document.getElementById("legende");
    let btn_ajout = document.getElementById("btn_ajout");
    form.style.display = 'none';
    prediction.style.display = 'block';
    legende.style.display = 'block';
    map.style.display = 'block';
    btn_ajout.style.display = 'block';

    try{
        json = JSON.parse(json.split("\n")[2].split("<")[0]);
    }
    catch{
        try{
            json = JSON.parse(json);
        }
        catch{
            console.log("erreur");
        }
    }

    //Initialisation des variables pour les clusters
    let size = json.length;
    let longitude = [];
    let latitude = [];
    let infos = [];
    let color = [];
    let trois_clusters = false;

    //Récupération des informations pour la map
    for(let i=0; i<size; i++){
        longitude.push(json[i][0]['longitude']);
        latitude.push(json[i][0]['latitude']);
        infos.push(`
        Nom : ${json[i][0]['nom']}<br>
        Hauteur tronc : ${json[i][0]['haut_tronc']}<br>
        Diamètre du tronc : ${json[i][0]['tronc_diam']}<br>
        Age estimé : ${json[i][0]['age_estim']}<br>
        Remarquable : ${json[i][0]['remarq']}<br>
        Longitude : ${json[i][0]['longitude']}<br>
        Latitude : ${json[i][0]['latitude']}<br>
        État : ${json[i][0]['etat']}<br>
        Stade de développement : ${json[i][0]['type_dev']}<br>
        Type de port : ${json[i][0]['type_port']}<br>
        Type de pied : ${json[i][0]['type_pied']}<br>`);
        
        //Différentes couleurs selon le cluster
        if(json[i][1] == '0'){
            color.push('#FF5733');
        }
        else if(json[i][1] == '1'){
            color.push('#606ADF');
        }
        else{
            color.push('#9B3F9C');
            trois_clusters = true;
        }
    }

    //Préparation de la légende
    let legendItem;
    let number;
    if(trois_clusters != true){
        legendItem = [{color: '#606ADF', name: 'Petit'}, {color: '#FF5733', name: 'Grand'}];
        if(json[49][1] == '0'){
            number = 'Grand';
        }
        else{
            number = 'Petit';
        }
    }
    else{
        legendItem = [{color: '#606ADF', name: 'Petit'}, {color: '#FF5733', name: 'Moyen'}, {color: '#9B3F9C', name: 'Grand'}];
        if(json[49][1] == '0'){
            number = 'Moyen';
        }
        else if(json[49][1] == '1'){
            number = 'Petit';
        }
        else{
            number = 'Grand';
        }
    }

    //Affichage de la prédiction
    prediction.innerHTML = "<p>L'arbre ajouté appartient au cluster : "+ number +".</p>";

    //Affichage de la légende
    let legendHTML = '<div class="legend">';
    legendHTML += '<p>Légende :</p>';
    legendItem.forEach(item => {
        legendHTML += `
            <div class="legend-item">
                <div class="legend-color" style="background-color: ${item.color};"></div>
                <span>${item.name}</span>
            </div>
        `;
    });
    legendHTML += '</div>';
    legende.innerHTML = legendHTML;

    //récupération des données pour la map
    var data = [
        {
            type: "scattermapbox",
            text: infos,
            lon: longitude,
            lat: latitude,
            marker: { color: color, size: 6 }
        }
    ];
    var layout = {
        dragmode: "zoom",
        mapbox: { style: "open-street-map", center: { lat: 49.8406544, lon: 3.2905211 }, zoom: 11 },
        margin: { r: 0, t: 0, b: 0, l: 0 }
    };
    //Affichage de la map
    Plotly.newPlot("map", data, layout);

    //Affichage du bouton ajout arbre et réécriture de la page
    btn_ajout.innerHTML = '<br><form id="btn_ajouter"><input class="btn btn-primary" type="submit" value="Ajouter un arbre"> <br>';
    document.getElementById("btn_ajouter").onsubmit = (event) => {
        form.style.display = 'block';
        prediction.style.display = 'none';
        legende.style.display = 'none';
        map.style.display = 'none';
        btn_ajout.style.display = 'none';
    }
}

document.getElementById("form_taille").onsubmit = (event) => {
    event.preventDefault()
    // récupération des valeurs des champs
    longitude = document.getElementById("longitude").value;
    latitude = document.getElementById("latitude").value;
    haut_tronc = document.getElementById("haut_tronc").value;
    tronc_diam = document.getElementById("tronc_diam").value;
    age_estim = document.getElementById("age_estim").value;
    type_situation = document.getElementById("type_situation").value;
    type_port = document.getElementById('type_port').value;
    precision_estime = document.getElementById("precision_estime").value;
    type_revetement = document.getElementById("type_revetement").value;
    clc_nbr_diag= document.getElementById("clc_nbr_diag").value;
    type_dev = document.getElementById("type_dev").value;
    type_pied = document.getElementById("type_pied").value;
    type_feuillage = document.getElementById("type_feuillage").value;
    remarq = document.getElementById("remarq").value
    etat = document.getElementById("etat").value;
    nom = document.getElementById("nom").value;
    nbr_cluster = document.getElementById("nbr_cluster").value;
    methode = document.getElementById("methode").value;
    
    ajaxRequest("POST", "php/requests.php/taille_arbre", pred_taille_callback, "longitude="+longitude+"&latitude="+latitude+"&haut_tronc="+haut_tronc+"&tronc_diam="+tronc_diam+"&age_estim="+age_estim+"&type_situation="+type_situation+"&type_port="+type_port+"&precision_estime="+precision_estime+"&type_revetement="+type_revetement+"&clc_nbr_diag="+clc_nbr_diag+"&type_dev="+type_dev+"&type_pied="+type_pied+"&type_feuillage="+type_feuillage+"&remarq="+remarq+"&etat="+etat+"&nom="+nom+"&nbr_cluster="+nbr_cluster+"&methode="+methode);
}

//Si pas de token renvoie vers la connexion
if (typeof Cookies.get("token") == "undefined"){
    window.location.href = "sign_in.html";
}

//Affiche l'identifiant
document.getElementById("button-id").innerHTML = Cookies.get("username");