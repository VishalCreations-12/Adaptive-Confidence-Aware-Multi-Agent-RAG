import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs" / "screenshots"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

def capture_all_screenshots():
    print("Starting Playwright automation to capture real Streamlit application screenshots...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 1000})
        page = context.new_page()

        print("Navigating to http://localhost:8501...")
        page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(5)  # Wait for Streamlit initial mount

        # 01_dashboard.png
        page.screenshot(path=str(DOCS_DIR / "01_dashboard.png"))
        print("Captured 01_dashboard.png")

        # Click Load Sample PDF button if present
        try:
            sample_btn = page.get_by_role("button", name="Load Automatic Sample Knowledge Base")
            if sample_btn.is_visible():
                sample_btn.click()
                time.sleep(6)  # Wait for indexing
        except Exception as e:
            print("Sample load button click notice:", e)

        # 02_document_ingestion.png
        sidebar = page.locator("[data-testid='stSidebar']")
        if sidebar.is_visible():
            sidebar.screenshot(path=str(DOCS_DIR / "02_document_ingestion.png"))
        else:
            page.screenshot(path=str(DOCS_DIR / "02_document_ingestion.png"))
        print("Captured 02_document_ingestion.png")

        # Type research question into input box
        query_input = page.get_by_placeholder("e.g. What is the efficiency rating of the NovaSolar-X module?")
        if query_input.is_visible():
            query_input.fill("NovaSync v3.2 zero-trust encryption AES-256 throughput latency Proof-of-State")
            query_input.press("Enter")
            time.sleep(5)  # Wait for full pipeline execution

        # 03_query_analysis.png
        page.screenshot(path=str(DOCS_DIR / "03_query_analysis.png"))
        print("Captured 03_query_analysis.png")

        # 08_v2_strategy_selector.png (Scroll to V2 Selector)
        v2_card = page.locator("div.v2-box")
        if v2_card.is_visible():
            v2_card.screenshot(path=str(DOCS_DIR / "08_v2_strategy_selector.png"))
        else:
            page.screenshot(path=str(DOCS_DIR / "08_v2_strategy_selector.png"))
        print("Captured 08_v2_strategy_selector.png")

        # 04_retrieval_agents.png
        ret_section = page.get_by_text("Multi-Agent Retrieval Outputs")
        if ret_section.is_visible():
            ret_section.scroll_into_view_if_needed()
            time.sleep(1)
        page.screenshot(path=str(DOCS_DIR / "04_retrieval_agents.png"))
        print("Captured 04_retrieval_agents.png")

        # 05_evidence_judge.png
        judge_section = page.get_by_text("Evidence Judge Evaluation")
        if judge_section.is_visible():
            judge_section.scroll_into_view_if_needed()
            time.sleep(1)
        page.screenshot(path=str(DOCS_DIR / "05_evidence_judge.png"))
        print("Captured 05_evidence_judge.png")

        # 06_confidence.png
        conf_section = page.get_by_text("Evidence Confidence Score")
        if conf_section.is_visible():
            conf_section.scroll_into_view_if_needed()
            time.sleep(1)
        page.screenshot(path=str(DOCS_DIR / "06_confidence.png"))
        print("Captured 06_confidence.png")

        # 07_grounded_answer.png
        ans_section = page.get_by_text("Final Grounded Answer")
        if ans_section.is_visible():
            ans_section.scroll_into_view_if_needed()
            time.sleep(1)
        page.screenshot(path=str(DOCS_DIR / "07_grounded_answer.png"))
        print("Captured 07_grounded_answer.png")

        # Open Research Dashboard expander
        try:
            expander = page.get_by_text("RESEARCH DASHBOARD: Five-Way Baseline & Benchmark Results")
            if expander.is_visible():
                expander.click()
                time.sleep(3)
        except Exception as e:
            print("Expander click notice:", e)

        # 09_five_way_comparison.png
        dash_section = page.get_by_text("Five-Way Baseline Quantitative Comparison")
        if dash_section.is_visible():
            dash_section.scroll_into_view_if_needed()
            time.sleep(1)
        page.screenshot(path=str(DOCS_DIR / "09_five_way_comparison.png"))
        print("Captured 09_five_way_comparison.png")

        # 10_research_dashboard.png
        plot_section = page.get_by_text("Publication Research Plot Gallery")
        if plot_section.is_visible():
            plot_section.scroll_into_view_if_needed()
            time.sleep(2)
        page.screenshot(path=str(DOCS_DIR / "10_research_dashboard.png"))
        print("Captured 10_research_dashboard.png")

        browser.close()
        print("All 10 Playwright screenshots captured successfully.")

if __name__ == "__main__":
    capture_all_screenshots()
