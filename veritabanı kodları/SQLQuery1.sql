-- 1. KULLANICILAR TABLOSU
CREATE TABLE Kullanicilar (
    kullanici_id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    sifre_hash VARCHAR(255) NOT NULL,
    telefon VARCHAR(20)
);

-- 2. ARAÇLAR TABLOSU (Temel Klasik Veriler)
CREATE TABLE Araclar (
    arac_id INT AUTO_INCREMENT PRIMARY KEY,
    sahip_id INT NOT NULL,
    marka VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    uretim_yili INT,
    vites_tipi VARCHAR(20),
    yakit_tipi VARCHAR(20),
    gunluk_fiyat DECIMAL(10,2) NOT NULL,
    arac_aciklamasi TEXT, -- Araç sahibinin girdiði ham metin
    FOREIGN KEY (sahip_id) REFERENCES Kullanicilar(kullanici_id) ON DELETE CASCADE
);

-- 3. YAPAY ZEKA AKILLI FÝLTRE VERÝLERÝ (Projenin Kalbi)
-- Yapay zeka modelinin ürettiði filtreleme parametrelerinin tutulduðu tablo
CREATE TABLE Yapay_Zeka_Filtre_Profilleri (
    arac_id INT PRIMARY KEY,
    ai_etiketleri JSON, 
    -- Örnek Veri: ["geniþ aile", "off-road", "ekonomik", "kamp", "bebek koltuðu"]
    
    vektor_degeri TEXT, 
    -- NLP (Doðal Dil Ýþleme) modelleri için cümlenin matematiksel karþýlýðý (Embedding). 
    -- Anlamsal arama (Semantic Search) yaparken bu sütun kullanýlýr.
    
    ai_kategori_tahmini VARCHAR(100), 
    -- Aracýn açýklamasýndan YZ'nin çýkardýðý ana kategori
    
    guncellenme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (arac_id) REFERENCES Araclar(arac_id) ON DELETE CASCADE
);

-- 4. KULLANICI ARAMA VE DAVRANIÞ GEÇMÝÞÝ (Kiþiselleþtirilmiþ Filtreleme Ýçin)
-- YZ'nin kullanýcýnýn ne tarz araçlar sevdiðini öðrenmesi için log tablosu
CREATE TABLE Arama_Gecmisi (
    arama_id INT AUTO_INCREMENT PRIMARY KEY,
    kullanici_id INT NOT NULL,
    aranan_metin VARCHAR(255), 
    -- Örn: "Dað yoluna uygun büyük araba"
    
    secilen_filtreler JSON, 
    -- Arayüzde týklanan filtrelerin logu (Örn: {"vites": "otomatik", "fiyat_max": 2000})
    
    arama_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kullanici_id) REFERENCES Kullanicilar(kullanici_id) ON DELETE CASCADE
);

-- 5. KÝRALAMA ÝÞLEMLERÝ (Sürecin Tamamlanmasý)
CREATE TABLE Kiralamalar (
    kiralama_id INT AUTO_INCREMENT PRIMARY KEY,
    arac_id INT NOT NULL,
    kiralayan_id INT NOT NULL,
    baslangic_tarihi DATETIME NOT NULL,
    bitis_tarihi DATETIME NOT NULL,
    toplam_tutar DECIMAL(10,2) NOT NULL,
    durum VARCHAR(20) DEFAULT 'AKTIF',
    FOREIGN KEY (arac_id) REFERENCES Araclar(arac_id),
    FOREIGN KEY (kiralayan_id) REFERENCES Kullanicilar(kullanici_id)
);