from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.services.bmkg_service import (
    get_weather_data,
    get_bmkg_location_catalog,
    find_nearest_location
)

from backend.services.maritime_service import (
    get_maritime_data
)

from backend.services.fuzzy_service import (
    classify_weather
)

from backend.services.reasoning_service import (
    calculate_reasoning
)

from backend.services.regional_service import (
    get_all_provinces,
    get_kabupaten_by_province,
    get_kecamatan_by_kabupaten,
    get_desa_by_kecamatan
)

import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()


def build_grounded_ai_answer(question: str, context: dict) -> str:
    if not context:
        return (
            "Saya belum bisa menjawab karena data cuaca saat ini belum tersedia. "
            "Silakan muat ulang dashboard atau cek koneksi ke BMKG."
        )

    weather_payload = context.get("weather") or {}
    maritime_payload = context.get("maritime") or {}

    if isinstance(weather_payload, dict) and "weather" in weather_payload:
        weather = weather_payload.get("weather") or {}
        location = weather_payload.get("location") or {}
    else:
        weather = weather_payload.get("weather") or {}
        location = {}

    if isinstance(maritime_payload, dict) and "forecast" in maritime_payload:
        maritime = maritime_payload.get("forecast") or {}
    else:
        maritime = maritime_payload or {}

    recommendation = context.get("recommendation") or {}
    reasoning = recommendation.get("reasoning") or {}
    fuzzy = recommendation.get("fuzzy") or {}

    village = location.get("village") or "lokasi yang dipantau"
    district = location.get("district") or ""
    city = location.get("city") or ""
    province = location.get("province") or ""

    place = ", ".join(
        part for part in [village, district, city, province] if part
    ) or "lokasi yang dipantau"

    temperature = weather.get("temperature")
    humidity = weather.get("humidity")
    precipitation = weather.get("precipitation")
    wind_speed = weather.get("wind_speed")
    cloud_cover = weather.get("cloud_cover")
    condition = weather.get("condition") or "-"

    wave_height = maritime.get("wave_height")
    wind_avg = maritime.get("wind_speed_avg")
    wind_max = maritime.get("wind_speed_max")
    ffx = maritime.get("ffx_category")

    hypothesis = reasoning.get("hypothesis") or "-"
    hypothesis_name = reasoning.get("hypothesis_name") or "Belum tersedia"
    confidence = reasoning.get("confidence")
    recommendation_text = reasoning.get("recommendation") or "Belum tersedia"
    classification = fuzzy.get("classification") or "-"

    base = (
        f"Berdasarkan data BMKG di {place}, kondisi cuaca saat ini adalah {condition}. "
        f"Suhu {temperature if temperature is not None else '-'} °C, kelembapan {humidity if humidity is not None else '-'}%, "
        f"curah hujan {precipitation if precipitation is not None else '-'} mm, angin atmosfer {wind_speed if wind_speed is not None else '-'} km/jam, "
        f"gelombang {wave_height if wave_height is not None else '-'} m, dan kategori angin {ffx if ffx else '-'} . "
        f"Klasifikasi fuzzy menunjukkan {classification}. "
        f"Sistem memilih hipotesis {hypothesis} ({hypothesis_name}) dengan confidence {confidence if confidence is not None else '-'}%. "
        f"Rekomendasi: {recommendation_text}"
    )

    if "hujan" in str(question).lower():
        return base + " Karena pertanyaan Anda terkait hujan, fokus utama adalah curah hujan dan visibilitas. Jika hujan kuat, risiko keputusan melaut meningkat."

    if "angin" in str(question).lower():
        return base + " Untuk angin, nilai yang paling relevan adalah angin rata-rata dan maksimum serta kategori FFX. Semakin tinggi angin, semakin besar risiko keputusan melaut."

    if "gelombang" in str(question).lower() or "ombak" in str(question).lower():
        return base + " Gelombang dan tinggi gelombang adalah indikator utama untuk keberangkatan. Gelombang yang tinggi memengaruhi stabilitas dan keselamatan kapal."

    if "aman" in str(question).lower() or "melaut" in str(question).lower():
        return base + " Berdasarkan evidence saat ini, keputusan melaut harus diambil dengan mempertimbangkan kondisi cuaca, gelombang, dan angin secara bersamaan, bukan hanya satu parameter saja."

    return base + " Saya menjawab berdasarkan data cuaca, maritim, dan hasil reasoning yang sedang aktif di dashboard."


