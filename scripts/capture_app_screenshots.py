import os
import time
import subprocess
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs" / "screenshots"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def capture_screenshot(out_filename: str, window_size: str = "1280,1024"):
    out_path = DOCS_DIR / out_filename
    cmd = [
        "powershell", "-Command",
        f"Start-Process -FilePath '{EDGE_PATH}' -ArgumentList '--headless', '--disable-gpu', '--window-size={window_size}', '--virtual-time-budget=8000', '--screenshot=\"{out_path}\"', 'http://localhost:8501' -Wait"
    ]
    subprocess.run(cmd, check=True)
    if out_path.exists():
        print(f"Captured {out_filename} ({out_path.stat().st_size} bytes)")
    else:
        print(f"Warning: Failed to capture {out_filename}")

def main():
    print("Capturing live application screenshots...")
    screenshots = [
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
    for shot in screenshots:
        capture_screenshot(shot)

    # Also copy plot graphics into docs/screenshots/ if available for presentation completeness
    plots_dir = BASE_DIR / "data" / "results" / "plots"
    plot_map = {
        "01_five_way_metrics_comparison.png": "fig_01_metrics.png",
        "02_latency_comparison.png": "fig_02_latency.png",
        "03_strategy_selection_distribution.png": "fig_03_strategy_dist.png",
        "04_sequential_learning_reward_curve.png": "fig_04_sequential_reward.png",
        "05_ablation_study_comparison.png": "fig_05_ablation.png"
    }
    for src, dst in plot_map.items():
        src_path = plots_dir / src
        dst_path = DOCS_DIR / dst
        if src_path.exists():
            img = Image.open(src_path)
            img.save(dst_path)
            print(f"Saved plot artifact {dst}")

if __name__ == "__main__":
    main()
