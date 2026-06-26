import json
import os
from data_manager import  (
    load_chat_karakter,
    simpan_chat_karakter,
    simpan_data_karakter,
    load_data_karakter
)
from character_manager import(
    tampilkan_daftar_karakter,
    tambah_karakter,
    edit_karakter,
    hapus_karakter,
    cari_karakter,
    info_karakter
)
from chat_manager import buka_chat

FILE_KARAKTER = "karakter.json"
FOLDER_CHAT ="chats"

karakter_list = []



def tampilkan_bantuan():
    print(""" Command yang tersedia:
          /help                          - akan menampilkan bantuan
          /add                           - akan menambah karakter
          /edit (nomor)                  - akan mengedit karakter berdasarkan nomor
          /delete (nomor)                - akan menghapus karakter berdasarkan nomor
          /history                       - akan menampilkan history chat
          /clear                         - akan menghapus semua history chat
          /search (kata kunci gaya/nama) - akan mencari karakter
          /info                          - memperlihatkan informasi detail karakter
          /exit                          - akan keluar dari program
        """)
     
karakter_list = load_data_karakter(karakter_list)

while True:
    tampilkan_daftar_karakter(karakter_list)
    pilihan = input("\nPilih nomor karakter atau ketik /help untuk melihat command: ").strip()

    if pilihan.lower() == "/exit":
        print("Arigatou sensei, sampai jumpa lagi!")
        break
    elif pilihan.lower() == "/add":
        tambah_karakter(karakter_list)
        continue
    elif pilihan.lower().startswith("/edit"):
        bagian_perintah = pilihan.split()

        if len(bagian_perintah) != 2:
            print("Format salah. Contoh penggunaan: /edit 4")
            continue

        if not bagian_perintah[1].isdigit():
            print("Nomor karakter harus berupa angka...")
            continue

        nomor_edit = int(bagian_perintah[1])
        edit_karakter(nomor_edit, karakter_list)
        continue
    elif pilihan.lower().startswith("/delete"):
        bagian_perintah = pilihan.split()

        if len(bagian_perintah) != 2:
            print("Format salah. Contoh penggunaan: /edit 4")
            continue
        
        if not bagian_perintah[1].isdigit():
            print("Nomor karakter harus berupa angka...")
            continue

        nomor_hapus = int(bagian_perintah[1])
        hapus_karakter(nomor_hapus, karakter_list)
        continue
    elif pilihan.lower() == "/help":
        tampilkan_bantuan()
        continue
    elif pilihan.lower().startswith("/search"):
        bagian_perintah = pilihan.split(maxsplit=1)

        if len(bagian_perintah) != 2:
            print("Format salah. Contoh penggunaan: /search kei atau /seacrh ramah")
            continue
        kata_kunci = bagian_perintah[1]
        cari_karakter(kata_kunci, karakter_list)
        continue
    elif pilihan.lower().startswith("/info"):
        bagian_perintah = pilihan.split()

        if len(bagian_perintah) != 2:
            print("Format salah. Contoh penggunaan: /info 2")
            continue

        if not bagian_perintah[1].isdigit():
            print("Nomor karakter harus berupa angka...")
            continue

        nomor_info =  int(bagian_perintah[1])
        info_karakter(nomor_info, karakter_list)
        continue

    if not pilihan.isdigit():
        print("Pilihan tidak valid. Silakan masukkan nomor karakter atau /exit atau /add.")
        continue

    pilihan = int(pilihan)
    if pilihan < 1 or pilihan > len(karakter_list):
        print("Pilihan tidak valid. Silakan pilih nomor karakter yang tersedia.")
        continue

    karakter_dipilih = karakter_list[pilihan - 1]
    buka_chat(karakter_dipilih, karakter_list)

