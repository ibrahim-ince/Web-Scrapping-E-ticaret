import pymongo
from bs4 import BeautifulSoup
import requests

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["vatanpcUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 1
deneme = 0
while sayfa <= 3:
    print(str(sayfa) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.vatanbilgisayar.com/notebook/?page=" + str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
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

        try:
            try:
                prc = soup1.find("p", attrs={"id": "webSpecial"}).text.replace("TL", "").strip()
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
        except:
            print("marka cekilemedi")

        try:
            ozlk = soup1.find("div", attrs={"id": "urun-ozellikleri"}).text.split("\n\n\n\n\n")
        except:
            print("ozellikler cekilemedi")

        for bul in ozlk:
            try:
                if bul.find("İşletim Sistemi") != -1:
                    isletimSis = bul[bul.rfind("\n") + 1:].strip()
            except: print("isletim sistemi cekilemedi")    
            try:
                if bul.find("İşlemci Teknolojisi") != -1:
                    islemciTipi = bul[bul.rfind("\n") + 1:].strip()
            except: print("islemci tipi cekilemedi")
            try:    
                if bul.find("İşlemci Nesli") != -1:
                    islemciNesli = bul[bul.rfind("\n") + 1:].strip()
            except: print("islemci nesi cekilemedi")
            try:   
                if bul.find("Ram (Sistem Belleği)") != -1:
                    ram = bul[bul.rfind("\n") + 1:].replace("GB", "").strip()
            except: print("ram cekilemedi")
            try:
                if bul.find("Disk Kapasitesi") != -1:
                    bul = bul.replace("İzle", "").strip()
                    ssd = bul[bul.rfind("\n") + 1:].replace("GB", "").strip()
            except: print("ssd cekilemedi")
            try:
                if bul.find("Ekran Boyutu") != -1:
                    ekranBoyutu = bul[bul.rfind("\n") + 1:].replace("inch", "").strip()
            except: print("ekran boyutu cekilemedi")
        
        tempDict = {'Baslik': baslik, 'Marka': marka, 'Fiyat': prc, 'Isletim Sistemi': isletimSis,'Islemci Tipi': islemciTipi, 'Islemci Nesli': islemciNesli, 'Ram': ram, 'SSD Boyutu': ssd, 'Ekran Boyutu': ekranBoyutu, 'urunLinki': link}
        print(myCol.insert_one(tempDict))
       