# Yapay Zeka Destekli Bireyler Arası Araç Kiralama Platformu
Bu proje, Yazılım Mühendisliği dersi kapsamında geliştirilmektedir.

## Ekip Üyeleri
- Mustafa Polat
- Erkan Özbey
- Duhan Harbi

## AI Destekli Araç Filtreleme
Bu proje, kullanıcıların doğal dil ile girdikleri arama kriterlerini OpenAI tabanlı bir servis aracılığıyla yapılandırılmış filtrelere çevirebilir.

### Eklenen Özellikler
- `backend/ai_filter.py`: Kullanıcının doğal dil girdisini JSON filtreye dönüştürür.
- `backend/main.py`: Yeni araç ekleme ve yapay zeka destekli filtreleme API rotaları eklenmiştir.
- `requirements.txt`: Gerekli Python paketleri tanımlandı.
- `.gitignore`: `.env`, `sql_app.db` ve Python cache dosyaları için ignore kuralları eklendi.
- `.env.example`: OpenAI anahtarının nasıl yapılandırılacağı gösterildi.

### Çalıştırma Adımları
1. Proje kök dizininde bir Python sanal ortamı oluşturun.
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. `backend` dizinine `.env` dosyası ekleyin ve `OPENAI_API_KEY` anahtarınızı yazın.
4. Sunucuyu başlatın:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Örnek API Kullanımı
- `POST /register`: Kullanıcı kaydı.
- `POST /login`: Giriş doğrulaması (şimdilik sahte token döner).
- `POST /cars/`: Araç ilanı ekleme.
- `GET /cars/`: Tüm araçları listeleme.
- `POST /filter/prompt`: Doğal dil promptunu alıp arama filtresi yaratma ve eşleşen araçları döndürme.

### Frontend Testi
- `backend/static/index.html` dosyası, backend API ile konuşmak için hazır bir örnek arayüz sunar.
- Sunucuyu başlattıktan sonra tarayıcıda `http://127.0.0.1:8000` adresini açarak:
  - doğal dil filtreleme yapabilir,
  - araç ekleyebilir,
  - tüm araçları görebilirsiniz.

### Örnek Veri Eklemek
- Proje kökünden şu komutu çalıştırarak örnek araç verisi ekleyin:
  ```bash
  python -m backend.seed_data
  ```
- Bu, `sql_app.db` içine kiralık araç verisi ve fotoğraflı örnek ilanları ekler.
- Var olan veritabanı dosyasını otomatik olarak siler ve yeniden oluşturur, böylece yeni `image_url` ve `available` alanları doğru şekilde kaydedilir.

### Güvenlik Notu
`.env` dosyanızda gerçek OpenAI anahtarınızı saklayın ve bu dosyayı public repo'ya göndermeyin.

