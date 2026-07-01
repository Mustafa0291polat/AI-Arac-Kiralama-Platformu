# Yapay Zeka Destekli Bireyler Arası Araç Kiralama Platformu

Bu proje, Yazılım Mühendisliği dersi kapsamında geliştirilmektedir.

## Ekip Üyeleri
- Mustafa Polat
- Erkan Özbey
- Duhan Harbi

## Ne Yapar?
Kullanıcılar araçlarını kiraya verebilir, kiralamak isteyenler ise ihtiyacını **kendi cümleleriyle** anlatarak arama yapabilir. Örneğin *"Hafta sonu dağda kamp yapacağız, araziye uygun bir araç lazım"* yazıldığında, OpenAI tabanlı filtre servisi bunu yapılandırılmış kriterlere (SUV, 4x4 vb.) çevirir ve eşleşen ilanları listeler.

## Teknolojiler
- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Yapay Zeka:** OpenAI (gpt-4o-mini) ile doğal dil → JSON filtre dönüşümü
- **Frontend:** Statik HTML + Tailwind CSS (backend/static altında)
- **Testler:** pytest (bellek içi SQLite ile, OpenAI çağrıları mock'lanır)

## Kurulum ve Çalıştırma

1. Proje kök dizininde sanal ortam oluşturun ve etkinleştirin:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. (İsteğe bağlı — akıllı arama için) `backend/.env.example` dosyasını `backend/.env` adıyla kopyalayıp kendi `OPENAI_API_KEY` değerinizi yazın. Anahtar yoksa site yine çalışır; yalnızca doğal dil araması devre dışı kalır ve kullanıcıya anlaşılır bir mesaj gösterilir.
4. Örnek araç verisini yükleyin (isteğe bağlı):
   ```bash
   python -m backend.seed_data
   ```
5. Sunucuyu proje kökünden başlatın:
   ```bash
   uvicorn backend.main:app --reload
   ```
6. Tarayıcıda `http://127.0.0.1:8000` adresini açın.

## Sayfalar
- `/` — Ana sayfa: doğal dil arama, ilan listesi, ilan verme formu
- `/kayit` — Üye kayıt formu
- `/giris` — Giriş formu

## API Uç Noktaları
- `POST /api/register/` — Kullanıcı kaydı (yalnızca `@gmail.com`, 18 yaş ve üzeri)
- `POST /api/login/` — Giriş doğrulaması
- `GET /cars/` — Kiralık durumdaki araçları listeler
- `POST /cars/` — Araç ilanı ekler
- `POST /upload-images/` — İlan fotoğraflarını yükler
- `POST /filter/prompt` — Doğal dil isteğini yapay zeka ile filtreye çevirip eşleşen araçları döndürür

## Testler
Proje kökünden:
```bash
python -m pytest backend/test_main.py -v
```
Testler kendi bellek içi veritabanını kullanır; gerçek `sql_app.db` dosyasına ve OpenAI'ye dokunmaz.

## Güvenlik Notu
Gerçek OpenAI anahtarınızı yalnızca `backend/.env` dosyasında saklayın. Bu dosya `.gitignore`'dadır ve asla repoya gönderilmemelidir.
