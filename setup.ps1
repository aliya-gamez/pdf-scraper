# To run this script, type ./setup.ps1 in powershell while in directory

$ErrorActionPreference = 'Stop'
Write-Host ''
# Python Check
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host 'Python not found. Please install to continue.' -ForegroundColor Red
    exit 1
}
else {
    Write-Host 'Python found' -ForegroundColor Green
}
# Virtual Environment files check
if (!(Test-Path 'venv')) {
    Write-Host 'Virtual environment not found, creating now...' -ForegroundColor Yellow
    python -m venv venv
}
else {
    Write-Host 'Virtual environment found' -ForegroundColor Green
}
# Activate check
if((Test-Path 'venv') -and !($env:VIRTUAL_ENV)) {
    Write-Host 'Activating virtual environment...' -ForegroundColor Green
    & .\venv\Scripts\Activate.ps1
}
elseif (!(Test-Path 'venv')) {
    Write-Host 'Virtual environment not found.' -ForegroundColor Red
    Write-Host 'Terminating...' -ForegroundColor Red
    exit 1
}
elseif ((Test-Path 'venv')) {
    Write-Host 'Virtual environment already activated' -ForegroundColor Green
}
# Last activation check
if(!($env:VIRTUAL_ENV)) {
    Write-Host 'Virtual environment is supposed to be activated, but its not...' -ForegroundColor Red
    Write-Host 'Terminating...' -ForegroundColor Red
    exit 1
}
else {
    # Installs
    Write-Host 'Installing dependencies...' -ForegroundColor Green
    Write-Host ''
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host ''
    pip list
    Write-Host ''
    Write-Host 'Environment ready.' -ForegroundColor Cyan
    Write-Host ''
}