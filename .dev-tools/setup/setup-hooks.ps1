# Git Hooks Setup for Windows

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Git Hooks Setup (Windows)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Get repository root
try {
    $repoRoot = git rev-parse --show-toplevel 2>$null
    if (-not $repoRoot) {
        throw "Not a git repository"
    }
    $repoRoot = $repoRoot.Replace('/', '\')
} catch {
    Write-Host " ERROR: Not a git repository" -ForegroundColor Red
    exit 1
}

$devToolsDir = Join-Path $repoRoot ".dev-tools"

if (-not (Test-Path $devToolsDir)) {
    Write-Host " ERROR: .dev-tools directory not found" -ForegroundColor Red
    exit 1
}

# Check if already installed
$hookPath = Join-Path $repoRoot ".git\hooks\commit-msg"
if ((Test-Path $hookPath) -and ((Get-Content $hookPath -Raw) -match "pre-commit")) {
    Write-Host " INFO: Hooks appear to be already installed." -ForegroundColor Yellow
    $response = Read-Host "Reinstall anyway? (y/N)"
    if ($response -notmatch "^[Yy]$") {
        Write-Host "Skipping installation."
        exit 0
    }
}

# Check Python
$pythonCmd = $null
foreach ($cmd in @('python', 'python3', 'py')) {
    try {
        $version = & $cmd --version 2>&1
        if ($version -match "Python 3") {
            $pythonCmd = $cmd
            break
        }
    } catch {
        continue
    }
}

if (-not $pythonCmd) {
    Write-Host " ERROR: Python 3 is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install from: https://www.python.org/downloads/"
    Write-Host "Check 'Add Python to PATH' during installation"
    exit 1
}

$pythonVersion = & $pythonCmd --version
Write-Host "Python 3 found: $pythonVersion" -ForegroundColor Green

# Install pre-commit
if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    Write-Host "pre-commit already installed" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host " Installing pre-commit framework..." -ForegroundColor Yellow
    try {
        & $pythonCmd -m pip install --user pre-commit 2>&1 | Out-Null
        Write-Host "pre-commit installed" -ForegroundColor Green
    } catch {
        Write-Host " WARNING: Could not install pre-commit" -ForegroundColor Yellow
    }
}

# Copy config
Write-Host ""
Write-Host " Configuring hooks..." -ForegroundColor Yellow
$configSource = Join-Path $devToolsDir "config\pre-commit-config.yaml"
$configDest = Join-Path $repoRoot ".pre-commit-config.yaml"
Copy-Item $configSource $configDest -Force
Write-Host " SUCCESS: Configuration copied" -ForegroundColor Green

# Install hooks
Set-Location $repoRoot
Write-Host ""
Write-Host "Installing Git hooks..." -ForegroundColor Yellow
try {
    # Try to find pre-commit in PATH or use python -m pre_commit
    $preCommitCmd = $null
    if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
        $preCommitCmd = "pre-commit"
    } else {
        $preCommitCmd = "$pythonCmd -m pre_commit"
    }
    
    # Install hooks using the found command
    Invoke-Expression "$preCommitCmd install" 2>&1 | Out-Null
    Invoke-Expression "$preCommitCmd install --hook-type commit-msg" 2>&1 | Out-Null
    Invoke-Expression "$preCommitCmd install --hook-type pre-push" 2>&1 | Out-Null
    Write-Host " SUCCESS: Hooks installed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "   SUCCESS: Setup Complete!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Hooks installed:" -ForegroundColor Cyan
    Write-Host "  commit-msg : Validates commit message format"
    Write-Host "  pre-commit : Validates Logic App workflows"
    Write-Host "  pre-push   : Validates branch naming"
    Write-Host ""
    Write-Host " INFO: Hooks only run on dev/feature branches, NOT on release" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Test your setup:" -ForegroundColor Cyan
    Write-Host "  git commit --allow-empty -m 'TEST-123 | test commit'"
    Write-Host ""
} catch {
    Write-Host " ERROR: Error installing hooks: $_" -ForegroundColor Red
    exit 1
}