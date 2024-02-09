import streamlit as st
from geopy.distance import geodesic
import folium

# Membuat function

def kota_bandung():
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

def jawa_barat():
    kota_coords = {
        "Kota Sukabumi": (-6.9369269, 106.8761097),
        "Kota Bogor": (-6.5950162, 106.7094886),
        "Kota Bandung": (-6.903272, 107.5607541),
        "Kota Cirebon": (-6.7426699, 108.4063758),
        "Kota Bekasi": (-6.2841152, 106.6779812),
        "Kota Depok": (-6.3876714, 106.7353941),
        "Kota Cimahi": (-6.8861666, 107.4672986),
        "Kota Tasikmalaya": (-7.3598042, 108.1503496),
        "Kota Banjar": (-7.3723955, 108.4950041),
        "Kabupaten Sukabumi": (-6.8492295, 106.8729016),
        "Kabupaten Cianjur": (-7.0515528, 106.4708709),
        "Kabupaten Bogor": (-6.5445738, 106.4844121),
        "Kabupaten Bandung": (-7.0626751, 107.2614852),
        "Kabupaten Garut": (-7.3414811, 107.1185812),
        "Kabupaten Tasikmalaya": (-7.4258211, 107.5138864),
        "Kabupaten Ciamis": (-7.3105189, 108.1177301),
        "Kabupaten Kuningan": (-6.9870978, 108.2593337),
        "Kabupaten Cirebon": (-6.760507, 108.2556177),
        "Kabupaten Majalengka": (-6.8061461, 107.6339381),
        "Kabupaten Sumedang": (-6.809099, 107.6508147),
        "Kabupaten Indramayu": (-6.4417654, 107.8669897),
        "Kabupaten Subang": (-6.809099, 107.6508147),
        "Kabupaten Purwakarta": (-6.5920294, 107.2451147),
        "Kabupaten Karawang": (-6.2640209, 107.0340434),
        "Kabupaten Bekasi": (-6.2669317, 106.7772559),
        "Kabupaten Bandung Barat": (-6.904469, 107.1245476),
        "Kabupaten Pangandaran": (-7.6396528, 108.2270064)
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

def tsp(coords):
        start_kota = st.selectbox("Pilih Nama Lokasi Keberangkatan:", list(coords.keys()))

        try :
            rute_tsp = tsp_greedy(start_kota, coords)
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
            peta_tsp = folium.Map(location=coords[start_kota], zoom_start=12)
        except KeyError :
            print("")

        for kota in coords:
            folium.Marker(coords[kota], popup=kota).add_to(peta_tsp)

        try :
            koordinat_rute = [coords[k] for k in rute_tsp] + [coords[start_kota]]

            folium.PolyLine(koordinat_rute, color='red', weight=2.5, opacity=1).add_to(peta_tsp)
            
            folium.Marker(
                location=coords[start_kota], 
                popup=start_kota,
                icon=folium.Icon(color='green')
                ).add_to(peta_tsp)
        except NameError :
            print("")

        # Tampilkan peta di Streamlit
        st.subheader("Peta Rute TSP")

        try :    
            html_map = peta_tsp._repr_html_()
            st.components.v1.html(html_map, width=800, height=490)
        except NameError :
            st.error("No Value")

# Streamlit UI
st.title("Travelling Salesman Problem (TSP) Dashboard")

tab1, tab2 = st.tabs(['Pilih Kota', 'Input Kota'])

with tab1:
    st.write('Pilih Kota')

    bandung = kota_bandung()
    kota = jawa_barat()

    pilihan = st.selectbox("Pilih Lokasi", ("Kota Bandung", "Jawa Barat"))

    if pilihan == "Kota Bandung":
        tsp(bandung)
    elif pilihan == "Jawa Barat":
        tsp(kota)

with tab2:
    # Input kota_coords
    kota_coords2 = input_kota_coords()
    tsp(kota_coords2)