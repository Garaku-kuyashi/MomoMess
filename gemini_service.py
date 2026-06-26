import os
import time
from dotenv import load_dotenv
from google import genai

BATAS_HISTORY = 6
MAKSIMAL_COBA = 2

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = None

if api_key:
    client = genai.Client(api_key=api_key)

def buat_jawaban_gemini(karakter, pesan_user, riwayat_chat):
    if client is None:
        return "API key belum ditemukan. Tolong periksa fil env..", False

    nama = karakter["nama"]
    gaya = karakter["gaya"]
    deskripsi = karakter.get("deskripsi", "Tidak ada deskripsi tambahan.")

    riwayat_teks = ""

    for chat in riwayat_chat[-BATAS_HISTORY:]:
        riwayat_teks += f"User: {chat.get('user', '')}\n"
        riwayat_teks += f"{nama}: {chat.get('assistant', '')}\n"

    prompt = f"""
Kamu adalah {nama} dalam aplikasi chat bernama Kivotos Messenger.

Gaya bicaramu: {gaya}
Deskrispi karaktermu: {deskripsi}

Aturan:
- Jawab sebagai karakter {nama}.
- Gunakan bahasa indonesia.
- Jawaban harus natural, singkat, dan cocok untuk chat.
- Jangan membuat jawaban terlalu panjang.
- Tetap sopan.

Riwayat percakapan:
{riwayat_teks}

Pesan terbaru dari user:
{pesan_user}

Balas hanya sebagai {nama}
"""

    for percobaan in range(1, MAKSIMAL_COBA + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text.strip(), True
        except Exception as e:
            print(f"Gemini gagal merespons. Percobaan {percobaan}/{MAKSIMAL_COBA}...")
            if percobaan < MAKSIMAL_COBA:
                time.sleep(2)
                print("Mencoba lagi dalam 2 detik...")
            else:
                return "Gemini sedang sibuk atau koneksi bermasalah. Coba kirim pesan lagi dalam beberapa saat.", False
            # return f"[Gemini sedang bermasalah: {e}]"