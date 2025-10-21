Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Logic Apps Tools Setup (Windows)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
$nodeCmd = $null
foreach ($cmd in @('node')) {
    try {
        $version = & $cmd --version 2>&1
        if ($version) {
            $nodeCmd = $cmd
            break
        }
    } catch { continue }
}

if (-not $nodeCmd) {
    Write-Host " ERROR: Node.js not installed" -ForegroundColor Red
    Write-Host "Install from: https://nodejs.org/"
    exit 1
}
Write-Host " SUCCESS: Node.js: $(node --version)" -ForegroundColor Green

# Check .NET
try {
    $dotnetVersion = dotnet --version 2>$null
    Write-Host " SUCCESS: .NET Core: $dotnetVersion" -ForegroundColor Green
} catch {
    Write-Host " WARNING: .NET Core SDK not installed" -ForegroundColor Yellow
    Write-Host "Install from: https://dotnet.microsoft.com/download/dotnet/3.1"
}

# Check/Install Azure Functions Core Tools
try {
    $funcVersion = func --version 2>$null
    Write-Host " SUCCESS: Azure Functions Core Tools: $funcVersion" -ForegroundColor Green
} catch {
    Write-Host " WARNING: Azure Functions Core Tools not found" -ForegroundColor Yellow
    Write-Host "Installing..."
    npm install -g azure-functions-core-tools@3 --unsafe-perm true
    
    try {
        $funcVersion = func --version 2>$null
        Write-Host " SUCCESS: Azure Functions Core Tools installed" -ForegroundColor Green
    } catch {
        Write-Host " WARNING: Installation failed" -ForegroundColor Yellow
    }
}

# Check/Install Azurite
try {
    azurite --version 2>$null | Out-Null
    Write-Host " SUCCESS: Azurite found" -ForegroundColor Green
} catch {
    Write-Host ""
    $response = Read-Host "Install Azurite (local storage emulator)? (Y/n)"
    if ($response -notmatch "^[Nn]$") {
        npm install -g azurite
        try {
            azurite --version 2>$null | Out-Null
            Write-Host " SUCCESS: Azurite installed" -ForegroundColor Green
        } catch {
            Write-Host " WARNING: Installation failed" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "   SUCCESS: Logic Apps Tools Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open VS Code"
Write-Host "  2. Install extensions: Azure Logic Apps (Standard)"
Write-Host "  3. Create local.settings.json"
Write-Host "  4. Run: func start"
Write-Host ""