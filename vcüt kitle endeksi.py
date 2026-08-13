import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import math
import json
from datetime import datetime

# ==========================================
# VERİTABANI YÖNETİCİSİ (SQLITE3)
# ==========================================
class DatabaseManager:
    def __init__(self, db_name="saglik_gecmisi.db"):
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
                yag_orani REAL
            )
        ''')
        self.conn.commit()

    def kayit_ekle(self, veri):
        self.cursor.execute('''
            INSERT INTO kayitlar (tarih, isim, yas, cinsiyet, kilo, boy, vki, vki_durum, bmr, tdee, yag_orani)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', veri)
        self.conn.commit()

    def kayitlari_getir(self):
        self.cursor.execute('SELECT * FROM kayitlar ORDER BY id DESC')
        return self.cursor.fetchall()

    def kayit_sil(self, kayit_id):
        self.cursor.execute('DELETE FROM kayitlar WHERE id = ?', (kayit_id,))
        self.conn.commit()

# ==========================================
# ÖZEL GÖSTERGE ÇİZİCİ (GAUGE METER)
# ==========================================
class BMIGauge(tk.Canvas):
    def __init__(self, parent, width=300, height=160, **kwargs):
        super().__init__(parent, width=width, height=height, bg="#2d2d2d", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.ciz_arkaplan()

    def ciz_arkaplan(self):
        self.delete("all")
        # Renkli Alanlar (Zayıf, Normal, Fazla, Obez)
        # Yay acıları: 180 derecelik yarım daire
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=135, extent=-33.75, fill="#3498db", outline="")
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=101.25, extent=-33.75, fill="#2ecc71", outline="")
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=67.5, extent=-33.75, fill="#f1c40f", outline="")
        self.create_arc(20, 20, self.width-20, self.height*2-20, start=33.75, extent=-33.75, fill="#e74c3c", outline="")

        # İç Beyaz/Koyu Daire (Donut görünümü için)
        self.create_oval(60, 60, self.width-60, self.height*2-60, fill="#2d2d2d", outline="")

        # Etiketler
        self.create_text(40, 130, text="18.5", fill="#ffffff", font=("Consolas", 8))
        self.create_text(110, 50, text="25", fill="#ffffff", font=("Consolas", 8))
        self.create_text(190, 50, text="30", fill="#ffffff", font=("Consolas", 8))
        self.create_text(260, 130, text="40", fill="#ffffff", font=("Consolas", 8))

    def ibre_guncelle(self, vki):
        self.ciz_arkaplan()
        # VKİ Değerini Dereceye Dönüştür (15 ile 40 arası haritalama)
        clamped_vki = max(15.0, min(vki, 40.0))
        # 15 VKİ = 135 derece, 40 VKİ = 0 derece
        orad = (clamped_vki - 15) / (40 - 15)
        aci_derece = 135 - (orad * 135)
        aci_radyan = math.radians(aci_derece)

        # İbre Merkez Noktası
        cx, cy = self.width / 2, self.height - 10
        r = self.width / 2 - 40

        ix = cx + r * math.cos(aci_radyan)
        iy = cy - r * math.sin(aci_radyan)

        # İbre Çizimi
        self.create_line(cx, cy, ix, iy, fill="#ffffff", width=3)
        self.create_oval(cx-6, cy-6, cx+6, cy+6, fill="#e74c3c", outline="#ffffff")
        self.create_text(cx, cy-25, text=f"VKİ: {vki:.1f}", fill="#ffffff", font=("Segoe UI", 12, "bold"))

