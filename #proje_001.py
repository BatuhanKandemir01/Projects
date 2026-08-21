import tkinter as tk
from tkinter import messagebox
import random

# ---------------------------------------------------------
# RENKLER
# ---------------------------------------------------------
BG = "#08091c"
SIDEBAR = "#0d0e25"
CARD = "#151633"
CARD_HOVER = "#1d1f47"
WHITE = "#ffffff"
TEXT = "#b8b9d6"
PURPLE = "#7c3cff"
PURPLE_LIGHT = "#a855f7"
PINK = "#ec4899"
BLUE = "#38bdf8"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#fb7185"

kullanici_adi = "Misafir"
son_kullanilanlar = []
favoriler = set()
hedef_sayi = random.randint(1, 100)
tahmin_hakki = 7


# ---------------------------------------------------------
# ANA PENCERE
# ---------------------------------------------------------
pencere = tk.Tk()
pencere.title("Python Projeler Merkezi")
pencere.geometry("1250x750")
pencere.minsize(1050, 650)
pencere.configure(bg=BG)

ana_alan = tk.Frame(pencere, bg=BG)
ana_alan.pack(side="right", fill="both", expand=True)


# ---------------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ---------------------------------------------------------
def temizle():
    for widget in ana_alan.winfo_children():
        widget.destroy()


def ekle_son_kullanilan(proje):
    if proje in son_kullanilanlar:
        son_kullanilanlar.remove(proje)
    son_kullanilanlar.insert(0, proje)

    if len(son_kullanilanlar) > 8:
        son_kullanilanlar.pop()


def baslik_ekle(baslik, aciklama=""):
    tk.Label(
        ana_alan, text=baslik, font=("Arial", 27, "bold"),
        fg=WHITE, bg=BG
    ).pack(anchor="w", padx=45, pady=(38, 4))

    if aciklama:
        tk.Label(
            ana_alan, text=aciklama, font=("Arial", 11),
            fg=TEXT, bg=BG
        ).pack(anchor="w", padx=45, pady=(0, 25))


def geri_butonu():
    tk.Button(
        ana_alan, text="← Ana Menüye Dön", command=ana_menu,
        font=("Arial", 10, "bold"), fg=WHITE, bg=PURPLE,
        activebackground=PURPLE_LIGHT, activeforeground=WHITE,
        bd=0, padx=16, pady=9, cursor="hand2"
    ).pack(anchor="w", padx=45, pady=(0, 20))


def kart(parent, baslik, aciklama, renk, komut, ikon="◆"):
    frame = tk.Frame(parent, bg=CARD, width=245, height=180)
    frame.pack_propagate(False)

    ikon_label = tk.Label(
        frame, text=ikon, font=("Arial", 28, "bold"),
        fg=renk, bg=CARD
    )
    ikon_label.pack(anchor="w", padx=20, pady=(20, 4))

    tk.Label(
        frame, text=baslik, font=("Arial", 14, "bold"),
        fg=WHITE, bg=CARD
    ).pack(anchor="w", padx=20)

    tk.Label(
        frame, text=aciklama, font=("Arial", 9),
        fg=TEXT, bg=CARD, wraplength=195, justify="left"
    ).pack(anchor="w", padx=20, pady=(6, 10))

    def tikla(event=None):
        komut()

    for item in (frame, ikon_label):
        item.bind("<Button-1>", tikla)
        item.bind("<Enter>", lambda e: frame.config(bg=CARD_HOVER))
        item.bind("<Leave>", lambda e: frame.config(bg=CARD))

    return frame


# ---------------------------------------------------------
# SOL MENÜ
# ---------------------------------------------------------
sol_menu = tk.Frame(pencere, bg=SIDEBAR, width=255)
sol_menu.pack(side="left", fill="y")
sol_menu.pack_propagate(False)

tk.Label(
    sol_menu, text="</>", font=("Arial", 28, "bold"),
    fg=WHITE, bg=PURPLE, width=4, pady=5
).pack(pady=(30, 10))

tk.Label(
    sol_menu, text="PYTHON", font=("Arial", 19, "bold"),
    fg=WHITE, bg=SIDEBAR
).pack()

tk.Label(
    sol_menu, text="PROJELER MERKEZİ", font=("Arial", 9),
    fg=TEXT, bg=SIDEBAR
).pack(pady=(0, 35))


