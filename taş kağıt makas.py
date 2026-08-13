import random

seçenekler = ["taş", "kağıt", "makas"]
while True:

    kullanıcı_seçimi = input("Taş, kağıt veya makas seçin (çıkmak için 'q' tuşuna basın): ").lower()
    if kullanıcı_seçimi == 'q':
        print("Oyun sonlandırıldı.")
        break
    elif kullanıcı_seçimi not in seçenekler:
        print("Geçersiz seçim. Lütfen tekrar deneyin.")
        continue

    bilgisayar_seçimi = random.choice(seçenekler)
    print(f"Bilgisayarın seçimi: {bilgisayar_seçimi}")

    if kullanıcı_seçimi == bilgisayar_seçimi:
        print("Berabere!")
    elif (kullanıcı_seçimi == "taş" and bilgisayar_seçimi == "makas") or \
         (kullanıcı_seçimi == "kağıt" and bilgisayar_seçimi == "taş") or \
         (kullanıcı_seçimi == "makas" and bilgisayar_seçimi == "kağıt"):
        print("Tebrikler! Kazandınız!")
    else:
        print("Üzgünüm, kaybettiniz.")