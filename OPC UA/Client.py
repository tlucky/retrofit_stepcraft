# Client.py sammelt Daten der OPC UA Server und speichert sie in Postgres-Datenbank
# Import der benoetigten Module
from opcua import Client
import time
import psycopg2  # fuer Kommunikation zu Postgres

# Sensor IDs fuer die Datenbank
id_beschleunigungssensor = 1
id_maschinenspannung = 2
id_spindelspannung = 3
id_maschinenstrom = 4
id_spindelstrom = 5
id_spindelleistung = 6
id_maschinenleistung = 7
id_temperatur = 8
id_x_richtung = 9
id_y_richtung = 10
id_z_richtung = 11
id_Teilezaehler = 12
id_x_weg = 13
id_y_weg = 14
id_z_weg = 15
# ID Primaerwerkzeuge
# hier steht das "_1" fuer den ersten Druckkopf, es können noch weitere hinzugefuegt werden
id_3d_druckkopf_ph40_1 = 1
id_hf_spindel_500w_1 = 2
# ID Sekundaerwerkzeuge
id_fraeser_4mm_1 = 1
id_fraeser_6mm_1 = 2
id_filament_1 = 3
# ID Maschine
id_maschine = 1

# Sonstige Variablen
x_geschw = 0
y_geschw = 0
z_geschw = 0
x_weg = 0
y_weg = 0
z_weg = 0
tstep = 1  # Zeitschritt erhoeht um Wert in Sekunden [s]
laufzeit = 0  # hier speichern
duration_time = time.time()  # Laufzeit Programm
old_filament = 0


# Verbindung zur Datenbank definieren
try:
    conn = psycopg2.connect(host="localhost", port="5432", dbname="IAT",
                            user="postgres", password="postgres")  # Datenbankname anpassen
    cur = conn.cursor()
    print("Connection to database successful")
except:
    print("Unable to connect to database")

# Verbindung zu OPC UA Servern herstellen
try:
    client = Client("opc.tcp://192.168.42.111:4840/")
    client.connect()
    print("Connection to OPC UA Server successful")
    # Verbindung zum dummy_Client herstellen
    dummy_client = Client("opc.tcp://localhost:4841/")
    dummy_client.connect()
    print("Connection to OPC UA Dummy-Server successful")
except:
    print("Unable to connect to OPC UA Server")

##########
#Funktionen
##########
# Query-Funktionen für Inserts in DB
def query_insert(id_sensor, wert):
    cur.execute("INSERT INTO sensordaten (id_prim_werkzeug, id_sek_werkzeug, id_sensor, wert) VALUES (%i, %i, %i, %f)" % (id_prim_werkzeug, id_sek_werkzeug, id_sensor, wert))

def query_laufzeit(id_prim_werkzeug):
    # Lesen und Schreiben der Laufzeit in Variable (prim_laufzeit)
    cur.execute("SELECT laufzeit, max_laufzeit, verbleibende_laufzeit FROM prim_werkzeuge \
                    WHERE id_prim_werkzeug = %i" % id_prim_werkzeug)  # max_laufzeit, verbleibende_laufzeit,
    prim_laufzeit = cur.fetchall()
    laufzeit = (prim_laufzeit[0][0])
    max_laufzeit = (prim_laufzeit[0][1])
    verbleibende_laufzeit = (prim_laufzeit[0][2])
    laufzeit += tstep
    cur.execute("UPDATE prim_werkzeuge SET laufzeit = %f, verbleibende_laufzeit = %f \
                    WHERE id_prim_werkzeug = %i" % (laufzeit, verbleibende_laufzeit, id_prim_werkzeug))

##########
#Implementierung
##########
    
# Abfrage der Leerlaufleistung aus Datenbank
leerlaufleistung = 54
cur.execute("SELECT leerlaufleistung FROM maschinen \
                    WHERE id_maschine = %i" % id_maschine)
maschinen_leerlaufleistung = cur.fetchall()[0][0]
print(maschinen_leerlaufleistung)