def menu_butonu(yazi, komut, ikon):
    return tk.Button(
        sol_menu, text=f"  {ikon}   {yazi}", command=komut,
        font=("Arial", 11, "bold"), fg=TEXT, bg=SIDEBAR,
        activeforeground=WHITE, activebackground="#20214a",
        anchor="w", bd=0, padx=25, pady=13, cursor="hand2"
    )


# ---------------------------------------------------------
# SAYFALAR
# ---------------------------------------------------------
def ana_menu():
    temizle()

    ust = tk.Frame(ana_alan, bg=BG)
    ust.pack(fill="x", padx=45, pady=(38, 10))

    tk.Label(
        ust, text=f"Hoş geldin, {kullanici_adi}! 👋",
        font=("Arial", 27, "bold"), fg=WHITE, bg=BG
    ).pack(anchor="w")

    tk.Label(
        ust, text="Bugün hangi Python projesini keşfetmek istersin?",
        font=("Arial", 11), fg=TEXT, bg=BG
    ).pack(anchor="w", pady=(5, 0))

    kullanici_karti = tk.Frame(ana_alan, bg="#20104a", height=80)
    kullanici_karti.pack(fill="x", padx=45, pady=(12, 24))
    kullanici_karti.pack_propagate(False)

    tk.Label(
        kullanici_karti, text="●", font=("Arial", 22),
        fg=GREEN, bg="#20104a"
    ).pack(side="left", padx=(20, 10))

    tk.Label(
        kullanici_karti, text=f"{kullanici_adi}\nAktif kullanıcı",
        font=("Arial", 11, "bold"), fg=WHITE, bg="#20104a",
        justify="left"
    ).pack(side="left")

    tk.Label(
        kullanici_karti, text="Ayarlar  →", font=("Arial", 10, "bold"),
        fg=PURPLE_LIGHT, bg="#20104a", cursor="hand2"
    ).pack(side="right", padx=22)
    kullanici_karti.winfo_children()[-1].bind("<Button-1>", lambda e: ayarlar())

    tk.Label(
        ana_alan, text="Popüler Projeler", font=("Arial", 17, "bold"),
        fg=WHITE, bg=BG
    ).pack(anchor="w", padx=45, pady=(0, 15))

    proje_alani = tk.Frame(ana_alan, bg=BG)
    proje_alani.pack(fill="x", padx=45)

    kart(
        proje_alani, "Hesap Makinesi", "Hızlı ve modern hesaplamalar yap.",
        PURPLE, hesap_makinesi, "⌘"
    ).grid(row=0, column=0, padx=(0, 18), pady=8)

    kart(
        proje_alani, "Sayı Bulmaca", "1 ile 100 arasındaki gizli sayıyı bul.",
        BLUE, sayi_bulmaca, "?"
    ).grid(row=0, column=1, padx=18, pady=8)

    kart(
        proje_alani, "Taş Kağıt Makas", "Bilgisayara karşı şansını dene.",
        PINK, tas_kagit_makas, "✊"
    ).grid(row=0, column=2, padx=18, pady=8)


def favorilerim():
    temizle()
    baslik_ekle("Favorilerim", "Yıldız verdiğin projeler burada görünür.")
    geri_butonu()

    alan = tk.Frame(ana_alan, bg=BG)
    alan.pack(fill="both", expand=True, padx=45)

    if not favoriler:
        tk.Label(
            alan, text="Henüz favori proje eklemedin. ⭐",
            font=("Arial", 14), fg=TEXT, bg=BG
        ).pack(pady=70)
        return

    for proje in favoriler:
        tk.Button(
            alan, text=f"★  {proje}", font=("Arial", 13, "bold"),
            fg=WHITE, bg=CARD, bd=0, anchor="w",
            padx=22, pady=16, cursor="hand2",
            command=lambda p=proje: proje_ac(p)
        ).pack(fill="x", pady=6)


def son_kullanilanlar_sayfasi():
    temizle()
    baslik_ekle("Son Kullanılanlar", "En son açtığın projeler.")
    geri_butonu()

    alan = tk.Frame(ana_alan, bg=BG)
    alan.pack(fill="both", expand=True, padx=45)

    if not son_kullanilanlar:
        tk.Label(
            alan, text="Henüz bir proje açmadın.",
            font=("Arial", 14), fg=TEXT, bg=BG
        ).pack(pady=70)
        return

    for proje in son_kullanilanlar:
        tk.Button(
            alan, text=f"◷  {proje}", font=("Arial", 13, "bold"),
            fg=WHITE, bg=CARD, bd=0, anchor="w",
            padx=22, pady=16, cursor="hand2",
            command=lambda p=proje: proje_ac(p)
        ).pack(fill="x", pady=6)


