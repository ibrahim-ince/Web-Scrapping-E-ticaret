import pymongo
from bs4 import BeautifulSoup
import requests

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["trendyolUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 1
deneme = 0
while sayfa <= 2:
    print(str(sayfa) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.trendyol.com/laptop-x-c103108" + "?pi=" + str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
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

    st1 = soup.find("div", attrs={"class": "prdct-cntnr-wrppr"})
    st2 = st1.find_all("div", attrs={"class": "p-card-wrppr with-campaign-view"})
    urunS = 0
    for details in st2:
        urunS += 1
        print(f"{urunS}. urun cekiliyor")
        lb = "https://www.trendyol.com/"
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
            prc = soup1.find("span", attrs={"class": "prc-dsc"}).text.replace("TL", "").strip()
        except:
            print("fiyat cekilemedi")
        
        try:
            baslik = soup1.find("h1", attrs={"class": "pr-new-br"}).text.strip()
        except:
            print("baslik cekilemedi")

        try:
            t = ls
            t = t.replace("/", "", 1)
            ti = t.find("/")
            marka = (t[0:ti]).title()
        except:
            print("marka cekilemedi")
        
        try:
            ozlk1 = soup1.find("ul", attrs={"class": "detail-attr-container"})
            ozlk2 = ozlk1.find_all("li", attrs={"class": "detail-attr-item"})
        except:
            print("ozellikler cekilemedi")

        for ozlk in ozlk2:
            try:
                if ozlk.text.find("İşletim Sistemi") == 0:
                    isletimSis = ozlk.text[16:]
            except: print("isletim sistemi cekilemedi")    
            try:
                if ozlk.text.find("İşlemci Tipi") == 0:
                    islemciTipi = ozlk.text[13:]
            except: print("islemci tipi cekilemedi")
            try:
                if ozlk.text.find("İşlemci Nesli") == 0:
                    islemciNesli = ozlk.text[14:]
            except: print("islemci nesli cekilemedi")
            try:
                if ozlk.text.find("Ram (Sistem Belleği)") == 0:
                    ram = ozlk.text[21:].replace("GB", "").strip()
            except: print("ram cekilemedi")
            try:
                if ozlk.text.find("SSD Kapasitesi") == 0:
                    ssd = ozlk.text[15:].replace("GB", "").strip()
            except: print("ssd cekilemedi")
            try:
                if ozlk.text.find("Ekran Boyutu") == 0:
                    ekranBoyutu = ozlk.text[13:].replace("inç", "").strip()
            except: print("ekran boyutu cekilemedi")

        tempDict = {'Baslik': baslik, 'Marka': marka, 'Fiyat': prc, 'Isletim Sistemi': isletimSis,'Islemci Tipi': islemciTipi, 'Islemci Nesli': islemciNesli, 'Ram': ram, 'SSD Boyutu': ssd, 'Ekran Boyutu': ekranBoyutu, 'urunLinki': link}
        print(myCol.insert_one(tempDict))
