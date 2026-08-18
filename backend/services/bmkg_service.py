import os
import math
import requests
from dotenv import load_dotenv

load_dotenv()

BMKG_URL = "https://api.bmkg.go.id/publik/prakiraan-cuaca"

BMKG_LOCATION_CATALOG = [
    {
        "name": "Kemayoran, Jakarta Pusat",
        "adm4": "31.71.03.1001",
        "maritime_code": "H.01",
        "lat": -6.164721,
        "lon": 106.845384
    },
    {
        "name": "Bandung, Jawa Barat",
        "adm4": "32.73.01.1001",
        "maritime_code": "H.02",
        "lat": -6.917464,
        "lon": 107.619123
    },
    {
        "name": "Surabaya, Jawa Timur",
        "adm4": "35.74.01.1001",
        "maritime_code": "H.03",
        "lat": -7.257472,
        "lon": 112.752090
    },
    {
        "name": "Makassar, Sulawesi Selatan",
        "adm4": "73.71.01.1001",
        "maritime_code": "H.04",
        "lat": -5.147665,
        "lon": 119.432732
    }
]


def get_bmkg_location_catalog():
    return BMKG_LOCATION_CATALOG


def get_weather_data(adm4=None):
    adm4 = adm4 or os.getenv("BMKG_ADM4", "31.71.03.1001")

    params = {
        "adm4": adm4
    }

    try:
        response = requests.get(
            BMKG_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return normalize_weather_data(data)

    except requests.RequestException as e:
        print(f"Error koneksi BMKG: {e}")
        return None

    except Exception as e:
        print(f"Error memproses data BMKG: {e}")
        return None


def find_nearest_location(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return None

    def haversine(a_lat, a_lon, b_lat, b_lon):
        radius = 6371
        d_lat = math.radians(b_lat - a_lat)
        d_lon = math.radians(b_lon - a_lon)
        a1 = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(a_lat))
            * math.cos(math.radians(b_lat))
            * math.sin(d_lon / 2) ** 2
        )
        return 2 * radius * math.asin(math.sqrt(a1))

    nearest = None
    nearest_distance = None

    for option in BMKG_LOCATION_CATALOG:
        distance = haversine(lat, lon, option["lat"], option["lon"])
        if nearest_distance is None or distance < nearest_distance:
            nearest = option
            nearest_distance = distance

    if nearest is None:
        return None

    nearest["distance_km"] = round(nearest_distance, 2)
    return nearest


def normalize_weather_data(data):

    lokasi = data["lokasi"]
    weather_groups = data["data"][0]["cuaca"]

    weather_items = []

    for group in weather_groups:
        for item in group:
            weather_items.append(item)

    if not weather_items:
        raise ValueError("Data cuaca BMKG kosong")

    current = weather_items[0]

    return {
        "location": {
            "adm4": lokasi.get("adm4"),
            "province": lokasi.get("provinsi"),
            "city": lokasi.get("kotkab"),
            "district": lokasi.get("kecamatan"),
            "village": lokasi.get("desa"),
            "latitude": lokasi.get("lat"),
            "longitude": lokasi.get("lon")
        },

        "weather": {
            "timestamp": current.get("local_datetime"),
            "temperature": current.get("t"),
            "humidity": current.get("hu"),
            "precipitation": current.get("tp"),
            "wind_speed": current.get("ws"),
            "cloud_cover": current.get("tcc"),
            "visibility": current.get("vs_text"),
            "condition": current.get("weather_desc")
        }
    }


if __name__ == "__main__":

    result = get_weather_data()

    print("\n=== DATA CUACA NORMALIZED ===")

    if result:
        print(result)
    else:
        print("Gagal mengambil data BMKG")