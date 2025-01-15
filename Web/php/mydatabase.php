<?php
require_once('constants.php');

class myDatabase{
    //Attribut
    private $myPDO;
    
    //Constructeur
    public function __construct(){
      try
    {
      $this->myPDO = new PDO('pgsql:host='.DB_SERVER.';port='.DB_PORT.';dbname='.DB_NAME, DB_USER, DB_PASSWORD);
    }
    catch (PDOException $exception)
    {
      error_log('Connection error: '.$exception->getMessage());
      header('HTTP/1.1 503 Service Unavailable');
      exit;
    }
    }
    //Vérifie que l'username et le password correspondent à un utilisateur
    public function checkUser($username, $password){
    try
    {
      $request = 'SELECT * FROM users WHERE username=:username AND password=encode(digest(:password, \'sha1\'), \'hex\')';
      $statement = $this->myPDO->prepare($request);
      $statement->bindParam (':username', $username, PDO::PARAM_STR, 50);
      $statement->bindParam (':password', $password, PDO::PARAM_STR, 40);
      $statement->execute();
      $result = $statement->fetch();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    if (!$result)
      return false;
    return true;
  }

  //Ajoute un token d'identification à un utilisateur
  public function addToken($username, $token){
    try
    { 
      $request = 'UPDATE users SET token=:token WHERE username=:username';
      $statement = $this->myPDO->prepare($request);
      $statement->bindParam(':username', $username, PDO::PARAM_STR, 50);
      $statement->bindParam(':token', $token, PDO::PARAM_STR, 20);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return true;
  }

  //Vérifie que le token corresponde bien à un utilisateur et renvoie l'username de l'utilisateur correspondant
  public function verifyToken($token)
  {
    try
    {
      $request = 'SELECT username FROM users WHERE token=:token';
      $statement = $this->myPDO->prepare($request);
      $statement->bindParam (':token', $token, PDO::PARAM_STR, 20);
      $statement->execute();
      $result = $statement->fetch();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    if (!$result)
      return false;
    return $result['username'];
  }
  //Ajoute un utilisateur
  public function addUser($username, $password){
    try{
      $request = "INSERT INTO users(username, password) VALUES(:username, encode(digest(:password, 'sha1'), 'hex'))";
      $statement = $this->myPDO->prepare($request);
      $statement->bindParam(":username", $username, PDO::PARAM_STR, 50);
      $statement->bindParam(":password", $password, PDO::PARAM_STR, 50);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return true;
  }

  //Ajoute un nouvel arbre de taille dans la bdd
  public function addArbreTaille($longitude, $latitude, $haut_tronc, $tronc_diam, $age_estim, $type_situation, $type_port, $precision_estime, $type_revetement, $clc_nbr_diag, $type_dev, $type_pied, $type_feuillage, $remarq, $etat, $nom){
    try{
      $request = "INSERT INTO Arbres(longitude, latitude, haut_tronc, tronc_diam, age_estim, type_situation, type_port, precision_estime, type_revetement, clc_nbr_diag, type_dev, type_pied, type_feuillage, remarq, etat, nom) VALUES (:longitude, :latitude, :haut_tronc, :tronc_diam, :age_estim, :type_situation, :type_port, :precision_estime, :type_revetement, :clc_nbr_diag, :type_dev, :type_pied, :type_feuillage, :remarq, :etat, :nom)";
      $statement =$this->myPDO->prepare($request);
      $statement->bindParam(":longitude", $longitude);
      $statement->bindParam(":latitude", $latitude);
      $statement->bindParam(":haut_tronc", $haut_tronc);
      $statement->bindParam(":tronc_diam", $tronc_diam);
      $statement->bindParam(":age_estim", $age_estim);
      $statement->bindParam(":type_situation", $type_situation);
      $statement->bindParam(":type_port", $type_port);
      $statement->bindParam(":precision_estime", $precision_estime);
      $statement->bindParam(":type_revetement", $type_revetement);
      $statement->bindParam(":clc_nbr_diag", $clc_nbr_diag);
      $statement->bindParam(":type_dev", $type_dev);
      $statement->bindParam(":type_pied", $type_pied);
      $statement->bindParam(":type_feuillage", $type_feuillage);
      $statement->bindParam(":remarq", $remarq);
      $statement->bindParam(":etat", $etat);
      $statement->bindParam(":nom", $nom);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log($exception->getMessage());
      return false;
    }
    return true;
  }

  //Recupere les infos d'un arbre pour les clusters
  public function infoArbreCluster(){
    try{
      $request = "SELECT a.nom, a.haut_tronc, a.tronc_diam, a.age_estim, a.remarq, a.longitude, a.latitude, a.etat, a.type_dev, a.type_port, a.type_pied FROM public.Arbres a ORDER BY a.ID DESC LIMIT 50";
      $statement = $this->myPDO->prepare($request);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return $statement->fetchAll(PDO::FETCH_ASSOC);
  }

  //Ajoute un nouvel arbre de taille dans la bdd
  public function addArbreAgeEtat($longitude, $latitude, $haut_tronc, $tronc_diam, $haut_tot, $type_situation, $precision_estime, $type_revetement, $clc_nbr_diag, $typ_dev, $type_pied, $type_feuillage, $remarq, $nom, $port){
    try{
      $request = "INSERT INTO arbres(longitude, latitude, haut_tronc, tronc_diam, haut_tot, type_situation, precision_estime, type_revetement, clc_nbr_diag, type_dev, type_pied, type_feuillage, remarq, nom, type_port) VALUES (:longitude, :latitude, :haut_tronc, :tronc_diam, :haut_tot, :type_situation, :precision_estime, :type_revetement, :clc_nbr_diag, :type_dev, :type_pied, :type_feuillage, :remarq, :nom, :port)";
      $statement =$this->myPDO->prepare($request);
      $statement->bindParam(":longitude", $longitude);
      $statement->bindParam(":latitude", $latitude);
      $statement->bindParam(":haut_tronc", $haut_tronc);
      $statement->bindParam(":tronc_diam", $tronc_diam);
      $statement->bindParam(":haut_tot", $haut_tot);
      $statement->bindParam(":type_situation", $type_situation);
      $statement->bindParam(":precision_estime", $precision_estime);
      $statement->bindParam(":type_revetement", $type_revetement);
      $statement->bindParam(":clc_nbr_diag", $clc_nbr_diag);
      $statement->bindParam(":type_dev", $typ_dev);
      $statement->bindParam(":type_pied", $type_pied);
      $statement->bindParam(":type_feuillage", $type_feuillage);
      $statement->bindParam(":remarq", $remarq);
      $statement->bindParam(":nom", $nom);
      $statement->bindParam(":port", $port);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log($exception->getMessage());
      return false;
    }
    return true;
  }

  //Recupere les infos d'un arbre en fonction de l'id
  public function infoArbre($id = NULL){
    if($id != NULL){
      if($id == 1){
        $id = "jeune";
      } else if($id == 2){
        $id = "adulte";
      } else if($id == 3){
        $id = "vieux";
      } else if($id == 4){
        $id = "senescent";
      } else if ($id == 5){
        try{
          $request = "SELECT a.id, a.nom, a.age_estim, a.haut_tot, a.haut_tronc, a.tronc_diam, a.remarq, a.longitude, a.latitude, a.etat, a.type_dev, a.type_port, a.type_pied FROM public.Arbres a";
          $statement = $this->myPDO->prepare($request);
          $statement->execute();
        }
        catch (PDOException $exception)
        {
          error_log('Request error: '.$exception->getMessage());
          return false;
        }
        return $statement->fetchAll(PDO::FETCH_ASSOC);
      }
      try{
        $request = "SELECT a.id, a.nom, a.age_estim, a.haut_tot, a.haut_tronc, a.tronc_diam, a.remarq, a.longitude, a.latitude, a.etat, a.type_dev, a.type_port, a.type_pied FROM public.Arbres a WHERE a.type_dev=:id";
        $statement = $this->myPDO->prepare($request);
        $statement->bindParam(":id", $id, PDO::PARAM_INT);
        $statement->execute();
      }
      catch (PDOException $exception)
      {
        error_log('Request error: '.$exception->getMessage());
        return false;
      }
      return $statement->fetchAll(PDO::FETCH_ASSOC);
    }
    else{
      try{
        $request = "SELECT a.id, a.nom, a.age_estim, a.haut_tot, a.haut_tronc, a.tronc_diam, a.remarq, a.longitude, a.latitude, a.etat, a.type_dev, a.type_port, a.type_pied FROM public.Arbres a";
        $statement = $this->myPDO->prepare($request);
        $statement->execute();
      }
      catch (PDOException $exception)
      {
        error_log('Request error: '.$exception->getMessage());
        return false;
      }
      return $statement->fetchAll(PDO::FETCH_ASSOC);
    }

   return $statement->fetchAll(PDO::FETCH_ASSOC);
  }

  //Recupere les infos d'un arbre en fonction de son id pour predire la taille
  public function getArbreByIdTaille($id){
    try{
      $request = "SELECT a.age_estim, a.haut_tronc, a.tronc_diam FROM public.Arbres a WHERE a.id=:id";
      $statement = $this->myPDO->prepare($request);
      $statement->bindParam(":id", $id, PDO::PARAM_INT);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return $statement->fetch(PDO::FETCH_ASSOC);
  }

  //Recupere les infos d'un arbre en fonction de son id pour predire l'age
  public function getArbreByIdAge($id){
    try{
      $request = "SELECT a.tronc_diam, a.haut_tot, a.haut_tronc, a.precision_estime, a.type_dev, a.type_pied, a.type_feuillage, a.type_situation, a.clc_nbr_diag FROM public.Arbres a WHERE a.id=:id";
      $statement = $this->myPDO->prepare($request);
      $statement->bindParam(":id", $id, PDO::PARAM_INT);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return $statement->fetch(PDO::FETCH_ASSOC);
  }

  //Recupere les infos d'un arbre en fonction de son id pour predire l'etat
  public function getArbreByIdEtat($id){
    try{
      $request = "SELECT a.type_revetement, a.type_situation, a.clc_nbr_diag, a.longitude FROM public.Arbres a WHERE a.id=:id";
      $statement = $this->myPDO->prepare($request);
      $statement->bindParam(":id", $id, PDO::PARAM_INT);
      $statement->execute();
    }
    catch (PDOException $exception)
    {
      error_log('Request error: '.$exception->getMessage());
      return false;
    }
    return $statement->fetch(PDO::FETCH_ASSOC);
  }
}
?>
