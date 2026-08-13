okul = int(input("Okuyormusun? (0: Evet, 1: Hayır): "))
yaş = int (input("Lütfen yaşınızı giriniz: "))


if yaş >= 18 and okul== 1:
    print("askere gelme yaşın geldi.")


elif yaş >= 18 and okul== 0:
    print("okulun bittiğinde askere gidebilirsin.")


else:
    print("askere gelme yaşın gelmedi.")