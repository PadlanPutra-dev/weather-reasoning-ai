# Weather Reasoning AI Frontend

Frontend aplikasi dashboard cuaca dan rekomendasi melaut berbasis React + Vite.

## Tentang Proyek

Aplikasi ini menampilkan:
- kondisi cuaca saat ini
- data maritim
- pemilihan wilayah Indonesia (provinsi, kabupaten/kota, kecamatan, desa/kelurahan)
- rekomendasi keputusan melaut berdasarkan reasoning fuzzy
- lokasi BMKG terdekat dan lokasi perangkat pengguna

## Teknologi

- React
- Vite
- JavaScript
- Lucide React
- Fetch API untuk komunikasi dengan backend

## Persiapan

Pastikan Node.js dan npm sudah terpasang di komputer Anda.

## Jalankan Aplikasi

1. Buka terminal di folder frontend
2. Install dependency:

```bash
npm install
```

3. Jalankan development server:

```bash
npm run dev
```

4. Buka URL yang ditampilkan oleh Vite, biasanya:

```bash
http://localhost:5173
```

## Konfigurasi Backend

Frontend berkomunikasi dengan backend FastAPI yang berjalan di:

```bash
http://127.0.0.1:8000
```

Jika backend Anda memakai URL lain, buat file `.env` di folder frontend dengan isi:

```env
VITE_API_URL=http://127.0.0.1:8000
```

## Endpoint Utama yang Digunakan

- `GET /api/regions/provinces`
- `GET /api/regions/kabupaten?province_code=...`
- `GET /api/regions/kecamatan?kabupaten_code=...`
- `GET /api/regions/desa?kecamatan_code=...`
- `GET /api/weather?adm4=...&maritime_code=...`
- `GET /api/recommendation?fisherman_status=belum_berangkat&adm4=...&maritime_code=...`
- `POST /api/location/nearest`

## Catatan

Jika backend belum aktif, UI tetap dapat dibuka dengan data fallback demo agar pengembangan frontend tetap bisa dilanjutkan.

## Struktur Utama

- `src/main.jsx` — komponen utama aplikasi
- `src/styles.css` — styling utama
- `index.html` — entry HTML

## Pengembangan Lanjutan

Beberapa hal yang masih bisa ditingkatkan:
- loading state per level wilayah
- polishing mobile layout
- validasi error lebih rapi
- optimasi performa request
- dokumentasi backend yang lebih lengkap
