<?php
$con=mysqli_connect("localhost","root","","lotto");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$sql="SELECT
	current_games.gameName,
	current_games.totalTicketsPrinted,
	game_prizes.paidTickets,
	game_prizes.winningTickets,
	game_prizes.prizeDescription,
	game_prizes.id
FROM
	current_games
	INNER JOIN game_prizes
	 ON current_games.gameId = game_prizes.gameID";
$result=mysqli_query($con,$sql);
$rarray = array();

// Associative array
foreach($result as $k => $v){
    $row=mysqli_fetch_assoc($result);
    
    
    if(is_array($row)){
		foreach ($row as $key=>$value){
        $rarray[] = array(
            $key => $row[$key]
        );
		}
        
    }
}

//foreach($rarray['266'] as $keys=>$values){
//    echo("$keys  $rarray[$keys]");
//    };
$json = json_encode($rarray);

echo($json);
echo(count($rarray));

//printf ("%s (%s)\n",$row["gameName"],$row["ticketPrice"],$row["totalTicketsPrinted"],$row["paidTickets"],$row["winningTickets"],$row["prizeDescription"],$row["tierNumber"],$row["gameID"]);

// Free result set
mysqli_free_result($result);

mysqli_close($con);
?> 