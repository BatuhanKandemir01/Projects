ilk = int(input("Lütfen bir sayi girin: "))
ikinci  = int(input("Lütfen başka bir sayi girin: "))
işlem = input("Lütfen yapmak istediğiniz işlemi seçin (toplama:+, çıkarma:-, çarpma:*, bölme:/, mod:%, üs:**, karekök:√): ")


if işlem == "+":
    sonuç = ilk + ikinci 
    print(f"{ilk} + {ikinci} = {sonuç}")
elif işlem == "-":
    sonuç = ilk - ikinci
    print(f"{ilk} - {ikinci} = {sonuç}")
elif işlem == "*":
    sonuç = ilk * ikinci
    print(f"{ilk} * {ikinci} = {sonuç}")
elif işlem == "/":
    sonuç = ilk / ikinci
    print(f"{ilk} / {ikinci} = {sonuç}")
elif işlem == "%":
    sonuç = ilk % ikinci
    print(f"{ilk} % {ikinci} = {sonuç}")
elif işlem == "**":
    sonuç = ilk ** ikinci
    print(f"{ilk} ** {ikinci} = {sonuç}")
elif işlem == "√":
    sonuç = ilk ** 0.5
    print(f"{ilk} √ {ikinci} = {sonuç}")