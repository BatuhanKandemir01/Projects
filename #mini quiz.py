# MINI QUIZ


print("       WELCOME TO MINI QUIZ!")

puan = 0
dogru = 0
yanlis = 0


def cevap_kontrol(cevap, dogru_cevaplar):
    global puan, dogru, yanlis

    # B yazılırsa otomatik doğru
    if cevap.strip().upper() == "B":
        print("Correct! +10 points")
        puan += 10
        dogru += 1
        return

    # Normal cevap kontrolü
    cevap = cevap.strip().lower()

    for dogru_cevap in dogru_cevaplar:
        if cevap == dogru_cevap.lower():
            print("Correct! +10 points")
            puan += 10
            dogru += 1
            return

    print("Wrong!")
    yanlis += 1


# SORU 1
cevap = input("1) What is 1 + 1? ")
cevap_kontrol(cevap, ["2"])


# SORU 2
cevap = input("2) What is your name? ")

if cevap.strip().upper() == "B":
    print("Correct! +10 points")
    puan += 10
    dogru += 1
elif cevap.strip() != "":
    print("Correct! +10 points")
    puan += 10
    dogru += 1
else:
    print("Wrong!")
    yanlis += 1


# SORU 3
cevap = input("3) How old are you? ")

if cevap.strip().upper() == "B":
    print("Correct! +10 points")
    puan += 10
    dogru += 1
elif cevap.strip() != "":
    print("Correct! +10 points")
    puan += 10
    dogru += 1
else:
    print("Wrong!")
    yanlis += 1


# SORU 4
cevap = input("4) What is 2.2? ")
cevap_kontrol(cevap, ["4"])


# SORU 5
cevap = input("5) Where do you live? ")

if cevap.strip().upper() == "B":
    print("Correct! +10 points")
    puan += 10
    dogru += 1
elif cevap.strip() != "":
    print("Correct! +10 points")
    puan += 10
    dogru += 1
else:
    print("Wrong!")
    yanlis += 1


# SORU 6
cevap = input(
    "6) A man has 12 apples. He gives 5 apples to his friend. "
    "How many apples does he have left? "
)
cevap_kontrol(cevap, ["7", "seven"])


# SORU 7
cevap = input(
    "7) A farmer has 48 chickens. He sells 17 chickens and then "
    "buys 25 more. Later, 8 of his chickens escape. "
    "How many chickens does the farmer have left? "
)
cevap_kontrol(cevap, ["48", "forty eight", "forty-eight"])


# SORU 8
cevap = input("8) Find the value of pi to 5 decimal places. ")
cevap_kontrol(cevap, ["3.14159"])


# SORU 9
print()
print("9) A distinguished theoretical physicist formulates a controversial")
print("conjecture concerning the ontological status of causality within a")
print("fundamentally non-deterministic universe.")
print()
print("He argues that if every observable phenomenon constitutes merely")
print("an emergent manifestation of probabilistic interactions occurring")
print("at a subatomic level, then the conventional distinction between")
print("cause and consequence may represent nothing more than an")
print("epistemological construct imposed upon reality by human cognition.")
print()
print("Considering these premises, explain whether causality should be")
print("regarded as an intrinsic feature of reality or as an emergent")
print("interpretative framework constructed by conscious observers.")
print()

cevap = input("Your answer: ")

# Q9 için anahtar kelimeler
cevap_kontrol(
    cevap,
    [
        "emergent",
        "emergent framework",
        "causality is emergent",
        "causality is an emergent framework"
    ]
)


# SORU 10
print()
print("10) Three men go to a hotel. Each of them pays 10 dollars,")
print("so they pay a total of 30 dollars for a room.")
print()
print("The hotel manager gives the bellboy 5 dollars to return")
print("to the three men. The men give 2 dollars to the bellboy")
print("as a tip and split the remaining 3 dollars.")
print()
print("Each man effectively paid 9 dollars, making 27 dollars.")
print("They also gave 2 dollars to the bellboy.")
print()
print("Where did the missing 1 dollar go?")
print()

cevap = input("Your answer: ")

cevap_kontrol(
    cevap,
    [
        "there is no missing dollar",
        "no dollar is missing",
        "the calculation is incorrect",
        "there is no missing 1 dollar"
    ]
)


# SONUÇ

print("          QUIZ FINISHED!")


print("Correct answers:", dogru)
print("Wrong answers:", yanlis)
print("Total score:", puan, "/ 100")

print()

if puan == 100:
    print("PERFECT SCORE! AMAZING!")
elif puan >= 80:
    print("Excellent!")
elif puan >= 60:
    print("Good job!")
elif puan >= 40:
    print("Not bad!")
else:
    print("Keep practicing!")

print()
print("Thanks for playing!")