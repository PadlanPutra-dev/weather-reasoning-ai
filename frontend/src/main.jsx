import React, { useEffect, useState } from "react";
import {
  createRoot
} from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  NavLink,
  useNavigate
} from "react-router-dom";
import {
  ArrowRight,
  BarChart3,
  Bot,
  CloudRain,
  CloudSun,
  History,
  Home,
  LogOut,
  MapPin,
  Menu,
  Navigation,
  RefreshCw,
  ShieldAlert,
  Ship,
  Thermometer,
  User,
  Waves,
  Wind,
  X,
  LocateFixed,
  Gauge,
  CheckCircle2,
  AlertTriangle,
  Anchor
} from "lucide-react";
import "./styles.css";

const API =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


/* =========================================================
   FALLBACK DATA
   Digunakan hanya jika backend belum tersedia.
========================================================= */

const fallbackWeather = {
  location: {
    adm4: "31.71.03.1001",
    province: "-",
    city: "-",
    district: "-",
    village: "-",
    latitude: 0,
    longitude: 0
  },

  weather: {
    timestamp: "-",
    temperature: null,
    humidity: null,
    precipitation: null,
    wind_speed: null,
    cloud_cover: null,
    visibility: "-",
    condition: "-"
  }
};


const fallbackRecommendation = {
  success: false,

  fuzzy: {
    classification: "-",

    membership: {
      TIDAK_HUJAN: 0,
      MENDUNG: 0,
      HUJAN: 0,
      EKSTREM: 0
    }
  },

  reasoning: {
    hypothesis: "-",

    hypothesis_name:
      "Data reasoning belum tersedia",

    recommendation:
      "Data rekomendasi belum tersedia.",

    scores: {
      H1: 0,
      H2: 0,
      H3: 0,
      H4: 0
    },

    candidate_hypotheses: [],

    confidence: 0,

    evidence: []
  },

  maritime: {
    forecast: {
      wind_speed_avg: null,
      wind_speed_max: null,
      wave_height: null,
      ffx_category: null
    },

    hazards: {
      lightning: null,
      visibility_bad: null,
      breaking_wave: null
    }
  }
};


/* =========================================================
   API HELPER
========================================================= */

async function apiGet(path, fallback = null) {
  try {
    const response = await fetch(
      `${API}${path}`
    );

    if (!response.ok) {
      throw new Error(
        `API ${response.status}`
      );
    }

    return await response.json();

  } catch (error) {
    console.error(
      `API Error ${path}:`,
      error
    );

    return fallback;
  }
}

