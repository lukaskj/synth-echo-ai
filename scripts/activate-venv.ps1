if (-not $env:VIRTUAL_ENV) {
  if (Test-Path "apps/backend/.venv/Scripts/Activate.ps1") {
    . "apps/backend/.venv/Scripts/Activate.ps1"
  } elseif (Test-Path "apps/backend/.venv/bin/Activate.ps1") {
    . "apps/backend/.venv/bin/Activate.ps1"
  } elseif (Test-Path "apps/backend/.venv/bin/activate") {
    . "apps/backend/.venv/bin/activate"
  } else {
    Write-Error "No virtual environment activation script found."
    exit 1
  }
}