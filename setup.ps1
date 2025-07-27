# setup-fatsh.ps1

# 1. Gereksinimleri yükle
Write-Host "📦 Installing requirements..."
pip install -r requirements.txt

# 2. fatsh dizin yolu
$CurrentDir = Join-Path (Get-Location) "fatsh"

# 3. fatsh dizini var mı kontrol et
if (!(Test-Path $CurrentDir)) {
    Write-Host "❌ Directory $CurrentDir does not exist!"
    exit 1
}

# 4. Kullanıcı ortam değişkenine PATH ekleme
$envPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not ($envPath -split ";" | Where-Object { $_ -eq $CurrentDir })) {
    [Environment]::SetEnvironmentVariable("Path", "$envPath;$CurrentDir", "User")
    Write-Host "✔️ Added $CurrentDir to user PATH"
} else {
    Write-Host "ℹ️ PATH already contains $CurrentDir"
}

# 5. Kullanıcıya bilgilendirme
Write-Host "🔄 Please restart your terminal for changes to take effect."

# 6. fatsh.py var mı kontrol et, varsa çalıştır
$FatshPy = Join-Path $CurrentDir "fatsh.py"
if (Test-Path $FatshPy) {
    Write-Host "🚀 Running fatsh.py..."
    python $FatshPy
} else {
    Write-Host "❌ fatsh.py not found in $CurrentDir"
}
