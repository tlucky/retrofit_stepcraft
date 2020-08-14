# Skript stellt einen Teilezähler bereit
# fungiert als zweite OPC UA Datenbank
# verdeutlicht Skalierbarkeit des Systems
# Import der Bibliotheken
from opcua import Server
import time
import os

# Setup des OPC-UA Servers
server = Server()
url = "opc.tcp://localhost:4841"  # IP-Adresse des Servers und Port
server.set_endpoint(url)
name = "Dummy OPC-UA SERVER"
addspace = server.register_namespace(name)

# Definition der OPC-UA Datenbankstruktur
node = server.get_objects_node()

Teilecnt = node.add_object(addspace, "Teilezähler")
Teileanzahl = Teilecnt.add_variable(addspace, "Anzahl gefräster Teile", 0)

cnt = 0
# Start des OPC-UA Servers
server.start()
print("Server gestartet: \n IP-Adresse: {}" .format(url))

try:
    while True:
        # Alle 15 s wird ein Teil fertiggestellt
        cnt += 1
        Teileanzahl.set_value(cnt)

        time.sleep(15)
finally:
    server.stop()
