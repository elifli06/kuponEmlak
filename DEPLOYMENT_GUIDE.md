# AWS Deployment Güncelleme Rehberi

Bu rehber, AWS üzerinde çalışan projenizi güncellemek için adımları içerir.

## Ön Hazırlık

### 1. Yerel Değişiklikleri Kontrol Et
```powershell
# Git status kontrolü
git status

# Değişiklikleri commit et
git add .
git commit -m "Frontend modernizasyonu - Profesyonel tasarım güncellemeleri"
```

### 2. Static Dosyaları Topla (Yerel)
```powershell
# Virtual environment aktif et (eğer varsa)
# .venv\Scripts\Activate.ps1

# Static dosyaları topla
python manage.py collectstatic --noinput
```

---

## Senaryo 1: EC2 Instance Üzerinde Manuel Deployment

### Adım 1: EC2'ye Bağlan
```powershell
# SSH ile bağlan (PowerShell'de SSH kullanabilirsiniz veya Git Bash)
ssh -i "your-key.pem" ubuntu@16.170.231.253
# veya
ssh -i "your-key.pem" ec2-user@16.170.231.253
```

### Adım 2: Proje Dizinine Git
```bash
cd /var/www/kuponEmlak  # veya projenizin olduğu dizin
# veya
cd ~/kuponEmlak
```

### Adım 3: Git'ten Çek veya Dosyaları Yükle
```bash
# Eğer Git kullanıyorsanız
git pull origin main
# veya
git pull origin master

# Eğer Git yoksa, dosyaları manuel olarak yüklemeniz gerekir
```

### Adım 4: Virtual Environment Aktif Et
```bash
source venv/bin/activate
# veya
source .venv/bin/activate
```

### Adım 5: Bağımlılıkları Güncelle
```bash
pip install -r requirements.txt
```

### Adım 6: Database Migration (Eğer varsa)
```bash
python manage.py migrate
```

### Adım 7: Static Dosyaları Topla
```bash
python manage.py collectstatic --noinput
```

### Adım 8: Gunicorn'u Yeniden Başlat
```bash
# Supervisor kullanıyorsanız
sudo supervisorctl restart kuponemlak

# Systemd kullanıyorsanız
sudo systemctl restart gunicorn

# Manuel çalıştırıyorsanız
pkill -f gunicorn
# Sonra tekrar başlat
gunicorn --bind 0.0.0.0:8000 kuponEmlak.wsgi:application
```

### Adım 9: Nginx Yeniden Başlat (Eğer kullanıyorsanız)
```bash
sudo nginx -t  # Test et
sudo systemctl restart nginx
```

---

## Senaryo 2: AWS Elastic Beanstalk Kullanıyorsanız

### Adım 1: EB CLI Kurulumu (Eğer yoksa)
```powershell
pip install awsebcli
```

### Adım 2: EB CLI ile Deploy
```powershell
# Proje dizinine git
cd V:\kuponEmlak\kuponEmlak-1

# EB init (ilk kez)
eb init -p python-3.11 kuponemlak --region eu-central-1

# EB create (ilk kez, sadece bir kez)
# eb create kuponemlak-env

# Deploy
eb deploy

# Veya belirli bir environment'a
eb deploy kuponemlak-env
```

### Adım 3: Environment Variables Kontrolü
```powershell
eb setenv DJANGO_SETTINGS_MODULE=kuponEmlak.settings
eb setenv DEBUG=False
```

---

## Senaryo 3: Git Push ile Otomatik Deploy (GitHub Actions veya CodePipeline)

### GitHub Actions Workflow Oluştur
`.github/workflows/deploy.yml` dosyası oluşturun:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main, master ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-central-1
      
      - name: Deploy to EB
        run: |
          pip install awsebcli
          eb deploy
