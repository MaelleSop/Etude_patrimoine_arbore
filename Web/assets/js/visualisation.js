function parseCookies() {
    // Obtenir tous les cookies sous forme de chaîne
    var cookies = document.cookie;
    
    // Créer un objet pour stocker les paires clé-valeur des cookies
    var cookieDict = {};

    // Diviser la chaîne de cookies par "; " pour obtenir un tableau de paires clé=valeur
    var cookieArray = cookies.split('; ');

    // Parcourir chaque paire clé=valeur
    for (var i = 0; i < cookieArray.length; i++) {
        // Diviser chaque paire clé=valeur par "=" pour séparer la clé et la valeur
        var cookiePair = cookieArray[i].split('=');

        // La clé est la première partie
        var key = cookiePair[0];

        // La valeur est la deuxième partie, si elle existe (sinon une chaîne vide)
        var value = cookiePair[1] || '';

        // Ajouter la clé et la valeur à l'objet cookieDict
        cookieDict[key] = decodeURIComponent(value);
    }

    return cookieDict;
}

//Requete qui renvoie toutes les informations des arbres
document.addEventListener('DOMContentLoaded', () => {
    ajaxRequest("GET", "php/requests.php/visualisation", afficheInfoArbre);
});

//Requete qui renvoie les informations des arbres en fonction du stade de développement
document.addEventListener('change', (event) => {
    if (event.target.id === 'development-stage-select') {
        const selectedValue = event.target.value;    
        ajaxRequest("GET", `php/requests.php/visualisation/${selectedValue}`, afficheInfoArbre);
    }
});

//Requete qui renvoie les informations des arbres en fonction de leur remarquabilité
document.addEventListener('change', (event) => {
    if (event.target.id === 'remarquable-select') {
        const selectedValue = event.target.value;
        ajaxRequest("GET", `php/requests.php/visualisation_remarqu/${selectedValue}`, afficheInfoArbre);
    }
});

//Requete qui renvoie les informations des arbres en fonction de leur état
document.addEventListener('change', (event) => {
    if (event.target.id === 'etat-select') {
        const selectedValue = event.target.value;
        ajaxRequest("GET", `php/requests.php/visualisation_etat/${selectedValue}`, afficheInfoArbre);
    }
});

