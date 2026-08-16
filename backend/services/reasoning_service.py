HYPOTHESES = {
    "H1": {
        "name": "Kondisi relatif aman",
        "recommendation": "Nelayan dapat melaut atau beraktivitas seperti biasa."
    },
    "H2": {
        "name": "Kondisi perlu kewaspadaan",
        "recommendation": "Nelayan dapat melaut dengan pembatasan, seperti durasi lebih singkat dan area dekat pantai."
    },
    "H3": {
        "name": "Kondisi tidak aman untuk berangkat",
        "recommendation": "Nelayan disarankan menunda keberangkatan sampai kondisi cuaca membaik."
    },
    "H4": {
        "name": "Kondisi berbahaya saat di laut",
        "recommendation": "Nelayan disarankan menghentikan aktivitas dan kembali ke daratan atau titik aman."
    }
}


def calculate_reasoning(
    fuzzy_result,
    precipitation,
    humidity,
    wind_speed,
    cloud_cover,
    weather_condition,
    fisherman_status
):
    """
    Abductive Reasoning untuk menentukan hipotesis
    berdasarkan evidence kondisi cuaca.
    """

    scores = {
        "H1": 0,
        "H2": 0,
        "H3": 0,
        "H4": 0
    }

    evidence = []

    classification = fuzzy_result.get("classification", "").upper()

    # =====================================================
    # E1. HASIL FUZZY
    # =====================================================

    if classification == "AMAN":
        scores["H1"] += 3
        evidence.append("Hasil fuzzy menunjukkan kondisi AMAN.")

    elif classification == "WASPADA":
        scores["H2"] += 3
        evidence.append("Hasil fuzzy menunjukkan kondisi WASPADA.")

    elif classification == "TIDAK AMAN":
        scores["H3"] += 4
        evidence.append("Hasil fuzzy menunjukkan kondisi TIDAK AMAN.")

    # =====================================================
    # E2. CURAH HUJAN
    # =====================================================

    if precipitation <= 1:
        scores["H1"] += 2
        evidence.append("Curah hujan rendah.")

    elif precipitation <= 10:
        scores["H2"] += 2
        scores["H3"] += 1
        evidence.append("Curah hujan sedang.")

    else:
        scores["H3"] += 3
        scores["H4"] += 2
        evidence.append("Curah hujan tinggi.")

    # =====================================================
    # E3. KECEPATAN ANGIN
    # =====================================================

    if wind_speed < 5:
        scores["H1"] += 2
        evidence.append("Kecepatan angin relatif lemah.")

    elif wind_speed < 10:
        scores["H2"] += 2
        scores["H3"] += 1
        evidence.append("Kecepatan angin sedang.")

    else:
        scores["H3"] += 3
        scores["H4"] += 2
        evidence.append("Kecepatan angin kuat.")

    # =====================================================
    # E4. TUTUPAN AWAN
    # =====================================================

    if cloud_cover >= 90 and precipitation > 10:
        scores["H3"] += 1
        evidence.append(
            "Tutupan awan sangat tinggi disertai hujan."
        )

    elif cloud_cover >= 80:
        scores["H2"] += 1
        evidence.append("Tutupan awan tinggi.")

    # =====================================================
    # E5. KELEMBAPAN
    # =====================================================

    if humidity >= 85 and precipitation <= 1:
        scores["H2"] += 1
        evidence.append(
            "Kelembapan tinggi meskipun curah hujan rendah."
        )

    # =====================================================
    # E6. STATUS NELAYAN
    # =====================================================

    if fisherman_status == "sudah_melaut":

        evidence.append(
            "Nelayan sudah berada di laut."
        )

        kondisi_buruk = (
            classification == "TIDAK AMAN"
            or precipitation > 10
            or wind_speed >= 10
        )

        if kondisi_buruk:
            scores["H4"] += 5

            evidence.append(
                "Kondisi memburuk ketika nelayan sudah berada di laut."
            )

    elif fisherman_status == "belum_berangkat":

        kondisi_buruk = (
            classification == "TIDAK AMAN"
            or precipitation > 10
            or wind_speed >= 10
        )

        if kondisi_buruk:
            scores["H3"] += 2

            evidence.append(
                "Kondisi tidak mendukung keberangkatan."
            )

    # =====================================================
    # PEMILIHAN HIPOTESIS
    # =====================================================

    priority = {
        "H4": 4,
        "H3": 3,
        "H2": 2,
        "H1": 1
    }

    selected_hypothesis = max(
        scores,
        key=lambda h: (scores[h], priority[h])
    )

    return {
        "hypothesis": selected_hypothesis,
        "hypothesis_name": HYPOTHESES[selected_hypothesis]["name"],
        "recommendation": HYPOTHESES[selected_hypothesis]["recommendation"],
        "scores": scores,
        "evidence": evidence
    }


if __name__ == "__main__":

    test_fuzzy = {
        "classification": "AMAN"
    }

    result = calculate_reasoning(
        fuzzy_result=test_fuzzy,
        precipitation=0,
        humidity=83,
        wind_speed=3.3,
        cloud_cover=21,
        weather_condition="Cerah",
        fisherman_status="belum_berangkat"
    )

    print("\n=== REASONING RESULT ===")
    print(result)