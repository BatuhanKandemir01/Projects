Satir_sayisi = 4
Sutun_sayisi = 4

for satir in range(1, Satir_sayisi + 1):
    boşluk = Satir_sayisi - satir
    yıldız = Sutun_sayisi - boşluk

    for sutun in range(1, boşluk + 1):
        print(" ", end='')
    for sutun in range(1, yıldız + 1):
        print("*", end=' ')
    print()