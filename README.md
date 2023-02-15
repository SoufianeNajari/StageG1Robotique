# Initialisation des robots
## Installation du système d'exploitation et configuration de la connexion wifi
* Installer RasperryPi Lite 64-bit sur les cartes SD : https://www.raspberrypi.com/software/operating-systems/
* Télecharger le fichier [wifi_hotspot/wpa_supplicant.conf](wifi_hotspot/wpa_supplicant.conf), modifier les lignes SSID et psk et le déplacer à la racine de la carte SD.
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
sudo nano /boot/config.txt -> Ajouter à la fin : 	#Enable uart			
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

## Odométrie et utilisation du gyroscope 
* *Voir [odometryV6.py](OdometryTest/odometryV6.py) pour un exemple d'utilisation fonctionnel*

## Modèle cinématique 
* *Voir cette [vidéo](https://www.youtube.com/watch?v=aE7RQNhwnPQ&) pour plus d'info*

![modèle cinématique](https://user-images.githubusercontent.com/35781656/219004975-273fa09d-434d-4916-b01c-2fa068f99a3e.jpg)


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

* Saisir le code suivant pour créer le serveur(l'entier associé à la variable port est choisi de manière aléatoire mais il doit par la suite être gardé pour les autres appareils amenés à se connecter au serveur)
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
Ici, le serveur stocke et affiche les messages qu'il reçoit dans une pile 'messages' dans la fonction receive, qui va ensuite être dépilée dans la fonction send pour renvoyer le message aux autres robots. "p" est une liste qui contient la liste des adresses des 3 robots.


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
* Comme pour le serveur, créer des thread pour que les robots puissent à la fois envoyer et recevoir des informations. La fonction receive est assez similaire à celui du serveur contrairement à la fonction send dans laquel les robots n'envoient pas ce qu'ils reçoivent mais les données rassemblées par leurs capteurs.

* Voir la librairie MakeBlock pour récupérer les données des capteurs et actionner les moteurs :
https://github.com/Makeblock-official/PythonForMegaPi

### Format JSON

* Pour que les données échangées soient faciles à décrypter, les messages sont envoyés sous format JSON
```
"{ "VD":vitesseD, "VG":vitesseG, "Distance":distance, "z" : z}"
```
Pour faire cela, importer la librairie json
```
import json
```

Pour convertir du python en json : 
```
msg = {
        "VD" : vitesseD,
        "VG" : vitesseG,
        "Distance" : distance,
        "z" : z
    }
msg = json.dumps(msg) # on obtient un json string
```

Pour convertir du json en python :
```
msg = msg.loads(s) # on obtient un dictionnaire python
print(msg["VD"]) # affiche vitesseD
```

## Node-RED

* Installer Node-RED sur le serveur en saisissant dans le terminal mobaxterm : 
```
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```
Pour accéder à Node-RED, saisir dans un navigateur : 
```
AdressIPRaspberry:1880
```

* Pour tracer des graphiques sur les différentes données des robots, importer le module dashboard:

![Node red import](https://user-images.githubusercontent.com/124148152/218455377-68676edf-a7a8-44f6-bbb8-140f79582564.jpg)
 
* Utiliser le format json des messages pour récupérer les données
 
![image](https://user-images.githubusercontent.com/124148152/218424080-634b2e25-d37a-42b6-a86b-70d9d733ed9c.png)

* Aller dans l'onglet dashboard pour observer les courbes
 
![Dashboard](https://user-images.githubusercontent.com/124148152/218455411-a6dbe2e1-3b98-4dc5-b15f-3358039da6fa.jpg)

* Pour différencier la provenance des données, utiliser le node switch qui peut faire des opérations de comparaison sur les adresses ip des robots qui émettent des données

![node_switch](https://user-images.githubusercontent.com/124148152/218455449-3519d3e5-d862-438d-adac-54bddaeda2b5.jpg)

* Importer le module ci-dessous pour utiliser un clavier ou une souris branchée au raspberry pi:

![import clavier raspberry](https://user-images.githubusercontent.com/124148152/218463295-c777e894-3a31-46ff-a807-eabef436ad55.jpg)