//Fonction qui affiche la carte principale du site et affiche le tableau des arbres (callback)
function afficheInfoArbre(info_arbre) {

    //Carte
    var data = [
        {
            type: "scattermapbox",
            text: info_arbre.map(arbre => generateHoverText(arbre)),
            lon: info_arbre.map(arbre => parseFloat(arbre.longitude)),
            lat: info_arbre.map(arbre => parseFloat(arbre.latitude)),
            hoverinfo: "text",
            marker: { color: "green", size: 6 }
        }
    ];

    var layout = {
        dragmode: "zoom",
        mapbox: { style: "open-street-map", center: { lat: 49.8406544, lon: 3.2905211 }, zoom: 11 },
        margin: { r: 0, t: 0, b: 0, l: 0 }
    };

    Plotly.newPlot("myDiv", data, layout);

    const corps = document.getElementById('table-container');

    if (!info_arbre.length) {
        corps.innerHTML = '<p>Aucun arbre trouvé.</p>';
        return;
    }

    let table = document.createElement('table');
    table.className = 'table table-striped';
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');

    // En-tête du tableau
    let headerRow = document.createElement('tr');
    const headers = ['ID', 'Espèce', 'Age', 'Hauteur Totale', 'Hauteur du Tronc', 'Diamètre du Tronc', 'Remarquable', 'Longitude', 'Latitude', 'État', 'Stade de développement', 'Forme de l\'arbre', 'Type de Pied', 'Afficher'];
    headers.forEach((headerText, index) => {
        let th = document.createElement('th');
        if (headerText === 'Remarquable'){
            th.innerHTML = 'Remarquable';
            let select = document.createElement('select');
            select.id = 'remarquable-select';
            select.className = 'form-select';
            select.innerHTML = `
                <option selected></option>
                <option value="1">Oui</option>
                <option value="0">Non</option>
                <option value="2">Tous</option>
            `;
            th.appendChild(select);
        } else if (headerText === 'État'){
            th.innerHTML = 'État';
            let select = document.createElement('select');
            select.id = 'etat-select';
            select.className = 'form-select';
            select.innerHTML = `
                <option selected></option>
                <option value="0">En place</option>
                <option value="1">Abattu</option>
                <option value="2">Essouché</option>
                <option value="3">Non-essouché</option>
                <option value="4">Remplacé</option>
                <option value="5">Supprimé</option>
                <option value="6">Tous</option>
            `;
            th.appendChild(select);
        } 
        else if (headerText === 'Stade de développement') {
            th.innerHTML = 'Stade de développement';
            let select = document.createElement('select');
            select.id = 'development-stage-select';
            select.className = 'form-select';
            select.innerHTML = `
                <option selected></option>
                <option value="1">Jeune</option>
                <option value="2">Adulte</option>
                <option value="3">Vieux</option>
                <option value="4">Sénéscent</option>
                <option value="5">Tous</option>
            `;
            th.appendChild(select);
        } else {
            th.textContent = headerText;
        }
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Corps du tableau
    info_arbre.forEach((arbre, index) => {
        let row = document.createElement('tr');
        Object.values(arbre).forEach(text => {
            let td = document.createElement('td');
            td.textContent = text;
            row.appendChild(td);
        });

        let radioCell = document.createElement('td');
        let radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'select_arbre';
        radio.value = arbre.id;
        radioCell.appendChild(radio);
        row.appendChild(radioCell);

        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    corps.innerHTML = '';
    corps.appendChild(table);
}

//Fonction qui génère le texte à afficher lorsqu'on survole un arbre sur la carte
function generateHoverText(arbre) {
    return `
        Nom : ${arbre.nom}<br>
        Age : ${arbre.age_estim}<br>
        Hauteur totale : ${arbre.haut_tot}<br>
        Hauteur tronc : ${arbre.haut_tronc}<br>
        Diamètre du tronc : ${arbre.tronc_diam}<br>
        Remarquable : ${arbre.remarq}<br>
        Longitude : ${arbre.longitude}<br>
        Latitude : ${arbre.latitude}<br>
        État : ${arbre.etat}<br>
        Stade de développement : ${arbre.type_dev}<br>
        Type de port : ${arbre.type_port}<br>
        Type de pied : ${arbre.type_pied}<br>`;
}

//Fonction qui effectue une requête AJAX pour prediction age taille ou tempêtes
document.addEventListener('click', (event) => {
    const targets = ['age', 'etat', 'taille'];

    if (targets.includes(event.target.id)) {
        if (event.target.id === 'taille') {
            const clusterValue = document.getElementById('cluster').value;
            const methodeValue = document.getElementById('methode').value;

            if (clusterValue && methodeValue) {
                const radios = document.getElementsByName('select_arbre');
                ajaxRequest("POST", "php/requests.php/pred_taille_tab", affichePredTailleResult, "methode=" + methodeValue + "&nbr_cluster=" + clusterValue);
            } else {
                console.log('Les deux sélecteurs doivent avoir des valeurs sélectionnées.');
            }
        } else if (event.target.id === 'age') {

            const radios = document.getElementsByName('select_arbre');
            let selectedValue = null;
            let arbreSelectionne = false;

            radios.forEach(radio => {
                if (radio.checked) {
                    selectedValue = radio.value;
                    arbreSelectionne = true;
                }
            });

            if (arbreSelectionne) {
                ajaxRequest("GET", `php/requests.php/arbreByIdAge/${selectedValue}`, affichePredAge);
            } else {
                console.log('Veuillez sélectionner un arbre.');
            }
        } else if (event.target.id === 'etat') {
            const radios = document.getElementsByName('select_arbre');
            let selectedValue = null;
            let arbreSelectionne = false;

            radios.forEach(radio => {
                if (radio.checked) {
                    selectedValue = radio.value;
                    arbreSelectionne = true;
                }
            });

            if (arbreSelectionne) {
                ajaxRequest("GET", `php/requests.php/arbreByIdEtat/${selectedValue}`, affichePredEtat);
            } else {
                console.log('Veuillez sélectionner un arbre.');
            }
        }
    }
});

//Verifie que les informations sont bien renseignées pour la prédiction de l'âge si oui envoie la requête et affiche le résultat dans la callback
function affichePredAge(data) {
    const affiche = document.getElementById('result');
    affiche.innerHTML = '';
    if (data.tronc_diam === null || data.haut_tot === null || data.haut_tronc === null || data.precision_estime === null || data.type_dev === null || data.type_pied === null || data.type_feuillage === null || data.type_feuillage === "inconnue" ||data.type_situation === null || data.clc_nbr_diag === null) {
        affiche.innerHTML = '<div class="alert alert-danger" role="alert">Information manquantes !</div>';
        return;
    } else {
        ajaxRequest("POST", `php/requests.php/pred_age_tab`, affichePredAgeResult, "tronc_diam=" + data.tronc_diam + "&haut_tot=" + data.haut_tot + "&haut_tronc=" + data.haut_tronc + "&precision_estime=" + data.precision_estime + "&typ_dev=" + data.type_dev + "&type_pied=" + data.type_pied + "&type_feuillage=" + data.type_feuillage + "&type_situation=" + data.type_situation + "&clc_nbr_diag=" + data.clc_nbr_diag);
    }
}

//Verifie que les informations sont bien renseignées pour la prédiction de l'état si oui envoie la requête et affiche le résultat dans la callback
function affichePredEtat(data) {
    const affiche = document.getElementById('result');
    affiche.innerHTML = '';
    if (data.type_revetement === null || data.type_situation === null || data.clc_nbr_diag === null || data.longitude === null) {
        affiche.innerHTML = '<div class="alert alert-danger" role="alert">Information manquantes !</div>';
        return;
    } else {
        ajaxRequest("POST", `php/requests.php/pred_racine_tab`, affichePredEtatResult, "type_revetement=" + data.type_revetement + "&type_situation=" + data.type_situation + "&clc_nbr_diag=" + data.clc_nbr_diag + "&longitude=" + data.longitude);
    }
}

//Fonction qui affiche le résultat de la prédiction de l'etat (callback)
function affichePredEtatResult(data) {
    const map = document.getElementById('map');
    const legende = document.getElementById('legende');
    legende.innerHTML = '';
    map.innerHTML = '';
    const tableau = document.getElementById('result');

    if (typeof data !== 'object') {
        console.error("Les données fournies ne sont pas un objet valide.");
        return;
    }

    let table = document.createElement('table');
    table.className = 'table table-striped';
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');

    let headerRow = document.createElement('tr');
    const headers = ['Prediction', 'RFC', 'log_reg', 'SGD'];
    headers.forEach((headerText, index) => {
        let th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    let prediction = data.prediction;
    let rfcValue = Object.values(data.rfc).join(', ');
    let logRegValue = Object.values(data.log_reg).join(', ');
    let sgdValue = Object.values(data.sgd).join(', ');

    if(rfcValue === '0'){
        rfcValue = "Ne va pas être déraciné";
    }
    else{
        rfcValue = "Va être déraciné";
    }
    if(logRegValue === '0'){
        logRegValue = "Ne va pas être déraciné";
    }
    else{
        logRegValue = "Va être déraciné";
    }
    if(sgdValue === '0'){
        sgdValue = "Ne va pas être déraciné";
    }
    else{
        sgdValue = "Va être déraciné";
    }

    let tr = document.createElement('tr');
    [prediction, rfcValue, logRegValue, sgdValue].forEach(text => {
        let td = document.createElement('td');
        td.textContent = text;
        tr.appendChild(td);
    });
    tbody.appendChild(tr);

    table.appendChild(tbody);
    tableau.innerHTML = '';
    tableau.appendChild(table);
    
}

//Fonction qui affiche le résultat de la prédiction de l'âge (callback)
function affichePredAgeResult(data) {
    const map = document.getElementById('map');
    const legende = document.getElementById('legende');
    map.innerHTML = '';
    legende.innerHTML = '';
    const tableau = document.getElementById('result');


    if (typeof data !== 'object') {
        console.error("Les données fournies ne sont pas un objet valide.");
        return;
    }

    let table = document.createElement('table');
    table.className = 'table table-striped';
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');

    // Création de l'en-tête du tableau
    let headerRow = document.createElement('tr');
    const headers = ['Prediction', 'RFC', 'MLP', 'SGD'];
    headers.forEach((headerText) => {
        let th = document.createElement('th');
        th.textContent = headerText;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    let prediction = data.prediction;
    let rfcValue = data.rfc;
    let mlpValue = data.mlp;
    let sgdValue = data.sgd;

    let tr = document.createElement('tr');
    [prediction, rfcValue, mlpValue, sgdValue].forEach(text => {
        let td = document.createElement('td');
        td.textContent = text;
        tr.appendChild(td);
    });
    tbody.appendChild(tr);

    table.appendChild(tbody);
    tableau.innerHTML = '';
    tableau.appendChild(table);
}

//Fonction qui affiche le résultat de la prédiction de la taille (callback)
function affichePredTailleResult(data) {
    const tableau = document.getElementById('result');
    tableau.innerHTML = '';
    //Réécriture de la page avec les nouveaux div
    let map = document.getElementById("map");
    let legende =document.getElementById("legende");
    try {
        data = JSON.parse(data.split('\n')[2].split("<")[0]);
    } catch (error) {
        try {
            data = JSON.parse(data);
        } catch (error) {
            console.error("Erreur lors de la récupération des données.");
        }
    }
    legende.style.display = 'block';
    map.style.display = 'block';

    //Initialisation des variables pour les clusters
    let size = data.length;
    let longitude = [];
    let latitude = [];
    let infos = [];
    let color = [];
    let trois_clusters = false;

    //Récupération des informations pour la map
    for(let i=0; i<size; i++){
        longitude.push(data[i][0]['longitude']);
        latitude.push(data[i][0]['latitude']);
        infos.push(`
        Nom : ${data[i][0]['nom']}<br>
        Hauteur tronc : ${data[i][0]['haut_tronc']}<br>
        Diamètre du tronc : ${data[i][0]['tronc_diam']}<br>
        Age estimé : ${data[i][0]['age_estim']}<br>
        Remarquable : ${data[i][0]['remarq']}<br>
        Longitude : ${data[i][0]['longitude']}<br>
        Latitude : ${data[i][0]['latitude']}<br>
        État : ${data[i][0]['etat']}<br>
        Stade de développement : ${data[i][0]['type_dev']}<br>
        Type de port : ${data[i][0]['type_port']}<br>
        Type de pied : ${data[i][0]['type_pied']}<br>`);
        
        //Différentes couleurs selon le cluster
        if(data[i][1] == '0'){
            color.push('#FF5733');
        }
        else if(data[i][1] == '1'){
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
        if(data[49][1] == '0'){
            number = 'Grand';
        }
        else{
            number = 'Petit';
        }
    }
    else{
        legendItem = [{color: '#606ADF', name: 'Petit'}, {color: '#FF5733', name: 'Moyen'}, {color: '#9B3F9C', name: 'Grand'}];
        if(data[49][1] == '0'){
            number = 'Moyen';
        }
        else if(data[49][1] == '1'){
            number = 'Petit';
        }
        else{
            number = 'Grand';
        }
    }

    //Affichage de la légende
    let legendHTML = '<div class="legend">';
    legendHTML += '<p style="display: flex;">Légende :</p>';
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

}

//Affiher le nom de l'utilisateur
document.getElementById("button-id").innerHTML = Cookies.get("username");
