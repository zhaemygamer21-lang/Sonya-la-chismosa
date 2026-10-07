import os
import time
import threading
import requests
from flask import Flask
from ntscraper import Nitter

# 1. Configuración de la mini aplicación Web para mantener vivo Render
app = Flask(__name__)

@app.route('/')
def home():
    return "El bot monitor de Twitter está activo y corriendo.", 200

# 2. Configuración de Cuentas y Webhook
# Reemplaza con los nombres de usuario exactos de las cuentas de Twitter que quieres seguir
CUENTAS_A_MONITOREAR = ["Panlyyy","j_jayyna","ginnynatnocha","fay_riezz","itscharlotty","EWaraha","Yoko_apasra","cindy_Waratin","malisorn00","srchafraeen","AngelssBecky","PundaoSpace","shellybenda","lena__lorena","miunatshaa","namtanTipnaree","filmracha","Ciize155cm","view_benyapa","thasornofficial","beonnnie","AppleLAPIS","nurdesoraya","phinyanech","mable_siriwalee","pangjiewr","linglingsirilak","ormmormm"]

def enviar_a_discord(link_tweet):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        print("Error: No se encontró la variable WEBHOOK_URL en Render.")
        return

    # Truco mágico: Reemplaza x.com o twitter.com por fxtwitter.com
    # Esto obliga a Discord a cargar las FOTOS y videos automáticamente
    link_corregido = link_tweet.replace("twitter.com", "fxtwitter.com").replace("x.com", "fxtwitter.com")

    payload = {
        "content": f"📢 **¡Nueva publicación detectada!**\n{link_corregido}"
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("Publicación enviada exitosamente a Discord con previsualización de foto.")
        else:
            print(f"Error al enviar a Discord: {response.status_code}")
    except Exception as e:
        print(f"Error de red al conectar con Discord: {e}")

# 3. Lógica del bucle de monitoreo
def bucle_monitoreo():
    scraper = Nitter()
    ultimo_tweet_url = {}

    print("Iniciando el escaneo de Twitter...")

    while True:
        for usuario in CUENTAS_A_MONITOREAR:
            try:
                # Buscamos los últimos 2 tweets del usuario de forma gratuita sin API keys
                datos = scraper.get_tweets(usuario, mode='user', number=2)
                
                if datos and 'tweets' in datos and len(datos['tweets']) > 0:
                    # El primer tweet de la lista es el más reciente
                    ultimo_tweet = datos['tweets'][0]
                    link_actual = ultimo_tweet.get('link')

                    if link_actual:
                        # Si es la primera vez que lee la cuenta, guarda el tweet actual para no saturar Discord con tweets viejos
                        if usuario not in ultimo_tweet_url:
                            ultimo_tweet_url[usuario] = link_actual
                            print(f"Cuenta @{usuario} cargada. Esperando nuevos tweets...")
                            continue

                        # Si el link cambió, significa que hay una nueva publicación
                        if link_actual != ultimo_tweet_url[usuario]:
                            print(f"¡Nuevo tweet detectado para @{usuario}!")
                            ultimo_tweet_url[usuario] = link_actual
                            enviar_a_discord(link_actual)
            
            except Exception as e:
                print(f"Error al revisar la cuenta de @{usuario}: {e}")
        
        # Espera 10 minutos (600 segundos) entre revisiones para evitar que bloqueen el script
        time.sleep(600)

# Lanzamos el bucle en un hilo separado para que Flask pueda responder a Render en paralelo
threading.Thread(target=bucle_monitoreo, daemon=True).start()
