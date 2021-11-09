import json
from urllib.request import urlopen

# def getCountry(ipAddress):
#     response = urlopen('http://freegeoip.net/json/'+ipAddress).read().decode('utf-8')
#     responseJson = json.loads(response)
#     return responseJson.get('country_code')

# print(getCountry('50.78.253.58'))

# https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId=203517

# def getProductInfo(ProductID):
#     response = urlopen('https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId='+ProductID).read().decode('utf-8')
#     responseJson = json.loads(response)
#     return responseJson.get('country_code')
    
# print(getProductInfo('203517'))

jsonString = '{"arrayOfNums":[{"number":0},{"number":1},{"number":2}],"arrayOfFruits":[{"fruit":"apple"},{"fruit":"banana"},{"fruit":"pear"}]}'
jsonObj = json.loads(jsonString)

print(jsonObj.get('arrayOfNums'))
print(jsonObj.get('arrayOfNums')[1])
print(jsonObj.get('arrayOfNums')[1].get('number') + jsonObj.get('arrayOfNums')[2].get('number'))
print(jsonObj.get('arrayOfFruits')[2].get('fruit'))