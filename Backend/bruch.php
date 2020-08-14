<?php
//DB Verbindung herstellen
$verbindung = pg_connect("host=localhost port=5432 dbname=IAT user=postgres password=postgres");

if(isset($_POST['Bruch'])){
    // Soll Bruch simuliert werden?
    $result = pg_query($verbindung, "UPDATE services SET laufzeit=1 WHERE id_service=4;");                                                                                                            
}
?>
<p style='color:white;'>Die vorliegende Funktion simuliert einen Werkzeugbruch. Dieser wird in Grafana angezeigt. Nichts wird kaputt gehen.</p>
<form method="post">
    <p style='color:white;'><input type='checkbox' name='Bruch'>Werkzeugbruch</p></input>
    <input type='submit' value='Werkzeugbruch simulieren'></input>
</form>
<a href='./werkzeugwahl.php'>Zur&uuml;ck</a>