try:
    while True:
        duration_time = time.time()  # Laufzeit Programm
        # Abfrage der Daten vom OPC UA Dummy-Server
        Teile_node = dummy_client.get_node("ns=2;i=2")
        Teile = Teile_node.get_value()

        # Abfrage der Daten vom OPC UA Server
        Beschleunigungs_node = client.get_node("ns=13;i=1")
        beschl = Beschleunigungs_node.get_value()

        Richtung_node = client.get_node("ns=14;i=1")
        richt = Richtung_node.get_value()

        Maschinenlaufzeit_node = client.get_node("ns=5;i=1")
        Maschinenlaufzeit = Maschinenlaufzeit_node.get_value()

        Maschinenspannung_node = client.get_node("ns=7;i=1")
        Maschinenspannung = Maschinenspannung_node.get_value()

        Maschinenstrom_node = client.get_node("ns=6;i=1")
        Maschinenstrom = Maschinenstrom_node.get_value()

        Maschinenleistung_node = client.get_node("ns=8;i=1")
        Maschinenleistung = Maschinenleistung_node.get_value()

        Spindelspannung_node = client.get_node("ns=10;i=1")
        Spindelspannung = Spindelspannung_node.get_value()

        Spindelstrom_node = client.get_node("ns=9;i=1")
        Spindelstrom = Spindelstrom_node.get_value()

        Spindelleistung_node = client.get_node("ns=11;i=1")
        Spindelleistung = Spindelleistung_node.get_value()

        Temperatur_node = client.get_node("ns=17;i=1")
        Temperatur = Temperatur_node.get_value()

        druck_node = client.get_node("ns=19;i=1")
        druck = druck_node.get_value()

        filament_node = client.get_node("ns=20;i=1")
        filament = filament_node.get_value()

        if druck == True:
            # Definition der IDs für Primaer- und Sekundaerwerkzeug
            # id für 3-D Druckkopf
            id_prim_werkzeug = id_3d_druckkopf_ph40_1
            id_sek_werkzeug = id_filament_1

            # Schreiben der Anzahl der gefraesten Teile in die Datenbank
            query_insert(id_Teilezaehler, id_Teilezaehler)
            
            # Schreiben der Beschleunigungen in Datenbank
            query_insert(id_x_richtung, beschl[0])
            query_insert(id_y_richtung, beschl[1])
            query_insert(id_z_richtung, beschl[2])

            # Schreiben der resultierenden Beschleunigungsrichtung in Datenbank
            query_insert(id_beschleunigungssensor, richt)

            # Schreiben der Druckbretttemperatur (Temperatur) in Datenbank
            query_insert(id_temperatur, Temperatur)

            # Integrieren vom Weg (x,y,z-Richtung) und schreiben in die DB
            x_geschw = beschl[0] * tstep + x_geschw
            x_weg = 0.5 * beschl[0] * tstep ** 2 + x_weg # + x_geschw
            query_insert(id_x_weg, x_weg)

            y_geschw = beschl[1] * tstep + y_geschw
            y_weg = 0.5 * beschl[1] * tstep ** 2 + y_weg
            query_insert(id_y_weg, y_weg)
			
            z_geschw = beschl[2] * tstep + z_geschw
            z_weg = 0.5 * beschl[2] * tstep ** 2 + z_weg
            query_insert(id_z_weg, z_weg)

            # Lesen und Schreiben der Laufzeit in Variable (maschinen)
            cur.execute("SELECT laufzeit FROM maschinen WHERE id_maschine = %i" % id_maschine)  # max_laufzeit, verbleibende_laufzeit,
            masch_laufzeit = cur.fetchall()
            laufzeit = (masch_laufzeit[0][0])
            print("Laufzeit Maschine " + str(laufzeit))
            laufzeit += tstep

            # Abfrage, ob Laufzeit von Primärwerkzeug und Maschine erhöht werden soll, wenn Leerlaufleistung überschritten wird
            if (maschinen_leerlaufleistung < Maschinenleistung):
                cur.execute("UPDATE maschinen SET laufzeit = %f WHERE id_maschine = %i" % (laufzeit, id_maschine))
                query_laufzeit(id_prim_werkzeug)

            # Lesen und Schreiben der Laufzeit in Variable (sek_laufzeit)
            if old_filament != filament:  #da filament die Ticks einfach hochzaehlt. Wuerde das nicht dort stehen wuerden immer hoehere Tickzahlen von der verbleibenden Laufzeit abgezogen
                cur.execute("SELECT laufzeit, max_laufzeit, verbleibende_laufzeit  \
                                FROM sek_werkzeuge WHERE id_sek_werkzeug = %i" % id_sek_werkzeug)
                sek_laufzeit = cur.fetchall()                
                laufzeit = (sek_laufzeit[0][0]) # bisherige Laufzeit auslesen
                max_laufzeit = (sek_laufzeit[0][1])
                verbleibende_laufzeit = (sek_laufzeit[0][2])
                laufzeit = laufzeit + (filament-old_filament) # zwischen der Skriptlaufzeit erfolgte Klicks auf Laufzeit addieren
                verbleibende_laufzeit = max_laufzeit - laufzeit
                cur.execute("UPDATE sek_werkzeuge SET laufzeit = %f, verbleibende_laufzeit = %f \
                                WHERE id_sek_werkzeug = %i AND id_prim_werkzeug = %i"
                            % (laufzeit, verbleibende_laufzeit, id_sek_werkzeug, id_prim_werkzeug))
                old_filament = filament


            # Schreiben der Maschinenspannung (Maschinenspannung) in Datenbank
            query_insert(id_maschinenspannung, Maschinenspannung)

            # Schreiben der Maschinenstrom (Maschinenstrom) in Datenbank
            query_insert(id_maschinenstrom, Maschinenstrom)

            # Schreiben der Maschinenleistung (Maschinenleistung) in Datenbank
            query_insert(id_maschinenleistung, Maschinenleistung)
                
            conn.commit()  # Query mit Commit erfolgreich abgeschlossen

        else:

            # Definition der IDs für Primaer- und Sekundaerwerkzeug
            id_prim_werkzeug = id_hf_spindel_500w_1  # id für HF-Spindel
            id_sek_werkzeug = id_filament_1  # id für 3-D Filament

            # Schreiben der Anzahl der gefraesten Teile in die Datenbank
            query_insert(id_Teilezaehler, id_Teilezaehler)
            query_insert(id_x_richtung, beschl[0])
            query_insert(id_y_richtung, beschl[1])
            query_insert(id_z_richtung, beschl[2])
            query_insert(id_beschleunigungssensor, richt)

            # Integrieren vom Weg (x,y,z-Richtung) und schreiben in die DB
            x_geschw = beschl[0] * tstep + x_geschw
            x_weg = 0.5 * beschl[0] * tstep ** 2  + x_weg + x_geschw
            query_insert(id_x_weg, x_weg)

            y_geschw = beschl[1] * tstep + y_geschw
            y_weg = 0.5 * beschl[1] * tstep ** 2 + y_weg + y_geschw
            query_insert(id_y_weg, y_weg)
			
            z_geschw = beschl[2] * tstep + z_geschw + z_geschw
            z_weg = 0.5 * beschl[2] * tstep ** 2 + z_weg
            query_insert(id_z_weg, z_weg)

            # Lesen und Schreiben der Laufzeit in Variable (maschinen)
            cur.execute("SELECT laufzeit FROM maschinen WHERE id_maschine = %i" % id_maschine)  # max_laufzeit, verbleibende_laufzeit,
            masch_laufzeit = cur.fetchall()
            laufzeit = (masch_laufzeit[0][0])
            print("Laufzeit Maschine " + str(laufzeit))
            laufzeit += tstep

            # Abfrage, ob Laufzeit von Primärwerkzeug und Maschine erhöht werden soll, wenn Leerlaufleistung überschritten wird
            if (maschinen_leerlaufleistung < Maschinenleistung):
                cur.execute("UPDATE maschinen SET laufzeit = %f WHERE id_maschine = %i" % (laufzeit, id_maschine))
                query_laufzeit(id_prim_werkzeug)
            
            # Lesen und Schreiben der Laufzeit in Variable (prim_laufzeit)
            query_laufzeit(id_prim_werkzeug)
            # Zusatz fuer 3D-Druck
            cur.execute("SELECT id_sek_werkzeug FROM ausgeruestet")
            WZID = cur.fetchall()
            id_sek_werkzeug = WZID[0][0]

            # Lesen und Schreiben der Laufzeit in Variable (sek_laufzeit)
            cur.execute("SELECT laufzeit, max_laufzeit, verbleibende_laufzeit FROM sek_werkzeuge \
                            WHERE id_sek_werkzeug = %i" % id_sek_werkzeug)
            sek_laufzeit = cur.fetchall()  # 1x3 Vektor fuer Laufzeit
            laufzeit = 0    # hier speichern
            laufzeit = (sek_laufzeit[0][0])  # Zerlegen von Vektor
            max_laufzeit = (sek_laufzeit[0][1])  # Zerlegen von Vektor
            verbleibende_laufzeit = (sek_laufzeit[0][2])  # Zerlegen von Vektor
            verbleibende_laufzeit = verbleibende_laufzeit - filament  # neu berechnen von verbleibende_laufzeit
            laufzeit += tstep   # neu berechnen von laufzeit

            # Abfrage, ob Laufzeit von Sekundärwerkzeug erhöht werden soll, wenn Leerlaufleistung überschritten wird
            if (maschinen_leerlaufleistung < Maschinenleistung):
                cur.execute("UPDATE sek_werkzeuge SET laufzeit = %f, verbleibende_laufzeit = %f WHERE id_sek_werkzeug = %i AND id_prim_werkzeug = %i"
                            % (laufzeit, verbleibende_laufzeit, id_sek_werkzeug, id_prim_werkzeug))

            # Schreiben der Werkezeugtemperatur (Temperatur) in Datenbank
            query_insert(id_temperatur, Temperatur)

            # Schreiben der Maschinenspannung (Maschinenspannung) in Datenbank
            query_insert(id_maschinenspannung, Maschinenspannung)

            # Schreiben der Maschinenstrom (Maschinenstrom) in Datenbank
            query_insert(id_maschinenstrom, Maschinenstrom)

            # Schreiben der Maschinenleistung (Maschinenleistung) in Datenbank
            query_insert(id_maschinenleistung, Maschinenleistung)

            # Schreiben der Spindelspannung (Spindelspannung) in Datenbank
            query_insert(id_spindelspannung, Spindelspannung)

            # Schreiben der Spindelstrom (Spindelstrom) in Datenbank
            query_insert(id_spindelstrom, Spindelstrom)

            # Schreiben der Spindelleistung (Spindelleistung) in Datenbank
            query_insert(id_spindelleistung, Spindelleistung)
            
            # Query mit Commit erfolgreich abschließen
            conn.commit()
        print("x: " + str(x_weg))
        print("y: " + str(y_weg))
        print("z: " + str(z_weg))
        time.sleep(tstep-(time.time()-duration_time)) # fuer stabileren Prozess
finally:
    # Verbindungen trennen
    client.disconnect()
    dummy_client.disconnect()
