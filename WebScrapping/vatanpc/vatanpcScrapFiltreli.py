import pymongo
from bs4 import BeautifulSoup
import requests

# dMarka = open("vatanpcMarka.txt", "w")
# dFiyat = open("vatanpcFiyat.txt", "w")
# dIslSis = open("vatanpcIslSis.txt", "w")
# dTipi = open("vatanpcTipi.txt", "w")
# dNesli = open("vatanpcNesli.txt", "w")
# dRam = open("vatanpcRam.txt", "w")
# dSsd = open("vatanpcSsd.txt", "w")
# dEkran = open("vatanpcEkran.txt", "w")
# dLink = open("vatanpcLink.txt", "w")

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["vatanpcUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 1
deneme = 0
while sayfa <= 20:
    print(str(sayfa) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.vatanbilgisayar.com/hp-dell-casper-asus-apple-acer-huawei-lenovo-msi/notebook/?page=" + str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
    except:
        print("timeout")
        if deneme < 2:
            deneme += 1
            print(f"{deneme}. kez tekrar deneniyor...")
            continue
        else:
            print("diger sayfa...")
            sayfa += 1
            deneme = 0
            continue
    print(r)
    deneme = 0
    sayfa += 1
    soup = BeautifulSoup(r.content, 'lxml')

    st1 = soup.find("div", attrs={"id": "productsLoad"})
    st2 = st1.find_all("div", attrs={"class": "product-list product-list--list-page"})
    urunS = 0
    for details in st2:
        urunS += 1
        print(f"{urunS}. urun cekiliyor")
        lb = "https://www.vatanbilgisayar.com"
        ls = details.a.get("href")
        link = lb + ls

        try:
            r1 = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        except:
            print("timeout")
            continue
        print(r1)
        deneme = 0
        soup1 = BeautifulSoup(r1.content, "lxml")
        
        prc = "---"
        baslik = "---"
        marka = "---"
        isletimSis = "---"
        islemciTipi = "---"
        islemciNesli = "---"
        ram = "---"
        ssd = "---"
        ekranBoyutu = "---"
        iptal = 0

        try:
            try:
                prc = soup1.find("p", attrs={"id": "webSpecial"}).text.replace("TL", "").strip().replace(".", "").replace(",", "")
                print("webe ozel fiyat!")
            except:
                prc = soup1.find("span", attrs={"class": "product-list__price"}).text.replace("TL", "").strip()
        except:
            print("fiyat cekilemedi")
        
        try:
            baslik = soup1.find("h1", attrs={"class": "product-list__product-name"}).text.strip()
        except:
            print("baslik cekilemedi")
        
        try:
            marka = baslik[:baslik.find(" ")]
            if marka == "Hp" or marka == "Victus" or marka == "Omen": marka = "HP"
            if marka == "Macbook": marka = "Apple"
        except:
            print("marka cekilemedi")

        try:
            ozlk = soup1.find("div", attrs={"id": "urun-ozellikleri"}).text.split("\n\n\n\n\n")
        except:
            print("ozellikler cekilemedi")

        for bul in ozlk:
            try:
                if bul.find("İşletim Sistemi") != -1:
                    isletimSis = bul[bul.rfind("\n") + 1:].strip().replace("11", "").replace("10", "").replace("64", "").replace("bit", "").replace("Bit", "").replace("Pro", "").replace("Home", "").replace(" ", "").strip()
                    if isletimSis == "Win": isletimSis = "Windows"
            except: print("isletim sistemi cekilemedi")    
            try:
                if bul.find("İşlemci Teknolojisi") != -1:
                    islemciTipi = bul[bul.rfind("\n") + 1:].replace("™", "").strip()
                    if islemciTipi.find("Core") != -1: islemciTipi = "Intel " + islemciTipi
                    if islemciTipi.find("Ryzen") != -1: islemciTipi = "AMD " + islemciTipi
            except: print("islemci tipi cekilemedi")
            try:    
                if bul.find("İşlemci Nesli") != -1:
                    islemciNesli = bul[bul.rfind("\n") + 1:].replace("AMD Ryzen", "").replace("Intel", "").strip().replace(" ", "")
                    if islemciNesli == "Belirtilmemiş":
                        if marka == "Apple":
                            islemciNesli = "M1"
                        else: iptal = 1
            except: print("islemci nesi cekilemedi")
            try:   
                if bul.find("Ram (Sistem Belleği)") != -1:
                    ram = bul[bul.rfind("\n") + 1:bul.rfind("\n") + 3].replace("GB", "").strip()
            except: print("ram cekilemedi")
            try:
                if bul.find("Disk Kapasitesi") != -1:
                    bul = bul.replace("İzle", "").strip()
                    ssd = bul[bul.rfind("\n") + 1:bul.rfind("\n") + 4].replace("GB", "").strip()
                    if ssd == "Yok": iptal = 1
                    if ssd.find("T") != -1:
                        ssd = ssd.replace("T", "").strip()
                        carpici = int(ssd)
                        ssd = ssd + "0" + str(carpici * 24)
            except: print("ssd cekilemedi")
            try:
                if bul.find("Ekran Boyutu") != -1:
                    ekranBoyutu = bul[bul.rfind("\n") + 1:].replace("inch", "").strip()
            except: print("ekran boyutu cekilemedi")
        
        if iptal == 1: continue
        tempDict = {'Baslik': baslik, 'Marka': marka, 'Fiyat': prc, 'Isletim Sistemi': isletimSis,'Islemci Tipi': islemciTipi, 'Islemci Nesli': islemciNesli, 'Ram': ram, 'SSD Boyutu': ssd, 'Ekran Boyutu': ekranBoyutu, 'urunLinki': link}
        print(myCol.insert_one(tempDict))

#         dMarka.write(tempDict['Marka'])
#         dMarka.write("\n")
#         dFiyat.write(tempDict['Fiyat'])
#         dFiyat.write("\n")
#         dIslSis.write(tempDict['Isletim Sistemi'])
#         dIslSis.write("\n")
#         dTipi.write(tempDict['Islemci Tipi'])
#         dTipi.write("\n")
#         dNesli.write(tempDict['Islemci Nesli'])
#         dNesli.write("\n")
#         dRam.write(tempDict['Ram'])
#         dRam.write("\n")
#         dSsd.write(tempDict['SSD Boyutu'])
#         dSsd.write("\n")
#         dEkran.write(tempDict['Ekran Boyutu'])
#         dEkran.write("\n")
#         dLink.write(tempDict['urunLinki'])
#         dLink.write("\n")
        
# dLink.close()
# dMarka.close()
# dFiyat.close()
# dIslSis.close()
# dTipi.close()
# dNesli.close()
# dRam.close()
# dSsd.close()
# dEkran.close()
       