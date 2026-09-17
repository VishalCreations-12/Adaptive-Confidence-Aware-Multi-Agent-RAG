import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs" / "screenshots"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

def capture_targeted_screenshots():
    print("Executing Playwright targeted capture sequence for 10 distinct UI sections...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 900}, device_scale_factor=1.5)
        page = context.new_page()

        page.goto("http://localhost:8501", wait_until="networkidle")
        page.wait_for_timeout(4000)

        # 01_dashboard.png - Main Header & Top Interface
        header = page.locator("div.main-header")
        if header.is_visible():
            header.screenshot(path=str(DOCS_DIR / "01_dashboard.png"))
        else:
            page.screenshot(path=str(DOCS_DIR / "01_dashboard.png"))
        print("Captured 01_dashboard.png")

        # Load Sample Knowledge Base
        try:
            sample_btn = page.get_by_text("Load Automatic Sample Knowledge Base")
            if sample_btn.is_visible():
                sample_btn.click()
                page.wait_for_timeout(7000)
        except Exception as e:
            print("Notice:", e)

        # 02_document_ingestion.png - Sidebar Ingestion Status
        sidebar = page.locator("[data-testid='stSidebar']")
        if sidebar.is_visible():
            sidebar.screenshot(path=str(DOCS_DIR / "02_document_ingestion.png"))
        else:
            page.screenshot(path=str(DOCS_DIR / "02_document_ingestion.png"))
        print("Captured 02_document_ingestion.png")

        # Type research question
        query_input = page.get_by_placeholder("e.g. What is the efficiency rating of the NovaSolar-X module?")
        if query_input.is_visible():
            query_input.fill("NovaSync v3.2 zero-trust encryption AES-256 throughput latency Proof-of-State")
            query_input.press("Enter")
            page.wait_for_timeout(6000)

        # 03_query_analysis.png - Query Analysis Section
        q_section = page.get_by_text("Query Analysis & Traits")
        if q_section.is_visible():
            q_section.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
        page.screenshot(path=str(DOCS_DIR / "03_query_analysis.png"))
        print("Captured 03_query_analysis.png")

        # 08_v2_strategy_selector.png - V2 Selector Box
        v2_box = page.locator("div.v2-box")
        if v2_box.is_visible():
            v2_box.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            v2_box.screenshot(path=str(DOCS_DIR / "08_v2_strategy_selector.png"))
        else:
            page.screenshot(path=str(DOCS_DIR / "08_v2_strategy_selector.png"))
        print("Captured 08_v2_strategy_selector.png")

        # 04_retrieval_agents.png - Multi-Agent Outputs Section
        ret_section = page.get_by_text("Multi-Agent Retrieval Outputs")
        if ret_section.is_visible():
            ret_section.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
        page.screenshot(path=str(DOCS_DIR / "04_retrieval_agents.png"))
        print("Captured 04_retrieval_agents.png")

        # 05_evidence_judge.png - Evidence Judge Evaluation Section
        judge_section = page.get_by_text("Evidence Judge Evaluation")
        if judge_section.is_visible():
            judge_section.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
        page.screenshot(path=str(DOCS_DIR / "05_evidence_judge.png"))
        print("Captured 05_evidence_judge.png")

        # 06_confidence.png - Confidence Meter
        conf_meter = page.locator("div.confidence-meter")
        if conf_meter.is_visible():
            conf_meter.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            conf_meter.screenshot(path=str(DOCS_DIR / "06_confidence.png"))
        else:
            page.screenshot(path=str(DOCS_DIR / "06_confidence.png"))
        print("Captured 06_confidence.png")

        # 07_grounded_answer.png - Grounded Answer Section
        ans_heading = page.get_by_text("Final Grounded Answer")
        if ans_heading.is_visible():
            ans_heading.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
        page.screenshot(path=str(DOCS_DIR / "07_grounded_answer.png"))
        print("Captured 07_grounded_answer.png")

        # Open Research Dashboard expander
        try:
            expander = page.get_by_text("RESEARCH DASHBOARD: Five-Way Baseline & Benchmark Results")
            if expander.is_visible():
                expander.click()
                page.wait_for_timeout(3000)
        except Exception as e:
            print("Notice:", e)

        # 09_five_way_comparison.png - Dataframe Table Section
        df_elem = page.locator("[data-testid='stDataFrame']")
        if df_elem.is_visible():
            df_elem.scroll_into_view_if_needed()
            page.wait_for_timeout(1000)
            df_elem.screenshot(path=str(DOCS_DIR / "09_five_way_comparison.png"))
        else:
            page.screenshot(path=str(DOCS_DIR / "09_five_way_comparison.png"))
        print("Captured 09_five_way_comparison.png")

        # 10_research_dashboard.png - Plot Gallery Section
        plot_heading = page.get_by_text("Publication Research Plot Gallery")
        if plot_heading.is_visible():
            plot_heading.scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
        page.screenshot(path=str(DOCS_DIR / "10_research_dashboard.png"))
        print("Captured 10_research_dashboard.png")

        browser.close()
        print("Targeted Playwright capture completed successfully.")

if __name__ == "__main__":
    capture_targeted_screenshots()
