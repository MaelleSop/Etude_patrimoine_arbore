<?php

require("mydatabase.php");
//Authentification via l'username et le mot de passe
function authenticate($db){
    //Récupère le login/mdp via le header Authorization
    if (isset($_SERVER["PHP_AUTH_USER"]) && isset($_SERVER["PHP_AUTH_PW"])){
        $username = $_SERVER["PHP_AUTH_USER"];
        $password = $_SERVER["PHP_AUTH_PW"];
        //Vérifie que le couple login/mdp corresponde à une entrée dans la table users
        if (!$db->checkUser($username, $password)){
            echo "a";
            header('HTTP/1.1 401 Unauthorized');
            exit;
        }
        else {
            //Créer un token pour l'utilisateur et lui renvoie si le couple login/mdp correspond à une entrée dans la table users
            $token = base64_encode(openssl_random_pseudo_bytes(12));
            $db->addToken($username, $token);
            header('Content-Type: text/html; charset=utf-8');
            header('Cache-control: no-store, no-cache, must-revalidate');
            header('Pragma: no-cache');

            header('HTTP/1.1 200 OK');
            echo $token;
            exit;
        }
    }
    else {
        header('HTTP/1.1 401 Unauthorized');
        exit;
    }
}

//Verification du Token
function verifyToken($db){
    //Récupération du token dans le header authorization
    $headers = getallheaders();
    $token = $headers["Authorization"];
    if (preg_match("/Bearer (.*)/", $token, $tab)){
        $token = $tab[1];
        $username = $db->verifyToken($token);
        if (!$username){
            header('HTTP/1.1 401 Unauthorized');
            exit;
        }
        return $username;
    }
    else{
        header('HTTP/1.1 401 Unauthorized');
        exit;
    }
}

function remove_accents($string) {
    return iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $string);
}

/*Erreurs Logs*/
error_reporting(E_ALL); // Error/Exception engine, always use E_ALL

ini_set('ignore_repeated_errors', TRUE); // always use TRUE

ini_set('display_errors', TRUE); // Error/Exception display, use FALSE only in production environment or real server. Use TRUE in development environment

ini_set('log_errors', TRUE); // Error/Exception file logging engine.
ini_set('error_log', '/var/log/php_errors.log'); // Logging file path


