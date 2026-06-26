import os
from data_manager import simpan_data_karakter

def potong_preview(teks, batas=50):
    if len(teks) > batas:
        return teks[:batas] + "....."
    return teks

def tampilkan_daftar_karakter(karakter_list):
    print("\n" + "=" * 40)
    print("      Kivotos Messenger")
    print("=" * 40)

    for nomor, karakter in enumerate(karakter_list, start=1):
        print(f"\n{nomor}, {karakter['nama']}")
        # print(f"Pesan terakhir: {karakter['pesan_terakhir']}")
        preview = potong_preview(karakter["pesan_terakhir"])
        print(f'    "{preview}"')

def cari_karakter(kata_kunci, karakter_list):
    kata_kunci = kata_kunci.lower().strip()

    if not kata_kunci:
        print("Kata kunci pencarian tidak boleh kosong...")
        return
    
    hasil = []

    for nomor, karakter in enumerate(karakter_list, start=1):
        nama = karakter["nama"].lower()
        gaya = karakter["gaya"].lower()

        if kata_kunci in nama or kata_kunci in gaya:
            hasil.append((nomor, karakter))

    print("\n--- HASIL PENCARIAN ---")

    if not hasil:
        print("Karakter tidak ditemukan")
        return

    for nomor, karakter in hasil:
        preview = potong_preview(karakter["pesan_terakhir"])
        print(f"\n{nomor}. {karakter['nama']}")
        print(f'   Gaya: {karakter["gaya"]}')
        print(f'   "{preview}"')

def info_karakter(nomor, karakter_list):
    if nomor < 1 or nomor > len(karakter_list):
        print("Nomor karakter tidak tersedia...")
        return

    karakter = karakter_list[nomor - 1]
    print("\n--- DETAIL KARAKTER ---")
    print(f"Nama  : {karakter['nama']}")
    print(f"Gaya  : {karakter['gaya']}")
    print(f"Pesan terakhir  : {karakter['pesan_terakhir']}")
    print(f"File chat  : {karakter['file_chat']}")
   

def buat_nama_file(nama):
    nama = nama.lower()
    nama = nama.replace("", "_")
    return nama + ".json"

def tambah_karakter(karakter_list):
    print("\n--- TAMBAH KARAKTER ---")

    nama = input("Nama karakter: ").strip()

    if not nama:
        print("Nama tidak boleh kosong...")
        return

    for karakter in karakter_list:
        if karakter["nama"].lower() == nama.lower():
            print("Nama karakter sudah ada...")
            return

    pesan_awal = input("Pesan awal: ").strip()

    if not pesan_awal:
        pesan_awal = "Belum ada pesan..."

    gaya = input("Gaya karakter: ").strip()
    deskripsi = input("Deskripsi karakter: ").strip()

    if not gaya:
        gaya = "ramah"

    if not deskripsi:
        deskripsi = "Karakter yang ramah dan sopan"

    karakter_baru = {
        "nama" : nama,
        "pesan_terakhir" : pesan_awal,
        "file_chat" : buat_nama_file(nama),
        "gaya" : gaya,
        "dekripsi" : deskripsi
    }

    karakter_list.append(karakter_baru)
    simpan_data_karakter(karakter_list)

    print(f"Karakter {nama} berhasil ditambahkan")

def edit_karakter(nomor, karakter_list):
    if nomor < 1 or nomor > len(karakter_list):
        print("Nomor karakter tidak tersedia di daftar...")
        return
    karakter = karakter_list[nomor - 1]

    print("\n--- EDIT KARAKTER ---")
    print(f"Nama sekarang                 : {karakter['nama']}")
    print(f"Gaya sekarang                 : {karakter['gaya']}")
    print(f"Deskripsi sekarang            : {karakter.get('deskripsi', 'Belum ada deskripsi')}")
    print(f"Pesan terakhir sekarang       : {karakter['pesan_terakhir']}")
    print("\nKosongkan input jika tidak ingin mengubah bagian tersebut.")

    nama_baru = input("Nama baru: ").strip()
    gaya_baru = input("Gaya baru: ").strip()
    deskripsi_baru = input("Deskripsi baru: ").strip()
    pesan_baru = input("Pesan baru: ").strip()

    if nama_baru:
        for data in karakter_list:
            if data["nama"].lower() == nama_baru.lower() and data != karakter:
                print("Nama tersebut sudah digunakan pada karakter lain.")
                return
        file_lama = karakter["file_chat"]
        file_baru = buat_nama_file(nama_baru)
        path_lama = os.path.join("chats", file_lama)
        path_baru = os.path.join("chats", file_baru)

        if os.path.exists(path_lama):
            os.rename(path_lama, path_baru)

        karakter["nama"] = nama_baru
        karakter["file_chat"] = file_baru


    if gaya_baru:
        karakter["gaya"] = gaya_baru

    if deskripsi_baru:
        karakter["deskripsi"]  = deskripsi_baru

    if pesan_baru:
        karakter["pesan_terakhir"] = pesan_baru

    simpan_data_karakter(karakter_list)
    print(f"Data karakter {karakter['nama']} berhasil diperbarui")

def hapus_karakter(nomor, karakter_list):
    if nomor < 1 or nomor > len(karakter_list):
            print("Nomor karakter tidak tersedia di daftar...")
            return
    karakter = karakter_list[nomor - 1]

    print("\n--- HAPUS KARAKTER ---")
    print(f"Nama karakter   : {karakter['nama']}")
    print(f"File chat       : {karakter['file_chat']}")

    konfirmasi = input(f'Ketik "hapus" untuk menghapus {karakter["nama"]}: ').strip().lower()

    if konfirmasi != "hapus":
        print("Prose dibatalkan...")
        return

    path_chat = os.path.join("chats", karakter["file_chat"])

    try:
        if os.path.exists(path_chat):
            os.remove(path_chat)
            print("File chat berhasil dihapus...")
        else:
            print("File chat tidak ditemukan, tetapi data karakter tetap dihapus")

        karakter_list.pop(nomor - 1)
        simpan_data_karakter(karakter_list)
        print(f"Karakter {karakter['nama']} berhasil dihapus...")
    except Exception as e:
        print("Gagal menghapus karakter:", e)
