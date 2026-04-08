$ErrorActionPreference = 'Stop'

Write-Host ''

# Python check
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host 'Python not found. Please install to continue.' -ForegroundColor Red
    exit 1
}
else {
    Write-Host 'Python found' -ForegroundColor Green
}

# Virtual Environment path creation/check
if (-not (Test-Path '../.venv')) {
    Write-Host 'Virtual environment path not found, creating now...' -ForegroundColor Yellow
    python -m venv ../.venv
}
else {
    Write-Host 'Virtual environment path found' -ForegroundColor Green
}

# Verify: Virtual Environment path creation/check
if (-not (Test-Path '../.venv')) {
    Write-Host 'Virtual environment path failed to create normally.' -ForegroundColor Red
    exit 1
}

# Virtual environment activation/check
if (!$env:VIRTUAL_ENV) {
    Write-Host 'Activating virtual environment...' -ForegroundColor Green
    & ..\.venv\Scripts\Activate.ps1
}
else {
    Write-Host 'Virtual environment already activated' -ForegroundColor Green
}

# Verify: Virtual environment activation/check
if (!$env:VIRTUAL_ENV) {
    Write-Host 'Virtual environment failed to activate.' -ForegroundColor Red
    exit 1
}

# Verify: Requirements file check
if (!(Test-Path '../requirements.txt')) {
    Write-Host 'requirements.txt not found' -ForegroundColor Red
    exit 1
}

# Installs
Write-Host 'Installing dependencies...' -ForegroundColor Green
Write-Host ''

python -m pip install --upgrade pip
python -m pip install -r ../requirements.txt

Write-Host ''

python -m pip list

Write-Host ''
Write-Host 'Environment ready.' -ForegroundColor Cyan
Write-Host ''