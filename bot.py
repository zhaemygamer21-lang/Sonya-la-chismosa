import os, time, requests, threading, re
from http.server import BaseHTTPRequestHandler, HTTPServer

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# TU LISTA MAESTRA DE FILTRADO PURIFICADA (ACTRICES Y PAREJAS GL)
KEYWORDS = [
    "Freen", "Sarocha", "Chankimha", "FreenBecky", "Becky", "Armstrong", "Lingling", "Sirilak", "Kwong",
    "Orm", "Kornnaphat", "Sethratanapong", "LingOrm", "Lena", "Lalina", "Schuett", "Miu", "Natsha",
    "Taechamongkalapiwat", "LenaMiu", "Faye", "Peraya", "Malisorn", "Atom", "Pariya", "Piyapanopas",
    "FayeAtom", "Lookmhee", "Punyapat", "Wangpongsathorn", "Sonya", "Saranphat", "Pedersen", "LMSY",
    "Namtan", "Tipnaree", "Weerawatnodom", "Film", "Rachanun", "Mahawan", "NamtanFilm", "Milk", "Pansa",
    "Vosbein", "Love", "Pattranite", "Limpatiyakorn", "MilkLove", "View", "Benyapa", "Jeenprasom", "Mim",
    "Rattanawadee", "Wongthong", "ViewMim", "Ginny", "Natnicha", "Pratipnatsiri", "Jayna", "Angelina",
    "Stevens", "GinnyJayna", "Engfa", "Waraha", "Charlotte", "Austin", "EngLot", "Apple", "Lapisara",
    "Intausmut", "Panthita", "AppleMim", "Nile", "Chanidapa", "Sommitthanakul", "Namwan", "Natchaya",
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
    "Oom", "Eisaya", "Hosuwan", "Bint", "Sireethorn", "Leearamwat", "Puinoon", "Warangsiri", "TanAdjusted",
    "Kanyaphat", "Na", "Nakhon", "FayMay", "Neko", "Jennie", "Lisa", "Jisoo", "Rosé", "BLACKPINK", "Mie",
    "Phattaranan", "Aya", "Orapan", "Kao", "Supassara", "Thanachart", "Jane", "Methika", "Ornstein", "Natt",
    "Pitcha", "Meo-Meow", "Jennis", "Tarwaan", "Kaew", "Spy", "Yipun", "Farida", "Bowkylion", "Pluto", 
    "Pluto The Series", "Pluto", "iqiyi", "iq.com"
]

# TUS 15 ENLACES PLANOS Y CANALES DE TRANSMISIÓN DE VIDEO
RutaChisme_1 = "https://daradaily.com"
RutaChisme_2 = "https://sanook.com"
RutaChisme_3 = "https://komchadluek.net"
RutaChisme_4 = "https://mydramalist.com"
RutaChisme_5 = "https://reddit.com"
RutaChisme_6 = "https://glflix.io"
RutaChisme_7 = "https://sapphicsignal.com"
RutaChisme_8 = "https://wetv.vip"
RutaChisme_9 = "https://gagaoolala.com"
RutaChisme_10 = "https://iq.com"
RutaChisme_11 = "https://oned.net"
RutaChisme_12 = "https://thaiupdate.info"
RutaChisme_13 = "https://glthai.com"
RutaChisme_14 = "https://glspotlight.com"

FUENTES_WEB = {
    "Daradaily (Chismes)": RutaChisme_1,
    "Sanook (Farandula Thai)": RutaChisme_2,
    "Komchadluek Entertainment": RutaChisme_3,
    "MyDramaList GL": RutaChisme_4,
    "Reddit r/GirlsLove": RutaChisme_5,
    "GL Flix Portal": RutaChisme_6,
    "Sapphic Signal": RutaChisme_7,
    "WeTV VIP GL": RutaChisme_8,
    "GagaOOLala Streaming": RutaChisme_9,
    "iQIYI Series": RutaChisme_10,
    "OneD Channel": RutaChisme_11,
    "Thai Update News": RutaChisme_12,
    "GLThai Portal": RutaChisme_13,
    "GL Spotlight Actresses": RutaChisme_14
}

