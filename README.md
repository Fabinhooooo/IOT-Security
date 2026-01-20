# Projet de Sécurisation IoT : ESP32-C6 (Secure Boot, Flash Encryption, OTA HTTPS)

Ce projet implémente une architecture de sécurité complète ("Trust Chain") pour un objet connecté basé sur l'ESP32-C6. Il couvre la sécurité matérielle, l'intégrité du firmware et la confidentialité des communications lors des mises à jour à distance (OTA).

## 🚀 Fonctionnalités Principales

### 1. Sécurité Matérielle (Device Security)
* **Flash Encryption :** Chiffrement matériel (AES-XTS) de la mémoire Flash. Empêche la lecture physique du firmware et des secrets (clés Wifi, certificats) en cas de vol du boîtier.
* **Secure Boot (V2) :** Vérification de la signature RSA-3072 du firmware au démarrage via une chaîne de confiance matérielle (eFuses). Empêche l'exécution de code non autorisé.

### 2. Mises à jour Sécurisées (Secure OTA)
* **Architecture A/B (Rollback) :** Utilisation d'une table de partition personnalisée (`partitions.csv`) avec deux slots d'application (`ota_0`, `ota_1`). Si une mise à jour échoue, le système revient automatiquement à la version précédente.
* **Signature Numérique :** Chaque mise à jour binaire est signée cryptographiquement avant déploiement. L'ESP32 vérifie cette signature avant l'écriture en mémoire.

### 3. Confidentialité Réseau (Data Privacy)
* **HTTPS / TLS :** Communication chiffrée entre l'ESP32 et le serveur de mise à jour.
* **Certificate Pinning :** L'ESP32 possède le certificat public du serveur (`ca_cert.pem`) intégré dans son firmware pour empêcher les attaques Man-in-the-Middle.

---

## 📂 Structure du Projet

* **`main/`** : Code source de l'application (logique Wifi, tâche OTA, configuration HTTPS).
* **`secure_keys/`** : Clés privées (RSA) pour le Secure Boot et la Flash Encryption (à ne jamais divulguer en production).
* **`ca_cert.pem` / `ca_key.pem`** : Certificats pour le serveur HTTPS (PKI locale).
* **`ota_server_https.py`** : Serveur Python sécurisé pour délivrer les mises à jour.
* **`iot_security_manager.py`** : Script utilitaire pour signer automatiquement les binaires après compilation.
* **`partitions.csv`** : Table de partitionnement définissant les zones OTA et NVS.

---

## 🛠️ Installation et Prérequis

### Prérequis
* ESP-IDF v5.x (Testé sur v5.4.3)
* Python 3
* Carte de développement ESP32-C6

### Configuration
1.  **Menuconfig :**
    ```bash
    idf.py menuconfig
    ```
    * *Security Features* -> Enable Flash Encryption & Secure Boot.
    * *Partition Table* -> Custom partition table (`partitions.csv`).
    * *Component config* -> ESP System Settings -> CPU Frequency (Set to 80MHz to avoid Brownout on USB power).

2.  **Génération des Clés :**
    Les clés de sécurité ont été générées et brûlées dans les eFuses lors de la première initialisation.

---

## 🔄 Workflow de Mise à Jour (OTA)

Pour déployer une nouvelle version du firmware :

1.  **Modification :** Changer le code dans `main/hello_world_main.c` (ex: changer le numéro de version).
2.  **Compilation :**
    ```bash
    idf.py build
    ```
3.  **Signature Automatique :**
    Lancer le script de gestion qui signe le binaire et le place à la racine du serveur :
    ```bash
    python iot_security_manager.py
    ```
4.  **Démarrage du Serveur :**
    ```bash
    python ota_server_https.py
    ```
5.  **Mise à jour de l'ESP32 :**
    Redémarrer l'ESP32 (Reset). Il détectera le nouveau fichier signé, le téléchargera via HTTPS et l'installera sur la partition passive.

---

## ✅ Tests de Validation

### Test 1 : Protection contre l'extraction (Flash Encryption)
Une tentative de lecture de la mémoire via `esptool` a été réalisée.
* **Commande :** `esptool.py -p COMx read_flash 0 0x200000 dump.bin`
* **Résultat :** Le fichier `dump.bin` contient des données aléatoires (bruit), rendant le reverse-engineering impossible.

### Test 2 : Protection contre l'injection (Anti-Sabotage)
Un fichier binaire valide a été corrompu manuellement (modification hexadécimale) pour simuler un firmware piraté ou corrompu.
* **Résultat :** L'ESP32 a rejeté la mise à jour avec l'erreur :
    > `E (...) esp_https_ota: Mismatch chip id`
    > `E (...) OTA_SECURE: Échec de la mise à jour`
    Le système est resté stable sur la version précédente.

### Test 3 : Confidentialité (HTTPS)
* **Résultat :** L'accès au serveur via HTTP (`http://...`) est refusé. L'accès via HTTPS est validé par le navigateur (cadenas présent), prouvant le chiffrement du canal de transport.

---

## ⚠️ Notes Techniques & Limitations

* **Brownout / Alimentation USB :** L'activation simultanée du Wifi, de l'écriture Flash et du chiffrement TLS provoque un pic de consommation élevé. Pour éviter les redémarrages intempestifs (Brownout Reset) lors du développement sur port USB standard, la fréquence CPU a été réduite à 80MHz et la taille des buffers RX/TX ajustée.
* **Certificats :** Ce projet utilise des certificats auto-signés pour l'environnement de développement local.

---

**Auteur :** [Security TEAM]
**Date :** Janvier 2026