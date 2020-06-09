#! /usr/bin/pwsh
Function PublishContent($resourceGroup, $storageName, $containerName)
{
    Push-Location $($MyInvocation.InvocationName | Split-Path)

    Write-Host "Begining the Uploading model files to Storage: $storageName" -ForegroundColor Yellow
    . "./Deploy-Dataset-Azure" 
    DeployDataset -Azure.ps1 -resourceGroup $resourceGroup -storageName $storageName -containerName $containerName
    Write-Host "Files uploaded..."

    Pop-Location
}