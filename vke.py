while True:
    try:
        kilo = float(input("Kilonuzu kilogram olarak girin (Örn: 75.5): "))
        break
    except ValueError:
        if kilo <= 0:
            if kilo >= 200:
                print("Hata: Kilo 200'den büyük olamaz! Lütfen geçerli bir kilo girin.\n")
            else:
                print("Hata: Kilo negatif olamaz! Lütfen geçerli bir kilo girin.\n")
        print("Hata: Geçersiz giriş! Lütfen harf yerine SADECE SAYI giriniz.\n")

while True:
    try:
        boy = float(input("Boyunuzu santimetre olarak girin (Örn: 175): "))
        break
    except ValueError:
        if boy <= 0:
            if boy >= 250:
                print("Hata: Boy 250'den büyük olamaz! Lütfen geçerli bir boy girin.\n")
            else:
                print("Hata: Boy negatif olamaz! Lütfen geçerli bir boy girin.\n")
        print("Hata: Geçersiz giriş! Lütfen harf yerine SADECE SAYI giriniz.\n")


vke = kilo / ((boy / 100) ** 2)


if vke < 18.5:
    print(f"Vücut Kitle Endeksiniz: {vke:.2f} - Zayıf")
elif 18.5 <= vke < 25:
    print(f"Vücut Kitle Endeksiniz: {vke:.2f} - Normal")
elif 25 <= vke < 30:
    print(f"Vücut Kitle Endeksiniz: {vke:.2f} - Kilolu")
elif 30 <= vke < 35:
    print(f"Vücut Kitle Endeksiniz: {vke:.2f} - Obez")
else:
    print(f"Vücut Kitle Endeksiniz: {vke:.2f} - Aşırı Obez")
