import pymongo
import json

def connCollection(db, coll_p):
    client = pymongo.MongoClient("mongodb+srv://doadmin:REDACTED@REDACTED.mongo.ondigitalocean.com/admin?tls=true&authSource=admin")

    db = client.get_database(db)
    coll = db.get_collection(coll_p)
    #
    # db = client.get_database("HR23")
    # coll = db.get_collection("Products")
    return coll


def getRefreshAccessTokens():

    coll = connCollection('HR23', 'Tokens')
    token = coll.find_one()

    return token


def setRefreshAccessTokens(_input):

    coll = connCollection('HR23', 'Tokens')
    coll.delete_many({})
    try:
        coll.insert_one(_input)
        return True
    except Exception as e:
        print(e)
        return False


from app import main

def addItemList(coll, itemFile):

    # with open(itemFile, 'r') as inFile:
    #     items = json.load(inFile)['Item']

    with open('items.json', 'r') as inFile:
        items = json.load(inFile)['Item']
    try:
        for item in items:
            print(item['Id'], item['Name'])
            coll.insert_one({"ProductId": item['Id'], "Name": item['Name'], "Stock": 0})
        return True
    except:
        return False

def updateInvoices(coll):
    try:
        main.refresh_token()
        invoices = json.loads(main.getAllInvoices())
        coll.delete_many({})
        coll.insert_many(invoices["QueryResponse"]["Invoice"])
        updateStock(invoices["QueryResponse"]["Invoice"])
        return True
    except:
        return False

def updateStock(invoices):
    coll = connCollection('HR23', 'Products')
    coll.update_many({}, [{'$set': {'orders': 0, 'balance': '$Stock'}}])
    for invoice in invoices:
        for item in invoice['Line']:
            if item['DetailType'] == 'SalesItemLineDetail' and item['SalesItemLineDetail']['ItemRef'][
                'value'] != 'SHIPPING_ITEM_ID':
                itemName = item['SalesItemLineDetail']['ItemRef']['name']
                itemID = item['SalesItemLineDetail']['ItemRef']['value']
                itemQty = item['SalesItemLineDetail']['Qty']

                coll.update_one({'ProductId': itemID}, {'$inc': {'balance': -itemQty, 'orders': itemQty}})

                # print(f'{itemQty}x {itemName} - {itemID}')

#
# coll = connCollection('HR23', 'Invoices')
# updateInvoices(coll)
