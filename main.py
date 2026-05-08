import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Görüntü İşleme Yazılımı")
        self.root.geometry("1100x650")
        
        self.original_image_array = None
        self.processed_image_array = None
        self.original_photo = None
        self.processed_photo = None

        self.setup_ui()

    def setup_ui(self):
        # Üst Menü (Menu Bar)
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Dosya Menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Aç (Open)", command=self.load_image)
        file_menu.add_command(label="Kaydet (Save As)", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        menubar.add_cascade(label="Dosya", menu=file_menu)

        # İşlemler Menüsü
        ops_menu = tk.Menu(menubar, tearoff=0)
        ops_menu.add_command(label="Gri Seviyeye Çevir", command=self.to_grayscale)
        ops_menu.add_command(label="YUV Kanallarını Göster", command=self.to_yuv_channels)
        ops_menu.add_command(label="Binary (Eşikleme)", command=self.apply_threshold)
        ops_menu.add_command(label="Histogram Çiz", command=self.plot_histogram)
        ops_menu.add_command(label="Histogram Eşitleme", command=self.histogram_equalization)
        ops_menu.add_command(label="Kontrast Germe", command=self.contrast_stretching)
        menubar.add_cascade(label="Piksel ve Renk İşlemleri", menu=ops_menu)

        # Ana Çerçeve (Görselleştirme için)
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sol Panel (Orijinal Görüntü)
        left_panel = tk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(left_panel, text="Orijinal Görüntü", font=("Arial", 12, "bold")).pack()
        self.canvas_orig = tk.Canvas(left_panel, bg="gray")
        self.canvas_orig.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Sağ Panel (İşlenmiş Görüntü)
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        tk.Label(right_panel, text="İşlenmiş Görüntü", font=("Arial", 12, "bold")).pack()
        self.canvas_proc = tk.Canvas(right_panel, bg="gray")
        self.canvas_proc.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- DOSYA İŞLEMLERİ ---
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            img = Image.open(file_path).convert("RGB")
            self.original_image_array = np.array(img)
            self.processed_image_array = np.copy(self.original_image_array)
            self.display_image(self.original_image_array, self.canvas_orig, is_original=True)
            self.display_image(self.processed_image_array, self.canvas_proc, is_original=False)

    def save_image(self):
        if self.processed_image_array is None:
            messagebox.showwarning("Uyarı", "Kaydedilecek işlenmiş bir görüntü yok!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            img = Image.fromarray(self.processed_image_array)
            img.save(file_path)
            messagebox.showinfo("Başarılı", "Görüntü başarıyla kaydedildi.")

    def display_image(self, img_array, canvas, is_original=True):
        img = Image.fromarray(img_array)
        
        # Canvas boyutlarına göre yeniden boyutlandırma (Sadece arayüzde düzgün görünmesi için)
        canvas.update()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w > 10 and h > 10:
            img.thumbnail((w, h), Image.Resampling.LANCZOS)
            
        photo = ImageTk.PhotoImage(img)
        if is_original:
            self.original_photo = photo
        else:
            self.processed_photo = photo
            
        canvas.create_image(w//2, h//2, image=photo, anchor=tk.CENTER)

    def check_image_loaded(self):
        if self.original_image_array is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü yükleyin!")
            return False
        return True

    def get_grayscale_array(self):
        # Y = 0.299R + 0.587G + 0.114B
        img = self.original_image_array
        r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        return gray.astype(np.uint8)

    # --- BÖLÜM B: RENK UZAYLARI VE PİKSEL OPERASYONLARI ---
    def to_grayscale(self):
        if not self.check_image_loaded(): return
        gray_array = self.get_grayscale_array()
        self.processed_image_array = gray_array
        self.display_image(self.processed_image_array, self.canvas_proc, is_original=False)

    def to_yuv_channels(self):
        if not self.check_image_loaded(): return
        img = self.original_image_array
        r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        
        # YUV Dönüşüm Matrisi İşlemleri (Kütüphanesiz)
        Y = 0.299 * r + 0.587 * g + 0.114 * b
        U = -0.147 * r - 0.289 * g + 0.436 * b
        V = 0.615 * r - 0.515 * g - 0.100 * b
        
        # U ve V kanallarını 0-255 aralığına kaydır (Görselleştirme için)
        U = np.clip(U + 128, 0, 255)
        V = np.clip(V + 128, 0, 255)
        
        Y, U, V = Y.astype(np.uint8), U.astype(np.uint8), V.astype(np.uint8)
        
        # Kanalları yan yana birleştir
        combined = np.hstack((Y, U, V))
        self.processed_image_array = combined
        self.display_image(self.processed_image_array, self.canvas_proc, is_original=False)
        messagebox.showinfo("Bilgi", "Sırasıyla Y, U ve V kanalları yan yana gösterilmektedir.")

    def apply_threshold(self):
        if not self.check_image_loaded(): return
        threshold_val = simpledialog.askinteger("Eşik Değeri", "0 ile 255 arasında bir eşik değeri (Threshold) girin:", minvalue=0, maxvalue=255)
        if threshold_val is not None:
            gray_array = self.get_grayscale_array()
            # Kütüphanesiz manuel eşikleme (NumPy matris koşulu)
            binary_array = np.where(gray_array > threshold_val, 255, 0).astype(np.uint8)
            self.processed_image_array = binary_array
            self.display_image(self.processed_image_array, self.canvas_proc, is_original=False)

    # --- BÖLÜM C: HİSTOGRAM VE KONTRAST İŞLEMLERİ ---
    def calculate_histogram(self, gray_array):
        # Hiçbir hazır histogram kütüphanesi kullanmadan 0-255 dizisi sayımı
        hist = np.zeros(256, dtype=int)
        # Optimizasyon: np.bincount numpy'ın çekirdek matris fonksiyonudur, cv2/plt değildir.
        counts = np.bincount(gray_array.flatten(), minlength=256)
        return counts

    def plot_histogram(self):
        if not self.check_image_loaded(): return
        gray_array = self.get_grayscale_array()
        hist = self.calculate_histogram(gray_array)
        
        # Yeni bir pencerede grafiği çizelim
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Görüntü Histogramı")
        hist_window.geometry("550x350")
        
        c = tk.Canvas(hist_window, width=512, height=300, bg="white")
        c.pack(pady=20)
        
        max_val = max(hist) if max(hist) > 0 else 1
        
        # Histogram çubuklarını manuel çizme
        for i in range(256):
            bar_height = int((hist[i] / max_val) * 280)
            x0 = i * 2
            y0 = 300
            x1 = x0 + 2
            y1 = 300 - bar_height
            c.create_rectangle(x0, y0, x1, y1, fill="black", outline="black")

    def histogram_equalization(self):
        if not self.check_image_loaded(): return
        gray_array = self.get_grayscale_array()
        hist = self.calculate_histogram(gray_array)
        
        # Kümülatif Dağılım Fonksiyonu (CDF)
        cdf = np.zeros(256, dtype=int)
        cdf[0] = hist[0]
        for i in range(1, 256):
            cdf[i] = cdf[i-1] + hist[i]
            
        # CDF'i maskele ve normalize et
        cdf_min = np.min(cdf[np.nonzero(cdf)])
        total_pixels = gray_array.size
        
        # H(v) = round(((cdf(v) - cdf_min) / (M*N - cdf_min)) * 255)
        cdf_normalized = np.round(((cdf - cdf_min) / (total_pixels - cdf_min)) * 255).astype(np.uint8)
        
        # Yeni pikselleri eşle
        eq_array = cdf_normalized[gray_array]
        
        self.processed_image_array = eq_array
        self.display_image(self.processed_image_array, self.canvas_proc, is_original=False)

    def contrast_stretching(self):
        if not self.check_image_loaded(): return
        min_val = simpledialog.askinteger("Alt Sınır", "Alt sınır değerini girin (ör. 0-255 arası mevcut min):", minvalue=0, maxvalue=255)
        max_val = simpledialog.askinteger("Üst Sınır", "Üst sınır değerini girin (ör. 0-255 arası mevcut max):", minvalue=0, maxvalue=255)
        
        if min_val is not None and max_val is not None and max_val > min_val:
            gray_array = self.get_grayscale_array()
            # Pikselleri sınırların içine kırp
            clipped = np.clip(gray_array, min_val, max_val)
            # Formül: P_yeni = (P_eski - Min) * (255 / (Max - Min))
            stretched = (clipped - min_val) * (255.0 / (max_val - min_val))
            
            self.processed_image_array = stretched.astype(np.uint8)
            self.display_image(self.processed_image_array, self.canvas_proc, is_original=False)
        elif max_val is not None and min_val is not None:
            messagebox.showerror("Hata", "Üst sınır, alt sınırdan büyük olmalıdır!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()