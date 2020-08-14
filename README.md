## Table of contents
* [General info](#general-info)
* [Example](#Example)


## General info
Ein Stepcraft wurde mit Sensorik ausgestattet, um unterschiedliche Prozesse zu tracken. Ein Raspberry Pi nimmt über I2C und GPIO verschiedene Sensorwerte auf und propagiert diese in OPC UA. Dazu werden die Werte in eine PostgreSQL Datenbank geschrieben. Grafana dient als Frontend und greift auf die Datenbank zu. Zudem visualisiert Grafana die unterschiedlichen Zustände des Stepcrafts und triggert bei Überschreiten gewisser Grenzwerte gewisse Services, z. B. Durchführung einer Wartung nach X Stunden.

<p align="center">
  <img src="https://github.com/tlucky/retrofit_stepcraft/blob/master/images/Gesamtfunktion.png" width="500" title="Gesamtfunktion">
</p>

## Example

