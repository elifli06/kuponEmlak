#!/bin/bash
# EC2 üzerinde çalıştırılacak deployment script

set -e  # Hata durumunda dur

echo "========================================"
echo "  Kup10 Emlak - Remote Deployment"
echo "========================================"
echo ""

# Proje dizini (güncelleyin)
PROJECT_DIR="/var/www/kuponEmlak"
cd $PROJECT_DIR

echo "[1/6] Git pull yapılıyor..."
git pull origin main || git pull origin master
echo "✓ Git pull tamamlandı"
echo ""

echo "[2/6] Virtual environment aktif ediliyor..."
source venv/bin/activate || source .venv/bin/activate
echo "✓ Virtual environment aktif"
echo ""

echo "[3/6] Bağımlılıklar güncelleniyor..."
pip install -r requirements.txt --quiet
echo "✓ Bağımlılıklar güncellendi"
echo ""

echo "[4/6] Database migration..."
python manage.py migrate --noinput
echo "✓ Migration tamamlandı"
echo ""

echo "[5/6] Static dosyalar toplanıyor..."
python manage.py collectstatic --noinput
echo "✓ Static dosyalar toplandı"
echo ""

echo "[6/6] Servisler yeniden başlatılıyor..."
# Supervisor kullanıyorsanız
if command -v supervisorctl &> /dev/null; then
    sudo supervisorctl restart kuponemlak || true
    echo "✓ Supervisor restart edildi"
fi

# Systemd kullanıyorsanız
if systemctl is-active --quiet gunicorn; then
    sudo systemctl restart gunicorn
    echo "✓ Gunicorn restart edildi"
fi

# Nginx reload
if systemctl is-active --quiet nginx; then
    sudo systemctl reload nginx
    echo "✓ Nginx reload edildi"
fi

echo ""
echo "========================================"
echo "  Deployment Başarıyla Tamamlandı!"
echo "========================================"
echo ""
echo "Test: http://kupon10emlak.com.tr"
echo ""

