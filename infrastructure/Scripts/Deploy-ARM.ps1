#! /usr/bin/pwsh
Function DeployARM($resourceGroup, $location, $resourcePrefixName)
{
    Pop-Location
    $deployment = 'deployment.json'

    Write-Host "--------------------------------------------------------" -ForegroundColor Yellow
    Write-Host "Deploying infrastructure" -ForegroundColor Yellow
    Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow

    $rg = $(az group show -n $resourceGroup -o json | ConvertFrom-Json)

    if (-not $rg) {
        Write-Host "$resourceGroup does not exist"
    } else {
        Write-Host "Begining the ARM deployment for Tessi Workshop resources " -ForegroundColor Yellow
        az group deployment create -g $resourceGroup --template-file $deployment --parameters resourcePrefixName=$resourcePrefixName
        Write-Host "ARM uploaded..."    
    }

    Push-Location Scripts
}