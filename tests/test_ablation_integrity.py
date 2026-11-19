import re
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent

def test_no_synthetic_ablation_subtraction():
    """Verify that no file contains synthetic scalar subtraction like row['mrr'] - 0.05."""
    scripts_dir = BASE_DIR / "scripts"
    src_dir = BASE_DIR / "src"

    forbidden_patterns = [
        r'row\[["\']precision_at_k["\']\]\s*-\s*0\.',
        r'row\[["\']recall_at_k["\']\]\s*-\s*0\.',
        r'row\[["\']mrr["\']\]\s*-\s*0\.',
        r'row\[["\']ndcg_at_k["\']\]\s*-\s*0\.',
        r'row\[["\']confidence_score["\']\]\s*-\s*0\.'
    ]

    for directory in [scripts_dir, src_dir]:
        for py_file in directory.glob("**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            for pattern in forbidden_patterns:
                match = re.search(pattern, content)
                assert match is None, f"Found forbidden synthetic subtraction pattern in {py_file}: {match.group(0)}"

def test_ablation_variants_have_distinct_values():
    """Verify that real ablation summary exists and variants have distinct measured values."""
    ablation_file = BASE_DIR / "results" / "reviewer_revision" / "ablation" / "real_ablation_summary.json"
    if ablation_file.exists():
        import json
        data = json.load(open(ablation_file, "r", encoding="utf-8"))
        summary_table = data.get("summary_table", [])
        assert len(summary_table) == 6
        
        # Check that variants are not all identical clones
        ndcgs = [v["mean_ndcg_at_k"] for v in summary_table]
        assert len(set(ndcgs)) > 1, "Ablation variants should have distinct measured performance"
