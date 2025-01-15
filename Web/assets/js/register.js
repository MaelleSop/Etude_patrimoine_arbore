// Submit du formulaire de création de compte pressé
document.getElementById("register-form").onsubmit = (event) => {
    
    // évite de déclencher l'évènement du bouton parent
    event.preventDefault();

    // récupération des valeurs des champs du formulaire
    username = document.getElementById("username").value;
    mdp_user = document.getElementById("password").value;
    confirm_mdp_user = document.getElementById("password-confirm").value;


    if (mdp_user != confirm_mdp_user){
        alert("Mots de passe différents !");
        exit();
    }

    var xhr = new XMLHttpRequest();

    // création du nouveau compte utilisateur dans la BDD
    xhr.open("POST", "php/requests.php/user"); 
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader("Authorization", "Basic "+btoa(username+":"+mdp_user));
    xhr.onload = () => {
        switch (xhr.status){
            case 200:
            case 201:
                window.location.href = 'accueil.html';
                break;
            default:
                httpErrors(xhr.status);
        }
    };
    xhr.onload = () => {
        // récupérer les données du site
        Cookies.set("username", username);
        Cookies.set("token", xhr.responseText);
        window.location.href = "accueil.html";
        
    };

    xhr.send();
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
}