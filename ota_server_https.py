import http.server
import ssl
import os

# Configuration
ADDR = "0.0.0.0"
PORT = 8070

# Vérification que les clés sont bien là
if not os.path.exists("ca_cert.pem") or not os.path.exists("ca_key.pem"):
    print("❌ ERREUR : Les fichiers ca_cert.pem et ca_key.pem sont introuvables !")
    exit()

# Création du serveur
server_address = (ADDR, PORT)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Activation du cadenas SSL (HTTPS)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="ca_cert.pem", keyfile="ca_key.pem")
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"🔒 SERVEUR SÉCURISÉ EN LIGNE !")
print(f"👉 https://172.20.10.3:{PORT}/ (Notez le 's' de https)")
print("---------------------------------------------------")

httpd.serve_forever()