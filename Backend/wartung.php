<form method="post">
<p style='color:white;'>
<?php
// Herstellen einer Verbindung zur DB
$verbindung = pg_connect("host=localhost port=5432 dbname=IAT user=postgres password=postgres") or die("Verbindung zur Datenbank konnte nicht hergestellt werden");

// Wurde Wartung durchgeführt?
if(isset($_POST['sure'])){
if($_POST['sure']=="on"){
echo "Wartung erfolgt</br>";
// Laufzeit in DB updaten
$result = pg_query($verbindung, "UPDATE maschinen SET laufzeit=0 WHERE id_maschine=1;");                                                                                                            
}}else{
if(isset($_POST['Wartung'])){
    // Wurde die Checkbox nicht ausgewählt? Hinweis geben!
    echo "<script>alert('Kästchen anwählen');</script>";
}
echo "Wurde die Wartung durchgef&uuml;hrt?</br>
Wurden die F&uuml;hrungen ge&ouml;lt und gefettet.
</br>
<a href='https://www.youtube.com/watch?v=Xlh3zJRHk0Q' target='_blank'>Wartungsanleitung</a>
</br>

<input type='hidden' name='Wartung' value='1'>
<input type='checkbox' name='sure'>Ich best&auml;tige, dass die Wartung ordnungsgem&auml;ß durchgeführt wurde.</input>
</br><input type='submit' name='submit' value='Wartung erledigt' /> </p>
</p>
</form>
";
}


//Am besten einbinden durch folgenden HTML-Code in einem Textfeld:
//<iframe src="http://192.168.42.110/wartung.php" height="100%" width="100%" frameBorder="0"></iframe>

?>