# Initialisation des robots
## Installation du système d'exploitation et configuration de la connexion wifi
* Installer RasperryPi Lite 64-bit sur les cartes SD : https://www.raspberrypi.com/software/operating-systems/
* Modifier le fichier [wifi_hotspot/wpa_supplicant.conf](wifi_hotspot/wpa_supplicant.conf) ( Uniquement les lignes SSID et psk )
* Déplacer le fichier dans la carte SD et démarrer le RaspberryPi dessus
* Il est possible de les connecter au réseau wifi hotspot crée par un RaspberryPi ce sera détaillé un peu plus bas.

## Configuration du RaspberryPi pour utiliser la librairie MakeBlock (Capteurs et Moteurs)
* Executer ces commandes / opérations dans l'ordre : 
```
sudo apt-get update
sudo apt-get full-upgrade
sudo apt install python3-pip
sudo reboot
sudo raspi-config -> Localisation Options -> WLAN -> FR
interface -> serial -> No / Yes
sudo nano /boot/config.txt -> Ajouter : 	#Enable uart			à la fin.
						enable_uart=1
						dtoverlay=pi3-disable-bt
												
sudo reboot
sudo systemctl disable hciuart
sudo pip install megapi
sudo pip install pyserial
```
Et la configuration est alors terminé vous pouvez tester cela en exécutant un script exemple MakeBlock : 
https://github.com/Makeblock-official/PythonForMegaPi/tree/master/examples

## Création d'un hotspot Wifi sur un des Raspberry : 
* Suivre le tutoriel indiqué sur ce site : https://raspap.com/#quick
* Faire une commande **ifconfig** pour vérifier que l'ip est bien celle indiqué sur le site
* Il est alors possible d'avoir accès au panel de configuration du hotspot via : [10.3.141.1](10.3.141.1)
* Sur ce panel il est utile de faire plusieurs choses : 
	- Changer le SSID, la clé wifi ainsi que le Channel si nécessaire 
 	- Mettre des ip static pour chaque robots pour faciliter la suite : DHCP Server -> Static Leases 
 ![image](https://user-images.githubusercontent.com/35781656/218414799-37e7afe9-2a4a-4825-a672-90806a005dd0.png)





# Communication UDP
## Création d'un serveur
* Importer les librairies suivantes:
```
import queue
import socket
import threading
```

* Déterminer l'adresse ip de la carte rasberry pi en saisissant dans son terminal mobaxterm :
```
ifconfig
```
![ifconfig](https://user-images.githubusercontent.com/124148152/218418722-fa955eca-8282-4e9a-90c5-6dba7f65835c.jpg)

* Saisir le code suivant pour créer le serveur(l'entier associé à la variable port est choisi de manière aléotoire mais il doit par la suite être gardé pour les autres appareils amenés à se connecter au serveur)
```
host = "10.3.141.1"
port = 4455
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))
```

* Saisir cette ligne pour recevoir un message :
```
message, addr = server.recvfrom(1024)
```
Addr correspond à l'adresse (ip, port) de l'appareil qui envoie le message. Le message reçu est un string codé en utf-8 qui peut être décodé par la ligne : 
```
message.decode("utf-8")
```

* Saisir cette ligne pour envoyer un message : 
```
server.sendto(msg, addr)
```
Msg correspond au string codé en utf-8 que l'on veut envoyer et adrr l'adresse (ip, port) de l'appareil à qui l'on veut envoyer ce message.

* Le serveur doit être en mesure de pourvoir à la fois envoyer et recevoir des messages. Pour cela, créer des thread avec 2 fonctions, send et receive, chargées de recevoir et d'envoyer des informations, qui vont être exécuteés parallèlement:
```
messages = queue.Queue()

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            print(message.decode("utf-8"))
        except:
            pass
                                 
def send():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            server.sendto(message, p[0])
            server.sendto(message, p[1])
            server.sendto(message, p[2])
            

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)
t1.start()
t2.start()
```
Ici, le serveur stock et affiche les messages qu'il reçoit dans une pile 'messages' dans la fonction receive, qui va ensuite être dépilée dans la fonction send pour renvoyer le message aux autres robots. "p" est une liste qui contient la liste des adresses des 3 robots.


## Création des robots clients

* Importer les librairies suivantes:
```
import queue
import socket
import threading
from megapi import *
```
* Déterminer l'adresse ip de la carte rasberry pi en saisissant dans son terminal mobaxterm :
```
ifconfig
```

* Saisir le code suivant pour créer le client robot (l'entier associé à la variable port est le même que pour le serveur):
```
port = 4455
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("", port))
```
* Comme pour le serveur, créer des thread pour que les robots puissent à la fois envoyer et recevoir des informations. La fonction receive est assez similaire à celui du serveur contrairement à la fonction send dans lequel les robots n'envoient pas ce qu'ils reçoivent mais les données de leurs capteurs.

* Pour récupérer les données des capteurs, voir la librairie MakeBlock :
https://github.com/Makeblock-official/PythonForMegaPi


## Node-RED

* Installer Node-RED sur le serveur en saisissant dans le terminal mobaxterm : 
```
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```
Pour accéder à Node-RED, saisir dans un navigateur : 
```
AdressIPRaspberry:1880
```

* 



