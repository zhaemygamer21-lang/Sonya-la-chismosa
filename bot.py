import os
import time
import threading
import requests
from flask import Flask

# 1. Configuración de la mini aplicación Web para mantener vivo Render
app = Flask(__name__)

@app.route('/')
def home():
    return "El bot monitor de Twitter está activo y corriendo.", 200

# 2. Configuración de Cuentas y Webhook
CUENTAS_A_MONITOREAR = ["panlyyy", "j_jayyna", "ginnynatnicha", "fay_riezz", 
    "itscharlotty", "EWaraha", "yoko_apasra", "Cindy_Waratin", 
    "maliisorn00", "srchafreen", "AngelssBecky", "_pundao", 
    "shellybenda", "lena__lorena", "miunatshaa", "NamtanTipnaree", 
    "filmracha", "Ciize155cm", "view_benyapa", "thasornofficial", 
    "beonnnie", "AppleLAPIS", "nurdesoraya", "phinyanech", 
    "mable_siriwalee", "pangjiewr", "linglingsirikak", "ormmormm",
    "Nesamahmoodii","daaddeaw1","heidi_amandajs","janeeeyeh","XZhae23153"]

def enviar_a_discord(link_tweet, usuario):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        print("Error: No se encontró la variable WEBHOOK_URL en Render.")
        return

    # Truco de fxtwitter para cargar FOTOS y videos automáticamente
    link_corregido = link_tweet.replace("twitter.com", "fxtwitter.com").replace("x.com", "fxtwitter.com")

    # ==========================================
    # MODIFICA AQUÍ EL MENSAJE SI DESEAS OTRO ESTILO:
    payload = {
            "content": f" **A CORRER QUE HAY CHISME!** La cuenta @{usuario} acaba de subir un nuevo tweet. {link_corregido}"
    }

    # ==========================================

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(f"Publicación de @{usuario} enviada exitosamente a Discord.")
        else:
            print(f"Error al enviar a Discord: {response.status_code}")
    except Exception as e:
        print(f"Error de red al conectar con Discord: {e}")

# 3. Lógica del bucle de monitoreo
def bucle_monitoreo():
    ultimo_tweet_url = {}
    print("Iniciando el escaneo de Twitter...")
    
    while True:
        for usuario in CUENTAS_A_MONITOREAR:
            try:
                # Usamos una instancia RSS funcional para extraer tweets públicos
                url_rss = f"https://privacydev.net{usuario}/rss"
                response = requests.get(url_rss, timeout=15)
                
                if response.status_code == 200 and "<item>" in response.text:
                    texto = response.text
                    inicio_link = texto.find("<link>") + 6
                    fin_link = texto.find("</link>")
                    link_actual = texto[inicio_link:fin_link].strip()
                    
                    if link_actual:
                        if usuario not in ultimo_tweet_url:
                            ultimo_tweet_url[usuario] = link_actual
                            print(f"Cuenta @{usuario} cargada correctamente.")
                            continue
                        
                        if link_actual != ultimo_tweet_url[usuario]:
                            ultimo_tweet_url[usuario] = link_actual
                            print(f"¡Nuevo tweet detectado para @{usuario}!")
                            enviar_a_discord(link_actual, usuario)
                else:
                    print(f"Saltando temporalmente a @{usuario} debido a una restricción de Twitter.")
            
            except Exception as e:
                print(f"Error escaneando a @{usuario}: {e}")
        
        # Espera 10 minutos antes de volver a revisar
        time.sleep(600)

        
        # Espera 10 minutos entre revisiones
        time.sleep(600)

# Lanzamos el bucle en un hilo separado
threading.Thread(target=bucle_monitoreo, daemon=True).start()
