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

# TUS 15 ENLACES RSS OFICIALES COPIADOS EXACTAMENTE LETRA POR LETRA
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
RutaChisme_15 = "https://reddit.com"

FUENTES_RSS = {
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
    "GL Spotlight Actresses": RutaChisme_14,
    "Reddit r/ThaiGL": RutaChisme_15
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

def enviar_a_discord(link, titulo, resumen, fuente, multimedia_url=None):
    payload = {
        "content": f"**¡¡A CORRER QUE HAY CHISME GL Y ACTUALIZACIÓN EN VIVO!! 👀 🚨**\n📌 **Fuente:** {fuente}",
        "embeds": [{
            "title": titulo if titulo else "Novedad en el catalogo GL",
            "description": resumen if resumen else "Haz clic en el enlace para ver los detalles multimedia de tus actrices favoritas.",
            "url": link,
            "color": 15418782
        }]
    }
    if multimedia_url and multimedia_url.startswith("http"):
        payload["embeds"][0]["image"] = {"url": multimedia_url}
    try:
        requests.post(WEBHOOK_URL, json=payload, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except:
        pass

def extraer_imagen(item_texto):
    for patron in [r'<media:content[^>]*url="([^"]+)"', r'<enclosure[^>]*url="([^"]+)"', r'<img[^>]*src="([^"]+)"']:
        match = re.search(patron, item_texto)
        if match: return match.group(1).strip()
    return None

def coincide_con_actrices(texto_a_revisar):
    t = texto_a_revisar.lower()
    return any(kw.lower() in t for kw in KEYWORDS)

def bucle_monitoreo():
    ultimas_noticias = {}
    print("Iniciando escaneo real RSS/XML sáfico con fotos...")
    while True:
        for nombre_fuente, url_rss in FUENTES_RSS.items():
            try:
                res = requests.get(url_rss, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=15)
                if res.status_code != 200 or "<item>" not in res.text: continue
                
                texto = res.text
                primer_item = texto[texto.find("<item>"):texto.find("</item>")+7]
                
                link = primer_item[primer_item.find("<link>")+6:primer_item.find("</link>")].strip().replace("<![CDATA[", "").replace("]]>", "")
                title = primer_item[primer_item.find("<title>")+7:primer_item.find("</title>")].strip().replace("<![CDATA[", "").replace("]]>", "")
                
                desc_inicio = primer_item.find("<description>") + 13
                desc_fin = primer_item.find("</description>")
                resumen = primer_item[desc_inicio:desc_fin].strip().replace("<![CDATA[", "").replace("]]>", "")
                resumen = re.sub(r'<[^>]+>', '', resumen)[:250] + "..."
                
                foto = extraer_imagen(primer_item)
                
                if link and (nombre_fuente not in ultimas_noticias or link != ultimas_noticias[nombre_fuente]):
                    ultimas_noticias[nombre_fuente] = link
                    
                    if any(x in url_rss for x in ["reddit", "glflix", "sapphicsignal", "glthai", "glspotlight"]) or coincide_con_actrices(title) or coincide_con_actrices(resumen):
                        enviar_a_discord(link, title, resumen, nombre_fuente, foto)
                        time.sleep(2)
            except:
                pass
        time.sleep(600) # Escanea las 15 plataformas cada 10 minutos

if __name__ == "__main__":
    bucle_monitoreo()
