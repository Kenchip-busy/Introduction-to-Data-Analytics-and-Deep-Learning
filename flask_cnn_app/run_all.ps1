# Run setup and test script for Flask CNN app
# Usage: Open PowerShell, cd d:\lab10\flask_cnn_app and run: .\run_all.ps1

$here = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Find a python executable
$pyCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pyCmd) { $pyCmd = (Get-Command py -ErrorAction SilentlyContinue).Source }

if (-not $pyCmd) {
    Write-Host "Python not found in PATH. Please install Python and ensure 'python' or 'py' is available." -ForegroundColor Red
    Write-Host "Download: https://www.python.org/downloads/ (check 'Add Python to PATH' during install)"
    exit 1
}

$venv = Join-Path $here ".venv"
$python = Join-Path $venv "Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "Creating virtual environment..."
    & $pyCmd -m venv $venv
}

if (-not (Test-Path $python)) {
    Write-Host "Failed to create virtual environment. Ensure Python is installed." -ForegroundColor Red
    exit 1
}

Write-Host "Upgrading pip and installing requirements..."
& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $here 'requirements.txt')

Write-Host "Running test script..."
& $python (Join-Path $here 'run_test.py')

Write-Host "Done." -ForegroundColor Green
