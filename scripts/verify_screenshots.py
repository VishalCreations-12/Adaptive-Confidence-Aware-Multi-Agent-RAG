import os
import numpy as np
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs" / "screenshots"

SCREENSHOTS = [
    "01_dashboard.png",
    "02_document_ingestion.png",
    "03_query_analysis.png",
    "04_retrieval_agents.png",
    "05_evidence_judge.png",
    "06_confidence.png",
    "07_grounded_answer.png",
    "08_v2_strategy_selector.png",
    "09_five_way_comparison.png",
    "10_research_dashboard.png"
]

def verify_all_images():
    print("Programmatically inspecting screenshot content and pixel variance...")
    all_valid = True

    for filename in SCREENSHOTS:
        filepath = DOCS_DIR / filename
        if not filepath.exists():
            print(f"❌ FAIL: {filename} does not exist.")
            all_valid = False
            continue

        size_kb = filepath.stat().st_size / 1024.0
        if size_kb < 15.0:
            print(f"[FAIL]: {filename} size too small ({size_kb:.1f} KB).")
            all_valid = False
            continue

        try:
            img = Image.open(filepath)
            width, height = img.size
            img_arr = np.array(img.convert("L"))
            pixel_std = float(np.std(img_arr))

            if pixel_std < 5.0:
                print(f"[FAIL]: {filename} appears blank or uniform color (std = {pixel_std:.2f}).")
                all_valid = False
            else:
                print(f"[PASS]: {filename} | Dimensions: {width}x{height} | Size: {size_kb:.1f} KB | Pixel std: {pixel_std:.2f}")

        except Exception as e:
            print(f"[FAIL]: {filename} error opening image: {e}")
            all_valid = False

    if all_valid:
        print("\nALL 10 SCREENSHOTS VERIFIED NON-BLANK, VALID AND CONTENT-RICH!")
    else:
        print("\nSOME SCREENSHOTS FAILED VALIDATION.")


if __name__ == "__main__":
    verify_all_images()
