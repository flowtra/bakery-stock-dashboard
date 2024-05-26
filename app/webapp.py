from flask import Flask, render_template, request, redirect, url_for
import pymongo
from app.mongo_funcs import updateInvoices, connCollection
app = Flask(__name__)


@app.route('/')
def index():
    client = pymongo.MongoClient(
        "mongodb+srv://doadmin:REDACTED@REDACTED.mongo.ondigitalocean.com/admin?tls=true&authSource=admin")

    db = client.get_database('HR23')
    coll = db.get_collection('Products')
    row_data = list(coll.find().sort('orders', -1))
    # cur = conn.execute('SELECT Id, Name, QtySold, QtyAvail FROM Items WHERE QtySold != 0 ORDER BY QtySold DESC ')
    # row_data = cur.fetchall()

    return render_template('index.html', table_data=row_data)


@app.route('/updateQty', methods=['POST'])
def updateQty():

    qtyToAdd = request.form['qtyToAdd']
    ProductId = request.form['id']
    print(f'Received request to add {qtyToAdd} to {ProductId}')
    client = pymongo.MongoClient(
        "mongodb+srv://doadmin:REDACTED@REDACTED.mongo.ondigitalocean.com/admin?tls=true&authSource=admin")

    db = client.get_database('HR23')
    coll = db.get_collection('Products')
    coll.update_one({"ProductId": ProductId}, {'$inc': {"Stock": int(qtyToAdd), "balance": int(qtyToAdd)}})
    print('added')

    return redirect(url_for('index'))


@app.route('/refreshInvoices', methods=['POST'])
def refreshInvoices():
    if updateInvoices(connCollection('HR23', 'Invoices')):
        return redirect(url_for('index'))

# app.run()