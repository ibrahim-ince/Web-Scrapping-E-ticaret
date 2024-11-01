import pymongo
from bs4 import BeautifulSoup
import requests

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["teknosaUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 0
deneme = 0
while sayfa < 2:
    print(str(sayfa) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.teknosa.com/laptop-notebook-c-116004?s=%3Arelevance&page=" + str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
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

    st1 = soup.find("div", attrs={"class": "plp-body"})
    st2 = st1.find("div", attrs={"class": "products"})
    st3 = st2.find_all("div", attrs={"id": "product-item"})
    urunS = 0
    for details in st3:
        urunS += 1
        print(f"{urunS}. urun cekiliyor")
        lb = "https://www.teknosa.com"
        ls = details.get("data-product-url")
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
            prc = soup1.find("div", attrs={"class": "prd-prc2"}).text.replace("TL", "").strip()
        except:
            print("fiyat cekilemedi")
        
        try:
            baslik = soup1.find("h1", attrs={"class": "pdp-title"}).text.strip()
        except:
            print("baslik cekilemedi")

        try:
            marka = baslik[:baslik.find(" ")]
        except:
            print("marka cekilemedi")
        
        try:
            ozlk1 = soup1.find("div", attrs={"class": "ptf-body"})
            ozlk2 = ozlk1.find_all("table")
        except:
            print("ozellikler cekilemedi")

        for bul in ozlk2:
                try:
                    ozlk = bul.find_all("tr")
                except:
                    continue
                list1 = ozlk[0].text.strip().split("\n")
                list2 = ozlk[1].text.strip().split("\n")
                if list1 == [''] or list2 == ['']: break
                try:
                    if "İşletim Sistemi Yazılımı" in list1:
                        isletimSis = list2[list1.index("İşletim Sistemi Yazılımı")]
                except: print("isletim sistemi cekilemedi")
                try:
                    if "İşlemci" in list1:
                        islemciTipi = list2[list1.index("İşlemci")]
                except: print("islemci tipi cekilemedi")
                try:
                    if "İşlemci Nesli" in list1:
                        islemciNesli = list2[list1.index("İşlemci Nesli")]
                except: print("islemci nesli cekilemedi")
                try:
                    if "Ram" in list1:
                        ram = list2[list1.index("Ram")]
                except: print("ram cekilemedi")
                try:
                    if "SSD Kapasitesi" in list1:
                        ssd = list2[list1.index("SSD Kapasitesi")]
                except: print("ssd cekilemedi")
                try:
                    if "Ekran Boyutu" in list1:
                        ekranBoyutu = list2[list1.index("Ekran Boyutu")]
                except: print("ekran boyutu cekilemedi")

        tempDict = {'Baslik': baslik, 'Marka': marka, 'Fiyat': prc, 'Isletim Sistemi': isletimSis,'Islemci Tipi': islemciTipi, 'Islemci Nesli': islemciNesli, 'Ram': ram, 'SSD Boyutu': ssd, 'Ekran Boyutu': ekranBoyutu, 'urunLinki': link}
        print(myCol.insert_one(tempDict))
       