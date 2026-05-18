# CLAUDE.md

Proyek belajar **CI/CD dengan FastAPI**. File ini memberi konteks ke Claude Code agar bisa membantu sesuai gaya belajar dan struktur proyek.

## Tujuan Belajar

1. Membangun REST API sederhana dengan FastAPI
2. Menulis unit test dengan pytest
3. Membuat pipeline CI (lint + test otomatis) dengan GitHub Actions
4. Membuat pipeline CD (build image Docker + deploy) — opsional tahap lanjut

> Fokus utama: **memahami alur**, bukan kompleksitas. Mulai dari yang paling kecil.

## Tech Stack

- **Python 3.11+**
- **FastAPI** — framework API
- **Uvicorn** — ASGI server
- **pytest** + **httpx** — testing
- **ruff** — linter & formatter (cepat, satu tools cukup)
- **GitHub Actions** — CI/CD runner
- **Docker** — containerization (opsional)

## Struktur Proyek

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # entry point FastAPI
│   └── routes/          # endpoint dipisah per modul
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml       # pipeline CI
├── requirements.txt
├── Dockerfile           # opsional
└── README.md
```

## Konvensi Kode

- Gunakan **type hints** di semua fungsi (FastAPI butuh ini untuk validasi otomatis).
- Setiap endpoint baru harus punya test minimal 1 happy path + 1 error case.
- Format & lint pakai `ruff` sebelum commit: `ruff check . && ruff format .`
- Pesan commit pakai gaya **conventional commits**: `feat:`, `fix:`, `test:`, `ci:`, `docs:`, `refactor:`.

## Perintah Penting

```bash
# Setup
python -m venv venv
source venv/bin/activate          # Linux/Mac
pip install -r requirements.txt

# Jalankan API lokal
uvicorn app.main:app --reload

# Jalankan test
pytest -v

# Lint & format
ruff check .
ruff format .
```

## Pipeline CI Minimum (`.github/workflows/ci.yml`)

Pipeline harus menjalankan, **berurutan** dan **gagalkan PR jika ada yang merah**:

1. Checkout code
2. Setup Python
3. Install dependencies (`pip install -r requirements.txt`)
4. Lint (`ruff check .`)
5. Test (`pytest`)

Trigger: `push` ke `main` dan setiap `pull_request`.

## Tahap Belajar (Roadmap)

Kerjakan satu per satu, jangan lompat:

- [ ] **Tahap 1** — Bikin endpoint `GET /health` yang return `{"status": "ok"}`
- [ ] **Tahap 2** — Tulis test pertama untuk `/health` pakai `TestClient`
- [ ] **Tahap 3** — Setup `ruff` dan pastikan kode bersih
- [ ] **Tahap 4** — Bikin `ci.yml` yang jalanin lint + test di GitHub Actions
- [ ] **Tahap 5** — Tambah endpoint CRUD sederhana (in-memory dulu, belum perlu database)
- [ ] **Tahap 6** — Tambah Dockerfile + workflow build image
- [ ] **Tahap 7** — Deploy otomatis ke platform pilihan (Railway / Fly.io / Render)

## Cara Claude Membantu

Ketika diminta bantuan, Claude sebaiknya:

- **Jelaskan dulu konsepnya** secara singkat sebelum kasih kode — ini proyek belajar.
- **Jangan skip tahap.** Kalau saya di Tahap 2, jangan kasih solusi lengkap Tahap 4.
- **Beri tahu kenapa**, bukan cuma apa. Contoh: kenapa pakai `TestClient` bukan request HTTP biasa.
- Tunjukkan **kesalahan umum** yang sering terjadi di tahap itu.
- Kalau ada lebih dari satu cara, sebut alternatifnya singkat, lalu rekomendasikan yang paling cocok untuk pemula.

## Catatan Pribadi

_Tulis di sini hal-hal yang sudah dipahami / yang masih bingung. Update terus seiring belajar._

- Belum paham: ...
- Sudah paham: ...