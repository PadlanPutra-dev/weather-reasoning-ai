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
    fisherman_status,
    ffx_category=None,
    wave_height=None,
    wave_category=None,
    lightning=None,
    visibility_bad=None,
    breaking_wave=None
):
    """
    Abductive Reasoning untuk menentukan kondisi keselamatan nelayan.
    """

    scores = {
        "H1": 0,
        "H2": 0,
        "H3": 0,
        "H4": 0
    }

    evidence = []

    classification = fuzzy_result.get(
        "classification", ""
    ).upper()

    # =====================================================
    # E1. HASIL FUZZY
    # =====================================================

    if classification in ["TIDAK_HUJAN", "AMAN"]:
        scores["H1"] += 3
        evidence.append(
            "Hasil fuzzy menunjukkan kondisi relatif aman."
        )

    elif classification in ["MENDUNG", "WASPADA"]:
        scores["H2"] += 3
        evidence.append(
            "Hasil fuzzy menunjukkan kondisi perlu kewaspadaan."
        )

    elif classification in ["HUJAN", "TIDAK AMAN", "TIDAK_AMAN"]:
        scores["H3"] += 4
        evidence.append(
            "Hasil fuzzy menunjukkan kondisi kurang aman."
        )

    elif classification == "EKSTREM":
        scores["H3"] += 4
        scores["H4"] += 3
        evidence.append(
            "Hasil fuzzy menunjukkan kondisi ekstrem."
        )

    # =====================================================
    # E2. CURAH HUJAN
    # =====================================================

    if precipitation is not None:

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
    # E3. KECEPATAN ANGIN ATMOSFER
    # =====================================================

    if wind_speed is not None:

        if wind_speed < 5:
            scores["H1"] += 2
            evidence.append(
                "Kecepatan angin atmosfer relatif lemah."
            )

        elif wind_speed < 10:
            scores["H2"] += 2
            scores["H3"] += 1
            evidence.append(
                "Kecepatan angin atmosfer sedang."
            )

        else:
            scores["H3"] += 3
            scores["H4"] += 2
            evidence.append(
                "Kecepatan angin atmosfer kuat."
            )

    # =====================================================
    # E4. ANGIN LAUT / FFX
    # =====================================================

    if ffx_category:

        ffx = ffx_category.lower()

        if ffx == "rendah":
            scores["H1"] += 1
            evidence.append(
                "Kecepatan angin laut relatif rendah."
            )

        elif ffx == "sedang":
            scores["H2"] += 2
            evidence.append(
                "Kecepatan angin laut berada pada kategori sedang."
            )

        elif ffx == "tinggi":
            scores["H3"] += 3
            scores["H4"] += 2
            evidence.append(
                "Kecepatan angin laut tinggi."
            )

    # =====================================================
    # E5. TUTUPAN AWAN
    # =====================================================

    if cloud_cover is not None:

        if cloud_cover >= 90 and precipitation > 10:
            scores["H3"] += 1
            evidence.append(
                "Tutupan awan sangat tinggi disertai hujan."
            )

        elif cloud_cover >= 80:
            scores["H2"] += 1
            evidence.append(
                "Tutupan awan tinggi."
            )

    # =====================================================
    # E6. KELEMBAPAN
    # =====================================================

    if humidity is not None:

        if humidity >= 85 and precipitation <= 1:
            scores["H2"] += 1
            evidence.append(
                "Kelembapan tinggi meskipun curah hujan rendah."
            )

    # =====================================================
    # E7. TINGGI GELOMBANG
    # =====================================================

    if wave_height is not None:

        if wave_height < 1.25:
            scores["H1"] += 2
            evidence.append(
                f"Tinggi gelombang relatif rendah ({wave_height} m)."
            )

        elif wave_height < 2.5:
            scores["H2"] += 2
            evidence.append(
                f"Tinggi gelombang sedang ({wave_height} m)."
            )

        elif wave_height < 4:
            scores["H3"] += 3
            scores["H4"] += 1
            evidence.append(
                f"Tinggi gelombang tinggi ({wave_height} m)."
            )

        else:
            scores["H4"] += 4
            evidence.append(
                f"Tinggi gelombang sangat tinggi ({wave_height} m)."
            )

    # =====================================================
    # E8. KATEGORI GELOMBANG BMKG
    # =====================================================

    if wave_category:

        wave_cat = wave_category.lower()

        if wave_cat == "rendah":
            scores["H1"] += 1

        elif wave_cat == "sedang":
            scores["H2"] += 1

        elif wave_cat == "tinggi":
            scores["H3"] += 2
            evidence.append(
                "BMKG mengategorikan gelombang sebagai tinggi."
            )

        elif wave_cat in ["sangat tinggi", "ekstrem"]:
            scores["H4"] += 3
            evidence.append(
                "BMKG mengategorikan gelombang sebagai sangat tinggi."
            )

    # =====================================================
    # E9. PETIR
    # =====================================================

    if lightning is True:
        scores["H3"] += 3
        scores["H4"] += 2
        evidence.append(
            "Terdapat indikasi petir."
        )

    # =====================================================
    # E10. VISIBILITY
    # =====================================================

    if visibility_bad is True:
        scores["H3"] += 2
        scores["H4"] += 1
        evidence.append(
            "Visibilitas buruk dapat mengganggu navigasi."
        )

    # =====================================================
    # E11. BREAKING WAVE
    # =====================================================

    if breaking_wave is True:
        scores["H4"] += 4
        evidence.append(
            "Terdapat indikasi breaking wave yang berbahaya."
        )

    # =====================================================
    # E12. STATUS NELAYAN
    # =====================================================

    if fisherman_status == "sudah_melaut":

        evidence.append(
            "Nelayan sudah berada di laut."
        )

        kondisi_buruk = (
            scores["H3"] > scores["H1"]
            or scores["H4"] > 0
            or precipitation > 10
            or wind_speed >= 10
            or (wave_height is not None and wave_height >= 2.5)
            or ffx_category == "tinggi"
            or lightning is True
            or breaking_wave is True
        )

        if kondisi_buruk:
            scores["H4"] += 5

            evidence.append(
                "Kondisi berbahaya saat nelayan sudah berada di laut."
            )

    elif fisherman_status == "belum_berangkat":

        kondisi_buruk = (
            precipitation > 10
            or wind_speed >= 10
            or (wave_height is not None and wave_height >= 2.5)
            or ffx_category == "tinggi"
            or lightning is True
            or breaking_wave is True
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