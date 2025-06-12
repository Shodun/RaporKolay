import tkinter as tk
from tkinter import ttk, filedialog
import sqlite3
from datetime import datetime
import openpyxl
import matplotlib.pyplot as plt
from collections import defaultdict
import os

class RaporKolayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RaporKolay")
        self.root.geometry("800x600")
        self.root.configure(bg="#ecf0f1")  # Flat UI clouds color
        
        # Veritabanı bağlantısı
        self.conn = sqlite3.connect("veriler.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS islemler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT,
                kategori TEXT,
                aciklama TEXT,
                tutar REAL
            )
        """)
        self.conn.commit()
        
        # Değişkenler
        self.kategori_var = tk.StringVar(value="Gelir")
        
        # Tema ayarları
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Flat UI Renk paleti
        self.colors = {
            "primary": "#1abc9c",       # Turquoise
            "secondary": "#2ecc71",     # Emerald
            "warning": "#e74c3c",       # Alizarin
            "background": "#ecf0f1",    # Clouds
            "card": "#ffffff",          # White
            "text": "#2c3e50",          # Midnight Blue
            "accent1": "#3498db",       # Peter River
            "accent2": "#9b59b6",       # Amethyst
            "dark": "#34495e",          # Wet Asphalt
            "light": "#f5f5f5"          # Light Gray
        }
        
        # Stil ayarları - Flat UI
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("Card.TFrame", background=self.colors["card"])
        self.style.configure("Main.TFrame", background=self.colors["background"])
        
        # Flat buton stili
        self.style.configure("TButton", 
                             font=("Segoe UI", 10),
                             background=self.colors["primary"],
                             foreground="white",
                             borderwidth=0,
                             focusthickness=0,
                             padding=8)
        
        # Flat label stili
        self.style.configure("TLabel", 
                             font=("Segoe UI", 10),
                             background=self.colors["background"],
                             foreground=self.colors["text"])
        
        # Card içindeki label stili
        self.style.configure("Card.TLabel", 
                             background=self.colors["card"],
                             foreground=self.colors["text"])
        
        # Giriş alanları
        self.style.configure("TEntry", 
                             font=("Segoe UI", 10),
                             fieldbackground=self.colors["light"],
                             borderwidth=1,
                             padding=6)
        
        # Combobox stili
        self.style.configure("TCombobox",
                             padding=6,
                             fieldbackground=self.colors["light"])
        
        # Tablo stili
        self.style.configure("Treeview", 
                             font=("Segoe UI", 10),
                             background=self.colors["card"],
                             fieldbackground=self.colors["card"],
                             foreground=self.colors["text"],
                             rowheight=30)
        
        self.style.configure("Treeview.Heading", 
                             font=("Segoe UI", 10, "bold"),
                             background=self.colors["primary"],
                             foreground="white",
                             padding=8)
        
        # Buton hover efekti
        self.style.map("TButton",
                       background=[("active", self.colors["accent1"])],
                       foreground=[("active", "white")])
                       
        # Treeview seçim rengi
        self.style.map("Treeview",
                      background=[("selected", self.colors["accent1"])],
                      foreground=[("selected", "white")])
        
        # Arayüz oluşturma
        self.create_widgets()
        
        # Verileri yükle
        self.listele()
    
    def create_widgets(self):
        # Ana çerçeve
        main_frame = ttk.Frame(self.root, padding=20, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol panel - Veri girişi
        left_frame = ttk.Frame(main_frame, padding=15, style="Card.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 15))
        
        # Başlık
        header_label = ttk.Label(left_frame, text="Yeni İşlem", 
                               font=("Segoe UI", 16, "bold"),
                               style="Card.TLabel")
        header_label.pack(pady=(0, 20), anchor="w")
        
        # Form alanları
        form_frame = ttk.Frame(left_frame, style="Card.TFrame")
        form_frame.pack(fill=tk.X, pady=5)
        
        # Kategori seçimi
        ttk.Label(form_frame, text="Kategori", 
                 style="Card.TLabel",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        kategori_combo = ttk.Combobox(form_frame, textvariable=self.kategori_var, 
                                     values=["Gelir", "Gider"], width=25)
        kategori_combo.pack(fill=tk.X, pady=(2, 15))
        
        # Açıklama girişi
        ttk.Label(form_frame, text="Açıklama", 
                 style="Card.TLabel",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.aciklama_entry = ttk.Entry(form_frame, width=25)
        self.aciklama_entry.pack(fill=tk.X, pady=(2, 15))
        
        # Tutar girişi
        ttk.Label(form_frame, text="Tutar (₺)", 
                 style="Card.TLabel",
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.tutar_entry = ttk.Entry(form_frame, width=25)
        self.tutar_entry.pack(fill=tk.X, pady=(2, 15))
        
        # Butonlar
        button_frame = ttk.Frame(left_frame, style="Card.TFrame")
        button_frame.pack(fill=tk.X, pady=15)
        
        # Özel buton stilleri
        self.style.configure("Primary.TButton", 
                            background=self.colors["primary"],
                            foreground="white")
        
        self.style.configure("Secondary.TButton", 
                            background=self.colors["secondary"],
                            foreground="white")
        
        self.style.configure("Warning.TButton", 
                            background=self.colors["warning"],
                            foreground="white")
        
        self.style.configure("Accent.TButton", 
                            background=self.colors["accent1"],
                            foreground="white")
        
        # Buton hover efektleri
        self.style.map("Primary.TButton",
                      background=[("active", "#16a085")])
        
        self.style.map("Secondary.TButton",
                      background=[("active", "#27ae60")])
        
        self.style.map("Warning.TButton",
                      background=[("active", "#c0392b")])
        
        self.style.map("Accent.TButton",
                      background=[("active", "#2980b9")])
        
        # Butonlar
        kaydet_btn = ttk.Button(button_frame, text="Kaydet", 
                               command=self.kaydet, 
                               style="Primary.TButton")
        kaydet_btn.pack(fill=tk.X, pady=5)
        
        sil_btn = ttk.Button(button_frame, text="Seçili Kaydı Sil", 
                            command=self.secili_kaydi_sil,
                            style="Warning.TButton")
        sil_btn.pack(fill=tk.X, pady=5)
        
        excel_btn = ttk.Button(button_frame, text="Excel'e Aktar", 
                              command=self.disari_aktar,
                              style="Secondary.TButton")
        excel_btn.pack(fill=tk.X, pady=5)
        
        grafik_btn = ttk.Button(button_frame, text="Aylık Grafik Göster", 
                               command=self.grafik_goster,
                               style="Accent.TButton")
        grafik_btn.pack(fill=tk.X, pady=5)
        
        # Durum etiketi
        self.durum_label = ttk.Label(left_frame, text="", 
                                    foreground=self.colors["primary"],
                                    style="Card.TLabel")
        self.durum_label.pack(pady=10)
        
        # Sağ panel - Tablo ve özet
        right_frame = ttk.Frame(main_frame, padding=15, style="Card.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Özet bilgileri
        ozet_frame = ttk.Frame(right_frame, style="Card.TFrame", padding=15)
        ozet_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Özet başlığı
        ttk.Label(ozet_frame, text="Finansal Özet", 
                 font=("Segoe UI", 16, "bold"),
                 style="Card.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Özet kartları
        ozet_cards = ttk.Frame(ozet_frame, style="Card.TFrame")
        ozet_cards.pack(fill=tk.X)
        
        # Gelir kartı
        gelir_card = ttk.Frame(ozet_cards, style="Card.TFrame", padding=10)
        gelir_card.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        ttk.Label(gelir_card, text="TOPLAM GELİR", 
                 font=("Segoe UI", 9, "bold"),
                 foreground=self.colors["dark"],
                 style="Card.TLabel").pack(anchor="w")
        
        self.gelir_label = ttk.Label(gelir_card, text="0 ₺", 
                                    foreground=self.colors["secondary"],
                                    font=("Segoe UI", 14, "bold"),
                                    style="Card.TLabel")
        self.gelir_label.pack(anchor="w", pady=(5, 0))
        
        # Gider kartı
        gider_card = ttk.Frame(ozet_cards, style="Card.TFrame", padding=10)
        gider_card.grid(row=0, column=1, padx=10, sticky="ew")
        
        ttk.Label(gider_card, text="TOPLAM GİDER", 
                 font=("Segoe UI", 9, "bold"),
                 foreground=self.colors["dark"],
                 style="Card.TLabel").pack(anchor="w")
        
        self.gider_label = ttk.Label(gider_card, text="0 ₺", 
                                    foreground=self.colors["warning"],
                                    font=("Segoe UI", 14, "bold"),
                                    style="Card.TLabel")
        self.gider_label.pack(anchor="w", pady=(5, 0))
        
        # Net kazanç kartı
        net_card = ttk.Frame(ozet_cards, style="Card.TFrame", padding=10)
        net_card.grid(row=0, column=2, padx=(10, 0), sticky="ew")
        
        ttk.Label(net_card, text="NET KAZANÇ", 
                 font=("Segoe UI", 9, "bold"),
                 foreground=self.colors["dark"],
                 style="Card.TLabel").pack(anchor="w")
        
        self.net_label = ttk.Label(net_card, text="0 ₺", 
                                  foreground=self.colors["primary"],
                                  font=("Segoe UI", 14, "bold"),
                                  style="Card.TLabel")
        self.net_label.pack(anchor="w", pady=(5, 0))
        
        # Sütun genişliklerini eşitle
        ozet_cards.grid_columnconfigure(0, weight=1)
        ozet_cards.grid_columnconfigure(1, weight=1)
        ozet_cards.grid_columnconfigure(2, weight=1)
        
        # İşlemler tablosu
        tablo_frame = ttk.Frame(right_frame, style="Card.TFrame", padding=15)
        tablo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tablo başlığı
        ttk.Label(tablo_frame, text="İşlem Geçmişi", 
                 font=("Segoe UI", 16, "bold"),
                 style="Card.TLabel").pack(anchor="w", pady=(0, 15))
        
        # Tablo ve kaydırma çubuğu
        table_container = ttk.Frame(tablo_frame)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(table_container, 
                                columns=("ID", "Tarih", "Kategori", "Açıklama", "Tutar"), 
                                show="headings",
                                style="Treeview")
        
        # Sütun genişlikleri
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Tarih", width=120, anchor="center")
        self.tree.column("Kategori", width=80, anchor="center")
        self.tree.column("Açıklama", width=200, anchor="w")
        self.tree.column("Tutar", width=100, anchor="e")
        
        # Sütun başlıkları
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        
        # Kaydırma çubuğu
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Satır renklendirme - daha flat renkler
        self.tree.tag_configure('gelir', background='#e8f8f5')  # Açık turkuaz
        self.tree.tag_configure('gider', background='#fdedec')  # Açık kırmızı
    
    def kaydet(self):
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
        kategori = self.kategori_var.get()
        aciklama = self.aciklama_entry.get()
        
        if not aciklama:
            self.durum_label.config(text="Açıklama alanı boş olamaz!", foreground=self.colors["warning"])
            return
        
        try:
            tutar = float(self.tutar_entry.get().replace(",", "."))
            if tutar <= 0:
                self.durum_label.config(text="Tutar sıfırdan büyük olmalı!", foreground=self.colors["warning"])
                return
        except ValueError:
            self.durum_label.config(text="Tutar sayısal olmalı!", foreground=self.colors["warning"])
            return
        
        self.cursor.execute("INSERT INTO islemler (tarih, kategori, aciklama, tutar) VALUES (?, ?, ?, ?)",
                           (tarih, kategori, aciklama, tutar))
        self.conn.commit()
        
        self.durum_label.config(text="Kayıt başarılı!", foreground=self.colors["secondary"])
        self.aciklama_entry.delete(0, tk.END)
        self.tutar_entry.delete(0, tk.END)
        self.listele()
    
    def listele(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        self.cursor.execute("SELECT * FROM islemler ORDER BY id DESC")
        for row in self.cursor.fetchall():
            tag = 'gelir' if row[2] == 'Gelir' else 'gider'
            formatted_tutar = f"{row[4]:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
            values = (row[0], row[1], row[2], row[3], formatted_tutar)
            self.tree.insert("", "end", values=values, tags=(tag,))
        
        self.raporu_guncelle()
    
    def raporu_guncelle(self):
        self.cursor.execute("SELECT SUM(tutar) FROM islemler WHERE kategori='Gelir'")
        toplam_gelir = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute("SELECT SUM(tutar) FROM islemler WHERE kategori='Gider'")
        toplam_gider = self.cursor.fetchone()[0] or 0
        
        net_kazanc = toplam_gelir - toplam_gider
        
        # Binlik ayırıcı ve ondalık virgül formatı (Türkçe para birimi formatı)
        gelir_str = f"{toplam_gelir:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
        gider_str = f"{toplam_gider:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
        net_str = f"{net_kazanc:,.2f} ₺".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Sadece değerleri göster, etiketler kartların üstünde
        self.gelir_label.config(text=f"{gelir_str}")
        self.gider_label.config(text=f"{gider_str}")
        self.net_label.config(text=f"{net_str}")
    
    def secili_kaydi_sil(self):
        secili = self.tree.selection()
        if not secili:
            self.durum_label.config(text="Silmek için bir kayıt seçin.", foreground=self.colors["warning"])
            return
        
        for item in secili:
            kayit = self.tree.item(item)["values"]
            kayit_id = kayit[0]
            self.cursor.execute("DELETE FROM islemler WHERE id=?", (kayit_id,))
            self.conn.commit()
        
        self.durum_label.config(text="Kayıt silindi.", foreground=self.colors["secondary"])
        self.listele()
    
    def disari_aktar(self):
        self.cursor.execute("SELECT * FROM islemler")
        veriler = self.cursor.fetchall()
        
        if not veriler:
            self.durum_label.config(text="Dışa aktarılacak veri yok.", foreground=self.colors["warning"])
            return
        
        dosya_yolu = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Dosyası", "*.xlsx")],
            title="Raporu Kaydet"
        )
        
        if not dosya_yolu:
            return
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "GelirGider"
        
        # Başlıklar
        basliklar = ["ID", "Tarih", "Kategori", "Açıklama", "Tutar (₺)"]
        ws.append(basliklar)
        
        # Veriler
        for satir in veriler:
            ws.append(satir)
        
        # Sütun genişliklerini ayarla
        ws.column_dimensions['A'].width = 10
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 40
        ws.column_dimensions['E'].width = 15
        
        try:
            wb.save(dosya_yolu)
            self.durum_label.config(text="Excel dosyası kaydedildi!", foreground=self.colors["secondary"])
        except Exception as e:
            self.durum_label.config(text=f"Hata: {e}", foreground=self.colors["warning"])
    
    def grafik_goster(self):
        self.cursor.execute("SELECT tarih, kategori, tutar FROM islemler")
        veriler = self.cursor.fetchall()
        
        if not veriler:
            self.durum_label.config(text="Grafik için yeterli veri yok.", foreground=self.colors["warning"])
            return
        
        aylik = defaultdict(lambda: {"Gelir": 0, "Gider": 0})
        
        for tarih, kategori, tutar in veriler:
            ay = datetime.strptime(tarih.split()[0], "%Y-%m-%d").strftime("%Y-%m")
            aylik[ay][kategori] += tutar
        
        aylar = sorted(aylik.keys())
        gelirler = [aylik[ay]["Gelir"] for ay in aylar]
        giderler = [aylik[ay]["Gider"] for ay in aylar]
        
        # Ay isimlerini daha okunabilir formata çevir
        ay_isimleri = []
        for ay in aylar:
            yil, ay_no = ay.split("-")
            ay_isimleri.append(f"{ay_no}/{yil}")
        
        # Flat UI için özel stil
        plt.style.use('ggplot')
        plt.rcParams['font.family'] = 'Segoe UI'
        plt.rcParams['axes.facecolor'] = '#ffffff'
        plt.rcParams['figure.facecolor'] = '#ffffff'
        plt.rcParams['axes.edgecolor'] = '#ecf0f1'
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.color'] = '#ecf0f1'
        plt.rcParams['grid.linestyle'] = '-'
        
        plt.figure(figsize=(12, 6))
        
        # Çubuk grafik - Flat UI renkleri
        bar_width = 0.35
        index = range(len(aylar))
        
        plt.bar([i - bar_width/2 for i in index], gelirler, bar_width, 
                label="Gelir", color=self.colors["secondary"], alpha=0.8)
        plt.bar([i + bar_width/2 for i in index], giderler, bar_width, 
                label="Gider", color=self.colors["warning"], alpha=0.8)
        
        # Çizgi grafik
        plt.plot(index, gelirler, 'o-', color="#27ae60", linewidth=2, alpha=0.8)
        plt.plot(index, giderler, 'o-', color="#c0392b", linewidth=2, alpha=0.8)
        
        # Net kazanç çizgisi
        net_kazanc = [gelirler[i] - giderler[i] for i in range(len(gelirler))]
        plt.plot(index, net_kazanc, 'o--', color=self.colors["primary"], linewidth=2, 
                 label="Net Kazanç", alpha=0.8)
        
        # Flat UI stili başlık ve etiketler
        plt.title("Aylık Gelir - Gider Grafiği", fontsize=18, pad=20, fontweight='bold', color=self.colors["dark"])
        plt.xlabel("Ay", fontsize=12, labelpad=10, color=self.colors["dark"])
        plt.ylabel("Tutar (₺)", fontsize=12, labelpad=10, color=self.colors["dark"])
        plt.xticks(index, ay_isimleri, rotation=45, color=self.colors["dark"])
        plt.yticks(color=self.colors["dark"])
        
        # Flat UI stili legend
        legend = plt.legend(fontsize=11, frameon=True)
        frame = legend.get_frame()
        frame.set_facecolor('white')
        frame.set_edgecolor(self.colors["background"])
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = RaporKolayApp(root)
    root.mainloop()
