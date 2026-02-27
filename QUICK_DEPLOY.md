# Hızlı Deployment Rehberi

Bu rehber, güvenlik güncellemeleri ile birlikte projeyi hızlıca deploy etmeniz için adımları içerir.

## 🚀 Hızlı Başlangıç

### Senaryo: EC2'de Git kullanıyorsanız (ÖNERİLEN)

#### 1. Yerel Değişiklikleri Commit ve Push Et

```powershell
# PowerShell'de
cd V:\kuponEmlak\kuponEmlak-1

# Tüm değişiklikleri ekle
git add .

# Commit et
git commit -m "Frontend modernizasyonu ve güvenlik güncellemeleri"

# Push et
git push origin main
# veya
git push origin master
```

#### 2. EC2'ye Bağlan ve Deploy Et

```powershell
# SSH ile bağlan (Git Bash veya WSL kullanabilirsiniz)
ssh -i "your-key.pem" ubuntu@16.170.231.253
```

#### 3. Production'da Güvenlik Güncellemesi

```bash
# Proje dizinine git
cd /var/www/kuponEmlak  # veya projenizin olduğu dizin

# Git pull
git pull origin main  # veya master

# Virtual environment aktif et
source venv/bin/activate  # veya .venv/bin/activate

# python-decouple kur (yeni eklenen)
pip install python-decouple

# .env dosyası oluştur (EĞER YOKSA)
nano .env
```

`.env` dosyasına şunu ekleyin:
```env
SECRET_KEY=<YENİ_BİR_SECRET_KEY_BURAYA>
DEBUG=False
ALLOWED_HOSTS=16.170.231.253,kupon10emlak.com.tr,www.kupon10emlak.com.tr
DB_NAME=kupondb
DB_USER=kuponuser
DB_PASSWORD=Zekiye_51.
DB_HOST=localhost
DB_PORT=5432
```

**Yeni SECRET_KEY oluştur:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Çıkan key'i .env dosyasındaki SECRET_KEY'e yapıştırın.

```bash
# .env dosyasını güvenli hale getir
chmod 600 .env

# Static dosyaları topla
python manage.py collectstatic --noinput

# Servisleri restart et
sudo supervisorctl restart kuponemlak  # veya
sudo systemctl restart gunicorn

# Nginx reload
sudo systemctl reload nginx
```

#### 4. Test Et

Tarayıcıda açın: http://kupon10emlak.com.tr

---

### Senaryo: Git Kullanmıyorsanız (SCP ile)

#### 1. Yerel Static Dosyaları Topla

```powershell
# PowerShell'de
cd V:\kuponEmlak\kuponEmlak-1
python manage.py collectstatic --noinput
```

#### 2. Dosyaları EC2'ye Yükle

```powershell
# Template dosyaları
scp -i "your-key.pem" -r templates\ ubuntu@16.170.231.253:/var/www/kuponEmlak/

# Settings.py (güvenlik güncellemeli)
scp -i "your-key.pem" kuponEmlak\settings.py ubuntu@16.170.231.253:/var/www/kuponEmlak/kuponEmlak/

# Requirements.txt
scp -i "your-key.pem" requirements.txt ubuntu@16.170.231.253:/var/www/kuponEmlak/

# Static dosyalar (eğer varsa)
scp -i "your-key.pem" -r staticfiles\ ubuntu@16.170.231.253:/var/www/kuponEmlak/
```

#### 3. EC2'de Güncellemeleri Yap

```bash
# SSH ile bağlan
ssh -i "your-key.pem" ubuntu@16.170.231.253

cd /var/www/kuponEmlak
source venv/bin/activate

# python-decouple kur
pip install -r requirements.txt

# .env dosyası oluştur (yukarıdaki gibi)
nano .env

# Güvenlik ayarları
chmod 600 .env

# Static dosyaları topla
python manage.py collectstatic --noinput

# Servisleri restart et
sudo supervisorctl restart kuponemlak
sudo systemctl reload nginx
```

---

## 📋 Deployment Checklist

### Önce (Local)
- [ ] Tüm değişiklikler commit edildi
- [ ] Static dosyalar toplandı (`collectstatic`)
- [ ] Test edildi (yerel olarak çalışıyor)

### Production'da
- [ ] Git pull yapıldı (veya dosyalar yüklendi)
- [ ] `python-decouple` kuruldu
- [ ] `.env` dosyası oluşturuldu ve dolduruldu
- [ ] Yeni `SECRET_KEY` oluşturuldu
- [ ] `.env` dosyası izinleri 600 yapıldı
- [ ] Static dosyalar toplandı
- [ ] Migration yapıldı (eğer varsa)
- [ ] Gunicorn restart edildi
- [ ] Nginx reload edildi
- [ ] Test edildi (site açılıyor mu?)

---

## 🆘 Sorun Giderme

### "No module named 'decouple'"
```bash
pip install python-decouple
```

### "SECRET_KEY not found"
- `.env` dosyasının proje dizininde olduğunu kontrol edin
- `.env` dosyasında `SECRET_KEY=` satırının olduğunu kontrol edin

### Static dosyalar görünmüyor
```bash
python manage.py collectstatic --noinput
# İzinleri kontrol et
chmod -R 755 staticfiles/
```

### 500 Error
```bash
# Logları kontrol et
sudo tail -f /var/log/gunicorn/error.log
# veya
sudo journalctl -u gunicorn -f
```

---

## 📞 Yardım

Detaylı bilgi için:
- `DEPLOYMENT_GUIDE.md` - Tüm deployment senaryoları
- `SECURITY_MIGRATION.md` - Güvenlik güncelleme detayları
- `remote_deploy.sh` - Otomatik deployment scripti

