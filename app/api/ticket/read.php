<?php

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF8");

//include db and game class files
include_once '../config/database.php';
include_once '../objects/games.php';

//init database and game obj
$database = new Database();
$db = $database->getConnection();

//init game obj
$games = new Games($db);

$stmt = $games->read();
$num = $stmt->rowCount();
if($num>0){
    
    //games array
    $games_arr=array();
    $games_arr["games"]=array();
    
    //loop through results
    
    while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
        extract($row);
        
        $game_info=array(
            "gameId"=>$gameId,
            "gameName"=>$gameName,
            "ticketPrice"=>$ticketPrice,
            "totalTicketsPrinted"=>$totalTicketsPrinted,
            "launchDate"=>$launchDate,
            "disableDate"=>$disableDate,
            "id"=>$id
        );
        
        array_push($games_arr["games"], $game_info);
        
    }
    
    http_response_code(200);
    
    //output ticket array in JSON
    
    echo json_encode($games_arr);
    
}
else{
    
    http_response_code(404);
    echo json_encode(array("message"=> "no tickets found"));
    

}
?>