```

---

## Senaryo 4: SCP ile Dosya Yükleme (Git Kullanmıyorsanız)

### PowerShell'den Dosya Yükleme
```powershell
# Tüm projeyi yükle (SSH key gerekli)
scp -i "your-key.pem" -r V:\kuponEmlak\kuponEmlak-1\* ubuntu@16.170.231.253:/var/www/kuponEmlak/

# Veya sadece template dosyalarını
scp -i "your-key.pem" -r V:\kuponEmlak\kuponEmlak-1\templates\ ubuntu@16.170.231.253:/var/www/kuponEmlak/
```

### Git Bash ile
```bash
scp -i "your-key.pem" -r /v/kuponEmlak/kuponEmlak-1/* ubuntu@16.170.231.253:/var/www/kuponEmlak/
```

---

## Önemli Notlar

### 1. Database Backup (ÖNEMLİ!)
```bash
# PostgreSQL backup
pg_dump -U kuponuser kupondb > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Static Dosyalar
- `collectstatic` komutunu mutlaka çalıştırın
- WhiteNoise kullanıldığı için static dosyalar `staticfiles/` klasöründe olmalı

### 3. Media Dosyalar
- Yüklenen resimler `media/` klasöründe
- Bu dosyalar kaybolmamalı, dikkatli olun!

### 4. Environment Variables
- `SECRET_KEY` production'da environment variable olmalı
- Database bilgileri güvenli tutulmalı

### 5. Test Et
Deploy sonrası mutlaka test edin:
- Ana sayfa açılıyor mu?
- İlanlar görünüyor mu?
- Resimler yükleniyor mu?
- CSS/JS dosyaları çalışıyor mu?

---

## Hızlı Güncelleme Scripti (EC2 için)

EC2 üzerinde şu script'i çalıştırabilirsiniz:

```bash
#!/bin/bash
# update.sh

cd /var/www/kuponEmlak
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo supervisorctl restart kuponemlak
sudo systemctl restart nginx
echo "Deployment tamamlandı!"
```

Kullanım:
```bash
chmod +x update.sh
./update.sh
```

---

## Sorun Giderme

### Static dosyalar görünmüyor
```bash
# Static dosyaları tekrar topla
python manage.py collectstatic --noinput

# Nginx ayarlarını kontrol et
sudo nginx -t

# WhiteNoise ayarlarını kontrol et
# settings.py'de STATICFILES_STORAGE doğru mu?
```

### 500 Error
```bash
# Logları kontrol et
sudo tail -f /var/log/gunicorn/error.log
# veya
sudo journalctl -u gunicorn -f
```

### Permission Hatası
```bash
# Static files klasörüne izin ver
sudo chmod -R 755 staticfiles/
sudo chown -R www-data:www-data staticfiles/
```

---

## Güvenlik Uyarıları ve Güncelleme

⚠️ **ÖNEMLİ:**
1. ✅ **GÜNCELLENDİ:** Artık environment variables kullanılıyor!
2. **Production'da mutlaka yapılması gerekenler:**
   - `.env` dosyası oluşturun (`.env.example` dosyasını referans alın)
   - Yeni bir `SECRET_KEY` oluşturun (daha önceki key açığa çıkmış olabilir)
   - `.env` dosyasını `.gitignore`'da olduğundan emin olun
   - `.env` dosya izinlerini 600 yapın: `chmod 600 .env`
3. **Detaylı güvenlik migration için:** `SECURITY_MIGRATION.md` dosyasını okuyun

### Hızlı Güvenlik Güncellemesi

```bash
# 1. EC2'ye bağlan
ssh -i "your-key.pem" ubuntu@16.170.231.253

# 2. Proje dizinine git
cd /var/www/kuponEmlak

# 3. .env dosyası oluştur
nano .env
# (İçeriği SECURITY_MIGRATION.md'den kopyalayın)

# 4. Yeni SECRET_KEY oluştur
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 5. python-decouple kur
source venv/bin/activate
pip install python-decouple

# 6. Servisleri restart et
sudo supervisorctl restart kuponemlak
```

