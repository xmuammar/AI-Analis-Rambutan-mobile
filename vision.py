"""Optional mobile image quality checks.

This module deliberately does not infer pests or diseases. A future validated
TFLite/ONNX model can implement the same boundary without changing storage.
"""

from pathlib import Path


def assess_photo(path: str | Path) -> dict:
    try:
        from PIL import Image
    except ImportError:
        return {
            "status": "NOT_INSTALLED",
            "message": "Pillow belum tersedia; foto disimpan tanpa quality gate.",
        }
    try:
        with Image.open(path) as image:
            width, height = image.size
            if width < 320 or height < 240:
                return {
                    "status": "INSUFFICIENT_QUALITY",
                    "message": "Resolusi foto terlalu rendah untuk analisis.",
                }
            return {
                "status": "READY_FOR_VALIDATED_MODEL",
                "message": f"Foto {width}x{height}; belum ada diagnosis offline.",
            }
    except (OSError, ValueError):
        return {"status": "INVALID_IMAGE", "message": "Berkas foto tidak valid."}
