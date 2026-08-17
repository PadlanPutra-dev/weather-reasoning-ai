import re
import requests
from urllib.parse import quote


BASE_URL = (
    "https://peta-maritim.bmkg.go.id/"
    "public_api/perairan/"
)


def get_maritime_data(maritime_code):
    if not maritime_code:
        return None

    url = (
        BASE_URL
        + quote(maritime_code, safe="")
        + ".json"
    )

    try:
        response = requests.get(
            url,
            timeout=20
        )

        response.raise_for_status()

        return normalize_maritime_data(
            response.json()
        )

    except requests.RequestException as e:
        print(f"Error koneksi BMKG maritim: {e}")
        return None

    except Exception as e:
        print(f"Error memproses data maritim BMKG: {e}")
        return None


def parse_wave_height(wave_desc):
    """
    Mengambil nilai tinggi gelombang maksimum
    dari format BMKG seperti:

    '1.25 - 2.5 m'
    '2.5 - 4.0 m'
    """

    if not wave_desc:
        return None

    numbers = re.findall(
        r"\d+(?:[.,]\d+)?",
        str(wave_desc)
    )

    if not numbers:
        return None

    values = [
        float(number.replace(",", "."))
        for number in numbers
    ]

    # Gunakan nilai maksimum sebagai representasi
    # konservatif untuk reasoning keselamatan.
    return max(values)


def get_ffx_category(wind_speed_max):
    """
    Kategori FFX berdasarkan kecepatan angin maksimum.

    < 11 knot       -> rendah
    11 - <15 knot   -> sedang
    >=15 knot       -> tinggi
    """

    if wind_speed_max is None:
        return None

    if wind_speed_max < 11:
        return "rendah"

    elif wind_speed_max < 15:
        return "sedang"

    return "tinggi"


def normalize_maritime_data(data):

    if not isinstance(data, dict):
        raise ValueError(
            "Format data maritim tidak dikenali"
        )

    forecast_data = data.get("data", [])

    if not forecast_data:
        raise ValueError(
            "Data prakiraan maritim kosong"
        )

    current = forecast_data[0]

    wind_speed_min = current.get(
        "wind_speed_min"
    )

    wind_speed_max = current.get(
        "wind_speed_max"
    )

    wave_desc = current.get(
        "wave_desc"
    )

    wave_height = parse_wave_height(
        wave_desc
    )

    ffx_category = get_ffx_category(
        wind_speed_max
    )

    return {
        "code": data.get("code"),
        "name": data.get("name"),
        "issued": data.get("issued"),
        "info": data.get("info"),

        "forecast": {
            "valid_from": current.get(
                "valid_from"
            ),

            "valid_to": current.get(
                "valid_to"
            ),

            "time_desc": current.get(
                "time_desc"
            ),

            "weather": current.get(
                "weather"
            ),

            "weather_desc": current.get(
                "weather_desc"
            ),

            "warning_desc": current.get(
                "warning_desc"
            ),

            "station_remark": current.get(
                "station_remark"
            ),

            "wave_category": current.get(
                "wave_cat"
            ),

            "wave_desc": wave_desc,

            "wave_height": wave_height,

            "wind_from": current.get(
                "wind_from"
            ),

            "wind_to": current.get(
                "wind_to"
            ),

            "wind_speed_min": wind_speed_min,

            "wind_speed_max": wind_speed_max,

            "ffx_category": ffx_category
        },

        # Belum tersedia dari endpoint yang digunakan.
        "hazards": {
            "lightning": None,
            "visibility_bad": None,
            "breaking_wave": None
        },

        # SS belum tersedia dari sumber yang digunakan.
        "sunshine_duration": None
    }