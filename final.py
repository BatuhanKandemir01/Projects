import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import math
import os
import webbrowser
from datetime import datetime

# Windows sistem sesleri için
try:
    import winsound
except ImportError:
    winsound = None

# ==========================================
# RENK PALETİ VE TEMA SABİTLERİ (SLATE DARK)
# ==========================================
BG_DARK = "#0f172a"        # Ana Arka Plan
CARD_BG = "#1e293b"        # Kart Arka Planı
CARD_BORDER = "#334155"    # Kart Kenarlıkları
ACCENT_BLUE = "#38bdf8"    # Birincil Vurgu
ACCENT_GREEN = "#10b981"   # Yeşil (Normal / İdeal)
ACCENT_YELLOW = "#f59e0b"  # Sarı (Uyarı)
ACCENT_RED = "#ef4444"     # Kırmızı (Tehlike)
TEXT_WHITE = "#f8fafc"     # Ana Metin
#TEXT_MUTED = "#94a3b8"     # İkincil Metin

# ==========================================
# VERİTABANI YÖNETİCİSİ
# ==========================================
class DatabaseManager:
    def __init__(self, db_name="health_suite_v2.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.tablo_olustur()

    def tablo_olustur(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS kayitlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT,
                isim TEXT,
                yas INTEGER,
                cinsiyet TEXT,
                kilo REAL,
                boy REAL,
                vki REAL,
                vki_durum TEXT,
                bmr REAL,
                tdee REAL,
                skor INTEGER
            )
        ''')
        self.conn.commit()

    def kayit_ekle(self, veri):
        self.cursor.execute('''
            INSERT INTO kayitlar (tarih, isim, yas, cinsiyet, kilo, boy, vki, vki_durum, bmr, tdee, skor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', veri)
        self.conn.commit()

    def kayitlari_getir(self):
        self.cursor.execute('SELECT * FROM kayitlar ORDER BY id ASC')
        return self.cursor.fetchall()

    def kayit_sil(self, kayit_id):
        self.cursor.execute('DELETE FROM kayitlar WHERE id = ?', (kayit_id,))
        self.conn.commit()

# ==========================================
# ANIMASYONLU GÖSTERGE (SMOOTH GAUGE)
# ==========================================
class AnimatedGauge(tk.Canvas):
    def __init__(self, parent, width=280, height=150, **kwargs):
        super().__init__(parent, width=width, height=height, bg=CARD_BG, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.mevcut_aci = 135
        self.hedef_aci = 135
        self.ciz_arkaplan()

    def ciz_arkaplan(self):
        self.delete("all")
        # Renkli Arclar (Zayıf, İdeal, Fazla, Obez)
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=135, extent=-33.75, fill="#0284c7", outline="")
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=101.25, extent=-33.75, fill=ACCENT_GREEN, outline="")
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=67.5, extent=-33.75, fill=ACCENT_YELLOW, outline="")
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=33.75, extent=-33.75, fill=ACCENT_RED, outline="")

        # İç Maske
        self.create_oval(55, 55, self.width-55, self.height*2-55, fill=CARD_BG, outline="")

        # Sayısal İşaretler
        self.create_text(35, 125, text="18.5", fill=TEXT_MUTED, font=("Consolas", 8, "bold"))
        self.create_text(105, 45, text="25", fill=TEXT_MUTED, font=("Consolas", 8, "bold"))
        self.create_text(175, 45, text="30", fill=TEXT_MUTED, font=("Consolas", 8, "bold"))
        self.create_text(245, 125, text="40", fill=TEXT_MUTED, font=("Consolas", 8, "bold"))

    def animasyonlu_set(self, vki):
        clamped_vki = max(15.0, min(vki, 40.0))
        orad = (clamped_vki - 15) / (40 - 15)
        self.hedef_aci = 135 - (orad * 135)
        self.vki_val = vki
        self._animasyon_adimi()

    def _animasyon_adimi(self):
        fark = self.hedef_aci - self.mevcut_aci
        if abs(fark) > 0.5:
            self.mevcut_aci += fark * 0.15
            self.ibre_ciz(self.mevcut_aci)
            self.after(20, self._animasyon_adimi)
        else:
            self.mevcut_aci = self.hedef_aci
            self.ibre_ciz(self.mevcut_aci)

    def ibre_ciz(self, aci_derece):
        self.ciz_arkaplan()
        aci_radyan = math.radians(aci_derece)

        cx, cy = self.width / 2, self.height - 10
        r = self.width / 2 - 35

        ix = cx + r * math.cos(aci_radyan)
        iy = cy - r * math.sin(aci_radyan)

        self.create_line(cx, cy, ix, iy, fill=TEXT_WHITE, width=3)
        self.create_oval(cx-5, cy-5, cx+5, cy+5, fill=ACCENT_BLUE, outline=TEXT_WHITE)
        if hasattr(self, 'vki_val'):
            self.create_text(cx, cy-25, text=f"{self.vki_val:.1f}", fill=TEXT_WHITE, font=("Segoe UI", 14, "bold"))

