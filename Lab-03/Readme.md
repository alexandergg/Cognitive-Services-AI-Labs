## Azure Search Configuration

### Azure Search: Create Index, Indexer, skillset and datasource

When you have your function app and running you should think that actually you have a function that Azure Search Skillset can consume it (Custom SKillset).

So, how can you used it? How can we start indexing information at the Index?

##### Step 1: Execute powershell script
For this step you will need to execute powershell script on `/Deploy/` folder:

```
.\DeployUnifiedAzSearch.ps1
```

- `subscriptionId`: Id of your subscription where you are going to deploy your resource group `Required`
- `subscriptionName`: Name of your subscription where you are going to deploy your resource group `Required`
- `resourceGroupName`: The name of your resource group where all infrastructure will be created `Required`
- `azsearchDatasourceName`: The name of the Azure Search Datasource you want it to create `Required`
- `skillsetName`: The name of the Azure Search Skillset you want it to create `Required`
- `cognitiveServiceName`: The name of your cognitive services `Required`
- `azSearchIndexName`: The name of the Azure Search Index you want it to create `Required`
- `indexerName`: The name of the Azure Search Indexer you want it to create `Required`

>Note: This file is a unified file. It will execute four powershells scripts during the execution:

    Deploy-Create-Datasource.ps1
    Deploy-Create-Skillset.ps1
    Deploy-Create-Index.ps1
    Deploy-Create-Indexer.ps1
