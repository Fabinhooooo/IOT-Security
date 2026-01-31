# Security Project LLMThings : ESP32-C6 (Secure Boot, Flash Encryption, OTA HTTPS)

This project implements a comprehensive security architecture (‘Trust Chain’) for a connected object based on the ESP32-C6. It covers hardware security, firmware integrity and communication confidentiality during remote updates (OTA).

## 🚀 Key Features

### 1. Sécurité Matérielle (Device Security)
* **Flash Encryption :** Hardware encryption (AES-XTS) of Flash memory. Prevents physical reading of firmware and secrets (Wi-Fi keys, certificates) in the event of theft of the box.
* **Secure Boot (V2) :** Verification of the RSA-3072 signature of the firmware at start-up via a hardware chain of trust (eFuses). Prevents unauthorised code from being executed.

### 2. Mises à jour Sécurisées (Secure OTA)
* **A/B Architecture (Rollback):** Use of a custom partition table (`partitions.csv`) with two application slots (`ota_0`, `ota_1`). If an update fails, the system automatically reverts to the previous version.
* **Digital Signature:** Each binary update is cryptographically signed before deployment. The ESP32 verifies this signature before writing to memory.

### 3. Confidentialité Réseau (Data Privacy)
* **HTTPS / TLS :** Encrypted communication between the ESP32 and the update server.
* **Certificate Pinning :** The ESP32 has the server's public certificate (`ca_cert.pem`) embedded in its firmware to prevent man-in-the-middle attacks.

---

## 📂 Structure du Projet

* **`main/`** : Application source code (Wi-Fi logic, OTA task, HTTPS configuration).
* **`secure_keys/`** : Private keys (RSA) for Secure Boot and Flash Encryption (never to be disclosed in production).
* **`ca_cert.pem` / `ca_key.pem`** : Certificates for the HTTPS server (local PKI).
* **`ota_server_https.py`** : Secure Python server for delivering updates.
* **`iot_security_manager.py`** : Utility script to automatically sign binaries after compilation.
* **`partitions.csv`** : Partitioning table defining the OTA and NVS areas.

---

## 🛠️ Installation and Prerequisites

### Prerequisites
* ESP-IDF v5.x (Test on v5.4.3)
* Python 3
* Development board ESP32-C6

### Configuration
1.  **Menuconfig :**
    ```bash
    idf.py menuconfig
    ```
    * *Security Features* -> Enable Flash Encryption & Secure Boot.
    * *Partition Table* -> Custom partition table (`partitions.csv`).
    * *Component config* -> ESP System Settings -> CPU Frequency (Set to 80MHz to avoid Brownout on USB power).

2.  **Key Generation :**
    The security keys were generated and burned into the eFuses during the initial initialisation.

---

## 🔄 Update Workflow (OTA)

To deploy a new firmware version :

1.  **Modification:** Change the code in `main/hello_world_main.c` (e.g., change the version number).
2.  **Compilation:**
```bash
idf.py build
```
3.  **Automatic Signing:**
    Run the management script that signs the binary and places it at the root of the server:
```bash
    python iot_security_manager.py
    ```
4.  **Starting the Server:**
```bash
python ota_server_https.py
```
5.  **Updating the ESP32:**
Restart the ESP32 (Reset). It will detect the new signed file, download it via HTTPS, and install it on the passive partition.

---

## ✅ Validation Tests

### Test 1: Protection against extraction (Flash Encryption)
An attempt to read the memory via `esptool` was made.
* **Command:** `esptool.py -p COMx read_flash 0 0x200000 dump.bin`
* **Result:** The `dump.bin` file contains random data (noise), making reverse engineering impossible.

### Test 2: Protection against injection (Anti-Tampering)
A valid binary file was manually corrupted (hexadecimal modification) to simulate pirated or corrupted firmware.
* **Result:** The ESP32 rejected the update with the error:
> `E (...) esp_https_ota: Mismatch chip id`
> `E (...) OTA_SECURE: Update failed`
The system remained stable on the previous version.

### Test 3: Confidentiality (HTTPS)
* **Result:** Access to the server via HTTP (`http://...`) is denied. Access via HTTPS is validated by the browser (padlock present), proving the encryption of the transport channel.

---

## ⚠️ Technical Notes & Limitations

* **Brownout / USB Power Supply:** Simultaneous activation of Wi-Fi, Flash writing and TLS encryption causes a high consumption spike. To avoid unexpected reboots (Brownout Reset) when developing on a standard USB port, the CPU frequency has been reduced to 80MHz and the size of the RX/TX buffers adjusted.
* **Certificates:** This project uses self-signed certificates for the local development environment.

---

**Author :** [Security TEAM]

**Date :** Janvier 2026
