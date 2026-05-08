# OpenCV Kullanmadan Görüntü İşleme Arayüzü

Bu proje, görüntü işleme algoritmalarının temel mantığını anlamak ve uygulamak amacıyla geliştirilmiştir. Projenin en büyük özelliği, **OpenCV veya benzeri hazır görüntü işleme kütüphaneleri kullanılmadan**, tüm işlemlerin düşük seviyeli **NumPy** matris operasyonları ile yapılmış olmasıdır.

## 🚀 Özellikler
Arayüz üzerinden aşağıdaki işlemler gerçekleştirilebilmektedir:
- **RGB'den Gri Seviyeye Dönüşüm:** Ağırlıklı toplama yöntemiyle ($Y = 0.299R + 0.587G + 0.114B$).
- **YUV Kanal Ayrımı:** Renk ve parlaklık bileşenlerinin (Y, U, V) gösterimi.
- **Binary (Eşikleme):** Kullanıcı tanımlı eşik değerine göre segmentasyon.
- **Histogram Oluşturma:** Görüntünün yoğunluk dağılımının manuel olarak çizilmesi.
- **Histogram Eşitleme:** Kümülatif dağılım fonksiyonu (CDF) kullanılarak kontrast iyileştirme.
- **Kontrast Germe:** Lineer normalizasyon ile görüntü dinamik aralığının artırılması.

## 🛠️ Kullanılan Teknolojiler
- **Python 3.x**
- **NumPy:** Matris operasyonları ve matematiksel hesaplamalar.
- **Tkinter:** Grafik kullanıcı arayüzü (GUI) tasarımı.
- **Pillow (PIL):** Görüntü okuma ve arayüzde gösterme işlemleri.

## 📂 Proje Yapısı
- `main.py`: Uygulamanın kaynak kodu.
- `Görüntü_İşleme_Raporu.pdf`: Projenin detaylı matematiksel anlatımını ve çıktı analizlerini içeren rapor.

## 💻 Kurulum
Projeyi yerel makinenizde çalıştırmak için:
1. Depoyu klonlayın: `git clone https://github.com/kullaniciadi/proje-adi.git`
2. Gerekli kütüphaneleri kurun: `pip install numpy pillow`
3. Uygulamayı çalıştırın: `python main.py`
