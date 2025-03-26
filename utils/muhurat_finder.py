def find_muhurats(date_str, latitude, longitude, timezone_offset, muhurat_type="marriage"):
    config = MUHURAT_TYPES.get(muhurat_type.lower(), MUHURAT_TYPES["marriage"])
    muhurats = []
    top_gpt_summary = ""

    base_time = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    for hour in range(5, 21, 2):
        dt = base_time.replace(hour=hour, minute=0, second=0)
        iso = dt.isoformat() + "Z"

        panchanga = get_panchanga(iso, latitude, longitude, timezone_offset)
        lagna = get_lagna_info(iso, latitude, longitude, timezone_offset)["lagna"]

        tithi_num = panchanga["tithi"].split()[1]
        nak = panchanga["nakshatra"].split("–")[0]
        yoga = panchanga["yoga"]

        score = 0
        reasons = []

        if tithi_num in config["tithis"]:
            score += config["weights"]["tithi"]
            reasons.append(f"Good Tithi ({tithi_num})")

        if nak in config["nakshatras"]:
            score += config["weights"]["nakshatra"]
            reasons.append(f"Favorable Nakshatra ({nak})")

        if yoga in config["yogas"]:
            score += config["weights"]["yoga"]
            reasons.append(f"Auspicious Yoga ({yoga})")

        if lagna in config["lagnas"]:
            score += config["weights"]["lagna"]
            reasons.append(f"Supportive Lagna ({lagna})")

        if score >= 6:
            muhurats.append({
                "time": dt.strftime("%H:%M"),
                "lagna": lagna,
                "tithi": panchanga["tithi"],
                "nakshatra": panchanga["nakshatra"],
                "yoga": yoga,
                "score": score,
                "reasons": reasons
            })

    # GPT Summary (top muhurat)
    if muhurats:
        top = sorted(muhurats, key=lambda x: -x["score"])[0]
        action = {
            "marriage": "marriage ceremony",
            "travel": "starting a journey",
            "business": "launching a business",
        }.get(muhurat_type, "important activity")

        top_gpt_summary = (
            f"Tomorrow’s best time for {action} is **{top['time']}** under **{top['lagna']} Lagna** "
            f"and **{top['yoga']} Yoga**, with **{top['nakshatra']}** and **{top['tithi']}**. "
            "This time is astrologically favorable and spiritually uplifting."
        )

    return {
        "muhurats": muhurats,
        "gpt_summary": top_gpt_summary
    }
