import os
import time
import requests
import threading
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# TU LISTA MAESTRA DE FILTRADO (Nombres, Shipps y Agencias)
KEYWORDS = [
    "Freen", "Sarocha", "Chankimha", "FreenBecky", "Becky", "Armstrong", "Lingling", "Sirilak", "Kwong",
    "Orm", "Kornnaphat", "Sethratanapong", "LingOrm", "Lena", "Lalina", "Schuett", "Miu", "Natsha",
    "Taechamongkalapiwat", "LenaMiu", "Faye", "Peraya", "Malisorn", "Atom", "Pariya", "Piyapanopas",
    "FayeAtom", "Lookmhee", "Punyapat", "Wangpongsathorn", "Sonya", "Saranphat", "Pedersen", "LMSY",
    "Namtan", "Tipnaree", "Weerawatnodom", "Film", "Rachanun", "Mahawan", "NamtanFilm", "Milk", "Pansa",
    "Vosbein", "Love", "Pattranite", "Limpatiyakorn", "MilkLove", "View", "Benyapa", "Jeenprasom", "Mim",
    "Rattanawadee", "Wongthong", "ViewMim", "Ginny", "Natnicha", "Pratipnatsiri", "Jayna", "Angelina",
    "Stevens", "GinnyJayna", "Engfa", "Waraha", "Charlotte", "Austin", "EngLot", "Apple", "Lapisara",
    "Intarasut", "Panthita", "AppleMim", "Nile", "Chanidapa", "Sommitthanakul", "Namwan", "Natchaya",
    "Vongbut", "NileNamwan", "Lilly", "Ladapa", "Thongkham", "Belle", "Jiratchaya", "Kittavornsakul",
    "LillyBelle", "Namneung", "Milin", "Dokthian", "Noey", "Kanteera", "Wadcharathadsanakul", "NamneungNoey",
    "Aphichaya", "Kamnoetsirikun", "Mersedes", "Kanyawee", "Songmuang", "AtomMersedes", "Bam", "Saralee",
    "Prasitdumrong", "Baipor", "Thitiya", "Jirapornsilp", "BamBamBaipor", "Tan", "Duangkaew", "Piyaoui",
    "Yada", "Narilya", "Gulmongkolpech", "TanYada", "June", "Nannirin", "Nippitthanon", "Enjoy", "Thidarat",
    "Chareonchaichana", "JuneEnjoy", "Fah", "Rachaya", "Nirinsawad", "Bell", "Patchamon", "Punyapidthaya",
    "FahBell", "Ormsin", "Supitcha", "Limsommut", "Folk", "Sutima", "Kruakitticharoen", "OrmsinFolk", "Anda",
    "Anunta", "Teavirat", "Lookkaew", "Kamollak", "Sangsubsin", "AndaLookkaew", "Noon", "Thunyaphat",
    "Inyawilert", "Praewa", "Putticha", "Boonyamas", "NoonPraewa", "Tungpang", "Pattaravadee", "Laosa",
    "Jessie", "Rattikarn", "TungpangJessie", "Tangkwa", "Phinyanech", "Nur", "Disraya", "Techapaibun",
    "TangkwaNur", "Shelly", "Phetsai", "Chanrueng-Benda", "Pundao", "Panyabaramee", "ShellyPundao", "Garn",
    "Nuttacha", "Mimie", "Wanthong", "GarnMimie", "May", "Yada", "Watcharamethakul", "MayNita", "Nita",
    "Anipan", "Chalermburanawong", "Minnie", "Thanawin", "Pannie", "MinniePannie", "Bommy", "Nontarat",
    "Netipoh", "Ning", "Nicharut", "Sakkasemrut", "BommyNing", "Meena", "Rina", "Chayakorn", "Aoom",
    "Thaweeporn", "Phingchamrat", "MeenaAoom", "Yuyee", "Alisa", "Intusmith", "Mint", "Mintita", "Wattanakul",
    "Care", "Chattarika", "Sittiprom", "Prigkhing", "Sureeyares", "Yakares", "Ratchayangkanont",
    "Bhapat", "Ahchariyasripong", "Charada", "Imraporn", "Chutimon", "Prasanwan", "Evarin", "Atichaichaowakit",
    "Plaifa", "Fay", "Apisara", "Jeanie", "Ornlin", "BamBam", "Thitaree", "Ciize", "Rutricha", "Phapakithi",
    "Emi", "Thasorn", "Klinnium", "Bonnie", "Pattraphus", "Borattasuwan", "Jan", "Ployshompoo", "Supasap",
    "JingJing", "Yu", "Kapook", "Ploynira", "Hiruntaveesin", "Jaoying", "Chawalitporn", "Pusomjit", "Mewnich",
    "Nannaphas", "Lertvilai", "Pahn", "Pathitta", "Pornsukchai", "Fond", "Nattanicha", "Chantaravareelekha",
    "Oom", "Eisaya", "Hosuwan", "Bint", "Sireethorn", "Leearamwat", "Puinoon", "Warangsiri", "Tanajarusworaphat",
    "Kanyaphat", "Na", "Nakhon", "FayMay", "Neko", "Jennie", "Lisa", "Jisoo", "Rosé", "BLACKPINK", "Mie",
    "Phattaranan", "Aya", "Orapan", "Kao", "Supassara", "Thanachart", "Jane", "Methika", "Ornstein", "Natt",
    "Pitcha", "Meo-Meow", "Jennis", "Tarwaan", "Kaew", "Spy", "Yipun", "FRT", "Star Hunter", "North Star",
    "GMMTV", "CHANGE2561", "Channel 3", "IDOLFACTORY", "MGI", "Beyond", "MeMindY", "VelCurve", "MONOMAX",
    "S.NUR", "Fabel", "Motion Minds", "Kongthup", "SiamSi", "WanneeWandee", "Conversation Thailand",
    "faridasrd", "Farida", "Solenn", "4EVE", "PP Krit", "Billkin", "Bowkylion", "Nont Tanont"
]

