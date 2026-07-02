# ============================================================
#  SISTEM MANAJEMEN TURNAMEN MOBILE LEGENDS ANTAR TIM
#  Mata Kuliah : Algoritma dan Pemrograman
#  Deskripsi   : Program CLI untuk mengelola data pertandingan
#                Mobile Legends menggunakan file CSV sebagai
#                penyimpanan data.
# ============================================================

import csv
import os

# ============================================================
# KONSTANTA GLOBAL
# Nama file CSV dan header kolom didefinisikan di sini agar
# mudah diubah jika diperlukan tanpa menelusuri seluruh kode.
# ============================================================

NAMA_FILE = "match.csv"
HEADER    = ["ID", "TimA", "TimB", "SkorA", "SkorB"]


# ============================================================
# FUNGSI: buat_file()
# Tujuan : Membuat file CSV beserta header-nya jika belum ada.
#          Fungsi ini dipanggil pertama kali saat program mulai
#          agar program tidak crash ketika file belum tersedia.
# ============================================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def buat_file():
    # os.path.exists() mengembalikan False jika file belum ada
    if not os.path.exists(NAMA_FILE):
        # Buat file baru dan langsung tulis baris header
        file = open(NAMA_FILE, mode="w", newline="")
        writer = csv.writer(file)
        writer.writerow(HEADER)
        file.close()
        print("[INFO] File '" + NAMA_FILE + "' berhasil dibuat.")


# ============================================================
# FUNGSI: baca_data()
# Tujuan : Membaca seluruh isi file CSV dan mengembalikan
#          hasilnya sebagai list of dictionary.
#          Setiap baris CSV menjadi satu dictionary dengan
#          key sesuai nama kolom (ID, TimA, TimB, SkorA, SkorB).
# ============================================================
def baca_data():
    # List kosong untuk menampung semua baris data
    daftar = []

    # Buka file dalam mode baca ("r")
    file = open(NAMA_FILE, mode="r", newline="")

    # DictReader otomatis menggunakan baris pertama sebagai key
    reader = csv.DictReader(file)

    # Iterasi setiap baris dan tambahkan ke list
    for baris in reader:
        daftar.append(baris)

    file.close()
    return daftar


# ============================================================
# FUNGSI: simpan_data()
# Tujuan : Menyimpan seluruh list data kembali ke file CSV.
#          File ditulis ulang dari awal (mode "w") setiap kali
#          fungsi ini dipanggil — ini adalah pola umum untuk
#          update dan hapus data pada file CSV.
# Parameter:
#   daftar — list of dictionary yang akan disimpan
# ============================================================
def simpan_data(daftar):
    # Buka file dengan mode tulis ("w") — menimpa isi lama
    file = open(NAMA_FILE, mode="w", newline="")

    # DictWriter membutuhkan fieldnames agar tahu urutan kolom
    writer = csv.DictWriter(file, fieldnames=HEADER)

    # Tulis baris header terlebih dahulu
    writer.writeheader()

    # Tulis setiap data satu per satu
    for baris in daftar:
        writer.writerow(baris)

    file.close()


# ============================================================
# FUNGSI: buat_id_otomatis()
# Tujuan : Membuat ID pertandingan baru secara otomatis.
#          Program membaca semua ID yang ada, mencari angka
#          terbesar, lalu menambahkan 1 untuk ID berikutnya.
#          Format: M001, M002, M003, dan seterusnya.
# Mengembalikan: string ID baru (contoh: "M004")
# ============================================================
def buat_id_otomatis():
    daftar = baca_data()

    # Jika belum ada data sama sekali, mulai dari M001
    if len(daftar) == 0:
        return "M001"

    # Cari angka ID terbesar dari seluruh data yang ada
    # (untuk menghindari duplikasi jika ada data yang dihapus)
    angka_max = 0
    for baris in daftar:
        # ID berbentuk "M001" → ambil bagian setelah "M" → "001"
        # Konversi ke int → 1
        angka = int(baris["ID"][1:])

        # Simpan jika angka ini lebih besar dari yang sebelumnya
        if angka > angka_max:
            angka_max = angka

    # Tambahkan 1 untuk membuat ID berikutnya
    angka_baru = angka_max + 1

    # zfill(3) memastikan format selalu 3 digit: 1 → "001"
    id_baru = "M" + str(angka_baru).zfill(3)

    return id_baru


