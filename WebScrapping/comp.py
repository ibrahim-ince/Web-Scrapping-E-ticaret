import pymongo

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
hbCol = myDB["hbUrunler"]
tkCol = myDB["teknosaUrunler"]
tyCol = myDB["trendyolUrunler"]
vcCol = myDB["vatanpcUrunler"]
finalCol = myDB["final"]
print(finalCol.delete_many({}).deleted_count)

sameList = []
sayac = 0
ctr = 0

for x in hbCol.find():
    for y in tkCol.find({'Marka': x['Marka'], 'Isletim Sistemi': x['Isletim Sistemi'], 'Islemci Tipi': x['Islemci Tipi'], 'Islemci Nesli': x['Islemci Nesli'], 'Ram': x['Ram'], 'SSD Boyutu': x['SSD Boyutu'], 'Ekran Boyutu': x['Ekran Boyutu']}):
        for z in tyCol.find({'Marka': x['Marka'], 'Isletim Sistemi': x['Isletim Sistemi'], 'Islemci Tipi': x['Islemci Tipi'], 'Islemci Nesli': x['Islemci Nesli'], 'Ram': x['Ram'], 'SSD Boyutu': x['SSD Boyutu'], 'Ekran Boyutu': x['Ekran Boyutu']}):
            for k in vcCol.find({'Marka': x['Marka'], 'Isletim Sistemi': x['Isletim Sistemi'], 'Islemci Tipi': x['Islemci Tipi'], 'Islemci Nesli': x['Islemci Nesli'], 'Ram': x['Ram'], 'SSD Boyutu': x['SSD Boyutu'], 'Ekran Boyutu': x['Ekran Boyutu']}):
                for f in finalCol.find():
                    if f['hbLink'] == x['urunLinki']:
                        ctr = 1
                        break
                if ctr == 0:
                    tempDict = {'Baslik': x['Baslik'], 'Marka': x['Marka'], 'Puan': x['Puan'], 'IsletimSistemi': x['Isletim Sistemi'], 'IslemciTipi': x['Islemci Tipi'], 'IslemciNesli': x['Islemci Nesli'], 'Ram': x['Ram'], 'SSDBoyutu': x['SSD Boyutu'], 'EkranBoyutu': x['Ekran Boyutu'], 'fotoUrl': x['fotoUrl'], 'hbFiyat': x['Fiyat'], 'hbLink': x['urunLinki'], 'tkFiyat': y['Fiyat'], 'tkLink': y['urunLinki'], 'tyFiyat': z['Fiyat'], 'tyLink': z['urunLinki'], 'vcFiyat': k['Fiyat'], 'vcLink': k['urunLinki']}
                    sayac += 1
                    print(f"{sayac}. eşleşme")
                    print(finalCol.insert_one(tempDict))
                else:
                    ctr = 0
                    break