from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from data_manager import (
    load_data_karakter,
    load_chat_karakter,
    simpan_chat_karakter,
    simpan_data_karakter
    
)
from gemini_service import buat_jawaban_gemini
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    karakter_list = load_data_karakter()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "karakter_list": karakter_list
        }
    )

@app.get("/chat/{nomor}", response_class=HTMLResponse)
def buka_chat(request: Request, nomor: int):
    karakter_list = load_data_karakter()

    if nomor < 0 or nomor >= len(karakter_list):
        return HTMLResponse("Karakter tidak ditemukan", status_code=404)

    karakter = karakter_list[nomor]
    history = load_chat_karakter(karakter)

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "karakter": karakter,
            "history": history,
            "nomor": nomor,
            "karakter_list" : karakter_list
        }
    )

@app.post("/chat/{nomor}")
async def kirim_pesan(
    nomor: int,
    pesan: str = Form(...)
):
    pesan = pesan.strip()

    if not pesan:
        return RedirectResponse(
            url=f"/chat/{nomor}",
            status_code=303
        )

    if len(pesan) > 1000:
        return RedirectResponse(
            url=f"/chat/{nomor}",
            status_code=303
        )

    
    karakter_list = load_data_karakter()
    karakter = karakter_list[nomor]
    history = load_chat_karakter(karakter)

    jawaban, berhasil = buat_jawaban_gemini(
        karakter,
        pesan,
        history
    )

    history.append({
        "user" : pesan,
        "assistant" : jawaban,
        "waktu" : datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    karakter["pesan_terakhir"] = jawaban

    simpan_chat_karakter(karakter, history)
    simpan_data_karakter(karakter_list)

    return RedirectResponse(
        url=f"/chat/{nomor}",
        status_code=303
    )