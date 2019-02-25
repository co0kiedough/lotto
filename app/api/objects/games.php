<?php
class Games{
    
    private $conn;
    private $table_name = 'current_games';
    
    public $gameId;
    public $gameName;
    public $ticketPrice;
    public $totalTicketsPrinted;
    public $launchDate;
    public $disableDate;
    public $id;
    
    // constructor
    public function __construct($db){
        $this->conn = $db;
    }
    
    function read(){
        
        $query = "SELECT
	lotto.current_games.gameId,
	lotto.current_games.gameName,
	lotto.current_games.ticketPrice,
	lotto.current_games.totalTicketsPrinted,
	lotto.current_games.launchDate,
	lotto.current_games.disableDate,
	lotto.current_games.id,
	lotto.game_prizes.paidTickets,
	lotto.game_prizes.winningTickets,
	lotto.game_prizes.prizeDescription,
	lotto.game_prizes.tierNumber
FROM
	lotto.game_prizes
	INNER JOIN lotto.current_games
	 ON lotto.game_prizes.gameID = lotto.current_games.gameId";
     
     // prepare query
     $stmt = $this->conn->prepare($query);
     
     //execute
     $stmt->execute();
     
     return $stmt;
        
    }
    
}
?>