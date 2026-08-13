a = int(input("Lütfen yaşınızı girin: "))
b = float(input("Lütfen boyunuzu santimetre cinsinden girin: "))


if b < 140:
    print("Boyunuz 140 cm'den kısa olduğu için bilet alamazsınız.")


elif a < 12:
    print("bilet fiyatı 50 TL'dir iyi eğlenceler.")


elif a >= 12 and a < 18:
    print("bilet fiyatı 100 TL'dir iyi eğlenceler.")


elif a >= 18:
    print("bilet fiyatı 200 TL'dir iyi eğlenceler.")