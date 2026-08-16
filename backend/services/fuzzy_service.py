import numpy as np
import skfuzzy as fuzz


def classify_weather(
    precipitation,
    humidity,
    wind_speed,
    cloud_cover,
    weather_condition
):
    """
    Fuzzy Logic untuk mengklasifikasikan kondisi cuaca.

    Output:
    TIDAK_HUJAN
    MENDUNG
    HUJAN
    EKSTREM
    """

    # =========================
    # 1. DOMAIN
    # =========================

    rain = np.arange(0, 51, 1)
    wind = np.arange(0, 31, 1)
    humidity_domain = np.arange(0, 101, 1)
    cloud = np.arange(0, 101, 1)

    # =========================
    # 2. MEMBERSHIP FUNCTION
    # =========================

    # Curah hujan
    rain_low = fuzz.trapmf(
        rain,
        [0, 0, 1, 5]
    )

    rain_medium = fuzz.trimf(
        rain,
        [2, 10, 25]
    )

    rain_high = fuzz.trapmf(
        rain,
        [15, 30, 50, 50]
    )

    # Angin
    wind_weak = fuzz.trapmf(
        wind,
        [0, 0, 3, 7]
    )

    wind_medium = fuzz.trimf(
        wind,
        [4, 10, 16]
    )

    wind_strong = fuzz.trapmf(
        wind,
        [12, 18, 30, 30]
    )

    # Kelembapan
    humidity_low = fuzz.trapmf(
        humidity_domain,
        [0, 0, 40, 60]
    )

    humidity_medium = fuzz.trimf(
        humidity_domain,
        [45, 65, 80]
    )

    humidity_high = fuzz.trapmf(
        humidity_domain,
        [70, 85, 100, 100]
    )

    # Tutupan awan
    cloud_low = fuzz.trapmf(
        cloud,
        [0, 0, 20, 40]
    )

    cloud_medium = fuzz.trimf(
        cloud,
        [25, 50, 75]
    )

    cloud_high = fuzz.trapmf(
        cloud,
        [60, 80, 100, 100]
    )

    # =========================
    # 3. FUZZIFICATION
    # =========================

    rain_low_value = fuzz.interp_membership(
        rain,
        rain_low,
        precipitation
    )

    rain_medium_value = fuzz.interp_membership(
        rain,
        rain_medium,
        precipitation
    )

    rain_high_value = fuzz.interp_membership(
        rain,
        rain_high,
        precipitation
    )

    wind_weak_value = fuzz.interp_membership(
        wind,
        wind_weak,
        wind_speed
    )

    wind_medium_value = fuzz.interp_membership(
        wind,
        wind_medium,
        wind_speed
    )

    wind_strong_value = fuzz.interp_membership(
        wind,
        wind_strong,
        wind_speed
    )

    humidity_high_value = fuzz.interp_membership(
        humidity_domain,
        humidity_high,
        humidity
    )

    cloud_medium_value = fuzz.interp_membership(
        cloud,
        cloud_medium,
        cloud_cover
    )

    cloud_high_value = fuzz.interp_membership(
        cloud,
        cloud_high,
        cloud_cover
    )

    # =========================
    # 4. RULE STRENGTH
    # =========================

    # Tidak hujan
    rule_no_rain = min(
        rain_low_value,
        wind_weak_value
    )

    # Mendung
    rule_cloudy = max(
        cloud_medium_value,
        min(
            cloud_high_value,
            rain_low_value,
            humidity_high_value
        )
    )

    # Hujan
    rule_rain = max(
        rain_medium_value,
        rain_high_value
    )

    # Ekstrem
    rule_extreme = max(
        min(rain_high_value, wind_strong_value),
        wind_strong_value
    )

    # =========================
    # 5. WEATHER CONDITION BMKG
    # =========================

    condition = weather_condition.lower()

    if "hujan" in condition:
        rule_rain = max(rule_rain, 0.7)

    elif "berawan" in condition:
        rule_cloudy = max(rule_cloudy, 0.6)

    elif "cerah" in condition:
        rule_no_rain = max(rule_no_rain, 0.8)

    # =========================
    # 6. FINAL CLASSIFICATION
    # =========================

    memberships = {
        "TIDAK_HUJAN": float(rule_no_rain),
        "MENDUNG": float(rule_cloudy),
        "HUJAN": float(rule_rain),
        "EKSTREM": float(rule_extreme)
    }

    classification = max(
        memberships,
        key=memberships.get
    )

    return {
        "classification": classification,
        "membership": memberships,
        "input": {
            "precipitation": precipitation,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "cloud_cover": cloud_cover,
            "weather_condition": weather_condition
        }
    }


# =========================
# TEST
# =========================

if __name__ == "__main__":

    result = classify_weather(
        precipitation=0,
        humidity=83,
        wind_speed=3.3,
        cloud_cover=21,
        weather_condition="Cerah"
    )

    print("\n=== FUZZY RESULT ===")
    print(result)