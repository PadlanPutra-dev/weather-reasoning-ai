import os
import requests
from dotenv import load_dotenv

load_dotenv()

BMKG_URL = "https://api.bmkg.go.id/publik/prakiraan-cuaca"


def get_weather_data():
    adm4 = os.getenv("BMKG_ADM4", "31.71.03.1001")

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