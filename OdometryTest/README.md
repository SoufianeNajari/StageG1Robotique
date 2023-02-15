# Odometrie :
* odometryV1 - V5 : Versions intermédiaires instables 
* odometryV6 : Fonction straight et TurnRight(angle) fonctionnelle, la fonction go présentes quelques bugs et la fonction turnLeft ne fonctionne pas ( On tourne alors à droite pour tourner à gauche )
* reset.py : Permet de mettre la vitesse des moteurs à 0 en cas de problème du programme 
* gyroRead.py : Permet de connaître l'orientation actuelle du gyro, ***seule l'orientation par rapport à l'axe z est utile et doit être remis à zero en appuyant sur la touche reset du megapi avant de commencer un programme necessitant le gyro***