# ============================================================
# FUNGSI: bersihkan_layar()
# Tujuan : Membersihkan tampilan terminal agar terlihat rapi.
#          os.name == "nt" berarti sistem operasi Windows.
#          Selain Windows (Linux/Mac) menggunakan perintah "clear".
# ============================================================
def bersihkan_layar():
    if os.name == "nt":
        os.system("cls")    # Perintah untuk Windows
    else:
        os.system("clear")  # Perintah untuk Linux / Mac


# ============================================================
# FUNGSI: tampilkan_menu()
# Tujuan : Menampilkan daftar menu utama program ke layar.
#          Dipisah menjadi fungsi tersendiri agar main() lebih
#          bersih dan mudah dibaca.
# ============================================================
def tampilkan_menu():
    print("\n" + "=" * 52)
    print("    SISTEM MANAJEMEN TURNAMEN MOBILE LEGENDS")
    print("=" * 52)
    print("  1. Tambah Pertandingan")
    print("  2. Tampilkan Pertandingan")
    print("  3. Cari Pertandingan")
    print("  4. Update Hasil Pertandingan")
    print("  5. Hapus Pertandingan")
    print("  6. Tampilkan Klasemen")
    print("  7. Keluar")
    print("=" * 52)


# ============================================================
# FUNGSI: cetak_tabel_pertandingan()
# Tujuan : Mencetak baris-baris pertandingan dalam format tabel
#          yang rapi ke layar. Dipisah agar bisa dipakai ulang
#          oleh tampilkan_pertandingan() dan cari_pertandingan().
# Parameter:
#   daftar — list of dictionary data pertandingan
# ============================================================
def cetak_tabel_pertandingan(daftar):
    # Cetak garis pemisah dan baris header tabel
    print("-" * 58)
    print(
        "{:<8} {:<14} {:<14} {:>6} {:>6}".format(
            "ID", "Tim A", "Tim B", "Skor A", "Skor B"
        )
    )
    print("-" * 58)

    # Cetak setiap baris data
    for baris in daftar:
        print(
            "{:<8} {:<14} {:<14} {:>6} {:>6}".format(
                baris["ID"],
                baris["TimA"],
                baris["TimB"],
                baris["SkorA"],
                baris["SkorB"]
            )
        )

    print("-" * 58)


# ============================================================
# FUNGSI: tambah_pertandingan()
# Tujuan : Menambahkan data pertandingan baru ke file CSV.
#          Meliputi: pembuatan ID otomatis, input data,
#          validasi, dan penyimpanan ke CSV.
# ============================================================
def tambah_pertandingan():
    print("\n--- TAMBAH PERTANDINGAN ---")

    # Langkah 1: Buat ID otomatis
    id_baru = buat_id_otomatis()
    print("ID Match   : " + id_baru + " (dibuat otomatis)")

    # Langkah 2: Input nama Tim A
    tim_a = input("Nama Tim A : ").strip().upper()
    if tim_a == "":
        print("[ERROR] Nama Tim A tidak boleh kosong.")
        return

    # Langkah 3: Input nama Tim B
    tim_b = input("Nama Tim B : ").strip().upper()
    if tim_b == "":
        print("[ERROR] Nama Tim B tidak boleh kosong.")
        return

    # Langkah 4: Validasi — Tim A dan Tim B tidak boleh sama
    if tim_a == tim_b:
        print("[ERROR] Tim A dan Tim B tidak boleh sama.")
        return

    # Langkah 5: Input dan validasi Skor Tim A
    input_skor_a = input("Skor " + tim_a + "    : ").strip()

    # isdigit() mengembalikan True hanya jika semua karakter angka
    # Ini sekaligus menolak input negatif seperti "-1"
    if not input_skor_a.isdigit():
        print("[ERROR] Skor harus berupa angka bulat tidak negatif.")
        return

    skor_a = int(input_skor_a)

    # Double-check: pastikan tidak negatif (skor 0 tetap valid)
    if skor_a < 0:
        print("[ERROR] Skor tidak boleh negatif.")
        return

    # Langkah 6: Input dan validasi Skor Tim B
    input_skor_b = input("Skor " + tim_b + "    : ").strip()

    if not input_skor_b.isdigit():
        print("[ERROR] Skor harus berupa angka bulat tidak negatif.")
        return

    skor_b = int(input_skor_b)

    if skor_b < 0:
        print("[ERROR] Skor tidak boleh negatif.")
        return

    # Langkah 7: Buat dictionary untuk pertandingan baru
    pertandingan_baru = {
        "ID"   : id_baru,
        "TimA" : tim_a,
        "TimB" : tim_b,
        "SkorA": str(skor_a),
        "SkorB": str(skor_b)
    }

    # Langkah 8: Baca data lama, tambah data baru, lalu simpan
    daftar = baca_data()
    daftar.append(pertandingan_baru)
    simpan_data(daftar)

    print("\n[SUKSES] Pertandingan berhasil ditambahkan!")
    print("         " + id_baru + " : " + tim_a + " vs " + tim_b +
          " | " + str(skor_a) + " - " + str(skor_b))


