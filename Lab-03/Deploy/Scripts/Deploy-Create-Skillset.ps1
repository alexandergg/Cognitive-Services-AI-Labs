#! /usr/bin/pwsh
Function CreateSkillset($resourceGroupName, $skillsetName, $cognitiveServiceName)
{
    $azSearchService = Get-AzSearchService -ResourceGroupName $resourceGroupName
    $azSearchAdminApiKey = Get-AzSearchAdminKeyPair -ResourceGroupName $resourceGroupName -ServiceName $azSearchService.name

    $headers = @{
    'api-key' = $azSearchAdminApiKey.Primary
    'Content-Type' = 'application/json'
    'Accept' = 'application/json' }

    $keys = Get-AzCognitiveServicesAccountKey -ResourceGroupName $resourceGroupName -name $cognitiveServiceName

    $a = Get-Content -Raw -Path skillsets/imageskillset.json | Convertfrom-json
    $a.name = $skillsetName
    $a.cognitiveServices.description = $cognitiveServiceName
    $a.cognitiveServices.key = $keys.Key1

    $body = ConvertTo-Json -InputObject $a -Depth 10
    $url = "https://{0}.search.windows.net/skillsets/{1}?api-version=2019-05-06" -f ($azSearchService.name, $skillsetName)
    Invoke-RestMethod -Uri $url -Headers $headers -Method Put -Body $body | ConvertTo-Json
}