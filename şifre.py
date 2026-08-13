import time
import sys

# 🔐 ŞİFRE
sifre = "1q2w3e4r"

yanlis_sayisi = 0

# 3. yanlıştan itibaren:
# 15 saniye → 1 dakika → 2 dakika → 5 dakika
# → 10 dakika → 15 dakika → 30 dakika
bekleme_sureleri = [
    15,
    60,
    120,
    300,
    600,
    900,
    1800
]

# 🔑 ŞİFRE KONTROLÜ
while True:
    girilen_sifre = input("🔑 Şifreyi gir: ")

    if girilen_sifre == sifre:
        print("\n✅ Şifre doğru!")
        print("📚 Python kelimeleri açılıyor...\n")
        break

    yanlis_sayisi += 1
    print("❌ Şifre yanlış!")

    if yanlis_sayisi <= 2:
        print("Tekrar dene.\n")

    elif yanlis_sayisi <= 9:
        index = yanlis_sayisi - 3
        sure = bekleme_sureleri[index]

        print(f"⏳ Bekleme: {sure} saniye")

        for kalan in range(sure, 0, -1):
            dakika = kalan // 60
            saniye = kalan % 60

            if dakika > 0:
                print(
                    f"\r⏰ Kalan: {dakika} dakika {saniye} saniye",
                    end=""
                )
            else:
                print(
                    f"\r⏰ Kalan: {saniye} saniye",
                    end=""
                )

            time.sleep(1)

        print("\n✅ Tekrar deneyebilirsin.\n")

    else:
        print("\n🚫 Çok fazla yanlış giriş yapıldı!")
        print("🔒 Program kapanıyor...")
        time.sleep(2)
        sys.exit()


# 📚 PYTHON ANAHTAR KELİMELERİ
kelimeler = [
    "False → Yanlış / hayır",
    "None → Hiçbir değer yok",
    "True → Doğru / evet",
    "and → Ve",
    "as → Olarak / takma ad",
    "assert → Doğrula / kontrol et",
    "async → Eşzamansız işlem",
    "await → Bekle",
    "break → Döngüyü durdur",
    "case → Durum",
    "class → Sınıf oluştur",
    "continue → Sonraki tura geç",
    "def → Fonksiyon tanımlar",
    "del → Sil",
    "elif → Yok eğer",
    "else → Değilse",
    "except → Hata yakala",
    "finally → Her durumda çalıştır",
    "for → Döngü",
    "from → Bir yerden içe aktar",
    "global → Global değişken",
    "if → Eğer",
    "import → İçe aktar",
    "in → İçinde",
    "is → Aynı mı?",
    "lambda → İsimsiz fonksiyon",
    "match → Değer eşleştirme",
    "nonlocal → Üst kapsamdaki değişken",
    "not → Değil",
    "or → Veya",
    "pass → Hiçbir şey yapma",
    "raise → Hata oluştur",
    "return → Değer döndür",
    "try → Denemeye çalış",
    "while → Koşul doğru olduğu sürece"
]

# 📖 KELİMELERİ EKRANA YAZDIR
print("════════════════════════════════════")
print("     🐍 PYTHON ANAHTAR KELİMELERİ")
print("════════════════════════════════════")

for kelime in kelimeler:
    print(kelime)

print("════════════════════════════════════")
print("✅ Toplam:", len(kelimeler), "kelime")