# ============================================================
# FUNGSI: tampilkan_pertandingan()
# Tujuan : Membaca dan menampilkan seluruh data pertandingan
#          dari file CSV dalam format tabel yang mudah dibaca.
# ============================================================
def tampilkan_pertandingan():
    print("\n--- DAFTAR SEMUA PERTANDINGAN ---")

    daftar = baca_data()

    # Cek apakah ada data yang tersimpan
    if len(daftar) == 0:
        print("[INFO] Belum ada data pertandingan yang tersimpan.")
        return

    # Tampilkan data dalam format tabel
    cetak_tabel_pertandingan(daftar)
    print("Total : " + str(len(daftar)) + " pertandingan")


# ============================================================
# FUNGSI: cari_pertandingan()
# Tujuan : Mencari pertandingan berdasarkan ID Match atau
#          nama Tim menggunakan algoritma Linear Search.
#
# Linear Search = periksa elemen satu per satu dari awal
# hingga akhir hingga data yang dicari ditemukan.
# Kompleksitas waktu: O(n)
# ============================================================
def cari_pertandingan():
    print("\n--- CARI PERTANDINGAN ---")
    print("  1. Cari berdasarkan ID Match")
    print("  2. Cari berdasarkan Nama Tim")

    pilihan = input("Pilih metode pencarian (1/2): ").strip()

    daftar = baca_data()

    # Cek apakah ada data
    if len(daftar) == 0:
        print("[INFO] Belum ada data pertandingan.")
        return

    # List untuk menyimpan semua hasil yang cocok
    hasil = []

    if pilihan == "1":
        # --- Pencarian berdasarkan ID Match ---
        keyword = input("Masukkan ID Match : ").strip().upper()

        # Linear Search: periksa setiap baris satu per satu
        for baris in daftar:
            if baris["ID"] == keyword:
                hasil.append(baris)
                # ID bersifat unik, bisa langsung berhenti jika sudah ketemu
                break

    elif pilihan == "2":
        # --- Pencarian berdasarkan Nama Tim ---
        keyword = input("Masukkan Nama Tim : ").strip().upper()

        # Linear Search: periksa kolom TimA dan TimB setiap baris
        for baris in daftar:
            if baris["TimA"] == keyword or baris["TimB"] == keyword:
                hasil.append(baris)

    else:
        print("[ERROR] Pilihan tidak valid. Masukkan 1 atau 2.")
        return

    # --- Tampilkan Hasil Pencarian ---
    if len(hasil) == 0:
        print("[INFO] Data dengan keyword '" + keyword + "' tidak ditemukan.")
    else:
        print("\nDitemukan " + str(len(hasil)) + " hasil pencarian:")
        cetak_tabel_pertandingan(hasil)


