<?php
class Tickets{
    
    private $conn;
    private $table_name = "current_games";
    
    // Scratch Off current_games keys
    
    public $gameId;
    public $gameName;
    public $ticketPrice;
    public $totalTicketsPrinted;
    public $launchDate;
    public $disableDate;
    
    
    public function __construct($db){
        $this->conn = $db;
    }
    
}