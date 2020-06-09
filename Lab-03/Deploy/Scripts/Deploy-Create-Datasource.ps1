#! /usr/bin/pwsh
Function CreateDatasource($resourceGroupName, $azsearchDatasourceName, $storageAccountName, $storageContainerName)
{
    $azSearchService = Get-AzSearchService -ResourceGroupName $resourceGroupName
    $azSearchAdminApiKey = Get-AzSearchAdminKeyPair -ResourceGroupName $resourceGroupName -ServiceName $azSearchService.name
    
    $headers = @{
    'api-key' = $azSearchAdminApiKey.Primary
    'Content-Type' = 'application/json' 
    'Accept' = 'application/json' }

    $storageAccountKey = (Get-AzStorageAccountKey -ResourceGroupName $resourceGroupName `
                        -Name $storageAccountName).Value[0]
    
    $storageConnectionString = "DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1}" `
            -f ($storageAccountName, $storageAccountKey)

    $a = Get-Content -Raw -Path datasource/datasource.json | Convertfrom-json
    $a.name = $azsearchDatasourceName
    $a.description = $azsearchDatasourceName
    $a.type = "azureblob"
    $a.credentials.connectionString = $storageConnectionString
    $a.container.name = $storageContainerName
    
    $body = ConvertTo-Json -InputObject $a -Depth 10
    $url = "https://{0}.search.windows.net/datasources/{1}?api-version=2019-05-06" `
            -f ($azSearchService.name, $azsearchDatasourceName)
    Invoke-RestMethod -Uri $url -Headers $headers -Method Put -Body $body | ConvertTo-Json
}