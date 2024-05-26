import requests
import json
headers = {
    "Authorization": "Bearer REDACTED",
    "Accept": "application/json"
}

with open('toUpdate_shippingCost.txt', 'r') as inFile:
    arr = inFile.read().splitlines()

for line in arr:
    invoiceNo, shipCost = line.split(',')

    query = f"select * from Invoice where DocNumber='{invoiceNo}'"
    dict = []
    r = requests.get(f'https://quickbooks.api.intuit.com/v3/company/REDACTED/query?query={query}&minorversion=65', headers=headers)
    invoiceJson = r.json()
    invoiceId = invoiceJson['QueryResponse']['Invoice'][0]['Id']
    invoiceSyncToken = invoiceJson['QueryResponse']['Invoice'][0]['SyncToken']
    invoiceLines = invoiceJson['QueryResponse']['Invoice'][0]['Line']
    for x in invoiceLines:
        dict.append(x)

    toAdd = {
                "Amount": int(shipCost),
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                    "ItemRef": {
                        "value": "SHIPPING_ITEM_ID"
                    }
                }
            }

    dict.append(toAdd)

    data = {
        "SyncToken": f"{invoiceSyncToken}",
        "Id": f"{invoiceId}",
        "sparse": 'true',
        "Line": dict
    }
    r = requests.post('https://quickbooks.api.intuit.com/v3/company/REDACTED/invoice?minorversion=65', json=data, headers=headers)
    print(r.text)
    print(f'Added ${shipCost} to {invoiceNo}')