# ==========================================
# GEÇMİŞ GRAFİK MOTORU
# ==========================================
class CanvasLineChart(tk.Canvas):
    def __init__(self, parent, width=500, height=200, **kwargs):
        super().__init__(parent, width=width, height=height, bg=CARD_BG, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height

    def ciz_grafik(self, veriler):
        self.delete("all")
        if not veriler or len(veriler) < 2:
            self.create_text(self.width/2, self.height/2, text="Grafik için en az 2 kayıt gereklidir.", fill=TEXT_MUTED, font=("Segoe UI", 10))
            return

        vkiler = [v[7] for v in veriler]
        tarihler = [v[1].split()[0] for v in veriler]

        padding = 40
        w = self.width - (padding * 2)
        h = self.height - (padding * 2)

        min_vki = max(10, min(vkiler) - 2)
        max_vki = min(50, max(vkiler) + 2)

        for i in range(4):
            y = padding + (h / 3) * i
            self.create_line(padding, y, self.width - padding, y, fill=CARD_BORDER, dash=(2, 2))
            val = max_vki - ((max_vki - min_vki) / 3) * i
            self.create_text(padding - 15, y, text=f"{val:.0f}", fill=TEXT_MUTED, font=("Consolas", 8))

        noktalar = []
        for i, vki in enumerate(vkiler):
            x = padding + (w / (len(vkiler) - 1)) * i
            y = padding + h - ((vki - min_vki) / (max_vki - min_vki)) * h
            noktalar.append((x, y))

            self.create_oval(x-4, y-4, x+4, y+4, fill=ACCENT_BLUE, outline=TEXT_WHITE)
            self.create_text(x, self.height - padding + 15, text=tarihler[i][-5:], fill=TEXT_MUTED, font=("Consolas", 7))

        for i in range(len(noktalar) - 1):
            self.create_line(noktalar[i][0], noktalar[i][1], noktalar[i+1][0], noktalar[i+1][1], fill=ACCENT_BLUE, width=2)

# ==========================================
# ÖZEL MAKRO İLERLEME BARI
# ==========================================
class MacroBar(tk.Frame):
    def __init__(self, parent, etiket, renk, **kwargs):
        super().__init__(parent, bg=CARD_BG, **kwargs)
        self.renk = renk

        self.lbl = tk.Label(self, text=f"{etiket}: 0g", bg=CARD_BG, fg=TEXT_WHITE, font=("Segoe UI", 9, "bold"), anchor="w")
        self.lbl.pack(fill="x")

        self.canvas = tk.Canvas(self, height=10, bg=CARD_BORDER, highlightthickness=0)
        self.canvas.pack(fill="x", pady=(2, 8))

    def guncelle(self, gram, max_gram=200):
        self.lbl.config(text=f"{self.lbl.cget('text').split(':')[0]}: {gram:.1f}g")
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        if w <= 1: w = 200
        oran = min(1.0, gram / max_gram)
        self.canvas.create_rectangle(0, 0, w * oran, 10, fill=self.renk, outline="")

# ==========================================
# ANA UYGULAMA (PRO DASHBOARD)
# ==========================================
class HealthDashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HealthPro Enterprise v2.0 - Biyometrik SaaS Paneli")
        
        # DÜZELTME 1: "1100 x 760" içerisindeki boşluklar kaldırıldı.
        self.geometry("1100x760")
        self.configure(bg=BG_DARK)

        self.db = DatabaseManager()
        self.stil_olustur()
        self.arayuz_kur()

    def stil_olustur(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(".", background=BG_DARK, foreground=TEXT_WHITE, font=("Segoe UI", 10))
        self.style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=CARD_BG, foreground=TEXT_MUTED, padding=[20, 8], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", ACCENT_BLUE)], foreground=[("selected", BG_DARK)])
        
        self.style.configure("Card.TFrame", background=CARD_BG, relief="flat")
        self.style.configure("TButton", background=ACCENT_BLUE, foreground=BG_DARK, borderwidth=0, font=("Segoe UI", 10, "bold"))
        self.style.map("TButton", background=[("active", "#0284c7")])

    def arayuz_kur(self):
        top_bar = tk.Frame(self, bg=CARD_BG, height=60)
        top_bar.pack(fill="x", side="top")
        
        lbl_logo = tk.Label(top_bar, text="⚡ HEALTHPRO SAAS", bg=CARD_BG, fg=ACCENT_BLUE, font=("Segoe UI", 14, "bold"))
        lbl_logo.pack(side="left", padx=20, pady=15)

        # DÜZELTME 2: px ve py -> padx ve pady olarak güncellendi.
        self.lbl_skor_badge = tk.Label(top_bar, text="Sağlık Skoru: --", bg=CARD_BORDER, fg=ACCENT_GREEN, font=("Segoe UI", 10, "bold"), padx=10, pady=4)
        self.lbl_skor_badge.pack(side="right", padx=20)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_dashboard = tk.Frame(self.notebook, bg=BG_DARK)
        self.tab_analytics = tk.Frame(self.notebook, bg=BG_DARK)

        self.notebook.add(self.tab_dashboard, text="🖥️ Canlı Kontrol Paneli")
        self.notebook.add(self.tab_analytics, text="📈 Geçmiş & Grafik Analizleri")

        self.sekme_dashboard_kur()
        self.sekme_analytics_kur()

    def sekme_dashboard_kur(self):
        sol_kart = tk.Frame(self.tab_dashboard, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        sol_kart.place(x=10, y=10, width=360, height=640)

        lbl_title = tk.Label(sol_kart, text="BİYOMETRİK PARAMETRELER", bg=CARD_BG, fg=TEXT_WHITE, font=("Segoe UI", 11, "bold"))
        lbl_title.pack(anchor="w", padx=15, pady=15)

        inputs = [
            ("Kullanıcı / Danışan Adı", "ent_isim", "Batuhan Kandemir"),
            ("Yaş", "ent_yas", "24"),
            ("Kilo (kg)", "ent_kilo", "75"),
            ("Boy (cm)", "ent_boy", "180")
        ]

        for label, var_name, def_val in inputs:
            lbl = tk.Label(sol_kart, text=label, bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 9))
            lbl.pack(anchor="w", padx=15, pady=(5, 0))
            ent = tk.Entry(sol_kart, bg=BG_DARK, fg=TEXT_WHITE, insertbackground=TEXT_WHITE, relief="flat", highlightbackground=CARD_BORDER, highlightthickness=1, font=("Segoe UI", 10))
            ent.insert(0, def_val)
            ent.pack(fill="x", padx=15, pady=(2, 8), ipady=4)
            setattr(self, var_name, ent)

        tk.Label(sol_kart, text="Cinsiyet", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(5, 0))
        self.var_cinsiyet = tk.StringVar(value="Erkek")
        f_cin = tk.Frame(sol_kart, bg=CARD_BG)
        f_cin.pack(fill="x", padx=15, pady=2)
        tk.Radiobutton(f_cin, text="Erkek", value="Erkek", variable=self.var_cinsiyet, bg=CARD_BG, fg=TEXT_WHITE, selectcolor=BG_DARK, activebackground=CARD_BG, activeforeground=TEXT_WHITE).pack(side="left")
        tk.Radiobutton(f_cin, text="Kadın", value="Kadın", variable=self.var_cinsiyet, bg=CARD_BG, fg=TEXT_WHITE, selectcolor=BG_DARK, activebackground=CARD_BG, activeforeground=TEXT_WHITE).pack(side="left", padx=15)

        tk.Label(sol_kart, text="Günlük Aktivite Düzeyi", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(5, 0))
        self.cmb_aktivite = ttk.Combobox(sol_kart, state="readonly", values=["Masa Başı / Hareketsiz", "Az Hareketli (1-3 Gün)", "Orta Hareketli (3-5 Gün)", "Çok Aktif (6-7 Gün)"])
        self.cmb_aktivite.current(1)
        self.cmb_aktivite.pack(fill="x", padx=15, pady=4)

        tk.Label(sol_kart, text="Beslenme Target/Hedefi", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w", padx=15, pady=(5, 0))
        self.cmb_hedef = ttk.Combobox(sol_kart, state="readonly", values=["Kilo Ver (Kalori Açığı)", "Kilonu Koru (Denge)", "Kilo Al / Kas Yap (Surplus)"])
        self.cmb_hedef.current(0)
        self.cmb_hedef.pack(fill="x", padx=15, pady=4)

        btn_calc = ttk.Button(sol_kart, text="⚡ HESAPLA VE METRİKLERİ İŞLE", command=self.hesapla_pro)
        btn_calc.pack(fill="x", padx=15, pady=20, ipady=6)

        sag_container = tk.Frame(self.tab_dashboard, bg=BG_DARK)
        sag_container.place(x=380, y=10, width=680, height=640)

        kpi_frame = tk.Frame(sag_container, bg=BG_DARK)
        kpi_frame.pack(fill="x")

        self.card_vki = self.kpi_kart_olustur(kpi_frame, "VKİ ENDEKSİ", "--", "Durum: Wait", ACCENT_BLUE)
        self.card_bmr = self.kpi_kart_olustur(kpi_frame, "BAZAL METABOLİZMA", "--", "BMR (kcal/gün)", ACCENT_GREEN)
        self.card_tdee = self.kpi_kart_olustur(kpi_frame, "GÜNLÜK KALORİ", "--", "TDEE Hedef", ACCENT_YELLOW)

        mid_frame = tk.Frame(sag_container, bg=BG_DARK)
        mid_frame.pack(fill="x", pady=15)

        gauge_card = tk.Frame(mid_frame, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        gauge_card.pack(side="left", fill="both", expand=True, padx=(0, 5))
        tk.Label(gauge_card, text="GÖRSEL VKİ SKALASI", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(pady=5)
        self.gauge = AnimatedGauge(gauge_card)
        self.gauge.pack(pady=5)

        macro_card = tk.Frame(mid_frame, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        macro_card.pack(side="right", fill="both", expand=True, padx=(5, 0))
        tk.Label(macro_card, text="GÜNLÜK HEDEF MAKROLAR", bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 9, "bold")).pack(pady=5, padx=10, anchor="w")
        
        self.bar_protein = MacroBar(macro_card, "Protein", ACCENT_BLUE)
        self.bar_protein.pack(fill="x", padx=10)
        self.bar_karb = MacroBar(macro_card, "Karbonhidrat", ACCENT_GREEN)
        self.bar_karb.pack(fill="x", padx=10)
        self.bar_yag = MacroBar(macro_card, "Sağlıklı Yağ", ACCENT_YELLOW)
        self.bar_yag.pack(fill="x", padx=10)

        report_card = tk.Frame(sag_container, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        report_card.pack(fill="both", expand=True)

        btn_bar = tk.Frame(report_card, bg=CARD_BG)
        btn_bar.pack(fill="x", padx=10, pady=5)
        tk.Label(btn_bar, text="ÖZET ANALİZ ÇIKTISI", bg=CARD_BG, fg=TEXT_WHITE, font=("Segoe UI", 9, "bold")).pack(side="left")
        
        ttk.Button(btn_bar, text="🌐 HTML Web Raporu Oluştur & Aç", command=self.export_html_rapor).pack(side="right")

        self.txt_out = tk.Text(report_card, bg=BG_DARK, fg=ACCENT_GREEN, font=("Consolas", 9), relief="flat", highlightthickness=0)
        self.txt_out.pack(fill="both", expand=True, padx=10, pady=5)

    def kpi_kart_olustur(self, parent, baslik, val, sub, renk):
        card = tk.Frame(parent, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=3)
        tk.Label(card, text=baslik, bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
        lbl_val = tk.Label(card, text=val, bg=CARD_BG, fg=renk, font=("Segoe UI", 16, "bold"))
        lbl_val.pack(anchor="w", padx=10)
        lbl_sub = tk.Label(card, text=sub, bg=CARD_BG, fg=TEXT_MUTED, font=("Segoe UI", 8))
        lbl_sub.pack(anchor="w", padx=10, pady=(0, 8))
        return (lbl_val, lbl_sub)

    def sekme_analytics_kur(self):
        chart_card = tk.Frame(self.tab_analytics, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        chart_card.pack(fill="x", padx=10, pady=10)
        tk.Label(chart_card, text="ZAMAN İÇİNDEKİ VKİ DEĞİŞİM GRAFİĞİ", bg=CARD_BG, fg=TEXT_WHITE, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=8)

        self.chart = CanvasLineChart(chart_card)
        self.chart.pack(fill="x", padx=15, pady=(0, 15))

        table_card = tk.Frame(self.tab_analytics, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        table_card.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("ID", "Tarih", "İsim", "Yaş", "Cins", "Kilo", "Boy", "VKİ", "Durum", "BMR", "TDEE", "Skor")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", height=8)
        
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=65, anchor="center")
        self.tree.column("Tarih", width=110)
        self.tree.column("İsim", width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        b_bar = tk.Frame(table_card, bg=CARD_BG)
        b_bar.pack(fill="x", padx=10, pady=5)
        ttk.Button(b_bar, text="Verileri Yenile", command=self.gecmis_yukle).pack(side="left")
        ttk.Button(b_bar, text="Seçili Kaydı Sil", command=self.kayit_sil).pack(side="left", padx=10)

    def hesapla_pro(self):
        try:
            isim = self.ent_isim.get()
            yas = int(self.ent_yas.get())
            kilo = float(self.ent_kilo.get())
            boy = float(self.ent_boy.get())
            cins = self.var_cinsiyet.get()

            boy_m = boy / 100.0 if boy > 3 else boy
            boy_cm = boy if boy > 3 else boy * 100.0

            vki = kilo / (boy_m ** 2)
            if vki < 18.5: durum = "Zayıf"; color = ACCENT_BLUE
            elif 18.5 <= vki < 25: durum = "İdeal Kilo"; color = ACCENT_GREEN
            elif 25 <= vki < 30: durum = "Fazla Kilolu"; color = ACCENT_YELLOW
            else: durum = "Obezite Risk"; color = ACCENT_RED

            if cins == "Erkek": bmr = (10 * kilo) + (6.25 * boy_cm) - (5 * yas) + 5
            else: bmr = (10 * kilo) + (6.25 * boy_cm) - (5 * yas) - 161

            akt_mult = [1.2, 1.375, 1.55, 1.725][self.cmb_aktivite.current()]
            tdee = bmr * akt_mult

            hedef_idx = self.cmb_hedef.current()
            if hedef_idx == 0: target_cal = tdee - 500
            elif hedef_idx == 1: target_cal = tdee
            else: target_cal = tdee + 400

            protein = kilo * 2.0
            yag = (target_cal * 0.25) / 9.0
            karb = (target_cal - (protein*4 + yag*9)) / 4.0

            vki_fark = abs(vki - 22.0)
            skor = max(20, int(100 - (vki_fark * 4)))

            self.card_vki[0].config(text=f"{vki:.1f}", fg=color)
            self.card_vki[1].config(text=f"Durum: {durum}")

            self.card_bmr[0].config(text=f"{bmr:.0f}")
            self.card_tdee[0].config(text=f"{target_cal:.0f}")

            self.gauge.animasyonlu_set(vki)
            self.bar_protein.guncelle(protein, 250)
            self.bar_karb.guncelle(max(0, karb), 350)
            self.bar_yag.guncelle(yag, 120)

            self.lbl_skor_badge.config(text=f"Sağlık Skoru: {skor}/100")

            self.last_report_data = {
                "isim": isim, "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "vki": vki, "durum": durum, "bmr": bmr, "tdee": target_cal,
                "protein": protein, "karb": karb, "yag": yag, "skor": skor, "kilo": kilo, "boy": boy_cm
            }

            report_txt = f"PRO ANALİZ RAPORU | {self.last_report_data['tarih']}\n"
            report_txt += f"--------------------------------------------------\n"
            report_txt += f"• Metrik Sağlık Skoru   : {skor}/100\n"
            report_txt += f"• Önerilen Su Tüketimi  : {kilo * 0.035:.2f} Litre/gün\n"
            report_txt += f"• Hedef Makro Dağılımı  : {protein:.0f}g P / {max(0, karb):.0f}g K / {yag:.0f}g Y\n"
            
            self.txt_out.delete("1.0", tk.END)
            self.txt_out.insert(tk.END, report_txt)

            t_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.db.kayit_ekle((t_str, isim, yas, cins, kilo, boy_cm, vki, durum, bmr, target_cal, skor))
            self.gecmis_yukle()

            if winsound:
                winsound.Beep(1000, 150)

        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler giriniz.")

    def gecmis_yukle(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        veriler = self.db.kayitlari_getir()
        for v in veriler:
            self.tree.insert("", "end", values=(v[0], v[1], v[2], v[3], v[4], v[5], v[6], f"{v[7]:.1f}", v[8], f"{v[9]:.0f}", f"{v[10]:.0f}", v[11]))
        
        self.chart.ciz_grafik(veriler)

    def kayit_sil(self):
        selected = self.tree.selection()
        if selected:
            kid = self.tree.item(selected[0])["values"][0]
            self.db.kayit_sil(kid)
            self.gecmis_yukle()

    def export_html_rapor(self):
        if not hasattr(self, 'last_report_data'):
            messagebox.showwarning("Uyarı", "Lütfen önce bir hesaplama yapın!")
            return

        d = self.last_report_data
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>HealthPro Raporu - {d['isim']}</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }}
                .card {{ background: #1e293b; border-radius: 12px; padding: 25px; margin-bottom: 20px; border: 1px solid #334155; }}
                h1 {{ color: #38bdf8; margin-top: 0; }}
                .metric {{ font-size: 24px; font-weight: bold; color: #10b981; }}
                .badge {{ background: #38bdf8; color: #0f172a; padding: 5px 12px; border-radius: 20px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>⚡ HEALTHPRO BIOMETRIC REPORT</h1>
                <p><strong>Danışan:</strong> {d['isim']} | <strong>Tarih:</strong> {d['tarih']}</p>
                <span class="badge">Sağlık Skoru: {d['skor']}/100</span>
            </div>
            <div class="card">
                <h3>Vücut Metrikleri</h3>
                <p>VKİ Değeri: <span class="metric">{d['vki']:.1f}</span> ({d['durum']})</p>
                <p>Bazal Metabolizma (BMR): <strong>{d['bmr']:.0f} kcal</strong></p>
                <p>Günlük Hedef Kalori: <strong>{d['tdee']:.0f} kcal</strong></p>
            </div>
            <div class="card">
                <h3>Günlük Makro İhtiyacı</h3>
                <ul>
                    <li>Protein: {d['protein']:.1f} gram</li>
                    <li>Karbonhidrat: {max(0, d['karb']):.1f} gram</li>
                    <li>Yağ: {d['yag']:.1f} gram</li>
                </ul>
            </div>
        </body>
        </html>
        """

        file_path = os.path.abspath("saglik_raporu.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_code)

        webbrowser.open(f"file://{file_path}")
        messagebox.showinfo("Rapor Hazır", "HTML Sağlık Raporu oluşturuldu ve varsayılan tarayıcınızda açıldı!")

if __name__ == "__main__":
    app = HealthDashboardApp()
    app.mainloop()