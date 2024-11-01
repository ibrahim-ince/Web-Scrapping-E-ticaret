import pymongo
from bs4 import BeautifulSoup
import requests

# dMarka = open("hbMarka.txt", "w")
# dFiyat = open("hbFiyat.txt", "w")
# dPuan = open("hbPuan.txt", "w")
# dIslSis = open("hbIslSis.txt", "w")
# dTipi = open("hbTipi.txt", "w")
# dNesli = open("hbNesli.txt", "w")
# dRam = open("hbRam.txt", "w")
# dSsd = open("hbSsd.txt", "w")
# dEkran = open("hbEkran.txt", "w")
# dLink = open("hbLink.txt", "w")

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["hbUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 1
deneme = 0
while sayfa <= 20:
    print(str(sayfa) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.hepsiburada.com/asus-lenovo-dell-hp-msi-huawei-apple-acer-casper/laptop-notebook-dizustu-bilgisayarlar-c-98?filtreler=islemcitipi:Intel%" + "E2%" + "82%AC20Core%" + "E2%" + "82%AC20i5,AMD%" + "E2%" + "82%AC20Ryzen%" + "E2%" + "82%AC207,AMD%" + "E2%" + "82%AC20Ryzen%" + "E2%" + "82%AC205,Intel%" + "E2%" + "82%AC20Core%" + "E2%" + "82%AC20i9,Intel%" + "E2%" + "82%AC20Core%" + "E2%" + "82%AC20i3,AMD%" + "E2%" + "82%AC20Ryzen%" + "E2%" + "82%AC209,AMD%" + "E2%" + "82%AC20Ryzen%" + "E2%" + "82%AC203,Apple%" + "E2%" + "82%AC20M1,Intel%" + "E2%" + "82%AC20Core%" + "E2%" + "82%AC20i7,Apple%" + "E2%" + "82%AC20M1%" + "E2%" + "82%AC20Pro%" + "E2%" + "82%AC20%" + "E2%" + "82%ACC3%" + "E2%" + "82%AC87ip,Apple%" + "E2%" + "82%AC20M1%" + "E2%" + "82%AC20Max%" + "E2%" + "82%AC20%" + "E2%" + "82%ACC3%" + "E2%" + "82%AC87ip&sayfa="+ str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
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

        prc = soup1.find("span", attrs={"id": "offering-price"}).text.replace("(Adet )", "").replace("TL", "").strip().replace(".", "").replace(",", ".")
        marka = soup1.find("span", attrs={"class": "brand-name"}).text.strip()
        if marka == "MSI": marka = "Msi" 
        baslik = soup1.find("h1", attrs={"id": "product-name"}).text.strip()
        
        puan = "---"
        fotoURL = "---"
        isletimSis = "---"
        islemciTipi = "---"
        islemciNesli = "---"
        ram = "---"
        ssd = "---"
        ekranBoyutu = "---"
        iptal = 0

        try:
            puan = soup1.find("span", attrs={"class": "rating-star"}).text.strip().replace(",", ".")
        except:
            print("puan cekilemedi")
        try:
            fotoURL = soup1.img.get("src")
        except:
            print("foto urlsi cekilemedi")

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
                    isletimSis = ozlk[i][1].replace("Home", "").replace("Pro", "").replace("11", "").replace("10", "").strip().title()
                    if isletimSis == "Linux" or isletimSis == "Ubuntu": isletimSis = "FreeDOS"
                    if isletimSis == "Yok (Free Dos)": isletimSis = "FreeDOS"
                    if isletimSis == "Macos": isletimSis = "MacOS"
            except: print("isletim sistemi cekilemedi")
            try:
                if ozlk[i][0] == "İşlemci Tipi":
                    islemciTipi = ozlk[i][1].replace("Çip", "").strip()
            except: print("islemci tipi cekilemedi")
            try:
                if ozlk[i][0] == "İşlemci Nesli":
                    islemciNesli = ozlk[i][1].replace("ş", "s").replace("ö", "o").replace("ç", "c").replace("ğ", "g").replace("İ", "I").replace("ü", "u")
                    if islemciNesli == "Yok":
                        if marka == "Apple": islemciNesli = "M1"
                        else: iptal = 1
            except: print("islemci nesli cekilemedi")
            try:
                if ozlk[i][0] == "Ram (Sistem Belleği)":
                    ram = ozlk[i][1].replace("GB", "").strip()
            except: print("ram cekilemedi")
            try:
                if ozlk[i][0] == "SSD Kapasitesi":
                    ssd = ozlk[i][1].replace("GB", "").strip()
                    if ssd == "Yok": iptal = 1
                    if ssd.find("TB") != -1:
                        ssd = ssd.replace("TB", "").strip()
                        carpici = int(ssd)
                        ssd = ssd + "0" + str(carpici * 24)
            except: print("ssd cekilemedi")
            try:
                if ozlk[i][0] == "Ekran Boyutu":
                    ekranBoyutu = ozlk[i][1].replace("inç", "").replace(",", ".").strip()
            except: print("ekran boyutu cekilemedi")
            i += 1

        if iptal == 1: continue
        tempDict = {'Baslik': baslik, 'Marka': marka, 'Fiyat': prc, 'Puan': puan, 'Isletim Sistemi': isletimSis,'Islemci Tipi': islemciTipi, 'Islemci Nesli': islemciNesli, 'Ram': ram, 'SSD Boyutu': ssd, 'Ekran Boyutu': ekranBoyutu, 'urunLinki': link, 'fotoUrl': fotoURL}
        print(myCol.insert_one(tempDict))

#         dMarka.write(tempDict['Marka'])
#         dMarka.write("\n")
#         dFiyat.write(tempDict['Fiyat'])
#         dFiyat.write("\n")
#         dPuan.write(tempDict['Puan'])
#         dPuan.write("\n")
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
# dPuan.close()
# dIslSis.close()
# dTipi.close()
# dNesli.close()
# dRam.close()
# dSsd.close()
# dEkran.close()
