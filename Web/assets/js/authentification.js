document.getElementById("login-form").onsubmit = (event) => {
    var userLogin, userPassword, xhr;
    event.preventDefault();
    userLogin = document.getElementById("username").value;
    userPassword = document.getElementById("password").value;

    xhr = new XMLHttpRequest();
    xhr.open("GET", "php/requests.php/authenticate");
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader("Authorization", "Basic "+btoa(userLogin+":"+userPassword));
    xhr.onload = () => {
        switch (xhr.status){
            case 200:
            case 201:
                Cookies.set("token", xhr.responseText);
                window.location.href = 'accueil.html';
                break;
            default:
                // si mdp incorrect
                document.getElementById("bad_pwd").style.display = "block";

                httpErrors(xhr.status);
        }
    };
    xhr.onloadend = () => {
        //Récupérer les données du site
        Cookies.set("username", userLogin);
        Cookies.set("token", xhr.responseText);
    };
    xhr.send();
    document.getElementById("login").value = userLogin;
    document.getElementById("password").value = "";
    
}

// Verifie que l'utilisateur est déjà connecté
if (typeof Cookies.get("token") !== 'undefined'){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "php/requests.php");
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader("Authorization", "Bearer " + Cookies.get("token"));
    xhr.onloadend = () => {
        if (xhr.status == 200){
            window.location.href = 'accueil.html';
        }
    }
    xhr.send();
}