def hakkinda():
    temizle()
    baslik_ekle("Hakkında", "Python Projeler Merkezi")
    geri_butonu()

    bilgi = tk.Frame(ana_alan, bg=CARD)
    bilgi.pack(fill="x", padx=45, pady=10)

    metin = (
        "Bu uygulama küçük Python projelerini tek bir modern arayüzde "
        "toplamak için tasarlandı.\n\n"
        "İçerik:\n"
        "• Hesap Makinesi\n"
        "• Sayı Bulmaca\n"
        "• Taş Kağıt Makas\n\n"
        "Sürüm: 1.0"
    )

    tk.Label(
        bilgi, text=metin, font=("Arial", 12),
        fg=TEXT, bg=CARD, justify="left",
        padx=28, pady=28
    ).pack(anchor="w")


def ayarlar():
    temizle()
    baslik_ekle("Ayarlar", "Profilini kişiselleştir.")
    geri_butonu()

    panel = tk.Frame(ana_alan, bg=CARD)
    panel.pack(fill="x", padx=45, pady=10)

    tk.Label(
        panel, text="Kullanıcı Adı", font=("Arial", 14, "bold"),
        fg=WHITE, bg=CARD
    ).pack(anchor="w", padx=28, pady=(28, 8))

    tk.Label(
        panel, text="Ana ekranda ve kullanıcı kartında görünür.",
        font=("Arial", 10), fg=TEXT, bg=CARD
    ).pack(anchor="w", padx=28, pady=(0, 10))

    isim_giris = tk.Entry(
        panel, font=("Arial", 13), bg="#0b0c22",
        fg=WHITE, insertbackground=WHITE, bd=0,
        width=35
    )
    isim_giris.insert(0, kullanici_adi)
    isim_giris.pack(anchor="w", padx=28, pady=(0, 18), ipady=10)

    def kaydet():
        global kullanici_adi
        yeni_isim = isim_giris.get().strip()

        if not yeni_isim:
            messagebox.showwarning("Uyarı", "Lütfen bir isim gir.")
            return

        kullanici_adi = yeni_isim
        messagebox.showinfo("Kaydedildi", "Kullanıcı adın güncellendi.")
        ana_menu()

    tk.Button(
        panel, text="Kaydet", command=kaydet,
        font=("Arial", 11, "bold"), fg=WHITE, bg=PURPLE,
        activebackground=PURPLE_LIGHT, activeforeground=WHITE,
        bd=0, padx=22, pady=11, cursor="hand2"
    ).pack(anchor="w", padx=28, pady=(0, 28))


# ---------------------------------------------------------
# PROJE SAYFALARI
# ---------------------------------------------------------
def proje_ac(proje):
    if proje == "Hesap Makinesi":
        hesap_makinesi()
    elif proje == "Sayı Bulmaca":
        sayi_bulmaca()
    elif proje == "Taş Kağıt Makas":
        tas_kagit_makas()


def favori_butonu(proje, parent):
    metin = "★ Favoriden Çıkar" if proje in favoriler else "☆ Favorilere Ekle"

    buton = tk.Button(
        parent, text=metin, font=("Arial", 10, "bold"),
        fg=YELLOW, bg=BG, bd=0, cursor="hand2",
        activebackground=BG, activeforeground=YELLOW
    )
    buton.pack(anchor="w", padx=45, pady=(0, 15))

    def degistir():
        if proje in favoriler:
            favoriler.remove(proje)
        else:
            favoriler.add(proje)
        buton.config(
            text="★ Favoriden Çıkar" if proje in favoriler else "☆ Favorilere Ekle"
        )

    buton.config(command=degistir)


