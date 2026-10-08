import os
import time
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# LISTA MAESTRA DE USUARIOS ORIGINALES
CUENTAS_A_MONITOREAR = [
    "Lookmheewang", "sonyasarann", "panlyyy", "j_jayyna", "ginnynatnicha", "fay_riezz",
    "itscharlotty", "EWaraha", "yoko_apasra", "Cindy_Warat", "malisorn00", "srchafreen",
    "AngelssBecky", "_pundao", "thasornofficial", "shellybenda", "lena__lorena", "miunatshaa", "NamtanTipnaree",
    "filmracha", "Ciize155cm", "view_benyapa", "thasornorfficial", "beonnnie", "AppleLAPIS",
    "nurdesoraya", "phinyanech", "mable_siriwalee", "pangjiewr", "linglingsirilak", "ormmormm",
    "Nesamahmoodii", "daaddeaw1", "heidi_amanda_js", "janeeeyeh", "XZhae23153"
]

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot activo")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Servidor)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def enviar_a_discord(link, usuario):
    payload = {
        "content": f"**¡¡A CORRER QUE HAY CHISME!!** 👀 🚨 La cuenta @{usuario} acaba de subir un nuevo tweet. ✨ {link}"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception:
        pass

def bucle_monitoreo():
    ultimo_tweet_url = {}
    
    while True:
        for usuario in CUENTAS_A_MONITOREAR:
            try:
                # Cambiado a un lector alternativo que sí responde correctamente
                url_rss = f"https://privacydev.net{usuario}/rss"
                response = requests.get(url_rss, timeout=15)
                
                if response.status_code == 200 and "<item>" in response.text:
                    texto = response.text
                    inicio_link = texto.find("<link>") + 6
                    fin_link = texto.find("</link>")
                    link_actual = texto[inicio_link:fin_link].strip()
                    
                    if link_actual:
                        # Si el link viene de nitter, lo convertimos a link real de twitter para ti
                        link_actual = link_actual.replace("nitter.privacydev.net", "twitter.com")
                        
                        if usuario not in ultimo_tweet_url:
                            ultimo_tweet_url[usuario] = link_actual
                            continue
                            
                        if link_actual != ultimo_tweet_url[usuario]:
                            ultimo_tweet_url[usuario] = link_actual
                            enviar_a_discord(link_actual, usuario)
            except Exception:
                pass
        time.sleep(600)

if __name__ == "__main__":
    bucle_monitoreo()
