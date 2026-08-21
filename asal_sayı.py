while True:
    try:
        n = int(input("lütfen bir sayı giriniz:"))

        if n < 0:
            print("negatif sayı giremzsiniz")
            continue


    except ValueError :
        print("lütfen bir  tam sayı giriniz")
        continue






    c = 1



    if n < 2 :
        print(n, "asal değildir")
        continue

    for i in range (2,n):
        if n % i == 0:
            print(n, "asal değildir")
            c = 0
            break
    if c == 1:
        print(n, "asaldır")