import os, time, requests, threading, re
from http.server import BaseHTTPRequestHandler, HTTPServer

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# LISTA MAESTRA DE FILTRADO REINTEGRADA Y EXPANDIDA (100% GL)
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
    "Pitcha", "Meo-Meow", "Jennis", "Tarwaan", "Kaew", "Spy", "Yipun", "FRT", "Star Hunter", "North Star",
    "GMMTV", "CHANGE2561", "Channel 3", "IDOLFACTORY", "MGI", "Beyond", "MeMindY", "VelCurve", "MONOMAX",
    "S.NUR", "Fabel", "Motion Minds", "Kongthup", "SiamSi", "WanneeWandee", "Conversation Thailand",
    "faridasrd", "Farida", "Solenn", "4EVE", "PP Krit", "Billkin", "Bowkylion", "Nont Tanont", "Pluto", 
    "Pluto The Series", "iqiyi", "iq.com", "North Star Entertainment", "Change2561 & N Star Studios", 
    "GagaOOLala", "WeTV", "WiTV", "OneD GL Spotlight", "Sapphic Signal GL Flix"
]

# FUENTES MULTI-PLATAFORMA REVISADAS CON SUS ENLACES RSS OFICIALES COMPLETOS
FUENTES_RSS = {
    "Daradaily (Chismes Thai)": "https://daradaily.com",
    "Sanook (Fotos Actrices)": "https://sanook.com",
    "Komchadluek (Prensa Farandula)": "https://komchadluek.net",
    "MyDramaList (Noticias de Series GL)": "https://mydramalist.com",
    "Reddit r/GirlsLove (Contenido de Fans - 24/7 ACTIVO)": "https://reddit.com",
    "Reddit r/kpop (BLACKPINK Updates)": "https://reddit.com",
    "YouTube GMMTV Oficial": "https://youtube.com",
    "YouTube IDOLFACTORY": "https://youtube.com",
    "YouTube MGI Grand TV": "https://youtube.com",
    "YouTube NineEntertain (Prensa)": "https://youtube.com",
    "YouTube News Plus (Entrevistas)": "https://youtube.com",
    "YouTube Becky Armstrong Official": "https://youtube.com",
    "YouTube Solenn Entertainment": "https://youtube.com",
    "YouTube Yulirvi GL": "https://youtube.com",
    "YouTube Cindy Waratin": "https://youtube.com",
    "YouTube T-POP Stage Show": "https://youtube.com",
    "YouTube 4EVE Official": "https://youtube.com",
    "YouTube Channel 3 Oficial": "https://youtube.com",
    "YouTube iQIYI Thailand": "https://youtube.com",
    "YouTube iQIYI Spanish": "https://youtube.com"
}

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot GL Hibrido Activo")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Servidor)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def enviar_a_discord(link, titulo, fuente, imagen_url=None):
    if "iQIYI" in fuente:
        prefix = "🚨 ¡¡NUEVO EPISODIO O ADELANTO GL EN iQIYI!! 🎬📱"
    elif "YouTube" in fuente:
        prefix = "🚨 ¡¡SALIÓ CAPÍTULO O VIDEO NUEVO GL!! 🎬🍿"
    else:
        prefix = "¡¡A CORRER QUE HAY CHISME GL!! 👀 🚨"
    payload = {"content": f"**{prefix}** - Fuente: {fuente} - Titulo: {titulo} - Enlace directo: {link}"}
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
    for kw in KEYWORDS:
        if kw.lower() in texto_minusculas:
            return True
    return False

def bucle_monitoreo():
    ultimas_noticias = {}
    print("Iniciando escaneo 100% sáfico...")
    while True:
        for nombre_fuente, url_rss in FUENTES_RSS.items():
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url_rss, headers=headers, timeout=15)
                if response.status_code != 200 or "<item>" not in response.text:
                    continue
                texto = response.text
                primer_item = texto[texto.find("<item>"):texto.find("</item>")+7]
                inicio_link = primer_item.find("<link>") + 6
                fin_link = primer_item.find("</link>")
                link_actual = primer_item[inicio_link:fin_link].strip().replace("<![CDATA[", "").replace("]]>", "")
                inicio_title = primer_item.find("<title>") + 7
                fin_title = primer_item.find("</title>")
                titulo_actual = primer_item[inicio_title:fin_title].strip().replace("<![CDATA[", "").replace("]]>", "")
                foto_actual = extraer_imagen(primer_item)
                if link_actual:
                    if nombre_fuente not in ultimas_noticias or link_actual != ultimas_noticias[nombre_fuente]:
                        ultimas_noticias[nombre_fuente] = link_actual
                        if "r/GirlsLove" in nombre_fuente or coincide_con_actrices(titulo_actual):
                            enviar_a_discord(link_actual, titulo_actual, nombre_fuente, foto_actual)
                            time.sleep(2)
            except Exception:
                pass
        time.sleep(600)

def iniciar_sistema():
    bucle_monitoreo()

if __name__ == '__main__':
    iniciar_sistema()