//Création de l'objet représentant la base de données
$myDb = new myDatabase;
//Acquisition des informations de la requête contenuent dans son URL
$requestMethod = $_SERVER['REQUEST_METHOD'];
$request = substr($_SERVER['PATH_INFO'], 1);
$request = explode('/', $request);
$requestRessource = array_shift($request);
$id = array_shift($request);
$id2 = array_shift($request);
if ($id == ''){
  $id = NULL;
  $id2 = NULL;
}
else {
    if($id2 == ""){
        $id2 = NULL;
    }
}
/* Gestion de la connexion de l'utilisateur, refuse les requetes ajax si non connecté */
//Obtention de l'identité de l'utilisateur via une connexion par mot de passe/token ou la creation d'un compte
if ($requestRessource == "authenticate"){
    authenticate($myDb);
}
//Création d'un utilisateur
else if ($requestMethod == "POST" && $requestRessource == "user"){
    if (isset($_SERVER["PHP_AUTH_USER"]) && isset($_SERVER["PHP_AUTH_PW"])){
        //Ajout de l'utilisateur
        $username = $_SERVER["PHP_AUTH_USER"];
        $password = $_SERVER["PHP_AUTH_PW"];
        $myDbReq = $myDb->addUser($username, $password);
        if(!$myDbReq){
            header('HTTP/1.1 400 Bad Request');
        }
        else{
            //Renvoie un token correspondant au nouvel utilisateur
            $token = base64_encode(openssl_random_pseudo_bytes(12));
            $myDb->addToken($username, $token);
            header('Content-Type: text/html; charset=utf-8');
            header('Cache-control: no-store, no-cache, must-revalidate');
            header('Pragma: no-cache');
            header('HTTP/1.1 201 Created');
            echo $token;
            exit;
        }
    }
    else{
        header('HTTP/1.1 400 Bad Request');
    }
}
else{
    //Vérifie que le token corresponde à un utilisateur
    $username = verifyToken($myDb);
    if (isset($_COOKIE["username"])){
        if($username != $_COOKIE["username"]){
            header('HTTP/1.1 401 Unauthorized');
            exit;
        }
    }
}
/*
Gestion de la base de données en fonction des requêtes de l'utilisateur:
*/
//Requête utilisé lors du chargement de la page web afin de vérifier si l'utilisateur est connecté
if($requestMethod == "GET" && $requestRessource == ""){
    header("HTTP/1.1 200 OK");
}
//Requête pour la prédiction de l'âge
else if($requestMethod == "POST" && $requestRessource == "taille_arbre"){
    $myDb->addArbreTaille($_POST['longitude'], $_POST['latitude'], $_POST['haut_tronc'], $_POST['tronc_diam'], $_POST['age_estim'], $_POST['type_situation'], $_POST['type_port'], $_POST['precision_estime'], $_POST['type_revetement'], $_POST['clc_nbr_diag'], $_POST['type_dev'], $_POST['type_pied'], $_POST['type_feuillage'], $_POST['remarq'], $_POST['etat'], strtolower(remove_accents($_POST['nom'])));

    if(isset($_POST['methode']) && isset($_POST['nbr_cluster']) && isset($_POST['age_estim']) && isset($_POST['haut_tronc']) && isset($_POST['tronc_diam'])){
        
        $tab_cluster = array();

        $tab = $myDb->infoArbreCluster();

        foreach($tab as $value){
            $cluster = array();
            $methode = escapeshellarg($_POST["methode"]);
            $nbr_cluser = escapeshellarg($_POST["nbr_cluster"]);
            $age_estim = escapeshellarg($value['age_estim']);
            $haut_tronc = escapeshellarg($value['haut_tronc']);
            $tronc_diam = escapeshellarg($value['tronc_diam']);
            exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite1.py ".$methode.' '.$nbr_cluser.' '.$age_estim.' '.$haut_tronc.' '.$tronc_diam);
            array_push($cluster, $value);
            array_push($cluster, file_get_contents("/home/isen/scripts/fonctionalite_1.json"));
            array_push($tab_cluster, $cluster);
        } 
        echo json_encode($tab_cluster);

    }
    else{
        header('HTTP/1.1 400 Bad Request');
        exit;
    }
     
}
//Requete pour la prediction sur la taille depuis la page visualisation
else if($requestMethod == "POST" && $requestRessource == "pred_taille_tab"){
    if(isset($_POST['methode']) && isset($_POST['nbr_cluster'])){
        
        $tab_cluster = array();

        $tab = $myDb->infoArbreCluster();

        foreach($tab as $value){
            $cluster = array();
            $methode = escapeshellarg($_POST["methode"]);
            $nbr_cluser = escapeshellarg($_POST["nbr_cluster"]);
            $age_estim = escapeshellarg($value['age_estim']);
            $haut_tronc = escapeshellarg($value['haut_tronc']);
            $tronc_diam = escapeshellarg($value['tronc_diam']);
            exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite1.py ".$methode.' '.$nbr_cluser.' '.$age_estim.' '.$haut_tronc.' '.$tronc_diam);
            array_push($cluster, $value);
            array_push($cluster, file_get_contents("/home/isen/scripts/fonctionalite_1.json"));
            array_push($tab_cluster, $cluster);
        } 
        echo json_encode($tab_cluster);

    }
    else{
        header('HTTP/1.1 400 Bad Request');
        exit;
    }
}
//Requete pour la prediction sur l'age et insertion en bdd
else if ($requestMethod == "POST" && $requestRessource == "pred_age"){
    if (isset($_POST["longitude"]) && isset($_POST["latitude"]) && isset($_POST["tronc_diam"]) && isset($_POST["haut_tot"]) && isset($_POST["haut_tronc"]) && isset($_POST["precision_estime"]) && isset($_POST["typ_dev"]) && isset($_POST["type_pied"]) && isset($_POST["type_feuillage"]) && isset($_POST["type_situation"]) && isset($_POST["clc_nbr_diag"]) && isset($_POST["nom"]) && isset($_POST["remarquable"]) && isset($_POST["type_revetement"]) && isset($_POST["port"])){
        switch($_POST["typ_dev"]){
            case "jeune":
                $dev = 1;
                break;
            case "adulte":
                $dev = 0;
                break;
            case "vieux":
                $dev = 3;
                break;
            case "senescent":
                $dev = 4;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        switch($_POST["type_feuillage"]){
            case "conifere":
                $feuille = 0;
                break;
            case "feuillu":
                $feuille = 1;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        switch($_POST["type_situation"]){
            case "alignement":
                $situ = 0;
                break;
            case "groupe":
                $situ = 1;
                break;
            case "isole":
                $situ = 2;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        switch($_POST["type_pied"]){
            case "gazon":
                $pied = 4;
                break;
            case "fosse arbre":
                $pied = 3;
                break;
            case "revetement non permeable":
                $pied = 1;
                break;
            case "bac de plantation":
                $pied = 0;
                break;
            case "terre":
                $pied = 2;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;

        }

        $tronc_diam = escapeshellarg($_POST['tronc_diam']);
        $haut_tot = escapeshellarg($_POST['haut_tot']);
        $haut_tronc = escapeshellarg($_POST['haut_tronc']);
        $precision_estime = escapeshellarg($_POST['precision_estime']);
        $clc_nbr_diag = escapeshellarg($_POST['clc_nbr_diag']);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite2.py -td ".$tronc_diam." -hto ".$haut_tot." -htr ".$haut_tronc." -fpe ".$precision_estime." -fsd ".$dev." -fpd ".$pied." -ff ".$feuille." -fs ".$situ." -cnd ".$clc_nbr_diag." -m mlp", $output_mlp);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite2.py -td ".$tronc_diam." -hto ".$haut_tot." -htr ".$haut_tronc." -fpe ".$precision_estime." -fsd ".$dev." -fpd ".$pied." -ff ".$feuille." -fs ".$situ." -cnd ".$clc_nbr_diag." -m sgd", $output_sgd);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite2.py -td ".$tronc_diam." -hto ".$haut_tot." -htr ".$haut_tronc." -fpe ".$precision_estime." -fsd ".$dev." -fpd ".$pied." -ff ".$feuille." -fs ".$situ." -cnd ".$clc_nbr_diag." -m rfc", $output_rfc);

        $longitude = filter_input(INPUT_POST, 'longitude', FILTER_VALIDATE_FLOAT);
        $latitude = filter_input(INPUT_POST, 'latitude', FILTER_VALIDATE_FLOAT);
        $haut_tronc = filter_input(INPUT_POST, 'haut_tronc', FILTER_VALIDATE_INT);
        $tronc_diam = filter_input(INPUT_POST, 'tronc_diam', FILTER_VALIDATE_INT);
        $haut_tot = filter_input(INPUT_POST, 'haut_tot', FILTER_VALIDATE_INT);
        $precision_estime = filter_input(INPUT_POST, 'precision_estime', FILTER_VALIDATE_INT);
        $clc_nbr_diag = filter_input(INPUT_POST, 'clc_nbr_diag', FILTER_VALIDATE_INT);
        $situ = strtolower(remove_accents(htmlspecialchars($_POST['type_situation'], ENT_QUOTES)));
        $type_revetement = strtolower(remove_accents(htmlspecialchars($_POST['type_revetement'], ENT_QUOTES)));
        $dev = strtolower(remove_accents(htmlspecialchars($_POST['typ_dev'], ENT_QUOTES)));
        $type_pied = strtolower(remove_accents(htmlspecialchars($_POST['type_pied'], ENT_QUOTES)));
        $feuille = strtolower(remove_accents(htmlspecialchars($_POST['type_feuillage'], ENT_QUOTES)));
        $remarquable = strtolower(remove_accents(htmlspecialchars($_POST['remarquable'], ENT_QUOTES)));
        $nom = strtolower(remove_accents(htmlspecialchars($_POST['nom'], ENT_QUOTES)));
        $port = strtolower(remove_accents(htmlspecialchars($_POST['port'], ENT_QUOTES)));

        $myDb->addArbreAgeEtat($longitude, $latitude, $haut_tronc, $tronc_diam, $haut_tot, $situ, $precision_estime, $type_revetement, $clc_nbr_diag, $dev, $type_pied, $feuille, $remarquable, $nom, $port);
        $mlp_json = file_get_contents("/home/isen/scripts/fonctionalite_2_mlp.json");
        $rfc_json = file_get_contents("/home/isen/scripts/fonctionalite_2_rfc.json");
        $sgd_json = file_get_contents("/home/isen/scripts/fonctionalite_2_sgd.json");
        echo "{\"prediction\": \"age\", \"mlp\": ".$mlp_json.", \"rfc\":".$rfc_json.", \"sgd\": ".$sgd_json."}";
    }
    else{
        header('HTTP/1.1 400 Bad Request');
        exit;
    }
}
//Requete pour la prediction sur le deracinement et insertion en bdd
else if ($requestMethod == "POST" && $requestRessource == "pred_racine"){
    if (isset($_POST["longitude"]) && isset($_POST["latitude"]) && isset($_POST["tronc_diam"]) && isset($_POST["haut_tot"]) && isset($_POST["haut_tronc"]) && isset($_POST["precision_estime"]) && isset($_POST["typ_dev"]) && isset($_POST["type_pied"]) && isset($_POST["type_feuillage"]) && isset($_POST["type_situation"]) && isset($_POST["clc_nbr_diag"]) && isset($_POST["nom"]) && isset($_POST["remarquable"]) && isset($_POST["type_revetement"]) && isset($_POST["port"])){
        switch($_POST["type_situation"]){
            case "alignement":
                $situ = 0;
                break;
            case "groupe":
                $situ = 1;
                break;
            case "isole":
                $situ = 2;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        switch($_POST["type_revetement"]){
            case "non":
                $type_revetement = 1;
                break;
            case "oui":
                $type_revetement = 0;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        $longitude = escapeshellarg($_POST["longitude"]);
        $clc_nbr_diag = escapeshellarg($_POST["clc_nbr_diag"]);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite3.py -m log_reg -r ".$type_revetement." -s ".$situ." -d ".$clc_nbr_diag." -l ".$longitude, $output_log);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite3.py -m sgd -r ".$type_revetement." -s ".$situ." -d ".$clc_nbr_diag." -l ".$longitude, $output_sgd);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite3.py -m forest -r ".$type_revetement." -s ".$situ." -d ".$clc_nbr_diag." -l ".$longitude, $output_rfc);
        $longitude = filter_input(INPUT_POST, 'longitude', FILTER_VALIDATE_FLOAT);
        $latitude = filter_input(INPUT_POST, 'latitude', FILTER_VALIDATE_FLOAT);
        $haut_tronc = filter_input(INPUT_POST, 'haut_tronc', FILTER_VALIDATE_INT);
        $tronc_diam = filter_input(INPUT_POST, 'tronc_diam', FILTER_VALIDATE_INT);
        $haut_tot = filter_input(INPUT_POST, 'haut_tot', FILTER_VALIDATE_INT);
        $precision_estime = filter_input(INPUT_POST, 'precision_estime', FILTER_VALIDATE_INT);
        $clc_nbr_diag = filter_input(INPUT_POST, 'clc_nbr_diag', FILTER_VALIDATE_INT);
        $situ = strtolower(remove_accents(htmlspecialchars($_POST['type_situation'], ENT_QUOTES)));
        $type_revetement = strtolower(remove_accents(htmlspecialchars($_POST['type_revetement'], ENT_QUOTES)));
        $dev = strtolower(remove_accents(htmlspecialchars($_POST['typ_dev'], ENT_QUOTES)));
        $type_pied = strtolower(remove_accents(htmlspecialchars($_POST['type_pied'], ENT_QUOTES)));
        $feuille = strtolower(remove_accents(htmlspecialchars($_POST['type_feuillage'], ENT_QUOTES)));
        $remarquable = strtolower(remove_accents(htmlspecialchars($_POST['remarquable'], ENT_QUOTES)));
        $nom = strtolower(remove_accents(htmlspecialchars($_POST['nom'], ENT_QUOTES)));
        $port = strtolower(remove_accents(htmlspecialchars($_POST['port'], ENT_QUOTES)));

        $myDb->addArbreAgeEtat($longitude, $latitude, $haut_tronc, $tronc_diam, $haut_tot, $situ, $precision_estime, $type_revetement, $clc_nbr_diag, $dev, $type_pied, $feuille, $remarquable, $nom, $port);

        $log_json = file_get_contents("/home/isen/scripts/fonctionalite_3_log_reg.json");
        $rfc_json = file_get_contents("/home/isen/scripts/fonctionalite_3_forest.json");
        $sgd_json = file_get_contents("/home/isen/scripts/fonctionalite_3_sgd.json");
        echo "{\"prediction\": \"tempete\", \"log_reg\": ".$log_json.", \"rfc\":".$rfc_json.", \"sgd\": ".$sgd_json."}";        
    }
    else{
        header('HTTP/1.1 400 Bad Request');
        exit;
    }
}
//Requete pour la prediction sur le deracinement depuis la page visualisation
else if ($requestMethod == "POST" && $requestRessource == "pred_racine_tab"){
    if (isset($_POST["longitude"]) && isset($_POST["type_situation"]) && isset($_POST["clc_nbr_diag"]) && isset($_POST["type_revetement"])){
        switch($_POST["type_situation"]){
            case "alignement":
                $situ = 0;
                break;
            case "groupe":
                $situ = 1;
                break;
            case "isole":
                $situ = 2;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        switch($_POST["type_revetement"]){
            case "non":
                $type_revetement = 1;
                break;
            case "oui":
                $type_revetement = 0;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        $longitude = escapeshellarg($_POST["longitude"]);
        $clc_nbr_diag = escapeshellarg($_POST["clc_nbr_diag"]);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite3.py -m log_reg -r ".$type_revetement." -s ".$situ." -d ".$clc_nbr_diag." -l ".$longitude, $output_log);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite3.py -m sgd -r ".$type_revetement." -s ".$situ." -d ".$clc_nbr_diag." -l ".$longitude, $output_sgd);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite3.py -m forest -r ".$type_revetement." -s ".$situ." -d ".$clc_nbr_diag." -l ".$longitude, $output_rfc);
        $log_json = file_get_contents("/home/isen/scripts/fonctionalite_3_log_reg.json");
        $rfc_json = file_get_contents("/home/isen/scripts/fonctionalite_3_forest.json");
        $sgd_json = file_get_contents("/home/isen/scripts/fonctionalite_3_sgd.json");
        echo "{\"prediction\": \"tempete\", \"log_reg\": ".$log_json.", \"rfc\":".$rfc_json.", \"sgd\": ".$sgd_json."}";
    }
}
//Requete pour la prediction sur l'age depuis la page visualisation
else if($requestMethod == "POST" && $requestRessource == "pred_age_tab"){
    if (isset($_POST["tronc_diam"]) && isset($_POST["haut_tot"]) && isset($_POST["haut_tronc"]) && isset($_POST["precision_estime"]) && isset($_POST["typ_dev"]) && isset($_POST["type_pied"]) && isset($_POST["type_feuillage"]) && isset($_POST["type_situation"]) && isset($_POST["clc_nbr_diag"])){
        switch($_POST["typ_dev"]){
            case "jeune":
                $dev = 1;
                break;
            case "adulte":
                $dev = 0;
                break;
            case "vieux":
                $dev = 3;
                break;
            case "senescent":
                $dev = 4;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        switch($_POST["type_feuillage"]){
            case "conifere":
                $feuille = 0;
                break;
            case "feuillu":
                $feuille = 1;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;
        }
        switch($_POST["type_situation"]){
            case "alignement":
                $situ = 0;
                break;
            case "groupe":
                $situ = 1;
                break;
            case "isole":
                $situ = 2;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;

            
        }
        switch($_POST["type_pied"]){
            case "gazon":
                $pied = 4;
                break;
            case "fosse arbre":
                $pied = 3;
                break;
            case "revetement non permeable":
                $pied = 1;
                break;
            case "bac de plantation":
                $pied = 0;
                break;
            case "terre":
                $pied = 2;
                break;
            default:
                header('HTTP/1.1 400 Bad Request');
                exit;

        }
        
        $tronc_diam = escapeshellarg($_POST['tronc_diam']);
        $haut_tot = escapeshellarg($_POST['haut_tot']);
        $haut_tronc = escapeshellarg($_POST['haut_tronc']);
        $precision_estime = escapeshellarg($_POST['precision_estime']);
        $clc_nbr_diag = escapeshellarg($_POST['clc_nbr_diag']);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite2.py -td ".$tronc_diam." -hto ".$haut_tot." -htr ".$haut_tronc." -fpe ".$precision_estime." -fsd ".$dev." -fpd ".$pied." -ff ".$feuille." -fs ".$situ." -cnd ".$clc_nbr_diag." -m mlp", $output_mlp);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite2.py -td ".$tronc_diam." -hto ".$haut_tot." -htr ".$haut_tronc." -fpe ".$precision_estime." -fsd ".$dev." -fpd ".$pied." -ff ".$feuille." -fs ".$situ." -cnd ".$clc_nbr_diag." -m sgd", $output_sgd);
        exec("cd /home/isen/scripts && /home/isen/myEnv/bin/python3 /home/isen/scripts/script_fonctionnalite2.py -td ".$tronc_diam." -hto ".$haut_tot." -htr ".$haut_tronc." -fpe ".$precision_estime." -fsd ".$dev." -fpd ".$pied." -ff ".$feuille." -fs ".$situ." -cnd ".$clc_nbr_diag." -m rfc", $output_rfc);

        $mlp_json = file_get_contents("/home/isen/scripts/fonctionalite_2_mlp.json");
        $rfc_json = file_get_contents("/home/isen/scripts/fonctionalite_2_rfc.json");
        $sgd_json = file_get_contents("/home/isen/scripts/fonctionalite_2_sgd.json");
        echo "{\"prediction\": \"age\", \"mlp\": ".$mlp_json.", \"rfc\":".$rfc_json.", \"sgd\": ".$sgd_json."}";
    }
    else{
        header('HTTP/1.1 400 Bad Request');
        exit;
    }
}
//Requete pour recuperer toutes les infos des arbres
else if($requestMethod == "GET" && $requestRessource == "visualisation"){
    if($id != NULL){
        $myDbReq = $myDb->infoArbre($id);
    }
    else {
        $myDbReq = $myDb->infoArbre();
    }
    if(!$myDbReq){
        header('HTTP/1.1 400 Bad Request');
    }
    else{
        header('HTTP/1.1 200 OK');
        echo json_encode($myDbReq);
    }
    exit;
}
//Requete pour recuperer les infos necessaire à la prediction de la taille
else if($requestMethod == "GET" && $requestRessource == "arbreByIdTaille"){
    $myDbReq = $myDb->getArbreByIdTaille($id);
    if(!$myDbReq){
        header('HTTP/1.1 400 Bad Request');
    }
    else{
        header('HTTP/1.1 200 OK');
        echo json_encode($myDbReq);
    }
}
//Requete pour recuperer les infos necessaire à la prediction de l'age
else if($requestMethod == "GET" && $requestRessource == "arbreByIdAge"){
    $myDbReq = $myDb->getArbreByIdAge($id);
    if(!$myDbReq){
        header('HTTP/1.1 400 Bad Request');
    }
    else{
        header('HTTP/1.1 200 OK');
        echo json_encode($myDbReq);
    }
}
//Requete pour recuperer les infos necessaire à la prediction du deracinement
else if($requestMethod == "GET" && $requestRessource == "arbreByIdEtat"){
    $myDbReq = $myDb->getArbreByIdEtat($id);
    if(!$myDbReq){
        header('HTTP/1.1 400 Bad Request');
    }
    else{
        header('HTTP/1.1 200 OK');
        echo json_encode($myDbReq);
    }
}
//Sinon mauvaise requete
else{
    header('HTTP/1.1 400 Bad Request');
    exit;
}

//headers
header('Content-Type: text/x-json; charset=utf-8');
header('Cache-control: no-store, no-cache, must-revalidate');
header('Pragma: no-cache');
?>
