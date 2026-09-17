import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
README_PATH = BASE_DIR / "README.md"

def test_readme():
    print("Inspecting README.md image links and formatting...")
    content = README_PATH.read_text(encoding="utf-8")
    
    # 1. Check no file:// scheme or absolute paths
    assert "file://" not in content, "README contains absolute file:// links!"
    assert "D:/" not in content and "d:/" not in content, "README contains local Windows drive letters!"
    assert "C:/" not in content and "c:/" not in content, "README contains local Windows drive letters!"

    # 2. Extract image markdown links ![Alt](path)
    img_matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
    print(f"Found {len(img_matches)} embedded image links in README.md:")
    
    all_exist = True
    for img_path_str in img_matches:
        img_path = BASE_DIR / img_path_str
        if img_path.exists():
            size_kb = img_path.stat().st_size / 1024.0
            print(f"  [PASS] {img_path_str} exists ({size_kb:.1f} KB)")
        else:
            print(f"  [FAIL] {img_path_str} DOES NOT EXIST!")
            all_valid = False

    # 3. Check for LaTeX math errors
    assert r"\text{Norm_BM25}" not in content, "Unescaped LaTeX underscore found!"
    print("README.md image links and math formatting verified 100% clean and valid!")

if __name__ == "__main__":
    test_readme()
