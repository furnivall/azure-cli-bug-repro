import azure.functions as func
import requests
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Create a DefaultAzureCredential instance to authenticate
# using the managed identity of the Azure Function
credential = DefaultAzureCredential()
key_vault_url = "https://your_key_vault.vault.azure.net/"
secret_name = "your-secret-name"
# Create a SecretClient to interact with the Azure Key Vault
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
app = func.FunctionApp()

@app.function_name(name="AzureTrigger")
@app.route(route="hello")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    requests.post(secret_client.get_secret(secret_name), json={"text": "Hello from Azure!"})
    return func.HttpResponse("AzureTrigger function processed a request!")
