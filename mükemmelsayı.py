while True:

    try:
        n = int(input("Lütfen bir sayı giriniz: "))

        if n < 0:
            print("Negatif sayı giremezsiniz.")
            continue

    except ValueError:
        print("Lütfen bir tam sayı giriniz.")
        continue

    toplam = 0

    for i in range(1, n):
        if n % i == 0:
            toplam = toplam + i

    if toplam == n:
        print("Bu sayı mükemmel sayıdır!")
    else:
        print("Bu sayı mükemmel sayı değildir.")