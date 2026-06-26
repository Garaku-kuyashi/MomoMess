import json
import os
from datetime import datetime

FILE_KARAKTER = "karakter.json"
FOLDER_CHAT ="chats"

def buat_folder_chat():
    if not os.path.exists(FOLDER_CHAT):
        os.makedirs(FOLDER_CHAT)

def ambil_path_chat(karakter):
    return os.path.join(FOLDER_CHAT, karakter["file_chat"])

def load_chat_karakter(karakter):
    buat_folder_chat()
    path_file = ambil_path_chat(karakter)

    try:
        with open(path_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Terjadi kesalahan saat memuat riwayat chat dari {path_file}. File mungkin rusak.")
        return []

def simpan_chat_karakter(karakter, history):
    buat_folder_chat()
    path_file = ambil_path_chat(karakter)

    try:
        with open(path_file, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan riwayat chat ke {path_file}: {e}")

def backup_chat_karakter(karakter, history):
    if not history:
        return
    os.makedirs("backup", exist_ok=True)

    nama_file_asli = karakter["file_chat"]
    nama_tanpa_ext = os.path.splitext(nama_file_asli)[0]

    waktu_backup = datetime.now().strftime("%Y%m%d_%H%M%S")

    nama_file_backup = f"{nama_tanpa_ext}_{waktu_backup}.json"
    path_backup = os.path.join("backup", nama_file_backup)

    try:
        with open(path_backup, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
        print(f"Backup history berhasil dibuat: {nama_file_backup}")
    except Exception as e:
        print(f"Gagal membuat backup history: {e}")

def ambil_daftar_backup(karakter):
    folder_backup = "backup"

    if not os.path.exists(folder_backup):
        return[]

    nama_file_asli = karakter["file_chat"]
    nama_tanpa_ext = os.path.splitext(nama_file_asli)[0]

    daftar_backup = []

    for nama_file in os.listdir(folder_backup):
        if nama_file.startswith(nama_tanpa_ext + "_") and nama_file.endswith(".json"):
            daftar_backup.append(nama_file)

    daftar_backup.sort(reverse=True)
    return daftar_backup

def load_backup_chat(nama_file_backup):
    path_backup = os.path.join("backup", nama_file_backup)
    try:
        with open(path_backup, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Gagal membaca file backup: {e}")
        return None

def simpan_data_karakter(karakter_list):
    try:
        with open(FILE_KARAKTER, "w", encoding="utf-8") as file:
            json.dump(karakter_list, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data karakter ke {FILE_KARAKTER}: {e}")

def load_data_karakter(karakter_list):
    # global karakter_list

    try:
        with open(FILE_KARAKTER, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        simpan_data_karakter(karakter_list)
        return karakter_list
    except json.JSONDecodeError:
        print("Terjadi kesalahan saat memuat riwayat chat dari. File mungkin rusak.")
        return karakter_list
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data karakter ke {FILE_KARAKTER}: {e}")
        return karakter_list