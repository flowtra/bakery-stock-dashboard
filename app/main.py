import json

import requests
from app.mongo_funcs import getRefreshAccessTokens, setRefreshAccessTokens
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes

def refresh_token():
    tokens = getRefreshAccessTokens()
    headers = {
        'Authorization': 'Basic REDACTED',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }
    data = f'grant_type=refresh_token&refresh_token={tokens["refresh_token"]}'
    r = requests.post('https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer', headers=headers, data=data)
    try:
        status = setRefreshAccessTokens(json.loads(r.text))
        if status:
            return r.json()
        else:
            return False
    except Exception as e:
        print(e)
        return False


def getCustomerData(custID):
    url = f'https://quickbooks.api.intuit.com/v3/company/REDACTED/customer/{custID}?minorversion=65'
    headers = {
        'Authorization': f'Bearer {getRefreshAccessTokens()["access_token"]}',
        'Accept': 'application/json;charset=UTF-8',
        'Content-type': '*/*'
    }
    r = requests.get(url, headers=headers)
    return r.json()

def getCustomerPhone_online(custID):
    custData = getCustomerData(custID)['Customer']
    print(custData)
    while True:
        try:
            return custData['Mobile']["FreeFormNumber"]
        except:
            return custData['PrimaryPhone']["FreeFormNumber"]


def getCustomerPhone_offline(custID):
    with open('customers.json', 'r') as inFile:
        custData = json.load(inFile)
    while True:
        for cust in custData['Customer']:
            if cust['Id'] == custID:
                try:
                    return cust['Mobile']["FreeFormNumber"]
                except:
                    try:
                        return cust['PrimaryPhone']["FreeFormNumber"]
                    except:
                        return ''

def getAllInvoices():
    url = 'https://quickbooks.api.intuit.com/v3/company/REDACTED/query?query=select * from Invoice MAXRESULTS 1000&minorversion=65'
    headers = {
        'Authorization': f'Bearer {getRefreshAccessTokens()["access_token"]}',
        'Accept': 'application/json;charset=UTF-8',
        'Content-type': '*/*'
    }
    r = requests.get(url, headers=headers)
    return r.text


if __name__ == '__main__':
    # access_token = refresh_token()["access_token"]
    tokens = refresh_token()
    access_token = tokens["access_token"]

    print(f'Welcome, your access token has been refreshed!\nAccess token: {access_token}')


    while True:
        try:
            opt = int(input(
                '''
                What would you like to do?
                [1] Refresh Access Token
                [2] Get all Invoices
                '''
            ))
        except ValueError:
            print('Please enter a valid integer.')
            continue
        if opt == 1:
            tokens = refresh_token()
            access_token = tokens["access_token"]

            print('Your access token has been refreshed.')
        elif opt == 2:
            invoices = getAllInvoices()
            with open('invoices.json', 'w') as outFile:
                outFile.write(str(invoices))
            print(invoices)