async function apiPost(path, body = {}, fallback = null) {
  try {
    const response = await fetch(
      `${API}${path}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      }
    );

    if (!response.ok) {
      throw new Error(
        `API ${response.status}`
      );
    }

    return await response.json();

  } catch (error) {
    console.error(
      `API Error ${path}:`,
      error
    );

    return fallback;
  }
}


/* =========================================================
   BRAND
========================================================= */

function Brand({ light = false }) {
  return (
    <Link
      to="/"
      className={`brand ${
        light ? "brand-light" : ""
      }`}
    >
      <span className="brand-mark">
        <Ship size={20} />
      </span>

      <span>
        <b>Pelaut</b>

        <small>
          SISTEM PENDUKUNG KEPUTUSAN
        </small>
      </span>
    </Link>
  );
}


/* =========================================================
   LANDING PAGE
========================================================= */

function Landing() {
  return (
    <div className="landing">

      <header className="public-nav">

        <Brand />

        <nav>
          <a href="#cara-kerja">
            Cara Kerja
          </a>

          <a href="#fitur">
            Fitur
          </a>

          <a href="#tentang">
            Tentang
          </a>
        </nav>

        <div className="nav-actions">

          <Link
            className="btn btn-outline"
            to="/login"
          >
            Masuk
          </Link>

          <Link
            className="btn btn-primary"
            to="/register"
          >
            Daftar Gratis
          </Link>

        </div>

      </header>


      <main>

        <section className="hero">

          <div className="eyebrow">
            DATA BMKG · FUZZY LOGIC · ABDUCTIVE REASONING
          </div>

          <h1>
            Keputusan Melaut yang Lebih Aman,
            <br />
            <em>
              Dibaca Seperti Instrumen Kapal.
            </em>
          </h1>

          <p>
            Pelaut membaca kondisi cuaca,
            mengolah evidence, kemudian
            memberikan rekomendasi yang
            dapat dijelaskan sebelum nelayan
            mengambil keputusan untuk melaut.
          </p>

          <div className="hero-actions">

            <Link
              className="btn btn-primary btn-large"
              to="/dashboard"
            >
              Mulai Sekarang
              <ArrowRight size={17} />
            </Link>

            <Link
              className="btn btn-outline btn-large"
              to="/dashboard"
            >
              Lihat Demo Dashboard
            </Link>

          </div>

        </section>


        <section
          id="cara-kerja"
          className="section"
        >

          <div className="eyebrow aqua">
            ALUR SISTEM
          </div>

          <h2>
            Empat tahap, satu keputusan
            yang dapat dijelaskan
          </h2>

          <p>
            Sistem memproses data cuaca
            hingga menghasilkan rekomendasi
            tindakan.
          </p>


          <div className="flow-grid">

            {[
              [
                "01",
                "PERCEPTION",
                "BACA CUACA",
                "Data cuaca diperoleh dari layanan BMKG."
              ],

              [
                "02",
                "REASONING",
                "NALAR EVIDENCE",
                "Fuzzy logic mengklasifikasikan kondisi cuaca."
              ],

              [
                "03",
                "DECISION",
                "PILIH HIPOTESIS",
                "Abductive reasoning menghitung dukungan setiap hipotesis."
              ],

              [
                "04",
                "ACTION",
                "REKOMENDASI",
                "Sistem memberikan rekomendasi tindakan."
              ]
            ].map((item) => (

              <div
                className="flow-card"
                key={item[0]}
              >

                <span>
                  {item[0]} · {item[1]}
                </span>

                <h3>
                  {item[2]}
                </h3>

                <p>
                  {item[3]}
                </p>

              </div>

            ))}

          </div>

        </section>


        <section
          id="fitur"
          className="section feature-section"
        >

          <div className="eyebrow aqua">
            FITUR
          </div>

          <h2>
            Sistem pendukung keputusan
            untuk nelayan
          </h2>

          <p>
            Semua informasi penting ditampilkan
            dalam satu dashboard.
          </p>


          <div className="feature-grid">

            {[
              [
                CloudSun,
                "Panel Cuaca",
                "Menampilkan kondisi cuaca terkini."
              ],

              [
                Gauge,
                "Fuzzy Logic",
                "Menampilkan derajat keanggotaan kondisi cuaca."
              ],

              [
                BarChart3,
                "Jejak Penalaran",
                "Menampilkan evidence dan skor hipotesis."
              ],

              [
                Navigation,
                "Lokasi",
                "Menampilkan lokasi BMKG dan lokasi perangkat."
              ],

              [
                History,
                "Riwayat",
                "Menyimpan hasil keputusan yang pernah dibuat."
              ],

              [
                Bot,
                "Tanya AI",
                "Membantu menjelaskan hasil rekomendasi."
              ]
            ].map(
              ([Icon, title, description]) => (

                <div
                  className="feature-card"
                  key={title}
                >

                  <div className="icon-box">
                    <Icon size={20} />
                  </div>

                  <h3>
                    {title}
                  </h3>

                  <p>
                    {description}
                  </p>

                </div>

              )
            )}

          </div>


          <div
            id="tentang"
            className="cta-strip"
          >

            <div>

              <h3>
                Siap membaca kondisi laut?
              </h3>

              <p>
                Gunakan dashboard untuk melihat
                kondisi dan rekomendasi melaut.
              </p>

            </div>

            <Link
              className="btn btn-primary"
              to="/dashboard"
            >
              Buka Dashboard
            </Link>

          </div>

        </section>

      </main>


      <footer>

        <span>
          2026 PELAUT · SISTEM PENDUKUNG KEPUTUSAN NELAYAN
        </span>

        <span>
          TIDAK MENGGANTIKAN PERINGATAN RESMI BMKG
        </span>

      </footer>

    </div>
  );
}


/* =========================================================
   AUTH
========================================================= */

function AuthLayout({
  register = false
}) {
  const navigate = useNavigate();

  const submit = () => {
    navigate("/dashboard");
  };

  return (
    <div className="auth-page">

      <div className="auth-quote">

        <Brand />

        <div className="quote">

          “Data cuaca menjadi evidence.
          Evidence menjadi alasan.
          Alasan menjadi keputusan.”

          <small>
            SISTEM PENDUKUNG KEPUTUSAN PELAUT
          </small>

        </div>


        <div className="metrics">

          <div>
            <b>4</b>
            <span>
              hipotesis keputusan
            </span>
          </div>

          <div>
            <b>5+</b>
            <span>
              parameter cuaca
            </span>
          </div>

          <div>
            <b>24/7</b>
            <span>
              pemantauan kondisi
            </span>
          </div>

        </div>

      </div>


      <div className="auth-panel">

        <Brand light />

        <div className="auth-form">

          <h1>
            {register
              ? "Buat akun kapal"
              : "Selamat datang kembali"}
          </h1>

          <p>
            {register
              ? "Daftarkan kapal untuk menggunakan sistem."
              : "Masuk untuk melihat kondisi perairan."}
          </p>


          {register && (
            <>
              <label>
                NAMA LENGKAP
                <input
                  placeholder="Nama anda"
                />
              </label>

              <label>
                NAMA KAPAL
                <input
                  placeholder="Contoh: Nelayan Jaya"
                />
              </label>

              <label>
                PELABUHAN PANGKAL
                <input
                  placeholder="Pangandaran"
                />
              </label>
            </>
          )}


          <label>
            EMAIL ATAU NAMA KAPAL
            <input
              placeholder="nama@gmail.com"
            />
          </label>


          <label>
            KATA SANDI
            <input
              type="password"
              placeholder="••••••••"
            />
          </label>


          {register && (
            <label className="check">

              <input
                type="checkbox"
              />

              <span>
                Saya memahami bahwa Pelaut
                merupakan sistem pendukung keputusan.
              </span>

            </label>
          )}


          <button
            className="btn btn-primary full"
            onClick={submit}
          >
            {register
              ? "DAFTARKAN KAPAL"
              : "MASUK"}
          </button>


          {!register && (
            <button
              className="btn btn-ghost full"
              onClick={() =>
                navigate("/dashboard")
              }
            >
              Masuk sebagai Tamu · Demo
            </button>
          )}


          <p className="auth-bottom">

            {register
              ? "Sudah punya akun? "
              : "Belum punya akun? "}

            <Link
              to={
                register
                  ? "/login"
                  : "/register"
              }
            >
              {register
                ? "Masuk"
                : "Daftar di sini"}
            </Link>

          </p>

        </div>

      </div>

    </div>
  );
}


/* =========================================================
   SIDEBAR
========================================================= */

function Sidebar({
  onClose
}) {
  const navigate = useNavigate();

  const links = [
    [
      "/dashboard",
      Home,
      "Beranda"
    ],

    [
      "/reasoning",
      BarChart3,
      "Jejak Penalaran"
    ],

    [
      "/history",
      History,
      "Riwayat Keputusan"
    ],

    [
      "/ai",
      Bot,
      "Tanya AI"
    ]
  ];

  return (
    <aside className="sidebar">

      <div className="sidebar-top">

        <Brand light />

        <button
          className="mobile-close"
          onClick={onClose}
        >
          <X />
        </button>

      </div>


      <div className="nav-title">
        NAVIGASI
      </div>


      {links.map(
        ([path, Icon, title]) => (

          <NavLink
            key={path}
            to={path}
            onClick={onClose}
            className={({ isActive }) =>
              isActive
                ? "side-link active"
                : "side-link"
            }
          >
            <Icon size={19} />
            {title}
          </NavLink>

        )
      )}


      <button
        className="side-link logout"
        onClick={() =>
          navigate("/")
        }
      >
        <LogOut size={19} />
        Keluar
      </button>


      <div className="location-card">

        <span>

          <span className="live-dot"></span>

          LOKASI AKTIF

        </span>

        <strong>
          Data BMKG
        </strong>

        <small>
          Lokasi mengikuti data cuaca
          yang diterima dari backend BMKG.
        </small>

      </div>

    </aside>
  );
}


/* =========================================================
   APP SHELL
========================================================= */

function AppShell({
  children
}) {
  const [
    menuOpen,
    setMenuOpen
  ] = useState(false);

  return (
    <div className="app-shell">

      <div
        className={
          menuOpen
            ? "sidebar-overlay show"
            : "sidebar-overlay"
        }
        onClick={() =>
          setMenuOpen(false)
        }
      />


      <div
        className={
          menuOpen
            ? "sidebar-wrap open"
            : "sidebar-wrap"
        }
      >

        <Sidebar
          onClose={() =>
            setMenuOpen(false)
          }
        />

      </div>


      <div className="main-content">

        <button
          className="mobile-menu"
          onClick={() =>
            setMenuOpen(true)
          }
        >
          <Menu />
        </button>

        {children}

      </div>

    </div>
  );
}


/* =========================================================
   LOCATION PANEL
========================================================= */

function LocationPanel({
  weather,
  deviceLocation,
  locating,
  locations = [],
  selectedLocation = null,
  onLocate,
  onSelectLocation,
  locationMode = "manual",
  autoFillAdm4 = null,
  onAutoFillReset = null
}) {
  const location = weather?.location;

  const [provinces, setProvinces] = useState([]);
  const [kabupaten, setKabupaten] = useState([]);
  const [kecamatan, setKecamatan] = useState([]);
  const [desa, setDesa] = useState([]);

  const [selectedProvince, setSelectedProvince] = useState("");
  const [selectedKabupaten, setSelectedKabupaten] = useState("");
  const [selectedKecamatan, setSelectedKecamatan] = useState("");
  const [selectedDesa, setSelectedDesa] = useState("");

  const selectedDesaName =
    desa.find((item) => item.code === selectedDesa)?.name || null;

  const isLocationSelectionComplete = Boolean(
    selectedProvince &&
      selectedKabupaten &&
      selectedKecamatan &&
      selectedDesa
  );

  const showBmkgLocationCard =
    isLocationSelectionComplete && locationMode !== "device";

  useEffect(() => {
    if (!autoFillAdm4) return;

    const parts = String(autoFillAdm4).split(".");
    if (parts.length < 4) return;

    const provinceCode = parts[0];
    setSelectedProvince(provinceCode);
    setSelectedKabupaten("");
    setSelectedKecamatan("");
    setSelectedDesa("");
  }, [autoFillAdm4]);

  useEffect(() => {
    if (!autoFillAdm4 || !selectedProvince) return;

    const parts = String(autoFillAdm4).split(".");
    if (parts.length < 4) return;

    const kabupatenCode = `${parts[0]}.${parts[1]}`;
    if (kabupaten.some((item) => item.code === kabupatenCode)) {
      setSelectedKabupaten(kabupatenCode);
    }
  }, [autoFillAdm4, selectedProvince, kabupaten]);

  useEffect(() => {
    if (!autoFillAdm4 || !selectedKabupaten) return;

    const parts = String(autoFillAdm4).split(".");
    if (parts.length < 4) return;

    const kecamatanCode = `${parts[0]}.${parts[1]}.${parts[2]}`;
    if (kecamatan.some((item) => item.code === kecamatanCode)) {
      setSelectedKecamatan(kecamatanCode);
    }
  }, [autoFillAdm4, selectedKabupaten, kecamatan]);

  useEffect(() => {
    if (!autoFillAdm4 || !selectedKecamatan) return;

    const desaCode = String(autoFillAdm4);
    if (desa.some((item) => item.code === desaCode)) {
      setSelectedDesa(desaCode);
    }
  }, [autoFillAdm4, selectedKecamatan, desa]);

  useEffect(() => {
    const fetchProvinces = async () => {
      const result = await apiGet(
        "/api/regions/provinces",
        { success: false, data: [] }
      );
      setProvinces(result?.data || []);
    };

    fetchProvinces();
  }, []);

  useEffect(() => {
    const fetchKabupaten = async () => {
      if (!selectedProvince) {
        setKabupaten([]);
        setKecamatan([]);
        setDesa([]);
        return;
      }

      const result = await apiGet(
        `/api/regions/kabupaten?province_code=${encodeURIComponent(selectedProvince)}`,
        { success: false, data: [] }
      );
      const nextKabupaten = result?.data || [];
      setKabupaten(nextKabupaten);

      if (!autoFillAdm4) {
        setSelectedKabupaten("");
      }

      setKecamatan([]);
      setDesa([]);
    };

    fetchKabupaten();
  }, [selectedProvince]);

  useEffect(() => {
    const fetchKecamatan = async () => {
      if (!selectedKabupaten) {
        setKecamatan([]);
        setDesa([]);
        return;
      }

      const result = await apiGet(
        `/api/regions/kecamatan?kabupaten_code=${encodeURIComponent(selectedKabupaten)}`,
        { success: false, data: [] }
      );
      const nextKecamatan = result?.data || [];
      setKecamatan(nextKecamatan);

      if (!autoFillAdm4) {
        setSelectedKecamatan("");
      }

      setDesa([]);
    };

    fetchKecamatan();
  }, [selectedKabupaten]);

  useEffect(() => {
    const fetchDesa = async () => {
      if (!selectedKecamatan) {
        setDesa([]);
        return;
      }

      const result = await apiGet(
        `/api/regions/desa?kecamatan_code=${encodeURIComponent(selectedKecamatan)}`,
        { success: false, data: [] }
      );
      const nextDesa = result?.data || [];
      setDesa(nextDesa);

      if (!autoFillAdm4) {
        setSelectedDesa("");
      }
    };

    fetchDesa();
  }, [selectedKecamatan]);

  const handleDesaSelect = async (desaCode) => {
    setSelectedDesa(desaCode);

    const desaData = desa.find((d) => d.code === desaCode);
    if (desaData && onSelectLocation) {
      const useCoords = deviceLocation || {
        latitude: -6.2088,
        longitude: 106.8456
      };

      const nearestResult = await apiPost(
        "/api/location/nearest",
        useCoords,
        null
      );

      if (nearestResult?.success && nearestResult.location) {
        onSelectLocation({
          ...nearestResult.location,
          desa_code: desaCode,
          desa_name: desaData.name
        });
      }
    }
  };

  return (
    <section className="panel location-panel">

      <div className="panel-title">

        <div>

          <h2>
            Lokasi Pemantauan
          </h2>

          <span>
            PILIH WILAYAH ATAU GUNAKAN LOKASI SAYA
          </span>

        </div>


        <button
          className="btn btn-outline"
          onClick={onLocate}
          disabled={locating}
        >

          <LocateFixed size={15} />

          {locating
            ? "Mencari..."
            : "Gunakan Lokasi Saya"}

        </button>

      </div>


      <div className="location-selector">

        {!isLocationSelectionComplete && (
          <div className="location-helper">
            Lengkapi semua level wilayah untuk menampilkan lokasi BMKG yang terpilih.
          </div>
        )}

        <div className="selector-group">
          <label>Provinsi</label>
          <select
            value={selectedProvince}
            onChange={(e) => {
              const nextValue = e.target.value;
              if (onAutoFillReset) onAutoFillReset();
              setSelectedProvince(nextValue);
              setSelectedKabupaten("");
              setSelectedKecamatan("");
              setSelectedDesa("");
              if (onSelectLocation) onSelectLocation(null);
            }}
          >
            <option value="">Pilih Provinsi</option>
            {provinces.map((prov) => (
              <option key={prov.code} value={prov.code}>
                {prov.name}
              </option>
            ))}
          </select>
        </div>

        <div className="selector-group">
          <label>Kabupaten/Kota</label>
          <select
            value={selectedKabupaten}
            onChange={(e) => {
              const nextValue = e.target.value;
              if (onAutoFillReset) onAutoFillReset();
              setSelectedKabupaten(nextValue);
              setSelectedKecamatan("");
              setSelectedDesa("");
              if (onSelectLocation) onSelectLocation(null);
            }}
            disabled={!selectedProvince}
          >
            <option value="">Pilih Kabupaten/Kota</option>
            {kabupaten.map((kabu) => (
              <option key={kabu.code} value={kabu.code}>
                {kabu.name}
              </option>
            ))}
          </select>
        </div>

        <div className="selector-group">
          <label>Kecamatan</label>
          <select
            value={selectedKecamatan}
            onChange={(e) => {
              const nextValue = e.target.value;
              if (onAutoFillReset) onAutoFillReset();
              setSelectedKecamatan(nextValue);
              setSelectedDesa("");
              if (onSelectLocation) onSelectLocation(null);
            }}
            disabled={!selectedKabupaten}
          >
            <option value="">Pilih Kecamatan</option>
            {kecamatan.map((kec) => (
              <option key={kec.code} value={kec.code}>
                {kec.name}
              </option>
            ))}
          </select>
        </div>

        <div className="selector-group">
          <label>Desa/Kelurahan</label>
          <select
            value={selectedDesa}
            onChange={(e) => handleDesaSelect(e.target.value)}
            disabled={!selectedKecamatan}
          >
            <option value="">Pilih Desa/Kelurahan</option>
            {desa.map((d) => (
              <option key={d.code} value={d.code}>
                {d.name}
              </option>
            ))}
          </select>
        </div>

      </div>


      {showBmkgLocationCard ? (
        <div className="location-grid">

          <div className="location-main">

            <div className="location-icon">
              <MapPin size={24} />
            </div>

            <div>

              <span className="location-label">
                LOKASI BMKG TERPILIH
              </span>

              <h3>
                {location?.village ||
                  selectedDesaName ||
                  "Lokasi tidak tersedia"}
              </h3>

              <p>
                {location?.district || "-"},{" "}
                {location?.city || "-"},{" "}
                {location?.province || "-"}
              </p>

            </div>

          </div>


          <div className="coordinate-box">

            <span>
              KOORDINAT BMKG
            </span>

            <strong>

              {typeof location?.latitude ===
                "number"
                ? location.latitude.toFixed(6)
                : "-"}

              {", "}

              {typeof location?.longitude ===
                "number"
                ? location.longitude.toFixed(6)
                : "-"}

            </strong>

          </div>

          <div className="coordinate-box">

            <span>
              LOKASI PERANGKAT
            </span>

            {deviceLocation ? (

              <strong>

                {deviceLocation.latitude.toFixed(
                  6
                )}

                {", "}

                {deviceLocation.longitude.toFixed(
                  6
                )}

              </strong>

            ) : (

              <strong className="muted">
                Belum digunakan
              </strong>

            )}

          </div>

        </div>
      ) : null}

    </section>
  );
}



/* =========================================================
   WEATHER CARDS
========================================================= */

function WeatherCards({
  weather,
  maritime
}) {
  const data =
    weather?.weather || {};

  const forecast =
    maritime?.forecast || {};


  const cards = [

    [
      Thermometer,
      "Suhu",
      data.temperature != null
        ? `${data.temperature} °C`
        : "-"
    ],

    [
      CloudRain,
      "Kelembapan",
      data.humidity != null
        ? `${data.humidity} %`
        : "-"
    ],

    [
      CloudRain,
      "Curah Hujan",
      data.precipitation != null
        ? `${data.precipitation} mm`
        : "-"
    ],

    [
      Wind,
      "Angin Atmosfer",
      data.wind_speed != null
        ? `${data.wind_speed} km/jam`
        : "-"
    ],

    [
      Wind,
      "Angin Laut",
      forecast.wind_speed_avg != null
        ? `${forecast.wind_speed_avg} knot`
        : "-"
    ],

    [
      Waves,
      "Gelombang",
      forecast.wave_height != null
        ? `${forecast.wave_height} m`
        : "-"
    ],

    [
      CloudSun,
      "Tutupan Awan",
      data.cloud_cover != null
        ? `${data.cloud_cover}/8`
        : "-"
    ],

    [
      Navigation,
      "Visibilitas",
      data.visibility || "-"
    ]

  ];


  return (
    <div className="weather-grid">

      {cards.map(
        ([Icon, title, value]) => (

          <div
            className="weather-card"
            key={title}
          >

            <div className="weather-card-top">

              <Icon size={18} />

              <span>
                {title}
              </span>

            </div>

            <strong>
              {value}
            </strong>

          </div>

        )
      )}

    </div>
  );
}


/* =========================================================
   MARITIME PANEL
========================================================= */

function MaritimePanel({
  maritime
}) {
  const forecast =
    maritime?.forecast || {};

  return (
    <section className="panel maritime-panel">

      <div className="panel-title">

        <div>

          <h2>
            Kondisi Maritim
          </h2>

          <span>
            PARAMETER YANG DIGUNAKAN DALAM PENALARAN
          </span>

        </div>

      </div>


      <div className="maritime-grid">

        <div>
          <span>
            ANGIN RATA-RATA
          </span>

          <strong>
            {forecast.wind_speed_avg != null
              ? `${forecast.wind_speed_avg} knot`
              : "-"}
          </strong>
        </div>


        <div>
          <span>
            ANGIN MAKSIMUM
          </span>

          <strong>
            {forecast.wind_speed_max != null
              ? `${forecast.wind_speed_max} knot`
              : "-"}
          </strong>
        </div>


        <div>
          <span>
            GELOMBANG
          </span>

          <strong>
            {forecast.wave_height != null
              ? `${forecast.wave_height} m`
              : "-"}
          </strong>
        </div>


        <div>
          <span>
            KATEGORI ANGIN
          </span>

          <strong>
            {forecast.ffx_category
              ? forecast.ffx_category.toUpperCase()
              : "-"}
          </strong>
        </div>

      </div>

    </section>
  );
}


/* =========================================================
   RECOMMENDATION CARD
========================================================= */

function RecommendationCard({
  reasoning
}) {
  const hypothesis =
    reasoning?.hypothesis;

  let title =
    "REKOMENDASI BELUM TERSEDIA";

  let type =
    "safe";


  if (hypothesis === "H1") {
    title =
      "KONDISI RELATIF AMAN";
    type =
      "safe";
  }

  if (hypothesis === "H2") {
    title =
      "WASPADA SAAT MELAUT";
    type =
      "warning";
  }

  if (hypothesis === "H3") {
    title =
      "SEBAIKNYA TUNDA KEBERANGKATAN";
    type =
      "danger";
  }

  if (hypothesis === "H4") {
    title =
      "TIDAK DISARANKAN MELAUT";
    type =
      "danger";
  }


  return (
    <div
      className={
        `recommendation-card ${type}`
      }
    >

      <div>

        <span className="danger-label">
          REKOMENDASI SISTEM
        </span>

        <h2>
          {title}
        </h2>

        <p>
          {reasoning?.recommendation ||
            "Rekomendasi tidak tersedia."}
        </p>


        {reasoning?.confidence != null && (
          <div className="confidence">

            <span>
              CONFIDENCE PENALARAN
            </span>

            <strong>
              {Number(
                reasoning.confidence
              ).toFixed(2)}
              %
            </strong>

          </div>
        )}

      </div>


      <div className="recommendation-icon">

        {type === "danger" ? (

          <ShieldAlert size={34} />

        ) : type === "warning" ? (

          <AlertTriangle size={34} />

        ) : (

          <CheckCircle2 size={34} />

        )}

      </div>

    </div>
  );
}


/* =========================================================
   FUZZY PANEL
========================================================= */

function FuzzyPanel({
  recommendation
}) {
  const membership =
    recommendation?.fuzzy?.membership ||
    fallbackRecommendation.fuzzy.membership;

  const classification =
    recommendation?.fuzzy?.classification ||
    "-";


  return (
    <section className="panel fuzzy">

      <div className="panel-title">

        <div>

          <h2>
            Panel Instrumen · Klasifikasi Fuzzy
          </h2>

          <span>
            μ = DERAJAT KEANGGOTAAN
          </span>

        </div>


        <span className="classification">
          {classification}
        </span>

      </div>


      <div className="fuzzy-grid">

        {Object.entries(
          membership
        ).map(
          ([key, value]) => (

            <div
              className="fuzzy-item"
              key={key}
            >

              <div className="circle-value">
                {Number(value).toFixed(2)}
              </div>

              <b>
                {key.replaceAll(
                  "_",
                  " "
                )}
              </b>

              <small>
                μ VALUE
              </small>

            </div>

          )
        )}

      </div>

    </section>
  );
}


/* =========================================================
   REASONING MINI
========================================================= */

function ReasoningMini({
  reasoning
}) {
  const scores =
    reasoning?.scores || {
      H1: 0,
      H2: 0,
      H3: 0,
      H4: 0
    };


  const maxScore =
    Math.max(
      ...Object.values(scores),
      1
    );


  const labels = {
    H1:
      "Aman melaut",

    H2:
      "Melaut dengan kewaspadaan",

    H3:
      "Menunda aktivitas melaut",

    H4:
      "Tidak disarankan melaut"
  };


  return (
    <section className="panel reasoning-mini">

      <div className="panel-title">

        <div>

          <h2>
            Jejak Penalaran · Abductive Reasoning
          </h2>

          <span>
            SKOR HIPOTESIS
          </span>

        </div>


        <Link to="/reasoning">
          Lihat detail →
        </Link>

      </div>


      <div className="chips">

        <span>
          E1 Cuaca
        </span>

        <span>
          E2 Hujan
        </span>

        <span>
          E3 Angin
        </span>

        <span>
          E4 FFX
        </span>

        <span>
          E5 Gelombang
        </span>

      </div>


      {[
        "H1",
        "H2",
        "H3",
        "H4"
      ].map(
        (hypothesis) => {

          const score =
            scores[hypothesis] || 0;

          const percentage =
            (score / maxScore) *
            100;


          return (
            <div
              className="score-row"
              key={hypothesis}
            >

              <b>
                {hypothesis}
              </b>

              <span>
                {labels[hypothesis]}
              </span>

              <strong>
                {score}
              </strong>

              <div className="bar">

                <i
                  style={{
                    width:
                      `${percentage}%`
                  }}
                />

              </div>

            </div>
          );
        }
      )}

    </section>
  );
}


/* =========================================================
   EVIDENCE PANEL
========================================================= */

function EvidencePanel({
  reasoning
}) {
  const evidence =
    reasoning?.evidence || [];


  return (
    <section className="panel action-panel">

      <div className="panel-title">

        <div>

          <h2>
            Evidence Utama
          </h2>

          <span>
            ALASAN REKOMENDASI
          </span>

        </div>

      </div>


      {evidence.length > 0 ? (

        evidence.map(
          (item, index) => (

            <p
              className="reason-item"
              key={index}
            >

              <b>
                {String(
                  index + 1
                ).padStart(2, "0")}
              </b>

              {item}

            </p>

          )
        )

      ) : (

        <p className="reason-item">
          <b>--</b>
          Evidence belum tersedia.
        </p>

      )}


      <div className="action-box">

        <strong>
          Tindakan yang disarankan
        </strong>

        <p>
          Ikuti rekomendasi sistem dan
          pantau kembali kondisi cuaca
          sebelum mengambil keputusan melaut.
        </p>

      </div>

    </section>
  );
}


/* =========================================================
   DASHBOARD
========================================================= */

function Dashboard() {

  const [weather, setWeather] =
    useState(null);

  const [maritime, setMaritime] =
    useState(null);

  const [recommendation, setRecommendation] =
    useState(null);

  const [status, setStatus] =
    useState("belum_berangkat");

  const [loading, setLoading] =
    useState(true);

  const [locations, setLocations] =
    useState([]);

  const [selectedLocation, setSelectedLocation] =
    useState(null);

  const [deviceLocation, setDeviceLocation] =
    useState(null);

  const [autoFillAdm4, setAutoFillAdm4] =
    useState(null);

  const [locationMode, setLocationMode] =
    useState("manual");

  const [locating, setLocating] =
    useState(false);


  /* =====================================================
     LOAD DATA
  ===================================================== */

  const loadData = async () => {

    setLoading(true);

    const locationParams = selectedLocation
      ? `?adm4=${encodeURIComponent(selectedLocation.adm4)}&maritime_code=${encodeURIComponent(selectedLocation.maritime_code || "")}`
      : "";

    const weatherResponse =
      await apiGet(
        `/api/weather${locationParams}`,
        null
      );


    const recommendationResponse =
      await apiGet(
        `/api/recommendation?fisherman_status=${status}${selectedLocation ? `&adm4=${encodeURIComponent(selectedLocation.adm4)}&maritime_code=${encodeURIComponent(selectedLocation.maritime_code || "")}` : ""}`,
        null
      );


    /*
      Backend /api/weather:

      {
        success: true,
        data: {
          atmosphere: {...},
          maritime: {...}
        }
      }

      Jadi data atmosfer dibaca dari:

      weatherResponse.data.atmosphere
    */

    const atmosphere =
      weatherResponse?.data?.atmosphere ||
      null;


    /*
      Backend /api/recommendation:

      {
        success: true,
        weather: {...},
        maritime: {...},
        fuzzy: {...},
        reasoning: {...}
      }
    */

    const maritimeData =
      recommendationResponse?.maritime ||
      null;


    setWeather(
      atmosphere ||
      fallbackWeather
    );


    setMaritime(
      maritimeData
    );


    setRecommendation(
      recommendationResponse
    );


    setLoading(false);
  };


  useEffect(() => {
    const fetchLocations = async () => {
      const result = await apiGet(
        "/api/locations",
        { success: false, locations: [] }
      );

      const nextLocations = result?.locations || [];
      setLocations(nextLocations);

      // Jangan pilih lokasi default secara otomatis.
      // Lokasi baru hanya dipilih setelah pengguna menyelesaikan
      // pemilihan wilayah atau menekan tombol "Gunakan Lokasi Saya".
      if (!selectedLocation && nextLocations.length > 0) {
        setSelectedLocation(null);
      }
    };

    fetchLocations();
  }, []);

  useEffect(() => {
    if (selectedLocation) {
      loadData();
    }
  }, [status, selectedLocation]);

  useEffect(() => {
    if (!selectedLocation) return;

    const timer = setInterval(() => {
      loadData();
    }, 30000);

    return () => clearInterval(timer);
  }, [status, selectedLocation]);


  /* =====================================================
     DEVICE LOCATION
  ===================================================== */

  const useDeviceLocation = () => {

    if (!navigator.geolocation) {

      alert(
        "Browser tidak mendukung lokasi perangkat."
      );

      return;
    }


    setLocating(true);


    navigator.geolocation.getCurrentPosition(

      async (position) => {

        const coords = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        };

        setLocationMode("device");
        setDeviceLocation(coords);

        const nearest = await apiPost(
          "/api/location/nearest",
          coords,
          null
        );

        if (nearest?.success && nearest.location) {
          setAutoFillAdm4(nearest.location.adm4 || null);
          setSelectedLocation(nearest.location);
        }

        setLocating(false);

      },


      () => {

        alert(
          "Lokasi tidak dapat diperoleh. Izinkan akses lokasi pada browser."
        );

        setLocating(false);

      },


      {
        enableHighAccuracy: true,
        timeout: 10000
      }

    );
  };


  /* =====================================================
     DATA UNTUK RENDER
  ===================================================== */

  const location =
    weather?.location ||
    fallbackWeather.location;


  const weatherData =
    weather?.weather ||
    fallbackWeather.weather;


  const reasoning =
    recommendation?.reasoning ||
    fallbackRecommendation.reasoning;


  const maritimeForecast =
    maritime?.forecast ||
    fallbackRecommendation.maritime.forecast;


  return (
    <AppShell>

      <div className="page-head">

        <div>

          <div className="eyebrow">
            KONDISI MELAUT
          </div>

          <h1>
            Dashboard
          </h1>

          <p className="page-subtitle">

            {weatherData.condition || "-"}

            {" · "}

            {weatherData.timestamp || "-"}

          </p>

        </div>


        <div className="head-actions">

          <button
            className="status-selector"
            onClick={() =>
              setStatus(
                status ===
                  "belum_berangkat"
                  ? "sudah_melaut"
                  : "belum_berangkat"
              )
            }
          >

            <Anchor size={16} />

            {status ===
            "belum_berangkat"
              ? "Belum Berangkat"
              : "Sudah Melaut"}

          </button>


          <button
            className="refresh"
            onClick={loadData}
            disabled={loading}
          >

            <RefreshCw
              size={16}
              className={
                loading
                  ? "spin"
                  : ""
              }
            />

          </button>

        </div>

      </div>


      {/* =================================================
          LOCATION
      ================================================= */}

      <LocationPanel

        weather={{
          ...weather,
          location
        }}

        deviceLocation={
          deviceLocation
        }

        locating={
          locating
        }
        locations={locations}
        selectedLocation={selectedLocation}
        onLocate={
          useDeviceLocation
        }
        onSelectLocation={(nextLocation) => {
          setAutoFillAdm4(null);
          setLocationMode("manual");
          setSelectedLocation(nextLocation);
        }}
        locationMode={locationMode}
        autoFillAdm4={autoFillAdm4}
        onAutoFillReset={() => setAutoFillAdm4(null)}

      />


      {/* =================================================
          WEATHER + MARITIME CARDS
      ================================================= */}

      <WeatherCards

        weather={{
          ...weather,
          weather: weatherData
        }}

        maritime={
          maritime
        }

      />


      {/* =================================================
          MARITIME DATA
      ================================================= */}

      <MaritimePanel
        maritime={maritime}
      />


      {/* =================================================
          RECOMMENDATION
      ================================================= */}

      <RecommendationCard
        reasoning={reasoning}
      />


      {/* =================================================
          FUZZY
      ================================================= */}

      <FuzzyPanel
        recommendation={
          recommendation
        }
      />


      {/* =================================================
          REASONING + EVIDENCE
      ================================================= */}

      <div className="dashboard-bottom">

        <ReasoningMini
          reasoning={
            reasoning
          }
        />

        <EvidencePanel
          reasoning={
            reasoning
          }
        />

      </div>

    </AppShell>
  );
}


/* =========================================================
   REASONING PAGE
========================================================= */

function Reasoning() {

  const [selectedLocation, setSelectedLocation] = useState(null);
  const [recommendation, setRecommendation] =
    useState(null);

  useEffect(() => {
    const fetchLocations = async () => {
      const result = await apiGet(
        "/api/locations",
        { success: false, locations: [] }
      );

      const nextLocations = result?.locations || [];
      const defaultLocation = nextLocations[0] || null;
      setSelectedLocation(defaultLocation);
    };

    fetchLocations();
  }, []);

  useEffect(() => {
    if (!selectedLocation) return;

    const params = `?fisherman_status=belum_berangkat&adm4=${encodeURIComponent(selectedLocation.adm4)}&maritime_code=${encodeURIComponent(selectedLocation.maritime_code || "")}`;

    apiGet(
      `/api/recommendation${params}`,
      null
    ).then(
      setRecommendation
    );

  }, [selectedLocation]);


  const reasoning =
    recommendation?.reasoning ||
    fallbackRecommendation.reasoning;


  const scores =
    reasoning.scores || {};


  const evidence =
    reasoning.evidence || [];


  const maxScore =
    Math.max(
      ...Object.values(scores),
      1
    );


  return (
    <AppShell>

      <div className="page-head">

        <div>

          <div className="eyebrow">
            ABDUCTIVE REASONING
          </div>

          <h1>
            Detail Penalaran
          </h1>

        </div>

      </div>


      {/* =================================================
          EVIDENCE
      ================================================= */}

      <section className="panel">

        <div className="panel-title">

          <div>

            <h2>
              Evidence yang Diproses
            </h2>

            <span>
              DATA AKTUAL DARI SISTEM
            </span>

          </div>

        </div>


        <div className="evidence-list">

          {evidence.length > 0 ? (

            evidence.map(
              (item, index) => (

                <div
                  className="evidence-item"
                  key={index}
                >

                  <div className="evidence-number">
                    E{index + 1}
                  </div>

                  <div>

                    <strong>
                      Evidence {index + 1}
                    </strong>

                    <p>
                      {item}
                    </p>

                  </div>

                </div>

              )
            )

          ) : (

            <p>
              Evidence belum tersedia.
            </p>

          )}

        </div>

      </section>


      <div className="two-panels">


        {/* =================================================
            SCORES
        ================================================= */}

        <section className="panel">

          <div className="panel-title">

            <div>

              <h2>
                Skor Hipotesis
              </h2>

              <span>
                HASIL ABDUCTIVE REASONING
              </span>

            </div>

          </div>


          {[
            "H1",
            "H2",
            "H3",
            "H4"
          ].map(
            (hypothesis) => {

              const score =
                scores[hypothesis] || 0;


              return (
                <div
                  className="hypo"
                  key={hypothesis}
                >

                  <div>

                    <b>
                      {hypothesis}
                    </b>

                    <span>

                      {hypothesis === "H1" &&
                        " Kondisi relatif aman"}

                      {hypothesis === "H2" &&
                        " Perlu kewaspadaan"}

                      {hypothesis === "H3" &&
                        " Tidak aman untuk berangkat"}

                      {hypothesis === "H4" &&
                        " Berbahaya saat di laut"}

                    </span>

                    <i>
                      {score}
                    </i>

                  </div>


                  <div className="hypo-bar">

                    <i
                      style={{
                        width:
                          `${(score / maxScore) * 100}%`
                      }}
                    />

                  </div>

                </div>
              );

            }
          )}


          <div className="selected">

            {reasoning.hypothesis || "-"}

            {" TERPILIH · "}

            {reasoning.hypothesis_name ||
              "Belum tersedia"}

          </div>


          {reasoning.confidence != null && (

            <div className="confidence reasoning-confidence">

              <span>
                CONFIDENCE
              </span>

              <strong>
                {Number(
                  reasoning.confidence
                ).toFixed(2)}
                %
              </strong>

            </div>

          )}

        </section>


        {/* =================================================
            RECOMMENDATION
        ================================================= */}

        <section className="panel">

          <div className="panel-title">

            <div>

              <h2>
                Rekomendasi
              </h2>

              <span>
                HASIL AKHIR SISTEM
              </span>

            </div>

          </div>


          <div className="recommendation-detail">

            <ShieldAlert size={30} />

            <h3>
              {reasoning.hypothesis_name ||
                "Belum tersedia"}
            </h3>

            <p>
              {reasoning.recommendation ||
                "Rekomendasi belum tersedia."}
            </p>

          </div>

        </section>

      </div>

    </AppShell>
  );
}


/* =========================================================
   HISTORY
========================================================= */

function HistoryPage() {

  const rows = [

    [
      "17 Agu 2026",
      "Belum berangkat",
      "Angin 10 km/jam · Hujan 0 mm",
      "H3",
      "Tunda"
    ],

    [
      "16 Agu 2026",
      "Belum berangkat",
      "Gelombang tinggi · Angin kuat",
      "H4",
      "Berbahaya"
    ],

    [
      "15 Agu 2026",
      "Sudah melaut",
      "Petir terdeteksi",
      "H4",
      "Berbahaya"
    ],

    [
      "14 Agu 2026",
      "Belum berangkat",
      "Hujan 30 mm · Angin 12 knot",
      "H2",
      "Waspada"
    ],

    [
      "13 Agu 2026",
      "Belum berangkat",
      "Cerah · Angin rendah",
      "H1",
      "Aman"
    ]

  ];


  return (
    <AppShell>

      <div className="page-head">

        <div>

          <div className="eyebrow">
            LOG REKOMENDASI SISTEM
          </div>

          <h1>
            Riwayat Keputusan
          </h1>

        </div>

      </div>


      <div className="filters">

        <button>
          Semua
        </button>

        <button>
          H1 · Aman
        </button>

        <button>
          H2 · Waspada
        </button>

        <button>
          H3 · Tunda
        </button>

        <button>
          H4 · Berbahaya
        </button>

      </div>


      <section className="panel history-table">

        <div className="table-wrap">

          <table>

            <thead>

              <tr>

                <th>
                  TANGGAL
                </th>

                <th>
                  STATUS NELAYAN
                </th>

                <th>
                  EVIDENCE
                </th>

                <th>
                  HIPOTESIS
                </th>

                <th>
                  STATUS
                </th>

              </tr>

            </thead>


            <tbody>

              {rows.map(
                (row) => (

                  <tr key={row[0]}>

                    <td>
                      {row[0]}
                    </td>

                    <td>
                      {row[1]}
                    </td>

                    <td>
                      {row[2]}
                    </td>

                    <td>

                      <span
                        className={
                          `badge ${row[3].toLowerCase()}`
                        }
                      >
                        {row[3]}
                      </span>

                    </td>

                    <td>
                      {row[4]}
                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      </section>

    </AppShell>
  );
}


/* =========================================================
   AI PAGE
========================================================= */

function AIPage() {

  const [
    selectedLocation,
    setSelectedLocation
  ] = useState(null);

  const [
    messages,
    setMessages
  ] = useState([

    {
      from: "ai",

      text:
        "Halo. Saya dapat membantu menjelaskan kondisi cuaca dan alasan rekomendasi sistem berdasarkan data aktif saat ini."
    }

  ]);


  const [
    input,
    setInput
  ] = useState("");

  const [
    sending,
    setSending
  ] = useState(false);

  useEffect(() => {
    const fetchLocations = async () => {
      const result = await apiGet(
        "/api/locations",
        { success: false, locations: [] }
      );

      const nextLocations = result?.locations || [];
      setSelectedLocation(nextLocations[0] || null);
    };

    fetchLocations();
  }, []);

  const send = async () => {

    const question =
      input.trim();


    if (!question || sending) {
      return;
    }


    setInput("");
    setSending(true);

    setMessages(
      (current) => [

        ...current,

        {
          from: "user",
          text: question
        }

      ]
    );

    const result = await apiPost(
      "/api/ai-chat",
      {
        question,
        adm4: selectedLocation?.adm4,
        maritime_code: selectedLocation?.maritime_code
      },
      { success: false, answer: "Saya tidak bisa menjawab saat ini karena data tidak tersedia." }
    );

    setMessages(
      (current) => [
        ...current,
        {
          from: "ai",
          text: result?.answer || "Saya tidak bisa menjawab saat ini karena data tidak tersedia."
        }
      ]
    );

    setSending(false);
  };


  return (
    <AppShell>

      <div className="page-head">

        <div>

          <div className="eyebrow">
            ASISTEN PENALARAN
          </div>

          <h1>
            Tanya AI
          </h1>

        </div>


        <span className="status-pill">

          <span className="live-dot"></span>

          Siap Menjawab

        </span>

      </div>


      <section className="chat-panel">

        <div className="chat-messages">

          {messages.map(
            (message, index) => (

              <div
                key={index}
                className={
                  `chat-row ${message.from}`
                }
              >

                <div className="chat-avatar">

                  {message.from === "ai" ? (
                    <Bot size={18} />
                  ) : (
                    <User size={18} />
                  )}

                </div>


                <div>

                  <div className="bubble">
                    {message.text}
                  </div>

                </div>

              </div>

            )
          )}

        </div>


        <div className="quick">

          <button
            onClick={() =>
              setInput(
                "Apakah aman melaut hari ini?"
              )
            }
          >
            Apakah aman melaut hari ini?
          </button>


          <button
            onClick={() =>
              setInput(
                "Mengapa sistem memilih H3?"
              )
            }
          >
            Mengapa sistem memilih H3?
          </button>


          <button
            onClick={() =>
              setInput(
                "Jelaskan kondisi angin"
              )
            }
          >
            Jelaskan kondisi angin
          </button>

        </div>


        <div className="chat-input">

          <input
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {

              if (e.key === "Enter") {
                send();
              }

            }}
            placeholder="Tanyakan kondisi cuaca..."
          />


          <button
            onClick={send}
            disabled={sending}
          >
            {sending ? "..." : <ArrowRight size={19} />}
          </button>

        </div>

      </section>

    </AppShell>
  );
}


/* =========================================================
   APP ROUTER
========================================================= */

function App() {

  return (
    <Routes>

      <Route
        path="/"
        element={
          <Landing />
        }
      />


      <Route
        path="/login"
        element={
          <AuthLayout />
        }
      />


      <Route
        path="/register"
        element={
          <AuthLayout register />
        }
      />


      <Route
        path="/dashboard"
        element={
          <Dashboard />
        }
      />


      <Route
        path="/reasoning"
        element={
          <Reasoning />
        }
      />


      <Route
        path="/history"
        element={
          <HistoryPage />
        }
      />


      <Route
        path="/ai"
        element={
          <AIPage />
        }
      />

    </Routes>
  );
}


/* =========================================================
   REACT ROOT
========================================================= */

createRoot(
  document.getElementById("root")
).render(

  <BrowserRouter>

    <App />

  </BrowserRouter>

);