def hesap_makinesi():
    ekle_son_kullanilan("Hesap Makinesi")
    temizle()
    baslik_ekle("Hesap Makinesi", "İşlemini yaz ve hesapla.")
    geri_butonu()
    favori_butonu("Hesap Makinesi", ana_alan)

    panel = tk.Frame(ana_alan, bg=CARD)
    panel.pack(padx=45, pady=8)

    ekran = tk.Entry(
        panel, font=("Arial", 22, "bold"), justify="right",
        bg="#08091c", fg=WHITE, insertbackground=WHITE,
        bd=0, width=22
    )
    ekran.grid(row=0, column=0, columnspan=4, padx=18, pady=18, ipady=14)

    def yaz(deger):
        ekran.insert("end", deger)

    def temizle_ekran():
        ekran.delete(0, "end")

    def hesapla():
        try:
            sonuc = str(eval(ekran.get(), {"__builtins__": {}}, {}))
            ekran.delete(0, "end")
            ekran.insert(0, sonuc)
        except Exception:
            ekran.delete(0, "end")
            ekran.insert(0, "Hata")

    tuslar = [
        ("C", temizle_ekran), ("(", lambda: yaz("(")), (")", lambda: yaz(")")), ("/", lambda: yaz("/")),
        ("7", lambda: yaz("7")), ("8", lambda: yaz("8")), ("9", lambda: yaz("9")), ("*", lambda: yaz("*")),
        ("4", lambda: yaz("4")), ("5", lambda: yaz("5")), ("6", lambda: yaz("6")), ("-", lambda: yaz("-")),
        ("1", lambda: yaz("1")), ("2", lambda: yaz("2")), ("3", lambda: yaz("3")), ("+", lambda: yaz("+")),
        ("0", lambda: yaz("0")), (".", lambda: yaz(".")), ("=", hesapla)
    ]

    for i, (metin, komut) in enumerate(tuslar):
        satir = i // 4 + 1
        sutun = i % 4

        renk = PURPLE if metin == "=" else "#252751"
        if metin == "C":
            renk = RED

        tk.Button(
            panel, text=metin, command=komut,
            font=("Arial", 14, "bold"), fg=WHITE, bg=renk,
            activebackground=PURPLE_LIGHT, activeforeground=WHITE,
            bd=0, width=5, height=2, cursor="hand2"
        ).grid(row=satir, column=sutun, padx=6, pady=6)

    # Son satırda = düğmesi biraz geniş görünür.
    panel.grid_columnconfigure(0, minsize=65)
    panel.grid_columnconfigure(1, minsize=65)
    panel.grid_columnconfigure(2, minsize=65)
    panel.grid_columnconfigure(3, minsize=65)


def sayi_bulmaca():
    global hedef_sayi, tahmin_hakki

    ekle_son_kullanilan("Sayı Bulmaca")
    temizle()
    baslik_ekle("Sayı Bulmaca", "1 ile 100 arasındaki gizli sayıyı bul.")
    geri_butonu()
    favori_butonu("Sayı Bulmaca", ana_alan)

    panel = tk.Frame(ana_alan, bg=CARD)
    panel.pack(fill="x", padx=45, pady=8)

    durum = tk.Label(
        panel, text=f"{tahmin_hakki} tahmin hakkın var.",
        font=("Arial", 15, "bold"), fg=BLUE, bg=CARD
    )
    durum.pack(pady=(28, 12))

    tahmin_giris = tk.Entry(
        panel, font=("Arial", 16), justify="center",
        bg="#08091c", fg=WHITE, insertbackground=WHITE, bd=0, width=15
    )
    tahmin_giris.pack(ipady=10)

    sonuc = tk.Label(
        panel, text="Tahminini gir ve şansını dene!",
        font=("Arial", 12), fg=TEXT, bg=CARD
    )
    sonuc.pack(pady=15)

    def yeni_oyun():
        global hedef_sayi, tahmin_hakki
        hedef_sayi = random.randint(1, 100)
        tahmin_hakki = 7
        durum.config(text=f"{tahmin_hakki} tahmin hakkın var.", fg=BLUE)
        sonuc.config(text="Yeni oyun başladı!", fg=TEXT)
        tahmin_giris.delete(0, "end")
        tahmin_giris.config(state="normal")

    def kontrol_et():
        global tahmin_hakki

        try:
            tahmin = int(tahmin_giris.get())
        except ValueError:
            sonuc.config(text="Lütfen geçerli bir sayı gir.", fg=RED)
            return

        if not 1 <= tahmin <= 100:
            sonuc.config(text="1 ile 100 arasında bir sayı gir.", fg=RED)
            return

        if tahmin == hedef_sayi:
            sonuc.config(text=f"Tebrikler! Sayı {hedef_sayi} idi. 🎉", fg=GREEN)
            tahmin_giris.config(state="disabled")
            return

        tahmin_hakki -= 1

        if tahmin_hakki == 0:
            sonuc.config(text=f"Hakkın bitti. Doğru sayı: {hedef_sayi}", fg=RED)
            tahmin_giris.config(state="disabled")
        elif tahmin < hedef_sayi:
            sonuc.config(text="Daha büyük bir sayı dene! ↑", fg=YELLOW)
        else:
            sonuc.config(text="Daha küçük bir sayı dene! ↓", fg=YELLOW)

        durum.config(text=f"{tahmin_hakki} tahmin hakkın var.")

    tk.Button(
        panel, text="Tahmin Et", command=kontrol_et,
        font=("Arial", 11, "bold"), fg=WHITE, bg=PURPLE,
        activebackground=PURPLE_LIGHT, activeforeground=WHITE,
        bd=0, padx=22, pady=11, cursor="hand2"
    ).pack(pady=(0, 12))

    tk.Button(
        panel, text="Yeni Oyun", command=yeni_oyun,
        font=("Arial", 10, "bold"), fg=TEXT, bg="#252751",
        activeforeground=WHITE, activebackground="#373a72",
        bd=0, padx=18, pady=9, cursor="hand2"
    ).pack(pady=(0, 28))

    tahmin_giris.bind("<Return>", lambda e: kontrol_et())


