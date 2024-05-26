import json
import sqlite3

conn = sqlite3.connect('Inventory.db')

with open('invoices.json', 'r') as inFile:
    invoices = json.load(inFile)['QueryResponse']['Invoice']

for invoice in invoices:
    for item in invoice['Line']:
        if item['DetailType'] == 'SalesItemLineDetail' and item['SalesItemLineDetail']['ItemRef']['value'] != 'SHIPPING_ITEM_ID':
            itemName = item['SalesItemLineDetail']['ItemRef']['name']
            itemID = item['SalesItemLineDetail']['ItemRef']['value']
            itemQty = item['SalesItemLineDetail']['Qty']

            conn.execute('UPDATE Items SET QtySold = QtySold + ? WHERE Id = ?', (itemQty, itemID))
            print(f'{itemQty}x {itemName} - {itemID}')

conn.commit()
conn.close()

# with open('items.json', 'r') as inFile:
#     items = json.load(inFile)['Item']
#
#
# for item in items:
#     print(item['Id'], item['Name'])
#     conn.execute('INSERT INTO Items VALUES (?, ? ,?)', (item['Id'], item['Name'], 0))
#
# conn.commit()
# conn.close()