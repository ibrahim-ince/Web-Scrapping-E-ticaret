import pymongo
from bs4 import BeautifulSoup
import requests

# dMarka = open("teknosaMarka.txt", "w")
# dFiyat = open("teknosaFiyat.txt", "w")
# dIslSis = open("teknosaIslSis.txt", "w")
# dTipi = open("teknosaTipi.txt", "w")
# dNesli = open("teknosaNesli.txt", "w")
# dRam = open("teknosaRam.txt", "w")
# dSsd = open("teknosaSsd.txt", "w")
# dEkran = open("teknosaEkran.txt", "w")
# dLink = open("teknosaLink.txt", "w")

myClient = pymongo.MongoClient("mongodb+srv://ibrahimi:lUBEA0erHpBJzyzg@cluster0.h8vf8m0.mongodb.net/?retryWrites=true&w=majority")
myDB = myClient["myDataBase"]
myCol = myDB["teknosaUrunler"]
print(myCol.delete_many({}).deleted_count)

sayfa = 0
deneme = 0
while sayfa < 20:
    print(str(sayfa + 1) + ". sayfa cekiliyor")
    try:
        r = requests.get("https://www.teknosa.com/laptop-notebook-c-116004?s=%3Arelevance%3Abrand%3A2271%3Abrand%3A2328%3Abrand%3A2152%3Abrand%3A240%3Abrand%3A2267%3Abrand%3A230%3Abrand%3A290%3Abrand%3A2389%3Abrand%3A204%3Aislemci_116-CLS-2500%3AIntel%2BCore%2Bi7%2B%2B%3Aislemci_116-CLS-2500%3AIntel%2BCore%2Bi5%2B%2B%3Aislemci_116-CLS-2500%3AIntel%2BCore%2Bi3%2B%2B%3Aislemci_116-CLS-2500%3AAMD%2BRyzen%2B5%2B%2B%3Aislemci_116-CLS-2500%3AAMD%2BRyzen%2B7%2B%2B%3Aislemci_116-CLS-2500%3AIntel%2BCore%2Bi9%2B%2B%3Aislemci_116-CLS-2500%3AAMD%2BRyzen%2B3%2B%2B%3Aislemci_116-CLS-2500%3AM1%2B%2B%3Aislemci_116-CLS-2500%3AM1%2BPro%2B%2B%3Aislemci_116-CLS-2500%3AApple%2BM1%2B%2B%3Aislemci_116-CLS-2500%3AApple%2BM1%2BPro%2B%2B%3Aislemci_116-CLS-2500%3AApple%2BM1%2BMax%2B%2B%3Aislemci_116-CLS-2500%3AAMD%2BRyzen%2B9%2B%2B&page=" + str(sayfa), headers={'User-Agent': 'Mozilla/5.0'})
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
        iptal = 0

        try:
            prc = soup1.find("div", attrs={"class": "prd-prc2"}).text.replace("TL", "").strip().replace(".", "").replace(",", ".")
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
                        if isletimSis == "macOS": isletimSis = "MacOS"
                except: print("isletim sistemi cekilemedi")
                try:
                    if "İşlemci" in list1:
                        islemciTipi = list2[list1.index("İşlemci")]
                        if islemciTipi == "M1": islemciTipi = "Apple M1"
                except: print("islemci tipi cekilemedi")
                try:
                    if "İşlemci Nesli" in list1:
                        islemciNesli = list2[list1.index("İşlemci Nesli")].replace("Intel Core", "").replace("AMD Ryzen", "").strip()
                        if islemciNesli == "Yok":
                            if marka == "Apple": islemciNesli = "M1"
                            else: iptal = 1
                except: print("islemci nesli cekilemedi")
                try:
                    if "Ram" in list1:
                        ram = list2[list1.index("Ram")].replace("GB", "").strip()
                except: print("ram cekilemedi")
                try:
                    if "SSD Kapasitesi" in list1:
                        ssd = list2[list1.index("SSD Kapasitesi")].replace("GB", "").strip()
                        if ssd == "Yok": iptal = 1
                        if ssd.find("TB") != -1:
                            ssd = ssd.replace("TB", "").strip()
                            carpici = int(ssd)
                            ssd = ssd + "0" + str(carpici * 24)
                except: print("ssd cekilemedi")
                try:
                    if "Ekran Boyutu" in list1:
                        ekranBoyutu = list2[list1.index("Ekran Boyutu")].replace('"', "").replace("inch", "").replace("inç", "").strip()
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
       