# ============================================================
# FUNGSI: update_hasil()
# Tujuan : Mengubah skor hasil pertandingan yang sudah ada.
#          Program mencari data berdasarkan ID menggunakan
#          Linear Search, lalu memperbarui skornya.
# ============================================================
def update_hasil():
    print("\n--- UPDATE HASIL PERTANDINGAN ---")

    id_cari = input("Masukkan ID Match yang ingin diupdate: ").strip().upper()

    daftar = baca_data()

    # Linear Search untuk menemukan posisi (index) data
    posisi = -1  # -1 berarti belum ditemukan
    for i in range(len(daftar)):
        if daftar[i]["ID"] == id_cari:
            posisi = i
            break  # Hentikan pencarian segera setelah ditemukan

    # Jika posisi masih -1, berarti ID tidak ada di data
    if posisi == -1:
        print("[ERROR] ID '" + id_cari + "' tidak ditemukan.")
        return

    # Tampilkan data lama sebelum diubah
    data_lama = daftar[posisi]
    print("\n  Data Saat Ini:")
    print("  ID    : " + data_lama["ID"])
    print("  Tim A : " + data_lama["TimA"] + " (Skor: " + data_lama["SkorA"] + ")")
    print("  Tim B : " + data_lama["TimB"] + " (Skor: " + data_lama["SkorB"] + ")")

    # Input skor baru untuk Tim A
    print("\n  Masukkan Skor Baru:")
    input_skor_a = input("  Skor " + data_lama["TimA"] + " : ").strip()

    if not input_skor_a.isdigit():
        print("[ERROR] Skor harus berupa angka bulat tidak negatif.")
        return

    skor_a_baru = int(input_skor_a)

    if skor_a_baru < 0:
        print("[ERROR] Skor tidak boleh negatif.")
        return

    # Input skor baru untuk Tim B
    input_skor_b = input("  Skor " + data_lama["TimB"] + " : ").strip()

    if not input_skor_b.isdigit():
        print("[ERROR] Skor harus berupa angka bulat tidak negatif.")
        return

    skor_b_baru = int(input_skor_b)

    if skor_b_baru < 0:
        print("[ERROR] Skor tidak boleh negatif.")
        return

    # Perbarui nilai skor pada posisi yang sudah ditemukan
    daftar[posisi]["SkorA"] = str(skor_a_baru)
    daftar[posisi]["SkorB"] = str(skor_b_baru)

    # Simpan seluruh data (termasuk yang baru diperbarui) ke CSV
    simpan_data(daftar)

    print("\n[SUKSES] Skor pertandingan " + id_cari + " berhasil diperbarui.")
    print("         " + data_lama["TimA"] + " vs " + data_lama["TimB"] +
          " | " + str(skor_a_baru) + " - " + str(skor_b_baru))


# ============================================================
# FUNGSI: hapus_pertandingan()
# Tujuan : Menghapus satu data pertandingan berdasarkan ID.
#          Program meminta konfirmasi sebelum menghapus agar
#          tidak terjadi penghapusan data yang tidak disengaja.
# ============================================================
def hapus_pertandingan():
    print("\n--- HAPUS PERTANDINGAN ---")

    id_cari = input("Masukkan ID Match yang ingin dihapus: ").strip().upper()

    daftar = baca_data()

    # Linear Search untuk menemukan posisi data yang akan dihapus
    posisi = -1
    for i in range(len(daftar)):
        if daftar[i]["ID"] == id_cari:
            posisi = i
            break

    # Jika ID tidak ditemukan
    if posisi == -1:
        print("[ERROR] ID '" + id_cari + "' tidak ditemukan.")
        return

    # Tampilkan data yang akan dihapus sebagai konfirmasi
    data_hapus = daftar[posisi]
    print("\n  Data yang akan dihapus:")
    print("  ID    : " + data_hapus["ID"])
    print("  Tim A : " + data_hapus["TimA"] + " (Skor: " + data_hapus["SkorA"] + ")")
    print("  Tim B : " + data_hapus["TimB"] + " (Skor: " + data_hapus["SkorB"] + ")")

    # Minta konfirmasi dari pengguna
    konfirmasi = input("\n  Apakah Anda yakin ingin menghapus? (Y/T): ").strip().upper()

    if konfirmasi == "Y":
        # Hapus elemen pada posisi yang ditemukan
        daftar.pop(posisi)

        # Simpan kembali data yang tersisa ke CSV
        simpan_data(daftar)

        print("[SUKSES] Pertandingan " + id_cari + " berhasil dihapus.")
    else:
        print("[INFO] Penghapusan dibatalkan.")


