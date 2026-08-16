from fastapi import FastAPI

from backend.services.bmkg_service import get_weather_data
from backend.services.fuzzy_service import classify_weather
from backend.services.reasoning_service import calculate_reasoning


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


@app.get("/api/weather")
def weather():

    weather_data = get_weather_data()

    if weather_data is None:
        return {
            "success": False,
            "message": "Gagal mengambil data BMKG"
        }

    return {
        "success": True,
        "data": weather_data
    }


@app.get("/api/fuzzy")
def fuzzy():

    weather_data = get_weather_data()

    if weather_data is None:
        return {
            "success": False,
            "message": "Gagal mengambil data BMKG"
        }

    weather = weather_data["weather"]

    fuzzy_result = classify_weather(
        precipitation=weather["precipitation"],
        humidity=weather["humidity"],
        wind_speed=weather["wind_speed"],
        cloud_cover=weather["cloud_cover"],
        weather_condition=weather["condition"]
    )

    return {
        "success": True,
        "weather": weather,
        "fuzzy": fuzzy_result
    }


@app.get("/api/recommendation")
def recommendation(
    fisherman_status: str = "belum_berangkat"
):

    weather_data = get_weather_data()

    if weather_data is None:
        return {
            "success": False,
            "message": "Gagal mengambil data BMKG"
        }

    weather = weather_data["weather"]

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
        fisherman_status=fisherman_status
    )

    return {
        "success": True,

        "weather": weather,

        "fuzzy": fuzzy_result,

        "reasoning": reasoning_result
    }