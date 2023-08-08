# azure-cli-bug-repro
Minimum viable reproduction for bug in Azure CLI / Azure SDK for Python - linked issues: https://github.com/Azure/azure-cli/issues/27111 https://github.com/Azure/azure-sdk-for-python/issues/31493


**Description:**
DefaultAzureCredential runs through a bunch of options, including AzureCliCredential.

When it reaches [this line](https://github.com/Azure/azure-sdk-for-python/blob/c4c18a7b427633c0519016d762dc141ae743e41b/sdk/identity/azure-identity/azure/identity/_credentials/azure_cli.py#L176) within AzureCliCredential, it will *always* fail the timeout with an outdated software version, as the cli prompt returned by `az account get-access-token --output json --resource <whatever>` embedded within that page will always return the following which requires a user response:
```
New Azure CLI version available. Running 'az upgrade' to update automatically.
This command is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
Your current Azure CLI version is 2.50.0. Latest version available is 2.51.0.
Please check the release notes first: https://docs.microsoft.com/cli/azure/release-notes-azure-cli
Do you want to continue? (Y/n):
```

**Steps to reproduce:**
- Replace key_vault_url and secret_name within [x/function_app.py](function_app.py) with some legitimate values.
- Use `func start` to start
- Optionally, attach a debugger of your choice to the process and watch the call to `return subprocess.check_output(args, **kwargs)` `venv/lib/python3.10/site-packages/azure/identity/_credentials/azure_cli.py` - [github link to specific line](https://github.com/Azure/azure-sdk-for-python/blob/c4c18a7b427633c0519016d762dc141ae743e41b/sdk/identity/azure-identity/azure/identity/_credentials/azure_cli.py#L195) 
- Run `curl  http://localhost:7071/api/hello` to trigger the http function
- Read your logs for the following string: AzureCliCredential: Failed to invoke the Azure CLI