# ============================================================
# FUNGSI: hitung_statistik_tim()
# Tujuan : Membaca semua pertandingan dan menghitung statistik
#          setiap tim: jumlah main, menang, seri, kalah, poin.
#
#          Aturan poin:
#            Menang = 3 poin
#            Seri   = 1 poin
#            Kalah  = 0 poin
#
#          Menggunakan dictionary untuk menyimpan data per tim
#          agar pencarian dan update bisa dilakukan dengan O(1).
#
# Mengembalikan: list of dictionary statistik tim
# ============================================================
def hitung_statistik_tim():
    daftar = baca_data()

    # Dictionary utama: key = nama tim, value = dict statistik
    statistik = {}

    # Proses setiap pertandingan satu per satu
    for baris in daftar:
        tim_a  = baris["TimA"]
        tim_b  = baris["TimB"]
        skor_a = int(baris["SkorA"])
        skor_b = int(baris["SkorB"])

        # --- Inisialisasi statistik Tim A jika belum tercatat ---
        if tim_a not in statistik:
            statistik[tim_a] = {
                "nama"  : tim_a,
                "main"  : 0,
                "menang": 0,
                "seri"  : 0,
                "kalah" : 0,
                "poin"  : 0
            }

        # --- Inisialisasi statistik Tim B jika belum tercatat ---
        if tim_b not in statistik:
            statistik[tim_b] = {
                "nama"  : tim_b,
                "main"  : 0,
                "menang": 0,
                "seri"  : 0,
                "kalah" : 0,
                "poin"  : 0
            }

        # Kedua tim menambah jumlah pertandingan yang dimainkan
        statistik[tim_a]["main"] += 1
        statistik[tim_b]["main"] += 1

        # --- Tentukan hasil pertandingan dan perbarui statistik ---

        if skor_a > skor_b:
            # Tim A menang, Tim B kalah
            statistik[tim_a]["menang"] += 1
            statistik[tim_a]["poin"]   += 3
            statistik[tim_b]["kalah"]  += 1
            # Tim B mendapat 0 poin, tidak perlu += 0

        elif skor_b > skor_a:
            # Tim B menang, Tim A kalah
            statistik[tim_b]["menang"] += 1
            statistik[tim_b]["poin"]   += 3
            statistik[tim_a]["kalah"]  += 1
            # Tim A mendapat 0 poin

        else:
            # Skor sama = Seri, masing-masing dapat 1 poin
            statistik[tim_a]["seri"] += 1
            statistik[tim_a]["poin"] += 1
            statistik[tim_b]["seri"] += 1
            statistik[tim_b]["poin"] += 1

    # Ubah dictionary menjadi list agar bisa diurutkan dengan Bubble Sort
    list_statistik = []
    for nama_tim in statistik:
        list_statistik.append(statistik[nama_tim])

    return list_statistik


