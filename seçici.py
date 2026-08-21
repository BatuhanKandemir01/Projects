sekil = int(input("""
Şekil seçiniz:
1 - Dikdörtgen
2 - Üçgen
Seçiminiz: """))

if sekil == 1:

    satır_sayısı = int(input("Dikdörtgenin satır sayısını giriniz: "))
    sütun_sayısı = int(input("Dikdörtgenin sütun sayısını giriniz: "))

    yatay = int(input("""
Yatay düzlem:
1 - dikik
2 - yatık
Seçiminiz: """))

    if yatay == 1:
        for i in range(satır_sayısı):
            print("*" * sütun_sayısı)

    elif yatay == 2:
        for i in range(satır_sayısı):
            print("*" * sütun_sayısı)

    else:
        print("Geçersiz yatay düzlem seçimi!")
        
elif sekil == 2:
    satır_sayısı = int(input("Üçgenin satır sayısını giriniz: "))

    ucgen_tipi = int(input("""
Üçgen tipini seçiniz:
1 - Sağa dayalı dik üçgen
2 - Sola dayalı dik üçgen
3 - İkizkenar üçgen
4 - Ters sağa dayalı dik üçgen
5 - Ters sola dayalı dik üçgen
Seçiminiz: """))

    yatay = int(input("""
Yatay düzlem:
1 - Düz
2 - Ters
Seçiminiz: """))

    if yatay == 1:

        if ucgen_tipi == 1:
            for i in range(1, satır_sayısı + 1):
                print("*" * i)

        elif ucgen_tipi == 2:
            for i in range(1, satır_sayısı + 1):
                print(" " * (satır_sayısı - i) + "*" * i)

        elif ucgen_tipi == 3:
            for i in range(1, satır_sayısı + 1):
                print(" " * (satır_sayısı - i) + "*" * (2 * i - 1))

        elif ucgen_tipi == 4:
            for i in range(satır_sayısı, 0, -1):
                print(" " * (satır_sayısı - i) + "*" * i)

        elif ucgen_tipi == 5:
            for i in range(satır_sayısı, 0, -1):
                print("*" * i)

        else:
            print("Geçersiz üçgen tipi!")

    elif yatay == 2:

        if ucgen_tipi == 1:
            for i in range(satır_sayısı, 0, -1):
                print("*" * i)

        elif ucgen_tipi == 2:
            for i in range(satır_sayısı, 0, -1):
                print(" " * (satır_sayısı - i) + "*" * i)

        elif ucgen_tipi == 3:
            for i in range(satır_sayısı, 0, -1):
                print(" " * (satır_sayısı - i) + "*" * (2 * i - 1))

        elif ucgen_tipi == 4:
            for i in range(1, satır_sayısı + 1):
                print(" " * (satır_sayısı - i) + "*" * i)

        elif ucgen_tipi == 5:
            for i in range(1, satır_sayısı + 1):
                print("*" * i)

        else:
            print("Geçersiz üçgen tipi!")

    else:
        print("Geçersiz yatay düzlem seçimi!")

else:
    print("Geçersiz şekil seçimi!")