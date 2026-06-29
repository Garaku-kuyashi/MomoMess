const history = document.getElementById("history");
const form = document.getElementById("chat-form");
const input = document.getElementById("pesan-input");
const sendButton = document.getElementById("send-button") 

// Selalu scroll ke pesan paling bawah saat halaman dibuka
if (history) {
    history.scrollTop = history.scrollHeight;
}

// Jika form tidak ada, hentikan script
if (!form) {
    throw new Error("Form chat tidak ditemukan!");
}

// Ambil nomor karakter dari atribut data
const nomor = form.dataset.nomor;

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const pesan = input.value.trim();

    if (!pesan) return;

    // Tampilkan pesan user langsung
    history.innerHTML += `
        <div class="flex justify-end">
            <div class="max-w-xl bg-blue-500 text-white rounded-2xl px-4 py-3 shadow">
                <p class="text-sm font-semibold mb-1">Kamu</p>
                <p>${pesan}</p>
            </div>
        </div>
    `;

    history.scrollTop = history.scrollHeight;

    input.value = "";
    input.disabled = true;

    sendButton.disabled = true;
    sendButton.textContent = "Mengirim...";
    sendButton.classList.add(
        "opacity-50",
        "cursor-not-allowed"
    );

    const typingId = "typing-indicator";

    history.innerHTML += `
    <div id="${typingId}" class="flex justify-start">
        <div class="max-w-xl bg-white rounded-2xl px-4 py-3 shadow border>
            <p class="text-sm font-semibold mb-1">
                ${document.getElementById("nama-karakter").textContent}
            </p>

            <p class="text-gray-500 italic">
                Sedang Mengetik...
            </p>
        </div>
    </div>
    `;

    history.scrollTop = history.scrollHeight

    try {
        const response = await fetch(`/api/chat/${nomor}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                pesan: pesan
            })
        });

        const data = await response.json();
        
        document.getElementById(typingId)?.remove();

        history.innerHTML += `
            <div class="flex justify-start">
                <div class="max-w-xl bg-white rounded-2xl px-4 py-3 shadow border">
                    <p class="text-sm font-semibold mb-1">
                        ${document.getElementById("nama-karakter").textContent}
                    </p>

                    <p>${data.assistant}</p>

                    <p class="text-xs text-gray-400 mt-2">
                        ${data.waktu}
                    </p>
                </div>
            </div>
        `;

        history.scrollTop = history.scrollHeight;
    }
    catch (err) {
        document.getElementById(typingId)?.remove();
        sendButton.disabled = false;
        sendButton.textContent = "Kirim";
        sendButton.classList.remove(
            "opacity-50",
            "cursor-not-allowed"
        );
        alert("Gagal mengirim pesan.");
        console.error(err);
    }

    input.disabled = false;
    input.focus();

    sendButton.disabled = false;
    sendButton.textContent = "Kirim";
    sendButton.classList.remove(
        "opacity-50",
        "cursor-not-allowed"
    );
});

input.addEventListener("keydown", function (e){
    if (e.key === "Enter"){
        e.preventDefault();
        form.requestSubmit();
    }

});