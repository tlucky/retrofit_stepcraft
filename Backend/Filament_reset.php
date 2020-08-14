<form method="post">
<p style='color:white;'>
<?php
//DB Verbindung herstellen
$verbindung = pg_connect("host=localhost port=5432 dbname=IAT user=postgres password=postgres") or die("Verbindung zur Datenbank konnte nicht hergestellt werden");

if(isset($_POST['id'])){
    //Wurde die Filament Rolle gewechselt? --> Updaten in der DB
    echo "Filament-Rolle gewechselt</br>";
    $result = pg_query($verbindung, "UPDATE sek_werkzeuge SET laufzeit=0, verbleibende_laufzeit=(SELECT max_laufzeit FROM sek_werkzeuge WHERE id_sek_werkzeug=$_POST[id]) WHERE id_sek_werkzeug=$_POST[id];");
}

//Welche Filamente sind in der DB vorhanden?
$result1 = pg_query($verbindung, "SELECT * FROM sek_werkzeuge WHERE id_prim_werkzeug=1;");
while ($row = pg_fetch_assoc($result1)) {
    // Welches Filament wurde gewechselt?
    echo "<input type='hidden' name='id' value='$row[id_sek_werkzeug]' checked=true></input></br>";
}
?>
<input type='submit' name='submit' value='Neues Filament eingesetzt' /> </p>
</p>
</form>