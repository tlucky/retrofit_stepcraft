# Server.py
# Skript läuft auf dem Raspberry Pi
# stellt Verbindung zur Sensorik her
# stellt OPC UA Server zur Verfügung

# Import der Bibliotheken
import opcua
import time
import sys
import os
import math
import board
import busio
import smbus
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

######
#löschen
acc_x2=0   
acc_y2=0
acc_z2=0
zeit=0
######

# Festlegung des BUS-Systems
bus = smbus.SMBus(1)
i2c = busio.I2C(board.SCL, board.SDA)

# GPIO-Bezeichnung BCM stezen
GPIO.setmode(GPIO.BCM)

# Definieren der I2C Register des Beschleunigungssensors
ACCEL_YOUT_H = 0x3B
ACCEL_XOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
PWR_MGM1 = 0x6B

# GPIO-Pins Encoder (gemeinsamer Encoder-Pin auf GND)
in_a = 17
in_b = 4

# Pullup-Widerstand einschalten
GPIO.setup(in_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(in_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Merker fuer Encoder-Zustand (global)
old_a = GPIO.input(in_a)
old_b = GPIO.input(in_b)

# Setup des OPC-UA Servers
server = opcua.Server()
url = "opc.tcp://192.168.42.111:4840"  # IP-Adresse des Servers und Port
server.set_endpoint(url)

# Definition der OPC-UA Datenbankstruktur
node = server.get_objects_node()

Beschl_Sensor = node.add_object(nodeid=12, bname="Beschleunigungssensor")
richtung = Beschl_Sensor.add_variable(nodeid=14, bname="Verfahrrichtung", val=0)
beschl = Beschl_Sensor.add_variable(nodeid=13, bname="Beschleunigungen", val=0)
richtung.set_writable()
beschl.set_writable()

Leistung = node.add_object(nodeid=2, bname="Leistungen")
Maschine = Leistung.add_object(nodeid=3, bname="Maschine")
Spindel = Leistung.add_object(nodeid=4, bname="Spindel")
Laufzeit = Maschine.add_variable(nodeid=5, bname="Maschinenlaufzeit", val=0)
I_Maschine = Maschine.add_variable(nodeid=6, bname="Maschinenstrom", val=0)
U_Maschine = Maschine.add_variable(nodeid=7, bname="Maschinenspannung", val=0)
P_Maschine = Maschine.add_variable(nodeid=8, bname="Maschinenleistung", val=0)
I_Spindel = Spindel.add_variable(nodeid=9, bname="Spindelstrom", val=0)
U_Spindel = Spindel.add_variable(nodeid=10, bname="Spindelspannung", val=0)
P_Spindel = Spindel.add_variable(nodeid=11, bname="Spindelleistung", val=0)
Laufzeit.set_writable()
I_Maschine.set_writable()
U_Maschine.set_writable()
I_Spindel.set_writable()
U_Spindel.set_writable()
P_Maschine.set_writable()
P_Spindel.set_writable()

Werkzeug = node.add_object(nodeid=15, bname="Werkzeug")
Temp = Werkzeug.add_variable(nodeid=17, bname="Werkzeugtemperatur", val=0)
Temp.set_writable()

Druck = node.add_object(nodeid=18, bname="3D-Druck")
Druckbool = Druck.add_variable(
    nodeid=19, bname="3D-Drucker in Betrieb", val=False, datatype=opcua.ua.ObjectIds.Boolean)
# hoffe das hier ist richtig mit Datatype und val=False <-evtl val=0
Verbrauch = Druck.add_variable(nodeid=20, bname="Filament-Verbrauch", val=0)
Druckbool.set_writable()
Verbrauch.set_writable()

#Standardwert setzen
Druckbool.set_value(False)

# Start des OPC-UA Servers
server.start()
print("Server gestartet: \n IP-Adresse: {}" .format(url))
t_renew = 1  # Datenaktualisierung einmal pro Sekunde
iDauerM = 0

# Auslesen des Beschleunigungssensors

def read_mpu_data(addr):
    # Es muessen zwei Register ausgelesen werden, da der Wert zwei Byte groß ist
    high = bus.read_byte_data(0x68, addr)
    low = bus.read_byte_data(0x68, addr+1)

    value = ((high << 8) | low)

    # Wert wird skaliert
    if(value > 32768):
        value = value - 65536
    return value


def read_temp_data():
    #Auslesen des I2C-Registers
    Temp = bus.read_byte_data(0x5a, 0x07) 
    return Temp

encoder_n = 0
def get_encoder():
  # liest den Encoder aus
  global old_a, old_b, encoder_n

  # GPIO-Pins einlesen
  new_a = GPIO.input(in_a)
  new_b = GPIO.input(in_b)

  # Falls sich etwas geaendert hat => Klick zählen 
  if (new_a != old_a or new_b != old_b):
      print("Klick")
      encoder_n += 1
  
  old_a = new_a
  old_b = new_b
  # entprellen
  time.sleep(0.02)

  return encoder_n

try:
    # Beschleunigungssensor initialisieren
    bus.write_byte_data(0x68, PWR_MGM1, 1)
    while True:
        # Auslesen der Beschleunigungswerte; Adresse: 0x68
        try:
            acc_x = read_mpu_data(ACCEL_XOUT_H)/1750+0.07+0.018
            print("x" + str(acc_x))
        except:
            acc_x = acc_x
            print("alt x")
        
        try:
            acc_y = - (read_mpu_data(ACCEL_YOUT_H)/1750+0.357-0.013)
            print("y" + str(acc_y))
        except:
            acc_y = acc_y
            print("alt y")
        
        try:
            acc_z = -(read_mpu_data(ACCEL_ZOUT_H)/1750-9.9-0.1)
            print("z" + str(acc_z))
        except:
            acc_z = acc_z
            print("alt z")
        
        # maximale Beschleunigung erkennen
        acc_res = [acc_x, acc_y, acc_z]
        
        # schreiben in OPC UA Datenbank
        beschl.set_value(acc_res)
        richtung.set_value(acc_res.index(max(acc_res)))
    
        # Berechnung des resultierenden Vektors
        beschleunigung_res = math.sqrt(acc_x**2+acc_y**2+acc_z**2)

        # Auslesen der Temperaturdaten; Adresse: 0x0E
        werk_Temp = read_temp_data()

        # Setzen der Temperaturdaten in Datenbank
        Temp.set_value(werk_Temp)

        #Auslesen des A/D-Wandlers; auslesen via Adafruit Library
        adc = Adafruit_ADS1x15.ADS1115()
        
        #Messbereich auswaehlen, siehe Tab4, Datenblatt ADS1115
        GAIN = 1
        
        values = [0]*4
        for i in range(4):
        #Alle Channels in einen Array lesen
            values[i] = adc.read_adc(i, gain=GAIN)        
        chan2 = values[1]
        maschstrom = -chan2/1500+15
                
        maschleist = 34*maschstrom
 
        # Maschinenlaufzeit ermitteln
        if chan2 > 0.2:
            iDauerM += 0.5

        # Setzen der Werte in die Datenbank
        Laufzeit.set_value(iDauerM)
        U_Maschine.set_value(34)
        I_Maschine.set_value(maschstrom)
        P_Maschine.set_value(maschleist)
            
        # Filament-Verbrauch erkennen
        klick = 0
        change = get_encoder()
        if change != 0:
            klick = klick + abs(change)
            Druckbool.set_value(True)
            # x/48 = eine Umdrehung
            # Setzen des Filament-Verbrauchs in die Datenbank
            Verbrauch.set_value(klick)            

        time.sleep(t_renew)
finally:
    server.stop()