<form method="post">
<p style='color:white;'>
<?php
//DB Verbindung herstellen
$verbindung = pg_connect("host=localhost port=5432 dbname=IAT user=postgres password=postgres") or die("Verbindung zur Datenbank konnte nicht hergestellt werden");

if(isset($_POST['id'])){
    // Wurde WZ erneuert? --> Update in DB
    echo "Werkzeug mit ID=$_POST[id] gewechselt</br>";
    $result = pg_query($verbindung, "UPDATE sek_werkzeuge SET laufzeit=0, verbleibende_laufzeit=0 WHERE id_sek_werkzeug=$_POST[id];");
}

//Welche WZs sind vorhanden?
$result1 = pg_query($verbindung, "SELECT * FROM sek_werkzeuge WHERE id_prim_werkzeug=2");
while ($row = pg_fetch_assoc($result1)) {
    echo "<input type='radio' name='id' value='$row[id_sek_werkzeug]'>$row[name]</input></br>";
}
?>
</br>
</br>
<input type='submit' name='submit' value='Neues Werkzeug eingesetzt' /> </p>
</p>
</form>
<a href='./werkzeugwahl.php'>Zur&uuml;ck</a>