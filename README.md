# 🎵 Popüler Müzik Trendleri Analiz Panosu

Bu Streamlit tabanlı interaktif pano, Spotify'dan alınan bir veri seti (yaklaşık 1000 şarkı) üzerinden müzik trendlerini görselleştirmek ve kullanıcıların istedikleri müzik özelliklerine göre filtreleme yapmasını sağlamak amacıyla geliştirilmiştir.

Amacımız, popülerlik, enerji ve dans edilebilirlik gibi metrikler arasındaki ilişkileri kolayca keşfetmektir.

## ✨ Uygulama Ekran Görüntüleri (Görsel Örnekler)

Uygulamanın ana sayfasından ve temel analiz çıktılarından görüntüler:

| Ana Pano ve Dağılım Grafiği | Filtrelenmiş Veri Önizlemesi |
| :---: | :---: |
| ![Ana Pano Görünümü](Ekran%20Resmi%202025-10-25%2014.15.40.png) | ![Filtrelenmiş Veri Önizlemesi](Ekran%20Resmi%202025-10-25%2014.17.09.png) |
| Seçilen Özelliklerin Dağılımı (Histogram) | Proje Klasör Yapısı |
| ![Seçilen Özelliklerin Dağılımı](Ekran%20Resmi%202025-10-25%2014.16.16.png) | ![Proje Klasör Yapısı](Ekran%20Resmi%202025-10-25%2013.41.01.png) |

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları takip edin:

### 1. Gereksinimler

Projenin Python bağımlılıklarını yüklemek için sanal ortamınızı aktifleştirin ve `requirements.txt` dosyasını kullanın.

```bash
# Proje klasörünüzde olduğunuzu varsayarak:
source venv/bin/activate
```

2. Bağımlılıkları Yükleme
Gerekli tüm Python kütüphanelerini (streamlit, pandas, plotly, numpy) yükleyin.

```bash
pip install -r requirements.txt
```
3. Veri Dosyasını Kontrol Etme
Uygulamanın düzgün çalışması için clean_data_final.csv dosyasının noktalı virgül (;) ile ayrılmış ve projenin ana dizininde bulunduğundan emin olun.

4. Uygulamayı Başlatma
Streamlit uygulamasını başlatmak için proje klasöründeyken şu komutu kullanın:

```bash
streamlit run app.py
```
Uygulama, tarayıcınızda otomatik olarak http://localhost:8501 adresinde açılacaktır.

📊 Kullanılan Veri Seti ve Metrikler
Veri Kaynağı: Spotify Tracks Dataset

Temel Metrikler: Popülerlik, Dans Edilebilirlik, Enerji, Ses Yüksekliği (Loudness) ve Sanatçı Adı (artist_name).

Veri Okuma Notu: Veri okuma sırasında Mac Numbers'tan kaynaklanan format ve ayırıcı hataları çözülmüştür.

🧑‍💻 Geliştirici
Rubina Erin
