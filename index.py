import streamlit as st
from geopy.distance import geodesic
import folium

# Membuat function

def input_kota_coords():
    kota_coords = {}
    jumlah_kota = st.number_input("Masukkan jumlah kota:", min_value=2, step=1)

    for i in range(jumlah_kota):
        nama_kota = st.text_input(f"Masukkan nama kota ke-{i+1}:", key=f"Kota_{i}")
        try :
            lat_lon = st.text_input(f"Masukkan latitude dan longitude untuk kota {nama_kota} (pisahkan dengan koma):", key=f"LatLon_{i}")
            lat, lon = map(float, lat_lon.split(','))
            kota_coords[nama_kota] = (lat, lon)
        except ValueError :
            st.error("Mohon masukkan Latitude dan Longitude dalam format")

    return kota_coords

def hitung_jarak(kota1, kota2, kota_coords):
    return geodesic(kota_coords[kota1], kota_coords[kota2]).kilometers

def tsp_greedy(start_kota, kota_coords):
    rute = [start_kota]
    kota_belum_dikunjungi = list(kota_coords.keys())
    kota_belum_dikunjungi.remove(start_kota)

    while kota_belum_dikunjungi:
        kota_saat_ini = rute[-1]
        jarak_minimal = float('inf')
        kota_terdekat = None

        for kota in kota_belum_dikunjungi:
            jarak = hitung_jarak(kota_saat_ini, kota, kota_coords)
            if jarak < jarak_minimal:
                jarak_minimal = jarak
                kota_terdekat = kota

        rute.append(kota_terdekat)
        kota_belum_dikunjungi.remove(kota_terdekat)

    return rute

# Streamlit UI
st.title("Travelling Salesman Problem (TSP) Dashboard")

# Input kota_coords
kota_coords = input_kota_coords()

# Input start_kota
start_kota = st.selectbox("Pilih nama kota start:", list(kota_coords.keys()))

# Hitung rute TSP
try :
    rute_tsp = tsp_greedy(start_kota, kota_coords)
except ValueError :
    st.error("No Value")

# Tampilkan hasil rute
st.subheader("Solusi TSP")
try :
    rute_string = ' - '.join(rute_tsp)
    st.write(f"{rute_string} - {start_kota}")
except NameError :
    st.error("No Value")

# Buat peta TSP
try :
    peta_tsp = folium.Map(location=kota_coords[start_kota], zoom_start=13)
except KeyError :
    print("")

for kota in kota_coords:
    folium.Marker(kota_coords[kota], popup=kota).add_to(peta_tsp)

try :
    koordinat_rute = [kota_coords[k] for k in rute_tsp] + [kota_coords[start_kota]]
    folium.PolyLine(koordinat_rute, color='red', weight=2.5, opacity=1).add_to(peta_tsp)
    legenda = f"Rute TSP dari {start_kota}: {' - '.join(rute_tsp)} - {start_kota}"
    folium.Marker(location=kota_coords[start_kota], popup=legenda, icon=folium.Icon(color='green')).add_to(peta_tsp)
except NameError :
    print("")

# Tampilkan peta di Streamlit
st.subheader("Peta Rute TSP")

try :    
    html_map = peta_tsp._repr_html_()
    st.components.v1.html(html_map, width=800, height=1500)
except NameError :
    st.error("No Value")
