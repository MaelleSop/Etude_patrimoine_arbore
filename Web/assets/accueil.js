//Si pas de token renvoie vers la connexion
if (typeof Cookies.get("token") == "undefined"){
    window.location.href = "sign_in.html";
}
document.getElementById("button-id").innerHTML = Cookies.get("username");