# ============================================================
# FUNGSI: bubble_sort()
# Tujuan : Mengurutkan list statistik tim menggunakan algoritma
#          Bubble Sort secara manual (tanpa sorted()).
#
#          Cara kerja Bubble Sort:
#          - Bandingkan dua elemen yang berdekatan (j dan j+1)
#          - Tukar posisi jika urutan belum benar
#          - Ulangi sebanyak (n-1) putaran
#          - Setelah setiap putaran, elemen terbesar "menggelembung"
#            ke posisi akhir (seperti gelembung naik ke permukaan)
#
#          Kriteria urutan (dari prioritas tertinggi ke terendah):
#            1. Poin terbesar berada di posisi paling atas
#            2. Jika poin sama → kemenangan terbanyak di atas
#            3. Jika poin & menang sama → nama tim urut alfabet
#
# Parameter : list_statistik (list of dictionary)
# Mengembalikan: list_statistik yang sudah terurut
# ============================================================
def bubble_sort(list_statistik):
    n = len(list_statistik)

    # Putaran luar: n-1 kali
    # Setiap putaran i, elemen pada posisi (n-1-i) sudah di tempat yang benar
    for i in range(n - 1):

        # Putaran dalam: bandingkan elemen berdekatan
        for j in range(n - 1 - i):

            # Ambil dua tim yang dibandingkan
            tim_kiri  = list_statistik[j]
            tim_kanan = list_statistik[j + 1]

            # Flag untuk menentukan apakah perlu ditukar
            harus_tukar = False

            # --- Kriteria 1: Poin lebih besar di kiri ---
            if tim_kiri["poin"] < tim_kanan["poin"]:
                harus_tukar = True

            # --- Kriteria 2: Poin sama, menang lebih banyak di kiri ---
            elif tim_kiri["poin"] == tim_kanan["poin"]:

                if tim_kiri["menang"] < tim_kanan["menang"]:
                    harus_tukar = True

                # --- Kriteria 3: Poin & menang sama, nama alfabet ---
                elif tim_kiri["menang"] == tim_kanan["menang"]:
                    # Nama yang lebih awal secara alfabet berada di kiri
                    if tim_kiri["nama"] > tim_kanan["nama"]:
                        harus_tukar = True

            # Lakukan penukaran jika diperlukan
            if harus_tukar:
                list_statistik[j]     = tim_kanan
                list_statistik[j + 1] = tim_kiri

    return list_statistik


# ============================================================
# FUNGSI: tentukan_mvp()
# Tujuan : Menentukan tim MVP (Most Valuable Player / Tim Terbaik)
#          berdasarkan jumlah kemenangan terbanyak.
#          Jika jumlah kemenangan sama, gunakan poin terbesar.
#          Menggunakan Linear Search untuk membandingkan semua tim.
#
# Parameter : list_statistik (list of dictionary)
# Mengembalikan: dictionary statistik tim MVP, atau None jika kosong
# ============================================================
def tentukan_mvp(list_statistik):
    # Jika tidak ada tim sama sekali, kembalikan None
    if len(list_statistik) == 0:
        return None

    # Mulai dengan tim pertama sebagai kandidat sementara
    mvp = list_statistik[0]

    # Bandingkan dengan seluruh tim lainnya (Linear Search)
    for i in range(1, len(list_statistik)):
        tim_saat_ini = list_statistik[i]

        # Jika tim ini punya lebih banyak kemenangan, ganti MVP
        if tim_saat_ini["menang"] > mvp["menang"]:
            mvp = tim_saat_ini

        # Jika kemenangan sama, bandingkan poin
        elif tim_saat_ini["menang"] == mvp["menang"]:
            if tim_saat_ini["poin"] > mvp["poin"]:
                mvp = tim_saat_ini

    return mvp


