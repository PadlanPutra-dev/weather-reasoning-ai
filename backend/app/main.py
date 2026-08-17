from fastapi import FastAPI

from backend.services.bmkg_service import (
    get_weather_data
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

import os
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(
    title="Weather Reasoning AI",
    description="AI rekomendasi kondisi cuaca untuk nelayan",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Weather Reasoning AI API aktif"
    }


def get_all_weather_data():

    weather_data = get_weather_data()

    if weather_data is None:
        return None

    maritime_code = os.getenv(
        "BMKG_MARITIME_CODE"
    )

    maritime_data = get_maritime_data(
        maritime_code
    )

    return {
        "atmosphere": weather_data,
        "maritime": maritime_data
    }


@app.get("/api/weather")
def weather():

    data = get_all_weather_data()

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
    fisherman_status: str = "belum_berangkat"
):

    data = get_all_weather_data()

    if data is None:
        return {
            "success": False,
            "message": "Gagal mengambil data BMKG"
        }

    weather = data["atmosphere"]["weather"]

    maritime = data["maritime"]

    if maritime is None:
        return {
            "success": False,
            "message": "Data maritim BMKG tidak tersedia"
        }

    maritime_forecast = maritime["forecast"]

    hazards = maritime["hazards"]

    fuzzy_result = classify_weather(
        precipitation=weather["precipitation"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
        cloud_cover=weather["cloud_cover"],
        weather_condition=weather["condition"]
    )

    reasoning_result = calculate_reasoning(
    fuzzy_result=fuzzy_result,

    precipitation=weather["precipitation"],
    humidity=weather["humidity"],
    wind_speed=weather["wind_speed"],
    cloud_cover=weather["cloud_cover"],
    weather_condition=weather["condition"],

    fisherman_status=fisherman_status,

    ffx_category=maritime["forecast"]["ffx_category"],
    wave_height=maritime["forecast"]["wave_height"],
    wave_category=maritime["forecast"]["wave_category"],

    lightning=maritime["hazards"]["lightning"],
    visibility_bad=maritime["hazards"]["visibility_bad"],
    breaking_wave=maritime["hazards"]["breaking_wave"]
)

    return {
        "success": True,

        "weather": data["atmosphere"],

        "maritime": data["maritime"],

        "fuzzy": fuzzy_result,

        "reasoning": reasoning_result
    }