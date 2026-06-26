from gemini_service import buat_jawaban_gemini
from data_manager import (
    load_chat_karakter,
    simpan_chat_karakter,
    simpan_data_karakter,
    backup_chat_karakter,
    ambil_daftar_backup,
    load_backup_chat
)
from datetime import datetime

def tampilkan_history(karakter, history_chat):
     if not history_chat:
          print("Belum ada riwayat chat dengan karakter ini...")
          return
     print("\n--- RIWAYAT CHAT ---")
     for chat in history_chat:
        waktu = chat.get("waktu", "waktu tidak tersedia")
        print(f"[{waktu}] Kamu: {chat['user']}")
        print(f"{karakter['nama']}: {chat['assistant']}")
        print("-" * 35)

def buka_chat(karakter, karakater_list):
    history_chat = load_chat_karakter(karakter)

    print("\n" + "=" * 40)
    print(f"CHAT DENGAN {karakter['nama'].upper()}")
    print("=" * 40)
    print("Command: /back, /history, /clear, /restore")

    while True:
        pesan_user = input("\nKamu: ").strip()

        if pesan_user.lower() == "/back":
            break
        elif pesan_user.lower() == "/history":
            tampilkan_history(karakter, history_chat)
            continue
        elif pesan_user.lower() == "/restore":
            daftar_backup = ambil_daftar_backup(karakter)

            if not daftar_backup:
                print("Belum ada backup untuk Karakter ini...")
                continue
            print("\n--- DAFTAR BACKUP ---")
            
            for nomor, nama_file in enumerate(daftar_backup, start=1):
                print(f"{nomor}. {nama_file}")

            print("0. Batal")

            try:
                pilihan_backup = int(input("Pilih backup yang ingin dipulihkan: "))
            except ValueError:
                print("Input harus berupa angka...")
                continue

            if pilihan_backup == 0:
                print("Restore dibatalkan...")
                continue

            if pilihan_backup < 1 or pilihan_backup > len(daftar_backup):
                print("Nomor backup tidak tersedia...")
                continue

            nama_file_backup = daftar_backup[pilihan_backup - 1]

            konfirmasi = input(f'Ketik "restore" untuk memulihakn {nama_file_backup}').strip().lower()

            if konfirmasi != "restore":
                print("Restore dibatalkan...")
                continue

            backup_chat_karakter(karakter, history_chat)
            history_baru = load_backup_chat(nama_file_backup)

            if history_baru is None:
                print("Restore gagal...")
                continue

            history_chat.clear()
            history_chat.extend(history_baru)

            simpan_chat_karakter(karakter, history_chat)

            if history_chat:
                karakter["pesan_terakhir"] = history_chat[-1]["assistant"]
            else:
                karakter["pesan_terakhir"] = "Belum ada pesan..."

            simpan_data_karakter(karakater_list)
            print(f"History berhasil dipulihkan dari {nama_file_backup}")
            continue

        elif pesan_user.lower() == "/clear":
            konfirmasi = input('Ketik "hapus" untuk menghapus seluruh history chat ini: ').strip().lower()

            if konfirmasi == "hapus":
                backup_chat_karakter(karakter, history_chat)
                history_chat.clear()
                simpan_chat_karakter(karakter, history_chat)

                karakter["pesan_terakhir"] = "Belum ada pesan..."
                simpan_data_karakter(karakater_list)
                print("Riwayat chat berhasil dihapus...")
            else:
                print("Proses dibatalkan...")
            continue

        if not pesan_user:
            print("Pesan tidak boleh kosong")
            continue

        print(f"{karakter['nama']} sedang mengetik...")

        jawaban, berhasil = buat_jawaban_gemini(
            karakter,
            pesan_user,
            history_chat
        )

        if not berhasil:
            print(f"{karakter['nama']}: {jawaban}")

        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M")
        history_chat.append({
            "user" : pesan_user,
            "assistant" : jawaban,
            "waktu" : waktu_sekarang
        })

        karakter["pesan_terakhir"] = jawaban

        simpan_chat_karakter(karakter, history_chat)
        simpan_data_karakter(karakater_list)

        print(f"{karakter['nama']}: {jawaban}")
     