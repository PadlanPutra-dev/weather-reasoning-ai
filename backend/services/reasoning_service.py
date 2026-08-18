HYPOTHESES = {
    "H1": {
        "name": "Kondisi relatif aman",
        "recommendation": (
            "Nelayan dapat melaut dengan tetap mengikuti "
            "informasi cuaca dan peringatan resmi BMKG."
        )
    },

    "H2": {
        "name": "Kondisi perlu kewaspadaan",
        "recommendation": (
            "Nelayan dapat melaut dengan kewaspadaan lebih tinggi, "
            "membatasi area dan durasi aktivitas."
        )
    },

    "H3": {
        "name": "Kondisi tidak aman untuk berangkat",
        "recommendation": (
            "Nelayan disarankan menunda keberangkatan "
            "sampai kondisi cuaca dan laut membaik."
        )
    },

    "H4": {
        "name": "Kondisi berbahaya saat di laut",
        "recommendation": (
            "Nelayan yang sudah berada di laut disarankan "
            "mengurangi atau menghentikan aktivitas dan menuju "
            "titik aman sesuai kondisi."
        )
    }
}


def calculate_reasoning(
    fuzzy_result,
    precipitation,
    humidity,
    wind_speed_knots,
    ffx_category,
    wave_height,
    lightning=False,
    visibility_bad=False,
    breaking_wave=False,
    sunshine_duration=None,
    weather_condition="",
    fisherman_status="belum_berangkat"
):
    """
    Abductive reasoning untuk menentukan kondisi keselamatan nelayan.

    Hipotesis:

    H1 = Kondisi relatif aman
    H2 = Kondisi perlu kewaspadaan
    H3 = Kondisi tidak aman untuk berangkat
    H4 = Kondisi berbahaya saat di laut

    Parameter utama:

    - wind_speed_knots
    - ffx_category
    - wave_height
    - lightning
    - visibility_bad
    - breaking_wave
    - fisherman_status

    Parameter pendukung:

    - precipitation
    - humidity
    - fuzzy_result
    - weather_condition
    """

    # =========================================================
    # NORMALISASI INPUT
    # =========================================================

    scores = {
        "H1": 0,
        "H2": 0,
        "H3": 0,
        "H4": 0
    }

    evidence = []

    classification = str(
        (fuzzy_result or {}).get(
            "classification",
            ""
        )
    ).upper()

    weather = str(
        weather_condition or ""
    ).strip().lower()

    ffx = str(
        ffx_category or ""
    ).strip().lower()

    try:
        wind = float(wind_speed_knots or 0)
    except (TypeError, ValueError):
        wind = 0

    try:
        wave = float(wave_height or 0)
    except (TypeError, ValueError):
        wave = 0

    try:
        rain = float(precipitation or 0)
    except (TypeError, ValueError):
        rain = 0

    try:
        rh = float(humidity or 0)
    except (TypeError, ValueError):
        rh = 0

    # Normalisasi status
    fisherman_status = str(
        fisherman_status or "belum_berangkat"
    ).strip().lower()

    if fisherman_status not in [
        "belum_berangkat",
        "sudah_melaut"
    ]:
        fisherman_status = "belum_berangkat"

    # =========================================================
    # STATUS NELAYAN
    # =========================================================

    if fisherman_status == "sudah_melaut":

        candidate_hypotheses = [
            "H2",
            "H4"
        ]

        evidence.append(
            "Nelayan sudah berada di laut sehingga sistem "
            "mengevaluasi kondisi kewaspadaan atau bahaya."
        )

    else:

        candidate_hypotheses = [
            "H1",
            "H2",
            "H3"
        ]

        evidence.append(
            "Nelayan belum berangkat sehingga sistem "
            "mengevaluasi keamanan untuk keputusan keberangkatan."
        )

    # =========================================================
    # E1. KONDISI CUACA FUZZY
    # =========================================================

    if classification:

        evidence.append(
            f"Hasil klasifikasi fuzzy: {classification}."
        )

    if weather in [
        "cerah",
        "cerah berawan",
        "tidak hujan",
        "tidak_hujan"
    ]:

        # Cuaca atmosfer baik.
        # Untuk kondisi sudah melaut, bukti ini tidak
        # langsung membuat H2/H4 menjadi aman.
        if fisherman_status == "belum_berangkat":
            scores["H1"] += 1

        evidence.append(
            "Kondisi atmosfer relatif baik."
        )

    elif weather in [
        "berawan",
        "mendung"
    ]:

        scores["H2"] += 1

        evidence.append(
            "Kondisi atmosfer berawan atau mendung."
        )

    elif "hujan" in weather:

        scores["H2"] += 2

        evidence.append(
            "Hujan terdeteksi pada kondisi atmosfer."
        )

    elif weather in [
        "ekstrem",
        "cuaca ekstrem",
        "cuaca_ekstrem"
    ]:

        scores["H3"] += 4
        scores["H4"] += 4

        evidence.append(
            "Kondisi atmosfer dikategorikan ekstrem."
        )

    # =========================================================
    # E2. CURAH HUJAN
    # =========================================================

    if rain >= 100:

        scores["H3"] += 3
        scores["H4"] += 3

        evidence.append(
            f"Curah hujan sangat tinggi ({rain:.1f} mm)."
        )

    elif rain >= 50:

        scores["H2"] += 2
        scores["H3"] += 2

        evidence.append(
            f"Curah hujan tinggi ({rain:.1f} mm)."
        )

    elif rain >= 20:

        scores["H2"] += 1

        evidence.append(
            f"Curah hujan berada pada tingkat sedang "
            f"({rain:.1f} mm)."
        )

    else:

        evidence.append(
            f"Curah hujan rendah ({rain:.1f} mm)."
        )

    # =========================================================
    # E3. KELEMBAPAN
    # =========================================================

    if rh >= 85:

        scores["H2"] += 1

        evidence.append(
            f"Kelembapan tinggi ({rh:.0f}%)."
        )

    # =========================================================
    # E4. ANGIN RATA-RATA
    # =========================================================

    if wind < 11:

        scores["H1"] += 2

        evidence.append(
            f"Kecepatan angin rata-rata rendah "
            f"({wind:.1f} knot)."
        )

    elif wind < 15:

        scores["H2"] += 2

        evidence.append(
            f"Kecepatan angin rata-rata berada pada "
            f"tingkat waspada ({wind:.1f} knot)."
        )

    else:

        scores["H3"] += 4
        scores["H4"] += 4

        evidence.append(
            f"Kecepatan angin rata-rata tinggi "
            f"({wind:.1f} knot)."
        )

    # =========================================================
    # E5. FFX / ANGIN MAKSIMUM
    # =========================================================

    if ffx == "sangat tinggi":

        scores["H3"] += 4
        scores["H4"] += 4

        evidence.append(
            "Kecepatan angin maksimum berada pada "
            "kategori sangat tinggi."
        )

    elif ffx == "tinggi":

        scores["H3"] += 3
        scores["H4"] += 3

        evidence.append(
            "Kecepatan angin maksimum berada pada "
            "kategori tinggi."
        )

    elif ffx == "sedang":

        scores["H2"] += 1

        evidence.append(
            "Kecepatan angin maksimum berada pada "
            "kategori sedang."
        )

    elif ffx == "rendah":

        evidence.append(
            "Kecepatan angin maksimum berada pada "
            "kategori rendah."
        )

    # =========================================================
    # E6. TINGGI GELOMBANG
    # =========================================================

    if wave <= 0.5:

        scores["H1"] += 2

        evidence.append(
            f"Tinggi gelombang rendah ({wave:.2f} m)."
        )

    elif wave < 1.25:

        scores["H2"] += 2

        evidence.append(
            f"Tinggi gelombang berada pada tingkat "
            f"kewaspadaan ({wave:.2f} m)."
        )

    elif wave <= 2.5:

        scores["H3"] += 4
        scores["H4"] += 4

        evidence.append(
            f"Tinggi gelombang berada pada tingkat "
            f"risiko meningkat ({wave:.2f} m)."
        )

    elif wave < 4:

        scores["H3"] += 5
        scores["H4"] += 5

        evidence.append(
            f"Tinggi gelombang sangat tinggi "
            f"({wave:.2f} m)."
        )

    else:

        scores["H3"] += 6
        scores["H4"] += 6

        evidence.append(
            f"Tinggi gelombang ekstrem "
            f"({wave:.2f} m)."
        )

    # =========================================================
    # E7. BAHAYA LANGSUNG
    # =========================================================

    direct_hazard = False

    if lightning is True:

        direct_hazard = True

        evidence.append(
            "Potensi petir terdeteksi."
        )

    if visibility_bad is True:

        direct_hazard = True

        evidence.append(
            "Visibilitas berada pada kondisi buruk."
        )

    if breaking_wave is True:

        direct_hazard = True

        evidence.append(
            "Gelombang pecah terdeteksi."
        )

    if direct_hazard:

        scores["H3"] += 5
        scores["H4"] += 5

        evidence.append(
            "Bahaya langsung terdeteksi sehingga "
            "risiko keselamatan meningkat."
        )

    # =========================================================
    # E8. KOMBINASI ANGIN DAN GELOMBANG
    # =========================================================

    high_wind = wind >= 15
    high_wave = wave >= 1.25

    if high_wind and high_wave:

        evidence.append(
            "Kombinasi angin minimal 15 knot dan "
            "gelombang minimal 1,25 m menunjukkan "
            "risiko keselamatan tinggi."
        )

        if fisherman_status == "belum_berangkat":

            scores["H3"] += 8

        else:

            scores["H4"] += 8

    # =========================================================
    # E9. KONDISI SUDAH MELAUT
    # =========================================================

    if fisherman_status == "sudah_melaut":

        if high_wind:

            scores["H4"] += 2

        if high_wave:

            scores["H4"] += 2

        if direct_hazard:

            scores["H4"] += 5

    # =========================================================
    # E10. BATASI HIPOTESIS BERDASARKAN STATUS
    # =========================================================

    if fisherman_status == "belum_berangkat":

        scores["H4"] = 0

    else:

        scores["H1"] = 0
        scores["H3"] = 0

    # =========================================================
    # E11. PEMILIHAN HIPOTESIS
    # =========================================================

    priority = {
        "H4": 4,
        "H3": 3,
        "H2": 2,
        "H1": 1
    }

    selected_hypothesis = max(
        candidate_hypotheses,
        key=lambda h: (
            scores[h],
            priority[h]
        )
    )

    # =========================================================
    # E12. CONFIDENCE
    # =========================================================

    candidate_scores = [
        scores[h]
        for h in candidate_hypotheses
    ]

    total_score = sum(candidate_scores)

    if total_score > 0:

        confidence = (
            scores[selected_hypothesis]
            / total_score
        ) * 100

    else:

        confidence = 0

    # =========================================================
    # RETURN
    # =========================================================

    return {
        "hypothesis": selected_hypothesis,

        "hypothesis_name": HYPOTHESES[
            selected_hypothesis
        ]["name"],

        "recommendation": HYPOTHESES[
            selected_hypothesis
        ]["recommendation"],

        "scores": scores,

        "candidate_hypotheses": candidate_hypotheses,

        "confidence": round(
            confidence,
            2
        ),

        "evidence": evidence
    }