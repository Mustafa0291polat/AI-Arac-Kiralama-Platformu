import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
client = None
if API_KEY:
    client = OpenAI(api_key=API_KEY)


FUEL_TYPES = ["Benzinli", "Benzin & LPG", "Dizel", "Hibrit", "Elektrikli"]
TRANSMISSION_TYPES = ["Manuel", "Otomatik"]
BODY_TYPES = ["Cabrio", "Coupe", "Coupe 4 kapı", "Hatchback 3 kapı", "Hatchback 5 kapı", "Sedan", "Station Wagon", "MPV", "Roadster"]
POWER_RANGES = ["50 HP'ye kadar", "51 - 75 HP", "76 - 100 HP", "101 - 125 HP", "126 - 150 HP", "151 - 175 HP", "176 - 200 HP", "201 - 225 HP", "226 - 250 HP", "251 - 275 HP", "276 - 300 HP", "301 - 325 HP", "326 - 350 HP", "351 - 375 HP", "376 - 400 HP", "401 - 425 HP", "426 - 450 HP", "451 - 475 HP", "476 - 500 HP", "501 - 525 HP", "526 - 550 HP", "551 - 575 HP", "576 - 600 HP", "601 HP ve üzeri"]
ENGINE_SIZES = ["1300 cm3' e kadar", "1301 - 1600 cm3", "1601 - 1800 cm3", "1801 - 2000 cm3", "2001 - 2500 cm3", "2501 - 3000 cm3", "3001 - 3500 cm3", "3501 - 4000 cm3", "4001 - 4500 cm3", "4501 - 5000 cm3", "5001 - 5500 cm3", "5501 - 6000 cm3", "6001 cm3 ve üzeri"]
DRIVE_TYPES = ["Önden Çekiş", "Arkadan İtiş", "4WD (Sürekli)", "AWD (Elektronik)"]
COLORS = ["Bej", "Beyaz", "Bordo", "Füme", "Gri", "Gümüş Gri", "Kahverengi", "Kırmızı", "Lacivert", "Mavi", "Mor", "Pembe", "Sarı", "Siyah", "Şampanya", "Turkuaz", "Turuncu", "Yeşil"]


OFFROAD_TERMS = [] 

DEFAULT_FILTER = {
    "city": None,
    "district": None,
    "price_min": 0,
    "price_max": 10000000,
    "year_min": 1970,
    "year_max": 2030,
    "fuel_type": [],
    "transmission": [],
    "km_min": 0,
    "km_max": 9999999,
    "body_type": [],
    "power_range": [],
    "engine_size": [],
    "drive_type": [],
    "color": [],
    "warranty": None,
    "heavy_damage": None,
    "seller_type": None,
    "available": "Kiralık",
}


SYSTEM_PROMPT = f"""Sen bir araç kiralama platformu için filtreleme asistanısın.
Kullanıcının doğal dilde yazdığı isteği analiz et ve AŞAĞIDAKİ KURALLARA GÖRE SADECE JSON çıktısı üret. Başka hiçbir şey yazma.

Çıktı alanları ve kesin kısıtlamalar:
- city: String (Örn: "İstanbul", "Ankara" veya belirtilmediyse null). Kesinlikle doğru ili yaz!
- district: String veya null
- price_min: Integer (varsayılan 0)
- price_max: Integer (varsayılan 10000000)
- year_min: Integer (varsayılan 1970)
- year_max: Integer (varsayılan 2030)
- fuel_type: Liste (Sadece şunlardan biri veya birkaçı olabilir: {', '.join(FUEL_TYPES)}. Belirtilmediyse [])
- transmission: Liste (Sadece: {', '.join(TRANSMISSION_TYPES)}. Belirtilmediyse [])
- km_min: Integer (varsayılan 0)
- km_max: Integer (varsayılan 9999999)
- body_type: Liste (Sadece: {', '.join(BODY_TYPES)}. Belirtilmediyse [])
- power_range: Liste (Sadece: {', '.join(POWER_RANGES)}. Belirtilmediyse [])
- engine_size: Liste (Sadece: {', '.join(ENGINE_SIZES)}. Belirtilmediyse [])
- drive_type: Liste (Sadece: {', '.join(DRIVE_TYPES)}. Belirtilmediyse [])
- color: Liste (Sadece: {', '.join(COLORS)}. Belirtilmediyse [])
- warranty: "Evet", "Hayır" veya null
- heavy_damage: "Evet", "Hayır" veya null
- seller_type: "Sahibinden", "Kurumdan" veya null
- available: "Kiralık"

Eğer kullanıcı bir ili (Örn: İstanbul) belirtmişse 'city' alanına o ili kesinlikle yazmalısın. Eğer bir alanı belirtmezse null veya [] (boş liste) kullan.
Asla açıklama yapma, sadece geçerli bir JSON formatında yanıt dön.
"""

def _ensure_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return [str(value)]

def prompt_to_filter(prompt: str):
    if not API_KEY or client is None:
        raise RuntimeError("OPENAI_API_KEY ortam değişkeni bulunamadı veya geçersiz.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )
    except Exception as e:
        raise RuntimeError(f"OpenAI isteği başarısız oldu: {e}")

    content = response.choices[0].message.content
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"AI çıktısı JSON olarak çözümlenemedi: {e}")

    parsed_filter = {**DEFAULT_FILTER, **parsed}

    parsed_filter["fuel_type"] = _ensure_list(parsed_filter.get("fuel_type"))
    parsed_filter["transmission"] = _ensure_list(parsed_filter.get("transmission"))
    parsed_filter["body_type"] = _ensure_list(parsed_filter.get("body_type"))
    parsed_filter["power_range"] = _ensure_list(parsed_filter.get("power_range"))
    parsed_filter["engine_size"] = _ensure_list(parsed_filter.get("engine_size"))
    parsed_filter["drive_type"] = _ensure_list(parsed_filter.get("drive_type"))
    parsed_filter["color"] = _ensure_list(parsed_filter.get("color"))

    return parsed_filter