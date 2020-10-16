# CO<sub>2</sub>-, Temperatur- und Feuchtigkeitmonitor

## Einleitung
Einfacher Datenlogger für CO<sub>2</sub>, Temperatur und Feuchtigkeit mit den Sensoren
* MH-Z19B https://pypi.org/project/mh-z19/
* DHT22 https://www.einplatinencomputer.com/raspberry-pi-temperatur-und-luftfeuchtigkeitssensor-dht22/

einem schwarz-rotem E-Paper Display,
* https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(B)

und einer CO<sub>2</sub> Ampel mit roter, gelber und grüner Leuchtdiode.


## Installationsschritte
* [Raspberry Pi OS lite ohne Monitor und Tastatus headless einrichten](https://www.tutonaut.de/anleitung-raspberry-pi-ohne-monitor-und-tastatur-headless-einrichten/)
* SSH verbindung mit Putty oder MobaXterm herstellen
* `sudo raspi-config`
  * Passwort ändern
  * optional Hostname ändern
  * SPI aktivieren für E-Paper Modul https://www.waveshare.com/wiki/2.9inch_e-Paper_Module_(B)
  * Serial Port aktivieren für CO2 Sensor https://github.com/UedaTakeyuki/mh-z19/wiki/How-to-Enable-Serial-Port-hardware-on-the-Raspberry-Pi
  * Finish und Reboot, dann bei neuem Hostname neu verbinden

  
  
  
  
  
