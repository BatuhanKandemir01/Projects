import tkinter as tk
import random

# Oyun Sabitleri
GENISLIK = 600
YUKSEKLIK = 400
KARE_BOYUTU = 20
HIZ = 100  # Milisaniye cinsinden (Kare hızı)

ARKA_PLAN = "#1e1e1e"
YILAN_RENK = "#00ff88"
YEM_RENK = "#ff3366"
YAZI_RENK = "#ffffff"


class YilanOyunu:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("VS Code - Yılan Oyunu (Saf Python)")
        self.pencere.resizable(False, False)

        # Skor ve Yön
        self.skor = 0
        self.yon = "Right"

        # Arayüz Elemanları
        self.skor_etiket = tk.Label(
            pencere,
            text=f"Skor: {self.skor}",
            font=("Consolas", 16, "bold"),
            bg=ARKA_PLAN,
            fg=YAZI_RENK,
        )
        self.skor_etiket.pack()

        self.tuval = tk.Canvas(
            pencere,
            bg=ARKA_PLAN,
            height=YUKSEKLIK,
            width=GENISLIK,
            highlightthickness=0,
        )
        self.tuval.pack()

        # Tuş Atamaları
        self.pencere.bind("<Up>", lambda event: self.yon_degistir("Up"))
        self.pencere.bind("<Down>", lambda event: self.yon_degistir("Down"))
        self.pencere.bind("<Left>", lambda event: self.yon_degistir("Left"))
        self.pencere.bind("<Right>", lambda event: self.yon_degistir("Right"))
        self.pencere.bind("<space>", lambda event: self.yeniden_baslat())

        # Başlangıç Değerleri
        self.yilan = [(100, 100), (80, 100), (60, 100)]
        self.yem = None
        self.oyun_bitti = False

        self.yem_olustur()
        self.oyun_dongusu()

    def yon_degistir(self, yeni_yon):
        # Yılanın kendi üzerine ters dönmesini engelle
        zıt_yonler = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if yeni_yon != zıt_yonler.get(self.yon):
            self.yon = yeni_yon

    def yem_olustur(self):
        x = random.randint(0, (GENISLIK // KARE_BOYUTU) - 1) * KARE_BOYUTU
        y = random.randint(0, (YUKSEKLIK // KARE_BOYUTU) - 1) * KARE_BOYUTU
        self.yem = (x, y)

    def hareket_et(self):
        bas_x, bas_y = self.yilan[0]

        if self.yon == "Up":
            yeni_bas = (bas_x, bas_y - KARE_BOYUTU)
        elif self.yon == "Down":
            yeni_bas = (bas_x, bas_y + KARE_BOYUTU)
        elif self.yon == "Left":
            yeni_bas = (bas_x - KARE_BOYUTU, bas_y)
        elif self.yon == "Right":
            yeni_bas = (bas_x + KARE_BOYUTU, bas_y)

        # Çarpmaları Kontrol Et
        if (
            yeni_bas[0] < 0
            or yeni_bas[0] >= GENISLIK
            or yeni_bas[1] < 0
            or yeni_bas[1] >= YUKSEKLIK
            or yeni_bas in self.yilan
        ):
            self.oyun_bitti = True
            return

        # Yılanı İlerlet
        self.yilan.insert(0, yeni_bas)

        # Yem Yendi mi?
        if yeni_bas == self.yem:
            self.skor += 10
            self.skor_etiket.config(text=f"Skor: {self.skor}")
            self.yem_olustur()
        else:
            self.yilan.pop()  # Yem yenmediyse kuyruktan sil

    def ciz(self):
        self.tuval.delete("all")

        if not self.oyun_bitti:
            # Yemi Çiz
            self.tuval.create_oval(
                self.yem[0],
                self.yem[1],
                self.yem[0] + KARE_BOYUTU,
                self.yem[1] + KARE_BOYUTU,
                fill=YEM_RENK,
                outline="",
            )

            # Yılanı Çiz
            for parca in self.yilan:
                self.tuval.create_rectangle(
                    parca[0],
                    parca[1],
                    parca[0] + KARE_BOYUTU,
                    parca[1] + KARE_BOYUTU,
                    fill=YILAN_RENK,
                    outline=ARKA_PLAN,
                )
        else:
            # Game Over Ekranı
            self.tuval.create_text(
                GENISLIK // 2,
                YUKSEKLIK // 2 - 20,
                text="GAME OVER",
                fill="#ff3333",
                font=("Consolas", 32, "bold"),
            )
            self.tuval.create_text(
                GENISLIK // 2,
                YUKSEKLIK // 2 + 20,
                text="Yeniden Başlamak İçin SPACE'e Basın",
                fill=YAZI_RENK,
                font=("Consolas", 14),
            )

    def oyun_dongusu(self):
        if not self.oyun_bitti:
            self.hareket_et()
            self.ciz()
            self.pencere.after(HIZ, self.oyun_dongusu)
        else:
            self.ciz()

    def yeniden_baslat(self):
        if self.oyun_bitti:
            self.skor = 0
            self.yon = "Right"
            self.skor_etiket.config(text=f"Skor: {self.skor}")
            self.yilan = [(100, 100), (80, 100), (60, 100)]
            self.oyun_bitti = False
            self.yem_olustur()
            self.oyun_dongusu()


if __name__ == "__main__":
    ana_pencere = tk.Tk()
    oyun = YilanOyunu(ana_pencere)
    ana_pencere.mainloop()