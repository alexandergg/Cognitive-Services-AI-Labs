#! /usr/bin/pwsh
param(
    [parameter(Mandatory=$true)][string]$resourceGroup,
    [parameter(Mandatory=$true)][string]$location,
    [parameter(Mandatory=$true)][string]$resourcePrefixName,
    [parameter(Mandatory=$true)][string]$subscription
)

Write-Host "Login in your account" -ForegroundColor Yellow
az login

Write-Host "Choosing your subscription" -ForegroundColor Yellow
az account set --subscription $subscription

Push-Location $($MyInvocation.InvocationName | Split-Path)
Push-Location Scripts

. "./Deploy-ARM.ps1"
DeployARM -resourceGroup $resourceGroup -location $location -resourcePrefixName $resourcePrefixName

$storageName = $(az resource list --resource-group $resourceGroup --resource-type Microsoft.Storage/storageAccounts -o json | ConvertFrom-Json)[0].name
$containerName = "$resourcePrefixName-day1"

. "./Deploy-Publish-Content"
PublishContent -Content.ps1 -resourceGroup $resourceGroup -storageName $storageName -containerName $containerName

Pop-Location
Pop-Location