# RED DE MONITOREO TOTALMENTE ACTUALIZADA (7 PORTALES + 11 CANALES DE YOUTUBE)
FUENTES_RSS = {
    # Portales de Noticias, Chismes y Foros Internacionales
    "Daradaily (Chismes Thai)": "https://daradaily.com",
    "Sanook (Fotos Actrices)": "https://sanook.com",
    "Komchadluek (Prensa Farándula)": "https://komchadluek.net",
    "MyDramaList (Noticias de Series GL)": "https://mydramalist.com",
    "Reddit r/GirlsLove (Fotos/Fans)": "https://reddit.com",
    "Reddit r/ThaiBL (Comunidad General)": "https://reddit.com",
    "Reddit r/kpop (BLACKPINK Updates)": "https://reddit.com",
    
    # Canales de YouTube de Productoras, Canales Propios y Prensa Thai
    "YouTube GMMTV Oficial": "https://youtube.com",
    "YouTube IDOLFACTORY": "https://youtube.com",
    "YouTube MGI Grand TV": "https://youtube.com",
    "YouTube NineEntertain (Prensa)": "https://youtube.com",
    "YouTube News Plus (Entrevistas)": "https://youtube.com",
    "YouTube Becky Armstrong Official": "https://youtube.com",
    "YouTube Solenn Entertainment": "https://youtube.com",
    
    # Canales de Fans en Español e Industria de Música T-Pop Populares
    "YouTube Yulirvi GL": "https://youtube.com",
    "YouTube Cindy Waratin": "https://youtube.com",
    "YouTube T-POP Stage Show (Música)": "https://youtube.com",
    "YouTube 4EVE Official (Grupo Pop)": "https://youtube.com"
}

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot Variedad Farandula Activo")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Servidor)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def enviar_a_discord(link, titulo, fuente, imagen_url=None):
    if "YouTube" in fuente:
        prefix = "🚨 ¡¡SALIÓ CAPÍTULO O VIDEO NUEVO!! 🎬🍿"
    else:
        prefix = "¡¡A CORRER QUE HAY CHISME!! 👀 🚨"

    payload = {
        "content": f"**{prefix}**\n\n📢 **Fuente:** {fuente}\n📌 **Título:** {titulo}\n\n✨ Enlace directo:\n{link}"
    }
    
    if imagen_url:
        payload["embeds"] = [{"image": {"url": imagen_url}}]

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        requests.post(WEBHOOK_URL, json=payload, headers=headers, timeout=10)
    except Exception:
        pass

def extraer_imagen(item_texto):
    try:
        url_match = re.search(r'<media:content[^>]*url="([^"]+)"', item_texto)
        if not url_match:
            url_match = re.search(r'<enclosure[^>]*url="([^"]+)"', item_texto)
        if not url_match:
            url_match = re.search(r'<img[^>]*src="([^"]+)"', item_texto)
        if url_match:
            return url_match.group(1).strip()
    except Exception:
        pass
    return None

def coincide_con_actrices(texto_a_revisar):
    texto_minusculas = texto_a_revisar.lower()
    # BUCLE DE MONITOREO TOTALMENTE PLANO Y COMPACTO
def bucle_monitoreo():
    ultimas_noticias = {}
    print("Iniciando escaneo masivo multi-plataforma...")
    
    while True:
        for nombre_fuente, url_rss in FUENTES_RSS.items():
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url_rss, headers=headers, timeout=15)
                if response.status_code != 200 or "<item>" not in response.text:
                    continue
                    
                texto = response.text
                primer_item = texto[texto.find("<item>"):texto.find("</item>")+7]
                
                # Extraer enlace de forma directa
                inicio_link = primer_item.find("<link>") + 6
                fin_link = primer_item.find("</link>")
                link_actual = primer_item[inicio_link:fin_link].strip().replace("<![CDATA[", "").replace("]]>", "")
                
                # Extraer título de forma directa
                inicio_title = primer_item.find("<title>") + 7
                fin_title = primer_item.find("</title>")
                titulo_actual = primer_item[inicio_title:fin_title].strip().replace("<![CDATA[", "").replace("]]>", "")
                
                foto_actual = extraer_imagen(primer_item)
                
                if not link_actual:
                    continue
                    
                if nombre_fuente not in ultimas_noticias:
                    ultimas_noticias[nombre_fuente] = link_actual
                    continue
                    
                if link_actual != ultimas_noticias[nombre_fuente]:
                    ultimas_noticias[nombre_fuente] = link_actual
                    if coincide_con_actrices(titulo_actual):
                        enviar_a_discord(link_actual, titulo_actual, nombre_fuente, foto_actual)
            except Exception:
                pass
        time.sleep(600)

if __name__ == "__main__":
    bucle_monitoreo()
