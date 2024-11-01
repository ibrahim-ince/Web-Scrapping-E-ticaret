import pymongo
from bs4 import BeautifulSoup
import requests

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["hbUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 1
deneme = 0
while sayfa <= 5:
    print(str(sayfa) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98" + "?sayfa=" + str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
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
    soup = BeautifulSoup(r.content, 'lxml')
    sayfa += 1

    st1 = soup.find("div", attrs={"class": "productListContent-pXUkO4iHa51o_17CBibU"})
    st2 = st1.find("ul", attrs={"class": "productListContent-frGrtf5XrVXRwJ05HUfU productListContent-rEYj2_8SETJUeqNhyzSm"})
    st3 = st2.find_all("li", attrs={"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})

    for details in st3:
        lb = "https://www.hepsiburada.com"
        ls = details.a.get("href")
        if ls.startswith("https://adservice"):
            continue
        link = lb + ls
        try:
            r1 = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
        except:
            print("timeout")
            continue
        print(r1)
        deneme = 0
        soup1 = BeautifulSoup(r1.content, "lxml")

        prc = soup1.find("span", attrs={"id": "offering-price"}).text.replace("(Adet )", "").replace("TL", "").strip()
        marka = soup1.find("span", attrs={"class": "brand-name"}).text.strip()
        baslik = soup1.find("h1", attrs={"id": "product-name"}).text.strip()
        
        puan = "---"
        fotoURL = "---"
        isletimSis = "---"
        islemciTipi = "---"
        islemciNesli = "---"
        ram = "---"
        ssd = "---"
        ekranBoyutu = "---"

        try:
            puan = soup1.find("span", attrs={"class": "rating-star"}).text.strip()
        except:
            puan = "puan cekilemedi"
        try:
            fotoURL = soup1.img.get("src")
        except:
            fotoURL = "foto urlsi cekilemedi"

        try:
            ozlk = soup1.find("table", attrs={"class": "data-list tech-spec"}).text.strip().split("\n\n\n\n")
            
            i = 0
            while i < len(ozlk):
                ozlk[i] = ozlk[i].split("\n\n")
                i += 1
        except:
            print("ozellikler cekilemedi")
        
        i = 0
        while i < len(ozlk):
            try:
                if ozlk[i][0] == "İşletim Sistemi":
                    isletimSis = ozlk[i][1]
            except: print("isletim sistemi cekilemedi")
            try:
                if ozlk[i][0] == "İşlemci Tipi":
                    islemciTipi = ozlk[i][1]
            except: print("islemci tipi cekilemedi")
            try:
                if ozlk[i][0] == "İşlemci Nesli":
                    islemciNesli = ozlk[i][1]
            except: print("islemci nesli cekilemedi")
            try:
                if ozlk[i][0] == "Ram (Sistem Belleği)":
                    ram = ozlk[i][1].replace("GB", "").strip()
            except: print("ram cekilemedi")
            try:
                if ozlk[i][0] == "SSD Kapasitesi":
                    ssd = ozlk[i][1].replace("GB", "").strip()
            except: print("ssd cekilemedi")
            try:
                if ozlk[i][0] == "Ekran Boyutu":
                    ekranBoyutu = ozlk[i][1].replace("inç", "").strip()
            except: print("ekran boyutu cekilemedi")
            i += 1
      
        tempDict = {'Baslik': baslik, 'Marka': marka, 'Fiyat': prc, 'Puan': puan, 'Isletim Sistemi': isletimSis,'Islemci Tipi': islemciTipi, 'Islemci Nesli': islemciNesli, 'Ram': ram, 'SSD Boyutu': ssd, 'Ekran Boyutu': ekranBoyutu, 'urunLinki': link, 'fotoUrl': fotoURL}
        print(myCol.insert_one(tempDict))
