import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# import csv  <--- BU ARTIK GEREKSİZ!

# ------------------------------------
# 1. Veri Yükleme ve Ön İşleme
# ------------------------------------

@st.cache_data
def load_data(file_path):
    
    # Numbers'taki GÖRÜNEN sütunların tam sırasına göre manuel olarak başlıkları tanımlayın.
    COL_NAMES = ['track_id', 'artists', 'album_name', 'track_name', 'popularity', 'duration_ms', 'explicit', 
                 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 
                 'time_signature', 'track_genre']

    try:
        # Bu sefer: Başlık satırı yok (header=None) ve sütun adlarını manuel olarak atıyoruz (names=).
        # İlk sütun (Numbers'ın indexi) atılacak.
        df = pd.read_csv(
            file_path, 
            sep=';',             # NOKTALI VİRGÜL AYIRICISI
            encoding='latin1',   
            header=None,         # Başlık yok
            names=['NUMBERS_INDEX'] + COL_NAMES, # Toplam 21 sütun adı atıyoruz
            skiprows=0           # Hiçbir satırı atlama (Çünkü veri satırıyla başlıyor ve ilk satırda index var)
        ) 
        
        # Numbers'ın bıraktığı ilk index sütununu kaldır.
        df = df.drop(columns=['NUMBERS_INDEX'])
        
        # Fazladan satırları atalım (eğer boş gelirse)
        df = df.dropna(how='all')
        
    except Exception as e:
        st.error(f"VERİ OKUMA HATA: Dosya okunamadı. Orijinal hata: {e}. Lütfen temizlediğiniz CSV dosyasını kontrol edin.")
        st.stop()
        
    # ----------------------------------------------------
    # SÜTUN TEMİZLEME VE İSİMLENDİRME 
    # ----------------------------------------------------
    
    # Artık 'artists' sütunu var, sadece yeniden adlandırıyoruz.
    if 'artists' in df.columns:
        df = df.rename(columns={'artists': 'artist_name'})
    else:
        # Bu hata, doğru sütun adları manuel atandığı için artık GÖRÜLMEMELİ.
        st.error("HATA: 'artists' sütunu bulunamadı. Lütfen veri setindeki sütun adlarını ve dosya yapısını kontrol edin.")
        st.stop()

    # 2. Sayısal dönüşüm ve NaN temizleme
    numeric_cols = ['danceability', 'popularity', 'energy', 'loudness']
    required_text_cols = ['artist_name', 'track_name']
    
    missing_cols = [col for col in numeric_cols + required_text_cols if col not in df.columns]
    if missing_cols:
        st.error(f"HATA: Veri setinde şu sütunlar eksik: {', '.join(missing_cols)}")
        st.stop()

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce') 

    df = df.dropna(subset=numeric_cols + required_text_cols).reset_index(drop=True)
    df['loudness'] = df['loudness'].abs()
    return df
# ------------------------------------
# 2. Streamlit Arayüzü (Sidebar & Filtreleme) ve KODUN KALANI
# ------------------------------------

# DOSYA ADI KONTROLÜ
FILE_PATH = 'clean_data_final.csv'
try:
    data = load_data(FILE_PATH)
except FileNotFoundError:
    st.error(f"HATA: '{FILE_PATH}' dosyası bulunamadı. Lütfen dosyanın proje klasöründe olduğundan emin olun.")
    st.stop()
    
# Sayfa Yapılandırması...
st.set_page_config(layout="wide") 
st.title('🎵 Popüler Müzik Trendleri Analiz Panosu')
st.markdown('### Spotify Dataset ile Dans Edilebilirlik ve Popülerlik Analizi')

# KENAR ÇUBUĞU (Sidebar)
st.sidebar.header('Filtreleme Ayarları')

# Popülerlik Filtresi Ekleme
min_pop = float(data['popularity'].min())
max_pop = float(data['popularity'].max())

popularity_threshold = st.sidebar.slider(
    'Minimum Popülerlik Eşiği',
    min_value=min_pop,
    max_value=max_pop,
    value=min_pop + 20 
)

# Dans Edilebilirlik Eşiği Seçici
min_dance = float(data['danceability'].min())
max_dance = float(data['danceability'].max())

danceability_threshold = st.sidebar.slider(
    'Minimum Dans Edilebilirlik Eşiği',
    min_value=min_dance,
    max_value=max_dance,
    value=0.5
)

# Filtrelenmiş veriyi oluştur
filtered_data = data[
    (data['danceability'] >= danceability_threshold) &
    (data['popularity'] >= popularity_threshold)
]

# Veri Önizlemesi
if st.sidebar.checkbox('Filtrelenmiş Veri Önizlemesini Göster'):
    st.subheader(f'Gösterilen Şarkı Sayısı: {len(filtered_data)}')
    st.dataframe(filtered_data.head())


# ------------------------------------
# 3. Temel Analiz ve Görselleştirme
# ------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.header('📈 Popülerlik vs. Dans Edilebilirlik')
    
    if not filtered_data.empty:
        fig_scatter = px.scatter(
            filtered_data, 
            x='danceability', 
            y='popularity', 
            color='energy', 
            size='popularity', 
            hover_data=['artist_name', 'track_name', 'energy'], 
            title='Dans Edilebilirlik, Enerji ve Popülerlik İlişkisi',
            labels={'danceability': 'Dans Edilebilirlik', 'popularity': 'Popülerlik'},
            height=450,
            opacity=0.5
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
         st.warning("Filtreleme kriterlerine uygun veri bulunamadı.")


with col2:
    st.header('🎶 En Popüler Sanatçılar (Top 10)')
    
    if 'artist_name' in filtered_data.columns and not filtered_data.empty:
        top_artists = filtered_data['artist_name'].value_counts().nlargest(10).sort_values(ascending=True)
        
        fig_bar = px.bar(
            top_artists,
            x=top_artists.values,
            y=top_artists.index,
            orientation='h', 
            title='Filtrelenmiş Veride En Çok Şarkısı Olan Sanatçılar',
            labels={'x': 'Şarkı Sayısı', 'y': 'Sanatçı Adı'},
            color=top_artists.values,
            color_continuous_scale=px.colors.sequential.Sunset
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Grafik için yeterli veri yok veya 'artist_name' sütunu eksik.")


# ------------------------------------
# 4. Genel Müzik Özelliklerinin Dağılımı (Histogram)
# ------------------------------------
st.markdown('---')
st.header('📊 Seçilen Özelliklerin Dağılımı')

feature_options = ['danceability', 'energy', 'loudness', 'speechiness', 'valence', 'tempo']
selected_feature = st.selectbox(
    'Görselleştirmek İstediğiniz Özelliği Seçin:',
    options=feature_options
)

if not filtered_data.empty:
    fig_hist = px.histogram(
        filtered_data,
        x=selected_feature,
        marginal="box", 
        title=f'{selected_feature.capitalize()} Dağılımı',
        height=400
    )
    st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.warning("Dağılım grafiği için filtrelenmiş veri bulunamadı.")


# ------------------------------------
# 5. Uygulamayı Başlatma Talimatı
# ------------------------------------

if __name__ == '__main__':
    pass