# IOT-Security
Internet Of Things Security Project

Tout d'abord ce qu'on a fait c'est installer l'extension de l'ESP sur VS Code, puis une fois cela fait on a lancer idf.py menuconfig pour avoir l'interface de configuration du noyau de l'ESP32.

ACTIVER LE CHIFFREMENT: On a activer la ligne "Enable Flash Encryption" (en mode développement).

COMPILATION: Ici on construit notre systéme sécurisé avec la commande "idf.py build".

ERREUR DE COMPILATION: Pas assez de memoire, donc on a modifier la "Partition Table" de 0x8000 à 0x10000.

SIGNATURE: On a lancé notre code avec "python iot_security_manager.py" et c'est un succes, le firmware est bien compilé et le script Python a correctement signé le binaire.
