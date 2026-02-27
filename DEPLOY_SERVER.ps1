# Kup10 Emlak - Server Deployment Komutları
# PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Kup10 Emlak - Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Local'de Git Commit ve Push
Write-Host "[1/3] Git commit ve push yapılıyor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Komutlar:" -ForegroundColor Green
Write-Host "  git add ." -ForegroundColor White
Write-Host "  git commit -m 'Footer düzeltildi ve CRV Software linki eklendi'" -ForegroundColor White
Write-Host "  git push origin main" -ForegroundColor White
Write-Host ""
$continue = Read-Host "Git push yaptınız mı? (E/H)"
if ($continue -ne "E") {
    Write-Host "Önce git push yapın!" -ForegroundColor Red
    exit
}

# 2. SSH ile Server'a Bağlan
Write-Host ""
Write-Host "[2/3] SSH ile server'a bağlanılıyor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "SSH Komutu:" -ForegroundColor Green
Write-Host "  ssh -i `"V:\kuponEmlak\kuponEmlak.pem`" ubuntu@16.170.231.253" -ForegroundColor White
Write-Host ""

# 3. Server'da Çalıştırılacak Komutlar
Write-Host "[3/3] Server'da çalıştırılacak komutlar:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Aşağıdaki komutları server'da sırayla çalıştırın:" -ForegroundColor Cyan
Write-Host ""
Write-Host "cd /home/ubuntu/kuponEmlak" -ForegroundColor Green
Write-Host "source venv/bin/activate" -ForegroundColor Green
Write-Host "git pull origin main" -ForegroundColor Green
Write-Host "python manage.py collectstatic --noinput" -ForegroundColor Green
Write-Host "sudo systemctl restart gunicorn" -ForegroundColor Green
Write-Host "sudo systemctl reload nginx" -ForegroundColor Green
Write-Host "sudo systemctl status gunicorn" -ForegroundColor Green
Write-Host ""
Write-Host "Deployment tamamlandı!" -ForegroundColor Green
Write-Host "Test: https://kup10emlak.com.tr" -ForegroundColor Cyan

