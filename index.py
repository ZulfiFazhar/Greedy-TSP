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
        "Rancasari": (-6.9539456, 107.6777669)
    }
    return kota_coords
        # "Gedebage": (-6.9505768, 107.6984879),
        # "Cibiru": (-6.9163257, 107.7192104),
        # "Panyileukan": (-6.9324362, 107.704441203971),
        # "Ujung Berung": (-6.9064866, 107.7073688),
        # "Cinambo": (-6.9328971, 107.6896073),
        # "Arcamanik": (-6.9179069, 107.6777669),
        # "Antapani": (-6.918583, 107.660007),
        # "Mandalajati": (-6.8975476, 107.6718469),
        # "Kiaracondong": (-6.9241819, 107.6481682),
        # "Batununggal": (-6.9529815, 107.630909),
        # "Sumur Bandung": (-6.9152353, 107.612654),
        # "Andir": (-6.9114323, 107.5771444),
        # "Cicendo": (-6.9009118, 107.5830623),
        # "Bandung Wetan": (-6.9047153, 107.6185727),
        # "Cibeunying Kidul": (-6.8984464, 107.6481682),
        # "Cibeuying Kaler": (-6.8937492, 107.6363296),
        # "Coblong": (-6.8919604, 107.6156133),
        # "Sukajadi": (-6.8903936, 107.5889804),
        # "Sukasari": (-6.866465412066975, 107.5841221316536),
        # "Cidadap": (-6.863482, 107.5904569)

def jawa_barat():
    kota_coords = {
        "Kota Sukabumi": (-6.928321402587708, 106.93293025148348),
        "Kota Bogor": (-6.596566663876446, 106.8037668905907),
        "Kota Bandung": (-6.911728885675809, 107.61798090819836),
        "Kota Cirebon": (-6.7358771403869575, 108.54273783107872),
        "Kota Bekasi": (-6.237608700273207, 106.97188794581838),
        "Kota Depok": (-6.404506760616969, 106.79697234762511),
        "Kota Cimahi": (-6.882252265828945, 107.54206579280836),
        "Kota Tasikmalaya": (-7.354854747830193, 108.21698654797164),
        "Kota Banjar": (-7.366750116329321, 108.53783174690206),
    }

    return kota_coords
        # "Kabupaten Sukabumi": (-7.1494884611305185, 106.86876947909825),
        # "Kabupaten Cianjur": (-6.81282455739, 107.15167983266056),
        # "Kabupaten Bogor": (-6.465670348406569, 106.96977860533183),
        # "Kabupaten Bandung": (-7.0242909551453145, 107.52987182218305),
        # "Kabupaten Garut": (-7.364597406113142, 107.79566573676748),
        # "Kabupaten Tasikmalaya": (-7.614759909077524, 108.25364994198331),
        # "Kabupaten Ciamis": (-7.328165691590737, 108.33745325085214),
        # "Kabupaten Kuningan": (-6.981429100665751, 108.4979187815114),
        # "Kabupaten Cirebon": (-6.7657450942872055, 108.45094087466123),
        # "Kabupaten Majalengka": (-6.838003226665918, 108.23017666665162),
        # "Kabupaten Sumedang": (-6.837055261419958, 107.92423291669608),
        # "Kabupaten Indramayu": (-6.347100867879999, 108.33079612192631),
        # "Kabupaten Subang": (-6.563989466152586, 107.75967723026652),
        # "Kabupaten Purwakarta": (-6.539083595642665, 107.45720728317856),
        # "Kabupaten Karawang": (-6.302464629592669, 107.29741241782335),
        # "Kabupaten Bekasi": (-6.36767590155025, 107.17257617632715),
        # "Kabupaten Bandung Barat": (-6.843156844111063, 107.47868731798154),
        # "Kabupaten Pangandaran": (-7.68544880499761, 108.65293626137321)

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
    return geodesic(kota_coords[kota1], kota_coords[kota2]).meters

def seleksi(kota_belum_dikunjungi, kota_saat_ini, kota_coords):
    jarak_minimal = float('inf')
    kota_terdekat = None

    for kota in kota_belum_dikunjungi:
        jarak = int(hitung_jarak(kota_saat_ini, kota, kota_coords))
        if jarak < jarak_minimal:
            jarak_minimal = jarak
            kota_terdekat = kota

    return kota_terdekat

def solusi(rute, kota_terdekat):
    rute.append(kota_terdekat)
    return rute

def layak(kota_belum_dikunjungi, kota_terdekat):
    kota_belum_dikunjungi.remove(kota_terdekat)
    return kota_belum_dikunjungi

def tsp_greedy(start_kota, kota_coords):
    rute = [start_kota]
    kota_belum_dikunjungi = list(kota_coords.keys())
    kota_belum_dikunjungi.remove(start_kota)

    while kota_belum_dikunjungi:
        kota_saat_ini = rute[-1]
        kota_terdekat = seleksi(kota_belum_dikunjungi, kota_saat_ini, kota_coords)
        rute = solusi(rute, kota_terdekat)
        kota_belum_dikunjungi = layak(kota_belum_dikunjungi, kota_terdekat)

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

    pilihan = st.selectbox("Pilih Lokasi", ("Jawa Barat", "Kota Bandung"))

    if pilihan == "Jawa Barat":
        tsp(kota)
    elif pilihan == "Kota Bandung":
        tsp(bandung)

with tab2:
    # Input kota_coords
    kota_coords2 = input_kota_coords()
    tsp(kota_coords2)