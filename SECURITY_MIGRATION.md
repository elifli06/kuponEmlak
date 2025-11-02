# Güvenlik Güncellemesi - Migration Rehberi

Bu rehber, projenizi güvenli environment variables kullanımına geçirmeniz için adımları içerir.

## ⚠️ ÖNEMLİ GÜVENLİK UYARISI

Production sunucunuzda şu an **SECRET_KEY ve database şifreleri açıkta**! Hemen düzeltin!

## Adım 1: Production Sunucuda .env Dosyası Oluştur

### EC2'ye SSH ile bağlan
```bash
ssh -i "your-key.pem" ubuntu@16.170.231.253
```

### Proje dizinine git
```bash
cd /var/www/kuponEmlak  # veya projenizin olduğu dizin
```

### .env dosyası oluştur
```bash
nano .env
```

### Şu içeriği ekleyin:
```env
# Django Secret Key - ÖNEMLİ: YENİ BİR KEY OLUŞTURUN!
SECRET_KEY=yeni-güvenli-secret-key-buraya

# Debug Mode
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=16.170.231.253,kupon10emlak.com.tr,www.kupon10emlak.com.tr

# Database Configuration
DB_NAME=kupondb
DB_USER=kuponuser
DB_PASSWORD=Zekiye_51.
DB_HOST=localhost
DB_PORT=5432
```

### Yeni SECRET_KEY Oluşturma
```bash
# Sunucuda Python ile yeni key oluştur
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Bu komuttan çıkan key'i .env dosyasındaki SECRET_KEY'e yapıştırın.

## Adım 2: .env Dosyasını Güvenli Hale Getir
```bash
# Sadece sahip okuyabilir
chmod 600 .env

# Doğru sahiplik (www-data veya ubuntu)
chown ubuntu:ubuntu .env
```

## Adım 3: Python-Decouple Kurulumu
```bash
# Virtual environment aktif et
source venv/bin/activate

# python-decouple kur
pip install python-decouple

# Requirements.txt güncelle
pip freeze > requirements.txt  # veya manuel olarak zaten ekledik
```

## Adım 4: Settings.py Güncellemesi

Settings.py artık environment variables kullanıyor. Sadece yeni dosyaları yükleyin:

```bash
# Git ile
git pull origin main

# Veya dosyaları manuel yükle
# settings.py ve requirements.txt dosyalarını güncelleyin
```

## Adım 5: Test Et
```bash
# Virtual environment aktif et
source venv/bin/activate

# Django'nun ayarları okuyabildiğini test et
python manage.py check

# Eğer hata varsa, .env dosyasını kontrol edin
```

## Adım 6: Servisleri Yeniden Başlat
```bash
# Gunicorn restart
sudo supervisorctl restart kuponemlak
# veya
sudo systemctl restart gunicorn

# Nginx reload
sudo systemctl reload nginx
```

## Adım 7: Test Et
Tarayıcıda açın: http://kupon10emlak.com.tr

## Sorun Giderme

### Hata: "SECRET_KEY not found"
- .env dosyasının proje dizininde olduğundan emin olun
- .env dosyasında SECRET_KEY satırının olduğunu kontrol edin
- Dosya izinlerini kontrol edin: `ls -la .env`

### Hata: "No module named 'decouple'"
```bash
pip install python-decouple
```

### Database bağlantı hatası
- .env dosyasındaki DB_PASSWORD doğru mu?
- PostgreSQL çalışıyor mu? `sudo systemctl status postgresql`

## Local Development İçin

Local'de de .env dosyası oluşturun:

```powershell
# Windows PowerShell
Copy-Item .env.example .env

# Dosyayı düzenleyin ve local değerlerinizi girin
notepad .env
```

Local .env örneği:
```env
SECRET_KEY=django-insecure-local-development-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=kupondb_local
DB_USER=postgres
DB_PASSWORD=localpassword
DB_HOST=localhost
DB_PORT=5432
```

## Güvenlik Checklist

- [ ] Production'da yeni SECRET_KEY oluşturuldu
- [ ] .env dosyası oluşturuldu ve dolduruldu
- [ ] .env dosyası .gitignore'da (commit edilmedi)
- [ ] .env dosya izinleri 600 (sadece sahip okuyabilir)
- [ ] Settings.py'de hardcoded şifreler kaldırıldı
- [ ] python-decouple kuruldu
- [ ] Test edildi ve çalışıyor
- [ ] Eski settings.py backup'ı alındı (güvenlik için)

## Yedekleme

Değişikliklerden önce mutlaka yedek alın:

```bash
# Settings.py yedeği
cp kuponEmlak/settings.py kuponEmlak/settings.py.backup

# Database yedeği
pg_dump -U kuponuser kupondb > backup_$(date +%Y%m%d).sql
```

