# AWS Deployment Script for PowerShell
# Bu script, projenizi AWS EC2'ye deploy etmek için kullanılır

param(
    [string]$ServerIP = "16.170.231.253",
    [string]$Username = "ubuntu",
    [string]$SSHKey = "your-key.pem",
    [string]$ProjectPath = "/var/www/kuponEmlak",
    [switch]$DryRun = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Kup10 Emlak - Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Static dosyaları topla
Write-Host "[1/5] Static dosyaları topluyor..." -ForegroundColor Yellow
if (-not $DryRun) {
    python manage.py collectstatic --noinput
    if ($LASTEXITCODE -ne 0) {
        Write-Host "HATA: Static dosyalar toplanamadı!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Static dosyalar hazır" -ForegroundColor Green
Write-Host ""

# 2. Git durumunu kontrol et
Write-Host "[2/5] Git durumu kontrol ediliyor..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "UYARI: Commit edilmemiş değişiklikler var!" -ForegroundColor Yellow
    $response = Read-Host "Yine de devam etmek istiyor musunuz? (y/n)"
    if ($response -ne "y") {
        Write-Host "Deployment iptal edildi." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Git durumu OK" -ForegroundColor Green
Write-Host ""

# 3. Deploy yöntemi seç
Write-Host "[3/5] Deploy yöntemini seçin:" -ForegroundColor Yellow
Write-Host "  1. SCP ile dosya yükleme (Git kullanmıyorsanız)" -ForegroundColor White
Write-Host "  2. SSH ile uzaktan komut çalıştırma (Git kullanıyorsanız)" -ForegroundColor White
Write-Host "  3. Elastic Beanstalk (EB CLI)" -ForegroundColor White
$choice = Read-Host "Seçiminiz (1/2/3)"

switch ($choice) {
    "1" {
        Write-Host "[4/5] SCP ile dosya yükleniyor..." -ForegroundColor Yellow
        
        if (-not (Test-Path $SSHKey)) {
            Write-Host "HATA: SSH key dosyası bulunamadı: $SSHKey" -ForegroundColor Red
            exit 1
        }
        
        if (-not $DryRun) {
            # Template dosyalarını yükle
            Write-Host "  → Template dosyaları yükleniyor..." -ForegroundColor Gray
            scp -i $SSHKey -r templates\ ${Username}@${ServerIP}:${ProjectPath}/templates/
            
            # Static dosyaları yükle
            if (Test-Path "staticfiles") {
                Write-Host "  → Static dosyalar yükleniyor..." -ForegroundColor Gray
                scp -i $SSHKey -r staticfiles\ ${Username}@${ServerIP}:${ProjectPath}/staticfiles/
            }
            
            Write-Host "✓ Dosyalar yüklendi" -ForegroundColor Green
        }
        
        # SSH ile uzaktan komutları çalıştır
        Write-Host "[5/5] Uzak sunucuda komutlar çalıştırılıyor..." -ForegroundColor Yellow
        if (-not $DryRun) {
            $commands = @"
cd $ProjectPath
source venv/bin/activate || source .venv/bin/activate
python manage.py collectstatic --noinput
sudo supervisorctl restart kuponemlak || sudo systemctl restart gunicorn
sudo systemctl reload nginx || sudo service nginx reload
echo 'Deployment tamamlandı!'
"@
            
            ssh -i $SSHKey ${Username}@${ServerIP} $commands
        }
    }
    
    "2" {
        Write-Host "[4/5] SSH ile uzaktan deploy..." -ForegroundColor Yellow
        
        if (-not (Test-Path $SSHKey)) {
            Write-Host "HATA: SSH key dosyası bulunamadı: $SSHKey" -ForegroundColor Red
            exit 1
        }
        
        if (-not $DryRun) {
            $commands = @"
cd $ProjectPath
git pull origin main || git pull origin master
source venv/bin/activate || source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart kuponemlak || sudo systemctl restart gunicorn
sudo systemctl reload nginx || sudo service nginx reload
echo 'Deployment tamamlandı!'
"@
            
            ssh -i $SSHKey ${Username}@${ServerIP} $commands
        }
        
        Write-Host "✓ Uzak deploy tamamlandı" -ForegroundColor Green
    }
    
    "3" {
        Write-Host "[4/5] Elastic Beanstalk'a deploy ediliyor..." -ForegroundColor Yellow
        
        # EB CLI kontrolü
        $ebInstalled = Get-Command eb -ErrorAction SilentlyContinue
        if (-not $ebInstalled) {
            Write-Host "EB CLI kurulu değil. Kuruluyor..." -ForegroundColor Yellow
            pip install awsebcli
        }
        
        if (-not $DryRun) {
            Write-Host "  → EB deploy başlatılıyor..." -ForegroundColor Gray
            eb deploy
        }
        
        Write-Host "✓ EB deploy tamamlandı" -ForegroundColor Green
    }
    
    default {
        Write-Host "Geçersiz seçim!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deployment Tamamlandı!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Test edin: http://kupon10emlak.com.tr" -ForegroundColor Cyan
Write-Host ""

