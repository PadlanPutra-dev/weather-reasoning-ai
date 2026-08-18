# Pelaut Frontend

Frontend React + Vite yang mengikuti desain Figma Pelaut.

## Jalankan

1. Pastikan Node.js terpasang.
2. Ekstrak folder.
3. Buka terminal di folder ini.
4. Jalankan `npm install`
5. Jalankan `npm run dev`

Frontend memakai backend FastAPI di `http://127.0.0.1:8000`.

Jika backend memakai URL lain, buat file `.env`:
`VITE_API_URL=http://127.0.0.1:8000`

Endpoint yang dipakai:
- GET `/api/weather`
- GET `/api/recommendation?fisherman_status=belum_berangkat`
- GET `/api/recommendation?fisherman_status=sudah_melaut`

Jika backend belum hidup, dashboard otomatis menampilkan data fallback demo sehingga UI tetap bisa dikerjakan.