# ==========================================
# ANA UYGULAMA PENCERESİ
# ==========================================
class HealthSuiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HealthPro Enterprise - Biyometrik Analiz Suite")
        self.geometry("950x700")
        self.configure(bg="#1e1e1e")

        self.db = DatabaseManager()
        self.stil_ayarla()
        self.arayuz_olustur()

    def stil_ayarla(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Koyu Tema Renkleri
        self.style.configure(".", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        self.style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#2d2d2d", foreground="#ffffff", padding=[15, 5])
        self.style.map("TNotebook.Tab", background=[("selected", "#007acc")])
        self.style.configure("TFrame", background="#1e1e1e")
        self.style.configure("TLabelframe", background="#2d2d2d", foreground="#007acc", borderwidth=1)
        self.style.configure("TLabelframe.Label", background="#2d2d2d", foreground="#007acc", font=("Segoe UI", 11, "bold"))
        self.style.configure("TButton", background="#007acc", foreground="#ffffff", borderwidth=0, font=("Segoe UI", 10, "bold"))
        self.style.map("TButton", background=[("active", "#005999")])

    def arayuz_olustur(self):
        # Başlık Barı
        baslik_frame = tk.Frame(self, bg="#007acc", height=50)
        baslik_frame.pack(fill="x")
        lbl_baslik = tk.Label(baslik_frame, text="HEALTHPRO BİYOMETRİK VE BESLENME ANALİZ SİSTEMİ", bg="#007acc", fg="white", font=("Segoe UI", 14, "bold"))
        lbl_baslik.pack(pady=10)

        # Tab Yapısı
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Sekmeler
        self.tab_analiz = ttk.Frame(self.notebook)
        self.tab_yag = ttk.Frame(self.notebook)
        self.tab_gecmis = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_analiz, text="📊 Genel Hesaplayıcı & Analiz")
        self.notebook.add(self.tab_yag, text="📐 Vücut Yağ Oranı (Donanma)")
        self.notebook.add(self.tab_gecmis, text="📜 Geçmiş Veri Tabanı")

        self.sekme_analiz_kur()
        self.sekme_yag_kur()
        self.sekme_gecmis_kur()

    # -------------------------------------------------------------
    # SEKME 1: GENEL HESAPLAYICI & ANALİZ
    # -------------------------------------------------------------
    def sekme_analiz_kur(self):
        left_frame = ttk.LabelFrame(self.tab_analiz, text=" Kullanıcı Biyometrik Verileri ", padding=15)
        left_frame.place(x=10, y=10, width=420, height=580)

        right_frame = ttk.LabelFrame(self.tab_analiz, text=" Analiz Sonuçları ve Gösterge ", padding=15)
        right_frame.place(x=440, y=10, width=480, height=580)

        # Girdi Alanları
        fields = [
            ("Ad Soyad / İsim:", "ent_isim"),
            ("Yaş:", "ent_yas"),
            ("Kilo (kg):", "ent_kilo"),
            ("Boy (cm):", "ent_boy")
        ]

        for i, (label_text, var_name) in enumerate(fields):
            lbl = ttk.Label(left_frame, text=label_text)
            lbl.grid(row=i, column=0, sticky="w", pady=8)
            ent = ttk.Entry(left_frame)
            ent.grid(row=i, column=1, sticky="ew", pady=8, padx=5)
            setattr(self, var_name, ent)

        # Cinsiyet
        ttk.Label(left_frame, text="Cinsiyet:").grid(row=4, column=0, sticky="w", pady=8)
        self.var_cinsiyet = tk.StringVar(value="Erkek")
        rb_e = ttk.Radiobutton(left_frame, text="Erkek", value="Erkek", variable=self.var_cinsiyet)
        rb_k = ttk.Radiobutton(left_frame, text="Kadın", value="Kadın", variable=self.var_cinsiyet)
        rb_e.grid(row=4, column=1, sticky="w")
        rb_k.grid(row=4, column=1, sticky="e")

        # Aktivite Seviyesi
        ttk.Label(left_frame, text="Aktivite Seviyesi:").grid(row=5, column=0, sticky="w", pady=8)
        self.cmb_aktivite = ttk.Combobox(left_frame, state="readonly", values=[
            "Masa Başı / Hareketsiz",
            "Az Hareketli (Haftada 1-3 gün)",
            "Orta Hareketli (Haftada 3-5 gün)",
            "Çok Hareketli (Haftada 6-7 gün)",
            "Aşırı Spor / Ağır İş"
        ])
        self.cmb_aktivite.current(0)
        self.cmb_aktivite.grid(row=5, column=1, sticky="ew", pady=8, padx=5)

        # Hedef
        ttk.Label(left_frame, text="Beslenme Hedefi:").grid(row=6, column=0, sticky="w", pady=8)
        self.cmb_hedef = ttk.Combobox(left_frame, state="readonly", values=[
            "Kilo Ver (Kalori Açığı)",
            "Kilonu Koru",
            "Kilo Al / Kas Yap (Kalori Fazlası)"
        ])
        self.cmb_hedef.current(1)
        self.cmb_hedef.grid(row=6, column=1, sticky="ew", pady=8, padx=5)

        # Hesapla Butonu
        btn_hesapla = ttk.Button(left_frame, text="KAPASİTELİ ANALİZİ BAŞLAT", command=self.hesapla_main)
        btn_hesapla.grid(row=7, column=0, columnspan=2, sticky="ew", pady=20)

        # Sağ Taraf (Sonuçlar)
        self.gauge = BMIGauge(right_frame)
        self.gauge.pack(pady=10)

        self.txt_sonuc = tk.Text(right_frame, bg="#1e1e1e", fg="#00ff88", font=("Consolas", 9), borderwidth=0)
        self.txt_sonuc.pack(fill="both", expand=True, pady=5)

        btn_rapor = ttk.Button(right_frame, text="💾 Raporu Dışa Aktar (TXT/JSON)", command=self.rapor_aktar)
        btn_rapor.pack(fill="x", pady=5)

    # -------------------------------------------------------------
    # SEKME 2: DONANMA YAĞ ORANI
    # -------------------------------------------------------------
    def sekme_yag_kur(self):
        frame = ttk.LabelFrame(self.tab_yag, text=" ABD Donanması Vücut Yağ Oranı Yöntemi ", padding=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(frame, text="Bel Çevresi (cm):").grid(row=0, column=0, sticky="w", pady=10)
        self.ent_bel = ttk.Entry(frame)
        self.ent_bel.grid(row=0, column=1, pady=10)

        ttk.Label(frame, text="Boyun Çevresi (cm):").grid(row=1, column=0, sticky="w", pady=10)
        self.ent_boyun = ttk.Entry(frame)
        self.ent_boyun.grid(row=1, column=1, pady=10)

        ttk.Label(frame, text="Kalça Çevresi (cm - Kadınlar İçin):").grid(row=2, column=0, sticky="w", pady=10)
        self.ent_kalca = ttk.Entry(frame)
        self.ent_kalca.grid(row=2, column=1, pady=10)

        btn_yag_hesapla = ttk.Button(frame, text="Yağ Oranını Hesapla", command=self.hesapla_yag_donanma)
        btn_yag_hesapla.grid(row=3, column=0, columnspan=2, sticky="ew", pady=20)

        self.lbl_yag_sonuc = ttk.Label(frame, text="Tahmini Yağ Oranı: -", font=("Segoe UI", 12, "bold"), foreground="#007acc")
        self.lbl_yag_sonuc.grid(row=4, column=0, columnspan=2, pady=10)

    # -------------------------------------------------------------
    # SEKME 3: GEÇMİŞ VERİTABANI
    # -------------------------------------------------------------
    def sekme_gecmis_kur(self):
        # Treeview Tablosu
        cols = ("ID", "Tarih", "İsim", "Yaş", "Cinsiyet", "Kilo", "Boy", "VKİ", "Durum", "BMR", "TDEE")
        self.tree = ttk.Treeview(self.tab_gecmis, columns=cols, show="headings", height=18)
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=75, anchor="center")

        self.tree.column("İsim", width=110)
        self.tree.column("Tarih", width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.tab_gecmis)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Yenile / Listele", command=self.gecmis_yukle).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Seçili Kaydı Sil", command=self.kayit_sil_main).pack(side="left", padx=5)

    # ==========================================
    # HESAPLAMA MANTIKLARI VE MOTOR
    # ==========================================
    def hesapla_main(self):
        try:
            isim = self.ent_isim.get().strip() or "Anonim"
            yas = int(self.ent_yas.get())
            kilo = float(self.ent_kilo.get())
            boy = float(self.ent_boy.get())
            cinsiyet = self.var_cinsiyet.get()

            if boy > 3: boy_m = boy / 100.0
            else: boy_m = boy; boy = boy * 100.0

            # 1. VKİ Hesaplama
            vki = kilo / (boy_m ** 2)
            if vki < 18.5: durum = "Zayıf"
            elif 18.5 <= vki < 25: durum = "Normal (İdeal)"
            elif 25 <= vki < 30: durum = "Fazla Kilolu"
            elif 30 <= vki < 35: durum = "1. Derece Obez"
            else: durum = "İleri Derece Obez"

            # 2. BMR (Mifflin-St Jeor)
            if cinsiyet == "Erkek":
                bmr = (10 * kilo) + (6.25 * boy) - (5 * yas) + 5
            else:
                bmr = (10 * kilo) + (6.25 * boy) - (5 * yas) - 161

            # 3. TDEE
            akt_çarpanlar = [1.2, 1.375, 1.55, 1.725, 1.9]
            tdee = bmr * akt_çarpanlar[self.cmb_aktivite.current()]

            # 4. Makro Dağılımı
            hedef_idx = self.cmb_hedef.current()
            if hedef_idx == 0: hedef_kalori = tdee - 500  # Kilo Ver
            elif hedef_idx == 1: hedef_kalori = tdee     # Koru
            else: hedef_kalori = tdee + 400              # Kilo Al

            protein_g = kilo * 2.0
            yag_g = (hedef_kalori * 0.25) / 9.0
            karb_g = (hedef_kalori - (protein_g * 4 + yag_g * 9)) / 4.0

            # 5. Su İhtiyacı
            su_litre = kilo * 0.035

            # UI Güncelle
            self.gauge.ibre_guncelle(vki)

            self.sonuc_metni = f"""
==================================================
           BİYOMETRİK SAĞLIK RAPORU
==================================================
Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Kullanıcı: {isim} | Yaş: {yas} | Cinsiyet: {cinsiyet}
--------------------------------------------------
[1] VÜCUT KİTLE ENDEKSİ (VKİ)
    • Değer        : {vki:.2f} kg/m²
    • Sağlık Durumu: {durum}

[2] ENERJİ METABOLİZMASI
    • Bazal Metabolizma (BMR) : {bmr:.0f} kcal/gün
    • Günlük İhtiyaç (TDEE)   : {tdee:.0f} kcal/gün
    • Hedef Kalori Alımı      : {hedef_kalori:.0f} kcal/gün

[3] HEDEF MAKRO BESİN DAĞILIMI
    • Protein     : {protein_g:.1f} g/gün
    • Karbonhidrat: {max(0, karb_g):.1f} g/gün
    • Yağ         : {yag_g:.1f} g/gün

[4] HİDRASYON
    • İdeal Su İhtiyacı: {su_litre:.2f} Litre/gün
==================================================
"""
            self.txt_sonuc.delete("1.0", tk.END)
            self.txt_sonuc.insert(tk.END, self.sonuc_metni)

            # Veritabanına Kaydet
            tarih_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.db.kayit_ekle((tarih_str, isim, yas, cinsiyet, kilo, boy, vki, durum, bmr, tdee, 0.0))
            self.gecmis_yukle()

        except ValueError:
            messagebox.showerror("Hata", "Lütfen tüm biyometrik verileri geçerli sayılar olarak giriniz!")

    def hesapla_yag_donanma(self):
        try:
            bel = float(self.ent_bel.get())
            boyun = float(self.ent_boyun.get())
            boy = float(self.ent_boy.get()) if self.ent_boy.get() else 170.0
            cinsiyet = self.var_cinsiyet.get()

            if cinsiyet == "Erkek":
                yag_orani = 495 / (1.0324 - 0.19077 * math.log10(bel - boyun) + 0.15456 * math.log10(boy)) - 450
            else:
                kalca = float(self.ent_kalca.get())
                yag_orani = 495 / (1.29579 - 0.35004 * math.log10(bel + kalca - boyun) + 0.22100 * math.log10(boy)) - 450

            self.lbl_yag_sonuc.config(text=f"Tahmini Vücut Yağ Oranı: %{yag_orani:.1f}")
        except Exception:
            messagebox.showerror("Hata", "Lütfen ölçümleri tam ve doğru giriniz (Kadınlar için Kalça Çevresi zorunludur).")

    def gecmis_yukle(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        kayitlar = self.db.kayitlari_getir()
        for k in kayitlar:
            # k: (id, tarih, isim, yas, cinsiyet, kilo, boy, vki, vki_durum, bmr, tdee, yag_orani)
            self.tree.insert("", "end", values=(k[0], k[1], k[2], k[3], k[4], k[5], k[6], f"{k[7]:.1f}", k[8], f"{k[9]:.0f}", f"{k[10]:.0f}"))

    def kayit_sil_main(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            kayit_id = item["values"][0]
            self.db.kayit_sil(kayit_id)
            self.gecmis_yukle()
            messagebox.showinfo("Başarılı", "Kayıt veritabanından silindi.")

    def rapor_aktar(self):
        if not hasattr(self, 'sonuc_metni'):
            messagebox.showwarning("Uyarı", "Önce bir hesaplama yapmalısınız!")
            return

        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Dosyası", "*.txt"), ("JSON Dosyası", "*.json")])
        if dosya_yolu:
            if dosya_yolu.endswith(".json"):
                data = {"rapor": self.txt_sonuc.get("1.0", tk.END)}
                with open(dosya_yolu, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            else:
                with open(dosya_yolu, "w", encoding="utf-8") as f:
                    f.write(self.txt_sonuc.get("1.0", tk.END))
            messagebox.showinfo("Başarılı", "Sağlık raporu başarıyla kaydedildi.")

# ==========================================
# UYGULAMAYI BAŞLAT
# ==========================================
if __name__ == "__main__":
    app = HealthSuiteApp()
    app.mainloop()