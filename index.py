import streamlit as st
from geopy.distance import geodesic
import folium

# Membuat function

def kota():
    kota_coords = {
        "Bandung Kulon": (-6.9174639, 107.6191228),
        "Babakan Ciparay": (-6.942333, 107.5771444),
        "Bojongloa Kaler": (-6.9315817, 107.5889804),
        "Bojongloa Kidul": (-6.9519605 , 107.5948986),
        "Astana Anyar": (-6.9276793 , 107.6001649),
        "Regol": (-6.940982 , 107.612654),
        "Lengkong": (-6.932694, 107.627449),
        "Bandung Kidul": (-6.9557571 , 107.6304105),
        "Buah Batu": (-6.952390, 107.651128),
        "Rancasari": (-6.9539456, 107.6777669),
        "Gedebage": (-6.9505768, 107.6984879),
        "Cibiru": (-6.9163257, 107.7192104),
        "Panyileukan": (-6.9324362, 107.704441203971),
        "Ujung Berung": (-6.9064866, 107.7073688),
        "Cinambo": (-6.9328971, 107.6896073),
        "Arcamanik": (-6.9179069, 107.6777669),
        "Antapani": (-6.918583, 107.660007),
        "Mandalajati": (-6.8975476, 107.6718469),
        "Kiaracondong": (-6.9241819, 107.6481682),
        "Batununggal": (-6.9529815, 107.630909),
        "Sumur Bandung": (-6.9152353, 107.612654),
        "Andir": (-6.9114323, 107.5771444),
        "Cicendo": (-6.9009118, 107.5830623),
        "Bandung Wetan": (-6.9047153, 107.6185727),
        "Cibeunying Kidul": (-6.8984464, 107.6481682),
        "Cibeuying Kaler": (-6.8937492, 107.6363296),
        "Coblong": (-6.8919604, 107.6156133),
        "Sukajadi": (-6.8903936, 107.5889804),
        "Sukasari": (-6.866465412066975, 107.5841221316536),
        "Cidadap": (-6.863482, 107.5904569)
    }

    return kota_coords

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

tab1, tab2 = st.tabs(['Pilih Kota', 'Input Kota'])

with tab1:
    st.write('Pilih Kota')

    kota_coords = kota()

    start_kota = st.selectbox("Pilih nama kota start:", list(kota_coords.keys()))

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
        peta_tsp = folium.Map(location=kota_coords[start_kota], zoom_start=12)
    except KeyError :
        print("")

    for kota in kota_coords:
        folium.Marker(kota_coords[kota], popup=kota).add_to(peta_tsp)

    try :
        koordinat_rute = [kota_coords[k] for k in rute_tsp] + [kota_coords[start_kota]]
        folium.PolyLine(koordinat_rute, color='red', weight=2.5, opacity=1).add_to(peta_tsp)
        legenda = f"Rute TSP dari {start_kota}: {' - '.join(rute_tsp)} - {start_kota}"
        folium.Marker(location=kota_coords[start_kota], popup=start_kota, icon=folium.Icon(color='green')).add_to(peta_tsp)
    except NameError :
        print("")

    # Tampilkan peta di Streamlit
    st.subheader("Peta Rute TSP")

    try :    
        html_map = peta_tsp._repr_html_()
        st.components.v1.html(html_map, width=800, height=490)
    except NameError :
        st.error("No Value")

with tab2:
    # Input kota_coords
    kota_coords2 = input_kota_coords()

    # Input start_kota
    start_kota2 = st.selectbox("Pilih nama kota start:", list(kota_coords2.keys()))

    # Hitung rute TSP
    try :
        rute_tsp2 = tsp_greedy(start_kota2, kota_coords2)
    except ValueError :
        st.error("No Value")

    # Tampilkan hasil rute
    st.subheader("Solusi TSP")
    try :
        rute_string2 = ' - '.join(rute_tsp2)
        st.write(f"{rute_string2} - {start_kota2}")
    except NameError :
        st.error("No Value")

    # Buat peta TSP
    try :
        peta_tsp2 = folium.Map(location=kota_coords2[start_kota2], zoom_start=13)
    except KeyError :
        print("")

    for kota in kota_coords2:
        folium.Marker(kota_coords2[kota], popup=kota).add_to(peta_tsp2)

    try :
        koordinat_rute2 = [kota_coords2[k] for k in rute_tsp2] + [kota_coords2[start_kota2]]
        folium.PolyLine(koordinat_rute2, color='red', weight=2.5, opacity=1).add_to(peta_tsp2)
        legenda2 = f"Rute TSP dari {start_kota2}: {' - '.join(rute_tsp2)} - {start_kota2}"
        folium.Marker(location=kota_coords2[start_kota2], popup=legenda2, icon=folium.Icon(color='green')).add_to(peta_tsp2)
    except NameError :
        print("")

    # Tampilkan peta di Streamlit
    st.subheader("Peta Rute TSP")

    try :    
        html_map2 = peta_tsp2._repr_html_()
        st.components.v1.html(html_map2, width=800, height=490)
    except NameError :
        st.error("No Value")