# ============================================================
# FUNGSI: tampilkan_klasemen()
# Tujuan : Menampilkan klasemen lengkap turnamen dengan format
#          tabel yang rapi, beserta info Juara dan MVP.
#
#          Alur fungsi ini:
#          1. Baca semua pertandingan dari CSV
#          2. Hitung statistik setiap tim
#          3. Urutkan dengan Bubble Sort
#          4. Tampilkan tabel klasemen
#          5. Tampilkan Juara dan MVP
# ============================================================
def tampilkan_klasemen():
    print("\n--- KLASEMEN TURNAMEN E-FOOTBALL INDONESIA ---")

    daftar = baca_data()

    # Cek apakah sudah ada data pertandingan
    if len(daftar) == 0:
        print("[INFO] Belum ada data pertandingan untuk dihitung klasemennya.")
        return

    # Langkah 1: Hitung statistik semua tim
    list_statistik = hitung_statistik_tim()

    # Langkah 2: Urutkan menggunakan Bubble Sort (bukan sorted()!)
    list_statistik = bubble_sort(list_statistik)

    # Langkah 3: Hitung ringkasan turnamen
    total_tim   = len(list_statistik)
    total_match = len(daftar)

    # Tampilkan ringkasan
    print("\n  Total Tim   : " + str(total_tim))
    print("  Total Match : " + str(total_match))

    # Langkah 4: Cetak tabel klasemen
    print("\n" + "-" * 68)
    print(
        "{:<6} {:<16} {:>6} {:>8} {:>6} {:>7} {:>6}".format(
            "Rank", "Tim", "Match", "Menang", "Seri", "Kalah", "Poin"
        )
    )
    print("-" * 68)

    # Cetak setiap tim beserta statistiknya
    rank = 1
    for tim in list_statistik:
        print(
            "{:<6} {:<16} {:>6} {:>8} {:>6} {:>7} {:>6}".format(
                rank,
                tim["nama"],
                tim["main"],
                tim["menang"],
                tim["seri"],
                tim["kalah"],
                tim["poin"]
            )
        )
        rank += 1

    print("-" * 68)

    # Langkah 5: Tampilkan Juara Turnamen (peringkat 1 = index 0)
    juara = list_statistik[0]

    print("\n" + "=" * 50)
    print("  [JUARA TURNAMEN]")
    print("  Tim    : " + juara["nama"])
    print("  Poin   : " + str(juara["poin"]))
    print("  Menang : " + str(juara["menang"]) + " kali")
    print("  Main   : " + str(juara["main"]) + " pertandingan")
    print("=" * 50)

    # Langkah 6: Tentukan dan tampilkan MVP Turnamen
    mvp = tentukan_mvp(list_statistik)

    if mvp is not None:
        print("\n" + "=" * 50)
        print("  [MVP TURNAMEN]")
        print("  Tim    : " + mvp["nama"])
        print("  Menang : " + str(mvp["menang"]) + " kali (terbanyak)")
        print("  Poin   : " + str(mvp["poin"]))
        print("  Main   : " + str(mvp["main"]) + " pertandingan")
        print("=" * 50)


# ============================================================
# FUNGSI: main()
# Tujuan : Fungsi utama yang menjadi titik masuk program.
#          Berisi loop utama yang terus berjalan hingga pengguna
#          memilih menu Keluar (pilihan 7).
#          Bertanggung jawab untuk:
#          - Inisialisasi file CSV
#          - Menampilkan menu
#          - Menerima input pilihan
#          - Memanggil fungsi yang sesuai
# ============================================================
def main():
    # Pastikan file CSV sudah ada sebelum program berjalan
    buat_file()
    clear()

    print("Mini Project by Ihsan Surya Ibrahim")
    print("502010125005")
    print("Teknik Informatika S-2")
    # Sambut pengguna
    print("\n" + "=" * 52)
    print("       Selamat Datang di Kejuaran Turnamen")
    print("             E-FOOTBALL INDONESIA")
    print("=" * 52)

    # Loop utama program — terus berjalan sampai pilihan 7
    while True:

        # Tampilkan menu pilihan
        tampilkan_menu()

        # Ambil input pilihan dari pengguna
        pilihan = input("Pilih menu (1-7): ").strip()

        # Routing ke fungsi yang sesuai berdasarkan pilihan
        if pilihan == "1":
            tambah_pertandingan()

        elif pilihan == "2":
            tampilkan_pertandingan()

        elif pilihan == "3":
            cari_pertandingan()

        elif pilihan == "4":
            update_hasil()

        elif pilihan == "5":
            hapus_pertandingan()

        elif pilihan == "6":
            tampilkan_klasemen()

        elif pilihan == "7":
            # Keluar dari loop dan akhiri program
            print("\n" + "=" * 52)
            print("  Terima kasih telah menggunakan program ini.")
            print("  Program selesai. Sampai jumpa!")
            print("=" * 52 + "\n")
            break

        else:
            # Input selain 1-7 dianggap tidak valid
            print("[ERROR] Pilihan tidak valid. Masukkan angka 1 sampai 7.")

        # Jeda sebelum kembali ke menu — beri waktu baca output
        input("\nTekan Enter untuk kembali ke menu utama...")


# ============================================================
# ENTRY POINT PROGRAM
# Blok ini memastikan main() hanya dipanggil ketika file ini
# dijalankan langsung, bukan ketika di-import sebagai modul.
# ============================================================
if __name__ == "__main__":
    main()
