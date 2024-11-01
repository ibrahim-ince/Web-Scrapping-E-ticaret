from django.shortcuts import render
import pymongo

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
finalCol = myDB["final"]

# # Create your views here.

markalar = []
ctr = 0

for m in finalCol.find():
    for m2 in markalar:
        if m['Marka'] == m2:
            ctr = 1
            break
    if ctr == 0:
        markalar.append(m['Marka'])
    else:
        ctr = 0

urunListe = finalCol.find()

def home(request):
    data = {
        "marka": markalar,
        "urunler": urunListe
    }
    return render(request, "index.html", data)

def detay(request, id):
    data = {
        "id": id
    }
    return render(request, "detay.html", data)





