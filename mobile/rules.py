def evaluate_condition(
    *, surface_dark: bool, standing_water: bool, leaf_wilt: bool, moisture: str
) -> dict:
    """Offline, explainable baseline; it is not a disease diagnosis."""
    evidence = []
    score = 0
    if standing_water or moisture == "WATERLOGGED":
        score += 2
        evidence.append("Genangan atau indikasi tanah tergenang.")
    if leaf_wilt:
        score += 2
        evidence.append("Daun tampak layu.")
    if moisture in {"VERY_DRY", "DRY"} or not surface_dark:
        score += 1
        evidence.append("Kelembapan rendah atau permukaan tanah tampak kering.")
    if not evidence:
        evidence.append("Tidak ada indikator risiko dari isian manual.")

    if score >= 3:
        condition, confidence = "PERLU_PERHATIAN", 0.75
    elif score:
        condition, confidence = "PANTAU", 0.60
    else:
        condition, confidence = "STABIL", 0.50
    return {
        "condition": condition,
        "confidence": confidence,
        "evidence": " ".join(evidence),
    }
