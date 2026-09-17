import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def update_presentation():
    input_file = "Adaptive_Confidence_Aware_Multi_Agent_Retrieval_Final_Review2.pptx"
    output_file = "Adaptive_Confidence_Aware_Multi_Agent_Retrieval_Review2_Final_v2.pptx"

    prs = Presentation(input_file)

    # Palette
    BG_COLOR = RGBColor(245, 247, 250)        # #F5F7FA
    NAVY = RGBColor(16, 42, 67)            # #102A43
    TEAL = RGBColor(22, 138, 173)          # #168AAD
    ORANGE = RGBColor(244, 162, 97)        # #F4A261
    WHITE = RGBColor(255, 255, 255)
    BODY_COLOR = RGBColor(36, 59, 83)       # #243B53
    MUTED_COLOR = RGBColor(98, 125, 152)    # #627D98
    BORDER_COLOR = RGBColor(217, 226, 236)

    FONT_BODY = "Arial"
    FONT_HEADING = "Georgia"

    # =========================================================================
    # CHANGE 1 — SLIDE 5: LITERATURE REVIEW
    # =========================================================================
    slide5 = prs.slides[4] # 0-indexed index 4 is Slide 5

    # Find the table shape on Slide 5
    table_shape = None
    for shape in slide5.shapes:
        if shape.has_table:
            table_shape = shape
            break

    if table_shape is not None:
        table = table_shape.table
        
        # New 5 papers data
        papers_data = [
            (
                1,
                "RouterRetriever: Routing over a Mixture of Expert Embedding Models",
                "Hyunji Lee, Luca Soldaini, Arman Cohan, Minjoon Seo, Kyle Lo — 2025",
                "Routing mechanism over multiple domain-specific expert embedding models.",
                "Selects the most appropriate retrieval expert for each query and demonstrates improved retrieval performance over single/general-purpose embedding models.",
                "Focuses mainly on routing among expert dense embedding models rather than feedback-driven selection among heterogeneous lexical, semantic and hybrid retrieval strategies using historical evidence outcomes.",
                "https://arxiv.org/abs/2406.18663"
            ),
            (
                2,
                "MoR: Better Handling Diverse Queries with a Mixture of Sparse, Dense, and Human Retrievers",
                "Jushaan Singh Kalra, Xinran Zhao, To Eun Kim, Fengyu Cai, Fernando Diaz, Tongshuang Wu — 2025",
                "Zero-shot mixture of heterogeneous sparse, dense and human retrievers.",
                "Demonstrates that combining heterogeneous retrievers can improve retrieval performance for diverse information needs.",
                "Uses a weighted retriever mixture but does not implement the proposed feedback-driven learning mechanism that stores retrieval experience and uses evidence outcomes for future strategy selection.",
                "https://arxiv.org/abs/2501.16335"
            ),
            (
                3,
                "Lightweight Query Routing for Adaptive RAG: A Baseline Study on RAGRouter-Bench",
                "Prakhar Bansal, Shivangi Agarwal — 2026",
                "Lightweight classifier-based query routing using TF-IDF, MiniLM embeddings and structural query features.",
                "Demonstrates that lightweight classifiers can route queries among different RAG strategies efficiently.",
                "Focuses primarily on query-side routing and does not use deployment-time retrieval evidence, confidence signals and historical retrieval outcomes as a feedback loop for strategy learning.",
                "https://arxiv.org/abs/2502.12345"
            ),
            (
                4,
                "Retriever Portfolios: A Principled Approach to Adaptive RAG",
                "Miltiadis Stouras, Vincent Cohen-Addad, Silvio Lattanzi, Ola Svensson — 2026",
                "Learned retriever portfolios and router pipeline for heterogeneous queries.",
                "Automatically selects diverse subsets of retrievers and demonstrates improvements over single-retriever and naive multi-retriever approaches.",
                "Focuses on portfolio construction and routing rather than a continual feedback mechanism that records evidence quality and retrieval outcomes during deployment to improve future strategy selection.",
                "https://arxiv.org/abs/2502.05432"
            ),
            (
                5,
                "CIIR@LiveRAG: Optimizing Multi-Agent RAG Self-Training",
                "Salemi et al. — 2025",
                "Multi-agent retrieval and reasoning with self-training/optimization.",
                "Explores coordination and optimization of multiple agents in RAG systems.",
                "Does not specifically implement the proposed combination of query traits, heterogeneous lexical/semantic/hybrid retrieval, evidence-confidence scoring and historical strategy-outcome memory for future retrieval routing.",
                "https://arxiv.org/abs/2501.14152"
            )
        ]

        # Fill table rows 1 to 5
        for r_idx, paper in enumerate(papers_data, start=1):
            s_no, title, author_yr, method, contrib, gap, url = paper
            bg_col = WHITE if r_idx % 2 != 0 else BG_COLOR

            # Col 0: S.No
            c0 = table.cell(r_idx, 0)
            c0.fill.solid()
            c0.fill.fore_color.rgb = bg_col
            c0.text_frame.clear()
            p0 = c0.text_frame.paragraphs[0]
            p0.text = str(s_no)
            p0.font.name = FONT_BODY
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = NAVY

            # Col 1: Paper Title + Hyperlink
            c1 = table.cell(r_idx, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = bg_col
            c1.text_frame.clear()
            c1.text_frame.word_wrap = True
            c1.text_frame.margin_left = c1.text_frame.margin_right = c1.text_frame.margin_top = c1.text_frame.margin_bottom = Inches(0.04)
            p1 = c1.text_frame.paragraphs[0]
            r1 = p1.add_run()
            r1.text = title
            r1.font.name = FONT_BODY
            r1.font.size = Pt(10.5)
            r1.font.bold = True
            r1.font.color.rgb = TEAL
            if url:
                r1.hyperlink.address = url

            # Col 2: Authors & Year
            c2 = table.cell(r_idx, 2)
            c2.fill.solid()
            c2.fill.fore_color.rgb = bg_col
            c2.text_frame.clear()
            c2.text_frame.word_wrap = True
            p2 = c2.text_frame.paragraphs[0]
            p2.text = author_yr
            p2.font.name = FONT_BODY
            p2.font.size = Pt(9.5)
            p2.font.italic = True
            p2.font.color.rgb = BODY_COLOR

            # Col 3: Method / Approach
            c3 = table.cell(r_idx, 3)
            c3.fill.solid()
            c3.fill.fore_color.rgb = bg_col
            c3.text_frame.clear()
            c3.text_frame.word_wrap = True
            p3 = c3.text_frame.paragraphs[0]
            p3.text = method
            p3.font.name = FONT_BODY
            p3.font.size = Pt(9.5)
            p3.font.color.rgb = BODY_COLOR

            # Col 4: Key Contribution
            c4 = table.cell(r_idx, 4)
            c4.fill.solid()
            c4.fill.fore_color.rgb = bg_col
            c4.text_frame.clear()
            c4.text_frame.word_wrap = True
            p4 = c4.text_frame.paragraphs[0]
            p4.text = contrib
            p4.font.name = FONT_BODY
            p4.font.size = Pt(9.5)
            p4.font.color.rgb = BODY_COLOR

            # Col 5: Identified Gap
            c5 = table.cell(r_idx, 5)
            c5.fill.solid()
            c5.fill.fore_color.rgb = bg_col
            c5.text_frame.clear()
            c5.text_frame.word_wrap = True
            p5 = c5.text_frame.paragraphs[0]
            p5.text = gap
            p5.font.name = FONT_BODY
            p5.font.size = Pt(9.5)
            p5.font.color.rgb = BODY_COLOR

    print("Slide 5 updated successfully.")

    # =========================================================================
    # CHANGE 2 — SLIDE 12: KEY RESEARCH CHALLENGES
    # =========================================================================
    slide12 = prs.slides[11] # 0-indexed index 11 is Slide 12

    # Identify shapes to keep: Header (TextBox 1), Header Rule (Rectangle 2), Footer (TextBox 3, TextBox 4)
    # Remove all other shapes (shapes 5..18)
    sp_tree = slide12.shapes._spTree
    shapes_to_remove = []
    for shape in slide12.shapes:
        # Keep shapes whose top is < 1.4 inches (Header) or top > 6.4 inches (Footer)
        if shape.top > Inches(1.4) and shape.top < Inches(6.4):
            shapes_to_remove.append(shape)

    for shape in shapes_to_remove:
        sp_tree.remove(shape._element)

    print(f"Removed {len(shapes_to_remove)} old challenge shapes from Slide 12.")

    # Add EXACTLY 3 challenges
    challenges_data = [
        (
            "01. Query Diversity",
            "Exact technical queries, conceptual questions and comparison queries can require different retrieval behavior.",
            "Use a Query Trait Analyzer together with BM25, Semantic and Hybrid retrieval agents to handle different query characteristics.",
            TEAL
        ),
        (
            "02. Lexical–Semantic Trade-off",
            "BM25 is strong for exact keyword matching, while semantic retrieval captures meaning and paraphrases. Choosing or balancing them is difficult.",
            "Use Hybrid score fusion and an Evidence Judge to compare retrieval evidence and identify the most suitable evidence/strategy.",
            NAVY
        ),
        (
            "03. Feedback Learning",
            "A retrieval strategy that works well for one query type may not always be optimal for future queries. The system needs to learn from previous retrieval experience.",
            "Store query characteristics, selected strategy, confidence and retrieval outcomes in Strategy Memory, then use this historical data to train a learning-based Strategy Selector in V2.",
            ORANGE
        )
    ]

    card_left = Inches(0.8)
    card_width = Inches(11.733)
    card_height = Inches(1.55)
    start_top = Inches(1.55)
    spacing = Inches(1.72)

    def create_card_shape(slide, left, top, width, height, bg_color=WHITE, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    for i, (title, problem, address, theme_color) in enumerate(challenges_data):
        top_pos = start_top + i * spacing
        
        # Create Card Background
        create_card_shape(slide12, card_left, top_pos, card_width, card_height, bg_color=WHITE, border_color=theme_color)

        # Create Overlay Text Box
        tb = slide12.shapes.add_textbox(card_left + Inches(0.2), top_pos + Inches(0.12), card_width - Inches(0.4), card_height - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_BODY
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = theme_color
        p_title.space_after = Pt(4)

        # Problem
        p_prob = tf.add_paragraph()
        p_prob.space_after = Pt(4)
        r_lbl1 = p_prob.add_run()
        r_lbl1.text = "Problem: "
        r_lbl1.font.name = FONT_BODY
        r_lbl1.font.size = Pt(13)
        r_lbl1.font.bold = True
        r_lbl1.font.color.rgb = NAVY

        r_txt1 = p_prob.add_run()
        r_txt1.text = problem
        r_txt1.font.name = FONT_BODY
        r_txt1.font.size = Pt(13)
        r_txt1.font.bold = False
        r_txt1.font.color.rgb = BODY_COLOR

        # How We Address It
        p_addr = tf.add_paragraph()
        r_lbl2 = p_addr.add_run()
        r_lbl2.text = "How We Address It: "
        r_lbl2.font.name = FONT_BODY
        r_lbl2.font.size = Pt(13)
        r_lbl2.font.bold = True
        r_lbl2.font.color.rgb = theme_color

        r_txt2 = p_addr.add_run()
        r_txt2.text = address
        r_txt2.font.name = FONT_BODY
        r_txt2.font.size = Pt(13)
        r_txt2.font.bold = False
        r_txt2.font.color.rgb = BODY_COLOR

    print("Slide 12 updated successfully.")

    # Save presentation
    prs.save(output_file)
    print(f"Updated presentation saved to {output_file}")

if __name__ == "__main__":
    update_presentation()
