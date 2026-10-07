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
CUENTAS_A_MONITOREAR = [
    "Panlyyy", "_I_jayyna", "ginnynatnocha", "fay_tlezz", 
    "itscharlotty", "Emaraha", "Yoko_apasra", "cindy_maratin", 
    "maliisorn00", "mrchrafawn", "Angelsabecky", "PundaoSpace", 
    "shellybenda", "lena__lorena", "miunatshaa", "nantantipartree", 
    "filmracha", "Ciize155cm", "view_benyapa", "thasorn_official", 
    "beonnnnie", "AppleLAPIS", "anurdesoraya", "phinyanech", 
    "mable_siriwatee", "apangjiew", "alinglingsirikak", "dormmorm"
]

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
        "content": f"🔥 **¡A CORRER QUE HAY CHISME!** 👀\n\n📢 La cuenta **@{usuario}** acaba de subir un nuevo tweet. Míralo aquí:\n👉 {link_corregido}"
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
    scraper = Nitter()
    ultimo_tweet_url = {}

    print("Iniciando el escaneo de Twitter...")

    while True:
        for usuario in CUENTAS_A_MONITOREAR:
            try:
                # Buscamos los últimos tweets
                datos = scraper.get_tweets(usuario, mode='user', number=2)
                
                if datos and 'tweets' in datos and isinstance(datos['tweets'], list) and len(datos['tweets']) > 0:
                    ultimo_tweet = datos['tweets'][0]
                    link_actual = ultimo_tweet.get('link')

                    if link_actual:
                        if usuario not in ultimo_tweet_url:
                            ultimo_tweet_url[usuario] = link_actual
                            print(f"Cuenta @{usuario} cargada correctamente.")
                            continue

                        if link_actual != ultimo_tweet_url[usuario]:
                            print(f"¡Nuevo tweet detectado para @{usuario}!")
                            ultimo_tweet_url[usuario] = link_actual
                            # Le pasamos el link y el nombre del usuario a la función
                            enviar_a_discord(link_actual, usuario)
                else:
                    print(f"La cuenta @{usuario} no tiene tweets públicos o está protegida por ahora.")
            
            except Exception as e:
                print(f"Saltando temporalmente a @{usuario} debido a una restricción de Twitter.")
        
        # Espera 10 minutos entre revisiones
        time.sleep(600)

# Lanzamos el bucle en un hilo separado
threading.Thread(target=bucle_monitoreo, daemon=True).start()
