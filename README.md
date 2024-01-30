# Traveling Salesman Problem (TSP) Dashboard

Aplikasi ini dibuat untuk menyelesaikan masalah Traveling Salesman Problem (TSP) menggunakan algoritma greedy. Aplikasi ini dibangun dengan Streamlit dan menggunakan library geopy untuk menghitung jarak antara kota-kota dan Folium untuk memvisualisasikan rute TSP pada peta.

[Link Demo Streamlit](https://tsp-using-greedy.streamlit.app/)

## Cara Menggunakan

1. Masukkan jumlah kota yang ingin Anda kunjungi.
2. Untuk setiap kota, masukkan nama kota dan koordinatnya (latitude dan longitude) dalam format 'lat, lon'.
3. Pilih kota awal dari daftar kota yang telah Anda masukkan.
4. Aplikasi akan menghitung rute TSP dan menampilkan urutan kota yang harus dikunjungi.
5. Aplikasi juga akan menampilkan peta dengan rute TSP yang dihasilkan.

## Fungsi Utama

- `input_kota_coords()`: Fungsi ini digunakan untuk meminta pengguna memasukkan jumlah kota, nama kota, dan koordinat kota. Fungsi ini mengembalikan kamus di mana kunci adalah nama kota dan nilai adalah tuple koordinat kota.
- `hitung_jarak(kota1, kota2, kota_coords)`: Fungsi ini menghitung jarak antara dua kota menggunakan koordinat mereka.
- `tsp_greedy(start_kota, kota_coords)`: Fungsi ini mengimplementasikan algoritma greedy untuk menyelesaikan TSP. Fungsi ini mengembalikan urutan kota yang harus dikunjungi untuk meminimalkan jarak total.

## Catatan

- Pastikan Anda memasukkan koordinat dengan benar dan dalam format yang benar ('lat, lon').
- Aplikasi ini menggunakan algoritma greedy, yang mungkin tidak selalu menghasilkan solusi optimal untuk TSP.
