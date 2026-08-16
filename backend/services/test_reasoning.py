from reasoning_service import calculate_reasoning


scenarios = [
    {
        "name": "Skenario 1 - Aman",
        "fuzzy": {"classification": "AMAN"},
        "precipitation": 0,
        "humidity": 70,
        "wind_speed": 3,
        "cloud_cover": 20,
        "condition": "Cerah",
        "status": "belum_berangkat"
    },
    {
        "name": "Skenario 2 - Waspada",
        "fuzzy": {"classification": "WASPADA"},
        "precipitation": 5,
        "humidity": 80,
        "wind_speed": 7,
        "cloud_cover": 70,
        "condition": "Mendung",
        "status": "belum_berangkat"
    },
    {
        "name": "Skenario 3 - Tidak Aman",
        "fuzzy": {"classification": "TIDAK AMAN"},
        "precipitation": 20,
        "humidity": 90,
        "wind_speed": 12,
        "cloud_cover": 95,
        "condition": "Hujan",
        "status": "belum_berangkat"
    },
    {
        "name": "Skenario 4 - Berbahaya di Laut",
        "fuzzy": {"classification": "TIDAK AMAN"},
        "precipitation": 20,
        "humidity": 90,
        "wind_speed": 12,
        "cloud_cover": 95,
        "condition": "Hujan",
        "status": "sudah_melaut"
    }
]


for scenario in scenarios:

    result = calculate_reasoning(
        fuzzy_result=scenario["fuzzy"],
        precipitation=scenario["precipitation"],
        humidity=scenario["humidity"],
        wind_speed=scenario["wind_speed"],
        cloud_cover=scenario["cloud_cover"],
        weather_condition=scenario["condition"],
        fisherman_status=scenario["status"]
    )

    print("\n" + "=" * 60)
    print(scenario["name"])
    print("=" * 60)

    print("Status nelayan :", scenario["status"])
    print("Kondisi cuaca  :", scenario["condition"])
    print("RR             :", scenario["precipitation"])
    print("Angin          :", scenario["wind_speed"])
    print("Fuzzy          :", scenario["fuzzy"]["classification"])

    print("\nScore:")
    for hypothesis, score in result["scores"].items():
        print(f"  {hypothesis}: {score}")

    print("\nKeputusan:")
    print(result["hypothesis"])
    print(result["hypothesis_name"])

    print("\nRekomendasi:")
    print(result["recommendation"])

    print("\nEvidence:")
    for item in result["evidence"]:
        print(f"- {item}")