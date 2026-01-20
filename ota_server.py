import http.server
import socketserver

# --- CONFIGURATION FORCÉE ---
PORT = 8070
# On force l'IP que vous avez trouvée dans ipconfig (Carte Wi-Fi)
IP_ADRESS = "192.168.1.200" 
DIRECTORY = "build"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"\n--- SERVEUR OTA SÉCURISÉ (WIFI) ---")
print(f"L'ESP32 doit se connecter à :")
print(f"👉 http://{IP_ADRESS}:{PORT}/hello_world.bin.signed")
print(f"-----------------------------------")

# On lie le serveur spécifiquement à cette carte réseau
with socketserver.TCPServer((IP_ADRESS, PORT), Handler) as httpd:
    print(f"Serveur écoute UNIQUEMENT sur {IP_ADRESS}:{PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt.")