<form method="post">
<?php
//Verbindung zu Postgres herstellen
$verbindung = pg_connect("host=localhost port=5432 dbname=IAT user=postgres password=postgres");

if(isset($_POST['WerkzeugID'])){
  // Falls Eingabe => verwendetes Werkzeug in DB schreiben
  $result = pg_query($verbindung, "UPDATE ausgeruestet SET id_sek_werkzeug=$_POST[WerkzeugID] WHERE id_maschine=1;");                                                                                                            
}
echo "<p style='color:white;'>Aktuell verwendetes Werkzeug: </br>";
//Auslesen des aktuell verwendeten Werkzeugs
$result1 = pg_query($verbindung, "SELECT * FROM sek_werkzeuge WHERE id_sek_werkzeug = (SELECT id_sek_werkzeug FROM ausgeruestet);");
while ($row = pg_fetch_assoc($result1)) {
    echo $row['name'];
    echo "</br>";
    //Auswählen des entsprechenden WZs
    if($row['id_sek_werkzeug']==1){
      echo "  <input type='radio' value='1' name='WerkzeugID' checked='checked'>4 mm Fr&auml;ser</input></br>";
      echo "  <input type='radio' value='2' name='WerkzeugID'>6 mm Fr&auml;ser</input>";    
    }elseif($row['id_sek_werkzeug']==2){
      echo "  <input type='radio' value='1' name='WerkzeugID'>4 mm Fr&auml;ser</input></br>";
      echo "  <input type='radio' value='2' name='WerkzeugID' checked='checked'>6 mm Fr&auml;ser</input>";
    }
}

//Am besten einbinden durch folgenden HTML-Code in einem Textfeld:
//<iframe src="http://192.168.42.110/werkzeugwahl.php" height="100%" width="100%" frameBorder="0"></iframe>
?>
</p>
<input type="submit" name="submit" value="Werkzeugwechseln" />
</form>

<a href='./wz_reset.php'>Neues Werkzeug eingesetzt?</a>
</br>
<a href='./bruch.php'>Werkzeugbruchsimulieren</a>