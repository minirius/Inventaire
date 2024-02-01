import json

def addnewitemtodatabase(id,name,amount,price,category):
    with open("database.json","r") as database:
        actualdata=json.load(database)
    actualdata.append({"id":id,"name":name,"amount":amount,"price":price,"category":category})
    datatodump = json.dumps(actualdata, indent=4)
    with open("database.json","w") as outfile:
        outfile.write(datatodump)
    
#addnewitemtodatabase(1,"test2",15,2,"thing")