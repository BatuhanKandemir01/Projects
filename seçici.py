satır_sayısı = int(input("Lütfen satır sayısını giriniz: "))
sütun_sayısı = int(input("Lütfen sütun sayısını giriniz: "))

ucgen_tipi = int(input("Lütfen üçgen tipini seçiniz (" \
"1: sağa dayalı Dik Üçgen," \
" 2: sola dayalı Dik Üçgen, " \
"3: İkizkenar Üçgen, " \
"4:ters sağa dayalı dik üçgen," \
"5:ters sola dayalı dik üçgen): "))

if ucgen_tipi == 1:
    for i in range(1, satır_sayısı + 1):
        print("*" * i)

elif ucgen_tipi == 2:
    for i in range(satır_sayısı, 0, -1):
        print("*" * i)

elif ucgen_tipi == 3:
    for i in range(1, satır_sayısı + 1):
        bosluk = sütun_sayısı - i
        print(" " * bosluk + "*" * (2 * i - 1))

elif ucgen_tipi == 4:
    for i in range(1, satır_sayısı + 1):
        bosluk = sütun_sayısı - i
        print(" " * bosluk + "*" * i)

elif ucgen_tipi == 5:
    for i in range(satır_sayısı, 0, -1):
        bosluk = sütun_sayısı - i
        print(" " * bosluk + "*" * i)

else:
    print("Geçersiz seçim!")