def tas_kagit_makas():
    ekle_son_kullanilan("Taş Kağıt Makas")
    temizle()
    baslik_ekle("Taş Kağıt Makas", "Seçimini yap, bilgisayara karşı oyna.")
    geri_butonu()
    favori_butonu("Taş Kağıt Makas", ana_alan)

    panel = tk.Frame(ana_alan, bg=CARD)
    panel.pack(fill="x", padx=45, pady=8)

    skor = {"Sen": 0, "Bilgisayar": 0}

    skor_yazisi = tk.Label(
        panel, text="Sen: 0   |   Bilgisayar: 0",
        font=("Arial", 16, "bold"), fg=BLUE, bg=CARD
    )
    skor_yazisi.pack(pady=(28, 18))

    sonuc = tk.Label(
        panel, text="Taş, kağıt veya makas seç.",
        font=("Arial", 13), fg=TEXT, bg=CARD
    )
    sonuc.pack(pady=(0, 20))

    secim_alani = tk.Frame(panel, bg=CARD)
    secim_alani.pack(pady=(0, 28))

    def oyna(secim):
        bilgisayar = random.choice(["Taş", "Kağıt", "Makas"])

        if secim == bilgisayar:
            mesaj = f"Bilgisayar: {bilgisayar} — Berabere!"
            renk = YELLOW
        elif (
            (secim == "Taş" and bilgisayar == "Makas") or
            (secim == "Kağıt" and bilgisayar == "Taş") or
            (secim == "Makas" and bilgisayar == "Kağıt")
        ):
            skor["Sen"] += 1
            mesaj = f"Bilgisayar: {bilgisayar} — Kazandın! 🎉"
            renk = GREEN
        else:
            skor["Bilgisayar"] += 1
            mesaj = f"Bilgisayar: {bilgisayar} — Bilgisayar kazandı."
            renk = RED

        sonuc.config(text=mesaj, fg=renk)
        skor_yazisi.config(
            text=f"Sen: {skor['Sen']}   |   Bilgisayar: {skor['Bilgisayar']}"
        )

    secenekler = [("✊\nTaş", "Taş", PURPLE), ("✋\nKağıt", "Kağıt", BLUE), ("✌\nMakas", "Makas", PINK)]

    for metin, secim, renk in secenekler:
        tk.Button(
            secim_alani, text=metin, command=lambda s=secim: oyna(s),
            font=("Arial", 14, "bold"), fg=WHITE, bg=renk,
            activebackground=PURPLE_LIGHT, activeforeground=WHITE,
            bd=0, width=11, height=4, cursor="hand2"
        ).pack(side="left", padx=10)


# Menü butonlarını, fonksiyonlar tanımlandıktan sonra oluşturuyoruz.
menu_butonu("Ana Menü", ana_menu, "⌂").pack(fill="x")
menu_butonu("Favorilerim", favorilerim, "★").pack(fill="x")
menu_butonu("Son Kullanılanlar", son_kullanilanlar_sayfasi, "◷").pack(fill="x")
menu_butonu("Hakkında", hakkinda, "ⓘ").pack(fill="x")

tk.Frame(sol_menu, bg=SIDEBAR, height=120).pack(fill="both", expand=True)

menu_butonu("Ayarlar", ayarlar, "⚙").pack(fill="x", pady=(0, 15))

ana_menu()
pencere.mainloop()