FUENTES_YOUTUBE = {
    "Nine Stars Studios": "https://youtube.com",
    "GMMTV": "https://youtube.com",
    "Cindy Waratin": "https://youtube.com",
    "iQIYI Spanish": "https://youtube.com",
    "Yo Soy Fabiiii": "https://youtube.com",
    "SNUR Entertainment": "https://youtube.com",
    "Idol Factory": "https://youtube.com",
    "Ch3Plus": "https://youtube.com",
    "Change2561": "https://youtube.com",
    "Star Hunter Entertainment": "https://youtube.com",
    "Magui Lopez": "https://youtube.com",
    "Meeshdee GL": "https://youtube.com",
    "Grand TV": "https://youtube.com",
    "Studio Wabi Sabi": "https://youtube.com",
    "Fabel Entertainment": "https://youtube.com",
    "Jeff Satur": "https://youtube.com",
    "Bowkylion": "https://youtube.com",
    "Pun Is Always Happy": "https://youtube.com",
    "Proxie TH": "https://youtube.com",
    "Youngohm": "https://youtube.com"
}

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Sonya bot Activo")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(("0.0.0.0", port), Servidor).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def enviar_a_discord(link, titulo, resumen, fuente, imagen_url=None, es_youtube=False):
    if es_youtube:
        encabezado = "🍿🎥 **¡¡SALIÓ CAPÍTULO, REACCIÓN O MÚSICA NUEVA EN YOUTUBE!!**"
    elif any(x in fuente.lower() for x in ["iqiyi", "wetv", "oned", "gagaoolala", "glflix"]):
        encabezado = "🎬📱 **¡¡NUEVO EPISODIO O ESTRENO GL DISPONIBLE EN PLATAFORMA!!**"
    else:
        encabezado = "👀🚨 **¡¡A CORRER QUE HAY CHISME GL DE ÚLTIMA HORA!!**"
        
    payload = {
        "content": f"{encabezado}\n📌 **Fuente:** {fuente}",
        "embeds": [{
            "title": titulo if titulo else "Novedad en el catalogo GL",
            "description": resumen if resumen else "Haz clic en el enlace para ver los detalles multimedia de tus actrices favoritas.",
            "url": link,
            "color": 15418782
        }]
    }
    if imagen_url and imagen_url.startswith("http"):
        payload["embeds"]["image"] = {"url": imagen_url}
    try:
        requests.post(WEBHOOK_URL, json=payload, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except:
        pass

def analizar_pagina(html_puro, url_base):
    try:
        foto = None
        img_match = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html_puro)
        if not img_match:
            img_match = re.search(r'<img[^>]+src="([^"]+)"', html_puro)
        
        if img_match:
            foto = img_match.group(1).strip()
            if foto.startswith("//"): foto = "https:" + foto
            if not foto.startswith("http"): foto = url_base.rstrip('/') + "/" + foto.lstrip('/')

        bloques = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)</a>', html_puro)
        for link, contenido in bloques:
            if not link.startswith("http") and link.startswith("/"):
                link = url_base.rstrip('/') + link
            if not link.startswith("http"): continue
            
            texto = re.sub(r'<[^>]+>', ' ', contenido)
            texto = re.sub(r'\s+', ' ', texto).strip()
            
            if len(texto) > 30 and not any(x in texto.lower() for x in ["términos", "privacidad", "cookies", "contacto", "condiciones"]):
                titulo = texto[:90]
                resumen = texto[90:340] if len(texto) > 90 else "Haz clic en el enlace para conocer los detalles multimedia en la plataforma oficial."
                return [(link, titulo, resumen, foto)]
    except:
        pass
    return None
def analizar_youtube(xml_puro):
    try:
        video_id = re.search(r'<yt:videoId>([^<]+)</yt:videoId>', xml_puro)
        title = re.search(r'<title>([^<]+)</title>', xml_puro)
        if video_id and title:
            v_id = video_id.group(1).strip()
            link = f"https://youtube.com{v_id}"
            foto = f"https://youtube.com{v_id}/maxresdefault.jpg"
            titulo_video = title.group(1).strip()
            resumen_video = "¡Canal oficial actualizado! Ya se encuentra disponible el nuevo video, episodio completo, cancion o reaccion de la farandula GL."
            return [(link, titulo_video, resumen_video, foto)]
    except:
        pass
    return None

def coincide_con_actrices(texto_a_revisar):
    t = texto_a_revisar.lower()
    return any(kw.lower() in t for kw in KEYWORDS)

def bucle_monitoreo():
    ultimas_noticias = {}
    print("Iniciando escaneo masivo sáfico (Web + 20 YouTube)...")
    while True:
        # 1. Monitoreo de Sitios Web y Plataformas
        for nombre_fuente, url in FUENTES_WEB.items():
            try:
                res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                if res.status_code != 200: continue
                noticias = analizar_pagina(res.text, url)
                if noticias:
                    for link, titulo, resumen, foto in noticias:
                        if nombre_fuente not in ultimas_noticias or link != ultimas_noticias[nombre_fuente]:
                            ultimas_noticias[nombre_fuente] = link
                            if any(x in url for x in ["reddit", "glflix", "sapphicsignal", "glthai", "glspotlight"]) or coincide_con_actrices(titulo) or coincide_con_actrices(resumen):
                                enviar_a_discord(link, titulo, resumen, nombre_fuente, foto, es_youtube=False)
                                time.sleep(2)
            except: pass

        # 2. Monitoreo Inmediato de los 20 canales de YouTube
        for nombre_canal, url_feed in FUENTES_YOUTUBE.items():
            try:
                res = requests.get(url_feed, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                if res.status_code != 200: continue
                video = analizar_youtube(res.text)
                if video:
                    for link, titulo, resumen, foto in video:
                        if nombre_canal not in ultimas_noticias or link != ultimas_noticias[nombre_canal]:
                            ultimas_noticias[nombre_canal] = link
                            enviar_a_discord(link, titulo, resumen, nombre_canal, foto, es_youtube=True)
                            time.sleep(2)
            except: pass

        time.sleep(450) # Escaneo continuo optimizado

if __name__ == "__main__":
    bucle_monitoreo()
