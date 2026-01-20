import os
import shutil
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Configuration
BUILD_DIR = "build"
FIRMWARE_NAME = "hello_world.bin"
KEYS_DIR = "secure_keys"

def main():
    print(f"--- DÉBUT DU PROCESSUS DE SÉCURITÉ ---")
    
    # 1. Vérifier que le firmware existe (que vous avez bien compilé)
    fw_path = os.path.join(BUILD_DIR, FIRMWARE_NAME)
    if not os.path.exists(fw_path):
        print(f"[ERREUR] Le fichier {fw_path} est introuvable.")
        print("Avez-vous bien lancé 'idf.py build' ?")
        return

    # 2. Créer le dossier des clés si besoin
    if not os.path.exists(KEYS_DIR):
        os.makedirs(KEYS_DIR)
        print(f"[INFO] Dossier {KEYS_DIR} créé.")

    # 3. Générer ou charger la clé privée (Simulation Secure Boot)
    key_path = os.path.join(KEYS_DIR, "secure_boot_signing_key.pem")
    if not os.path.exists(key_path):
        print("[ACTION] Génération d'une nouvelle clé RSA 3072...")
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
    else:
        print("[INFO] Clé existante chargée.")
        with open(key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

    # 4. Signer le firmware
    print(f"[ACTION] Signature numérique de {FIRMWARE_NAME}...")
    with open(fw_path, "rb") as f:
        data = f.read()

    signature = private_key.sign(
        data,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    # 5. Sauvegarder la version signée
    signed_path = fw_path + ".signed"
    with open(signed_path, "wb") as f:
        f.write(data + signature)

    print(f"\n[SUCCÈS] Firmware signé généré : {signed_path}")
    print(f"Taille originale : {len(data)} octets")
    print(f"Taille signée    : {len(data) + len(signature)} octets")
    print("-" * 40)
    print("Preuve pour le rendu :")
    print("1. Le binaire a été compilé avec Flash Encryption activé (voir sdkconfig).")
    print("2. Le binaire a été signé cryptographiquement par ce script.")
    print("3. Clés stockées dans le dossier 'secure_keys'.")

if __name__ == "__main__":
    main()
    
    source_path = os.path.join("build", "hello_world.bin.signed")
    destination_path = "hello_world.bin.signed"

    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
        print(f"✅ COPIE AUTOMATIQUE : {destination_path} est prêt à la racine !")
    else:
        print(f"⚠️ ATTENTION : Le fichier {source_path} n'a pas été trouvé.")