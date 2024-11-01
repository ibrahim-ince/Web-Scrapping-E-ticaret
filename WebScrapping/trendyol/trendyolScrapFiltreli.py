import pymongo
from bs4 import BeautifulSoup
import requests

# dMarka = open("trendyolMarka.txt", "w")
# dFiyat = open("trendyolFiyat.txt", "w")
# dIslSis = open("trendyolIslSis.txt", "w")
# dTipi = open("trendyolTipi.txt", "w")
# dNesli = open("trendyolNesli.txt", "w")
# dRam = open("trendyolRam.txt", "w")
# dSsd = open("trendyolSsd.txt", "w")
# dEkran = open("trendyolEkran.txt", "w")
# dLink = open("trendyolLink.txt", "w")

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["trendyolUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 1
deneme = 0
while sayfa <= 20:
    print(str(sayfa) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.trendyol.com/sr?wb=102323%2C101606%2C101849%2C104964%2C103505%2C101470%2C102324%2C103502%2C107655&wc=103108&attr=168%7C3359_1950_1949_1948_852655_852657_243383_25555_7511_7510_7509&pi=" + str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
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
        lb = "https://www.trendyol.com"
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
            prc = soup1.find("span", attrs={"class": "prc-dsc"}).text.replace("TL", "").strip().replace(".", "").replace(",", ".")
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
                    isletimSis = ozlk.text[16:].replace("11", "").replace(" ", "").strip()
                    if isletimSis == "MacOs": isletimSis = "MacOS"
                    if isletimSis == "FreeDos" or isletimSis == "Ubuntu" or isletimSis == "Linux": isletimSis = "FreeDOS"
                    continue
            except: print("isletim sistemi cekilemedi")    
            try:
                if ozlk.text.find("İşlemci Tipi") == 0:
                    islemciTipi = ozlk.text[13:]
                    continue
            except: print("islemci tipi cekilemedi")
            try:
                if ozlk.text.find("İşlemci Nesli") == 0:
                    islemciNesli = ozlk.text[14:].replace(" ", "").strip()
                    if islemciNesli == "Belirtilmemiş" or islemciNesli == "Yok" or islemciNesli == "---":
                        if marka == "Apple": islemciNesli = "M1"
                        else: iptal = 1
                    continue
            except: 
                iptal = 1
                print("islemci nesli cekilemedi")
            try:
                if ozlk.text.find("Ram (Sistem Belleği)") == 0:
                    if ozlk.text.find("Ram (Sistem Belleği) Tipi") == 0:
                        continue
                    ram = ozlk.text[21:].replace("GB", "").strip()
            except: print("ram cekilemedi")
            try:
                if ozlk.text.find("SSD Kapasitesi") == 0:
                    ssd = ozlk.text[15:].replace("GB", "").strip()
                    if ssd.find("TB") != -1:
                        ssd = ssd.replace("TB", "").strip()
                        carpici = int(ssd)
                        ssd = ssd + "0" + str(carpici * 24)
                    if ssd == "Yok" or ssd == "SSD Yok" or int(ssd) < 100: iptal = 1
                    continue
            except:
                iptal = 1
                print("ssd cekilemedi")
            try:
                if ozlk.text.find("Ekran Boyutu") == 0:
                    ekranBoyutu = ozlk.text[13:].replace("inç", "").replace(",", ".").strip()
                    continue
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
