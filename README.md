# CO<sub>2</sub>-, Temperatur- und Feuchtigkeitmonitor

## Einleitung
Raspberry Pi Datenlogger für CO<sub>2</sub>, Temperatur und Feuchtigkeit mit den Sensoren
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

* Git und Python3 Pakete installieren
  ````sh
  sudo apt install git python3-pip python3-pil python3-pandas python3-matplotlib
  ````
* pip installieren und Python3 Tools upgraden
  ````sh
  sudo python3 -m pip install --upgrade pip setuptools wheel
  ````  
* Python3 Pakete installieren
  ````sh
  sudo pip3 install RPi.GPIO spidev Adafruit_DHT mh-z19
  ````    
* e-Paper Treiber GitHub Seite von Waveshare https://github.com/waveshare/e-Paper
  ````sh
  sudo git clone https://github.com/waveshare/e-Paper
  cd e-Paper/RaspberryPi\&JetsonNano/
  sudo python3 setup.py install
  ````
* Unterordner "devel" erstellen und dieses Repository mit git klonen
  ````sh  
  cd ~
  mkdir devel
  cd devel
  git clone https://github.com/ego1105/co2_monitor.git  
  ````
* Cronjob erstellen, der co2_monitor.sh jede Minute aufruft
  ````sh  
  crontab -e
  # m h  dom mon dow   command
  * * * * * /home/pi/devel/co2_monitor/co2_monitor.sh
  ````    

  