def call_openai_chat(question: str, context: dict) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return build_grounded_ai_answer(question, context)

    prompt = (
        "Anda adalah asisten analisis cuaca untuk nelayan. "
        "Jawab dengan singkat, jelas, dan berbasis data saja. "
        "Gunakan konteks berikut sebagai sumber kebenaran: "
        f"{json.dumps(context, ensure_ascii=False)}\n\n"
        f"Pertanyaan pengguna: {question}"
    )

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Kamu adalah asisten cuaca dan keputusan melaut yang grounded pada data aktual."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 300
            },
            timeout=30
        )

        response.raise_for_status()
        payload = response.json()
        return payload["choices"][0]["message"]["content"].strip()

    except Exception:
        return build_grounded_ai_answer(question, context)


load_dotenv()


app = FastAPI(
    title="Weather Reasoning AI",
    description="AI rekomendasi kondisi cuaca untuk nelayan",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {
        "message": "Weather Reasoning AI API aktif"
    }


def get_all_weather_data(adm4=None, maritime_code=None):

    weather_data = get_weather_data(adm4=adm4)

    if weather_data is None:
        return None

    maritime_code = maritime_code or os.getenv(
        "BMKG_MARITIME_CODE"
    )

    maritime_data = get_maritime_data(
        maritime_code
    )

    return {
        "atmosphere": weather_data,
        "maritime": maritime_data
    }


@app.get("/api/locations")
def locations():
    return {
        "success": True,
        "locations": get_bmkg_location_catalog()
    }


@app.get("/api/regions/provinces")
def regions_provinces():
    """Get all provinces (level 1)."""
    return {
        "success": True,
        "data": get_all_provinces()
    }


@app.get("/api/regions/kabupaten")
def regions_kabupaten(province_code: str = None):
    """Get kabupaten/kota by province code (level 2)."""
    if not province_code:
        return {
            "success": False,
            "message": "province_code wajib diisi"
        }

    return {
        "success": True,
        "data": get_kabupaten_by_province(province_code)
    }


@app.get("/api/regions/kecamatan")
def regions_kecamatan(kabupaten_code: str = None):
    """Get kecamatan by kabupaten code (level 3)."""
    if not kabupaten_code:
        return {
            "success": False,
            "message": "kabupaten_code wajib diisi"
        }

    return {
        "success": True,
        "data": get_kecamatan_by_kabupaten(kabupaten_code)
    }


@app.get("/api/regions/desa")
def regions_desa(kecamatan_code: str = None):
    """Get desa/kelurahan by kecamatan code (level 4)."""
    if not kecamatan_code:
        return {
            "success": False,
            "message": "kecamatan_code wajib diisi"
        }

    return {
        "success": True,
        "data": get_desa_by_kecamatan(kecamatan_code)
    }


@app.get("/api/weather")
def weather(adm4: str = None, maritime_code: str = None):

    data = get_all_weather_data(
        adm4=adm4,
        maritime_code=maritime_code
    )

    if data is None:
        return {
            "success": False,
            "message": "Gagal mengambil data BMKG"
        }

    return {
        "success": True,
        "data": data
    }


@app.get("/api/fuzzy")
def fuzzy():

    data = get_all_weather_data()

    if data is None:
        return {
            "success": False,
            "message": "Gagal mengambil data BMKG"
        }

    weather = data["atmosphere"]["weather"]

    fuzzy_result = classify_weather(
        precipitation=weather["precipitation"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
        cloud_cover=weather["cloud_cover"],
        weather_condition=weather["condition"]
    )

    return {
        "success": True,
        "weather": data["atmosphere"],
        "maritime": data["maritime"],
        "fuzzy": fuzzy_result
    }


@app.get("/api/recommendation")
def recommendation(
    fisherman_status: str = "belum_berangkat",
    adm4: str = None,
    maritime_code: str = None
):

    allowed_status = [
        "belum_berangkat",
        "sudah_melaut"
    ]

    if fisherman_status not in allowed_status:
        return {
            "success": False,
            "message": (
                "fisherman_status harus "
                "'belum_berangkat' atau 'sudah_melaut'"
            )
        }

    data = get_all_weather_data(
        adm4=adm4,
        maritime_code=maritime_code
    )

    if data is None:
        return {
            "success": False,
            "message": "Gagal mengambil data BMKG"
        }

    weather_data = data["atmosphere"]
    maritime_data = data["maritime"]

    if maritime_data is None:
        return {
            "success": False,
            "message": "Data maritim BMKG tidak tersedia"
        }

    weather = weather_data["weather"]
    forecast = maritime_data["forecast"]
    hazards = maritime_data["hazards"]

    fuzzy_result = classify_weather(
        precipitation=weather["precipitation"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
        cloud_cover=weather["cloud_cover"],
        weather_condition=weather["condition"]
    )

    wind_speed_avg = forecast.get(
        "wind_speed_avg"
    )

    wind_speed_max = forecast.get(
        "wind_speed_max"
    )

    wave_height = forecast.get(
        "wave_height"
    )

    ffx_category = forecast.get(
        "ffx_category"
    )

    if wind_speed_avg is None:
        return {
            "success": False,
            "message": (
                "Data kecepatan angin rata-rata "
                "tidak tersedia"
            )
        }

    if wave_height is None:
        return {
            "success": False,
            "message": (
                "Data tinggi gelombang "
                "tidak tersedia"
            )
        }

    if ffx_category is None:
        return {
            "success": False,
            "message": (
                "Kategori angin maksimum "
                "tidak tersedia"
            )
        }

    reasoning_result = calculate_reasoning(

        fuzzy_result=fuzzy_result,

        precipitation=weather["precipitation"],

        humidity=weather["humidity"],

        wind_speed_knots=wind_speed_avg,

        ffx_category=ffx_category,

        wave_height=wave_height,

        lightning=hazards.get(
            "lightning"
        ),

        visibility_bad=hazards.get(
            "visibility_bad"
        ),

        breaking_wave=hazards.get(
            "breaking_wave"
        ),

        weather_condition=weather["condition"],

        fisherman_status=fisherman_status
    )

    return {

        "success": True,

        "weather": weather_data,

        "maritime": maritime_data,

        "fuzzy": fuzzy_result,

        "reasoning": reasoning_result,

        "derived": {

            "wind_speed_knots": wind_speed_avg,

            "wind_speed_max_knots": wind_speed_max,

            "wave_height_m": wave_height
        }
    }


@app.post("/api/location/nearest")
def nearest_location(payload: dict):
    lat = (payload or {}).get("latitude")
    lon = (payload or {}).get("longitude")

    if lat is None or lon is None:
        raise HTTPException(status_code=400, detail="latitude dan longitude wajib diisi")

    match = find_nearest_location(lat, lon)
    if match is None:
        return {
            "success": False,
            "message": "Tidak dapat menemukan lokasi BMKG terdekat"
        }

    return {
        "success": True,
        "location": match
    }


@app.post("/api/ai-chat")
def ai_chat(payload: dict):
    question = str((payload or {}).get("question") or "").strip()

    if not question:
        raise HTTPException(status_code=400, detail="Pertanyaan tidak boleh kosong")

    adm4 = (payload or {}).get("adm4")
    maritime_code = (payload or {}).get("maritime_code")

    data = get_all_weather_data(
        adm4=adm4,
        maritime_code=maritime_code
    )
    if data is None:
        return {
            "success": False,
            "message": "Data cuaca BMKG tidak tersedia saat ini."
        }

    recommendation_result = recommendation(
        fisherman_status="belum_berangkat",
        adm4=(payload or {}).get("adm4"),
        maritime_code=(payload or {}).get("maritime_code")
    )

    context = {
        "weather": data.get("atmosphere") or {},
        "maritime": data.get("maritime") or {},
        "recommendation": recommendation_result if isinstance(recommendation_result, dict) else {}
    }

    answer = call_openai_chat(question, context)

    return {
        "success": True,
        "answer": answer,
        "context": context
    }


@app.get("/api/test-reasoning")
def test_reasoning():

    scenarios = [
        {
            "name": "H1 - Relatif Aman",
            "status": "belum_berangkat",
            "wind": 8,
            "ffx": "rendah",
            "wave": 0.5
        },
        {
            "name": "H2 - Perlu Kewaspadaan",
            "status": "belum_berangkat",
            "wind": 13,
            "ffx": "sedang",
            "wave": 1.0
        },
        {
            "name": "H3 - Tidak Aman Berangkat",
            "status": "belum_berangkat",
            "wind": 26,
            "ffx": "tinggi",
            "wave": 2.5
        },
        {
            "name": "H4 - Berbahaya Saat di Laut",
            "status": "sudah_melaut",
            "wind": 26,
            "ffx": "tinggi",
            "wave": 2.5
        }
    ]

    results = []

    fuzzy_dummy = {
        "classification": ""
    }

    for scenario in scenarios:

        result = calculate_reasoning(
            fuzzy_result=fuzzy_dummy,

            precipitation=0,

            humidity=68,

            wind_speed_knots=scenario["wind"],

            ffx_category=scenario["ffx"],

            wave_height=scenario["wave"],

            fisherman_status=scenario["status"]
        )

        results.append({

            "scenario": scenario["name"],

            "input": {
                "status": scenario["status"],
                "wind_speed_avg": scenario["wind"],
                "ffx_category": scenario["ffx"],
                "wave_height": scenario["wave"]
            },

            "output": {
                "hypothesis": result["hypothesis"],
                "hypothesis_name": result["hypothesis_name"],
                "confidence": result["confidence"],
                "scores": result["scores"]
            }

        })

    return {
        "success": True,
        "results": results
    }