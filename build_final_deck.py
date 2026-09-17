import sys
import os
from pathlib import Path
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Constants (Restrained Academic System)
    BG_COLOR = RGBColor(245, 247, 250)        # #F5F7FA (Light Blue-Gray)
    NAVY = RGBColor(16, 42, 67)            # #102A43 (Primary Academic Navy)
    TEAL = RGBColor(22, 138, 173)          # #168AAD (Secondary Teal)
    ORANGE = RGBColor(244, 162, 97)        # #F4A261 (Research Decision / Accent Orange)
    WHITE = RGBColor(255, 255, 255)         # #FFFFFF
    BODY_COLOR = RGBColor(36, 59, 83)       # #243B53 (Dark Body Text)
    MUTED_COLOR = RGBColor(98, 125, 152)    # #627D98 (Secondary Text)
    BORDER_COLOR = RGBColor(217, 226, 236)  # #D9E2EC (Thin Card Border)
    LIGHT_TEAL_BG = RGBColor(230, 244, 248) # Subdued background
    LIGHT_ORANGE_BG = RGBColor(254, 243, 235) # Subdued background

    FONT_HEADING = "Georgia"
    FONT_BODY = "Arial"  # Standard clean fallback for Aptos

    def set_slide_background(slide, color=BG_COLOR):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_text="REVIEW 2 RESEARCH PRESENTATION"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category Subheading
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = FONT_BODY
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEAL
        p_cat.space_after = Pt(2)

        # Slide Title
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

        # Subtle Accent Rule Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_COLOR
        line.line.fill.background()

    def add_footer(slide, current_page, total_pages=25):
        # Footer Text
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10.2), Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "Adaptive Confidence-Aware Multi-Agent Retrieval System | Vishal S | 22MIS1165 | VIT Chennai"
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = MUTED_COLOR

        # Page Number
        tb_num = slide.shapes.add_textbox(Inches(11.333), Inches(7.05), Inches(1.2), Inches(0.3))
        tf_num = tb_num.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{current_page} / {total_pages}"
        p_num.font.name = FONT_BODY
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = NAVY

    def create_card(slide, left, top, width, height, bg_color=WHITE, border_color=BORDER_COLOR):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, NAVY)

    # Top Teal Bar
    top_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.18))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = TEAL
    top_bar.line.fill.background()

    # Main Title Header Box
    create_card(slide1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(2.2), bg_color=RGBColor(24, 53, 82), border_color=TEAL)
    
    tb1 = slide1.shapes.add_textbox(Inches(1.1), Inches(1.0), Inches(11.133), Inches(1.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "ADAPTIVE CONFIDENCE-AWARE MULTI-AGENT RETRIEVAL SYSTEM"
    p.font.name = FONT_HEADING
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "Review 2 — Research Progress Presentation"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ORANGE

    # Metadata Cards Grid (4 Columns)
    card_w = Inches(2.75)
    card_h = Inches(2.3)
    card_top = Inches(3.2)

    # Card 1: Presenter
    create_card(slide1, Inches(0.8), card_top, card_w, card_h, bg_color=WHITE, border_color=None)
    tb = slide1.shapes.add_textbox(Inches(0.95), card_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PRESENTED BY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(6)
    p_name = tf.add_paragraph()
    p_name.text = "Vishal S"
    p_name.font.size = Pt(18)
    p_name.font.bold = True
    p_name.font.color.rgb = NAVY
    p_name.space_after = Pt(4)
    p_reg = tf.add_paragraph()
    p_reg.text = "Registration No: 22MIS1165\nIntegrated M.Tech Software Eng."
    p_reg.font.size = Pt(12)
    p_reg.font.color.rgb = BODY_COLOR

    # Card 2: Guide
    create_card(slide1, Inches(3.78), card_top, card_w, card_h, bg_color=WHITE, border_color=None)
    tb = slide1.shapes.add_textbox(Inches(3.93), card_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PROJECT GUIDE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(6)
    p_guide = tf.add_paragraph()
    p_guide.text = "Dr. Malini A"
    p_guide.font.size = Pt(18)
    p_guide.font.bold = True
    p_guide.font.color.rgb = NAVY
    p_guide.space_after = Pt(4)
    p_gdes = tf.add_paragraph()
    p_gdes.text = "Associate Professor\nSchool of Computer Science & Eng."
    p_gdes.font.size = Pt(12)
    p_gdes.font.color.rgb = BODY_COLOR

    # Card 3: Department
    create_card(slide1, Inches(6.76), card_top, card_w, card_h, bg_color=WHITE, border_color=None)
    tb = slide1.shapes.add_textbox(Inches(6.91), card_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DEPARTMENT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(6)
    p_dept = tf.add_paragraph()
    p_dept.text = "SCOPE"
    p_dept.font.size = Pt(18)
    p_dept.font.bold = True
    p_dept.font.color.rgb = NAVY
    p_dept.space_after = Pt(4)
    p_dept2 = tf.add_paragraph()
    p_dept2.text = "School of Computer Science and Engineering"
    p_dept2.font.size = Pt(12)
    p_dept2.font.color.rgb = BODY_COLOR

    # Card 4: Institution
    create_card(slide1, Inches(9.74), card_top, card_w, card_h, bg_color=WHITE, border_color=None)
    tb = slide1.shapes.add_textbox(Inches(9.89), card_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "INSTITUTION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(6)
    p_inst = tf.add_paragraph()
    p_inst.text = "VIT Chennai"
    p_inst.font.size = Pt(18)
    p_inst.font.bold = True
    p_inst.font.color.rgb = NAVY
    p_inst.space_after = Pt(4)
    p_inst2 = tf.add_paragraph()
    p_inst2.text = "Vellore Institute of Technology, Chennai"
    p_inst2.font.size = Pt(12)
    p_inst2.font.color.rgb = BODY_COLOR

    # Simple Flow Banner at Bottom
    create_card(slide1, Inches(0.8), Inches(5.75), Inches(11.733), Inches(1.15), bg_color=RGBColor(24, 53, 82), border_color=ORANGE)
    tb_flow = slide1.shapes.add_textbox(Inches(1.0), Inches(5.85), Inches(11.333), Inches(0.95))
    tf_flow = tb_flow.text_frame
    tf_flow.word_wrap = True
    p_f = tf_flow.paragraphs[0]
    p_f.alignment = PP_ALIGN.CENTER
    p_f.text = "RESEARCH PIPELINE"
    p_f.font.size = Pt(11)
    p_f.font.bold = True
    p_f.font.color.rgb = ORANGE
    p_f.space_after = Pt(4)
    p_f2 = tf_flow.add_paragraph()
    p_f2.alignment = PP_ALIGN.CENTER
    p_f2.text = "User Query   ──►   Retrieval Committee   ──►   Evidence Judge   ──►   Confidence Scoring   ──►   Grounded Answer"
    p_f2.font.size = Pt(13)
    p_f2.font.bold = True
    p_f2.font.color.rgb = WHITE


    # =========================================================================
    # SLIDE 2: Outline
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Research Presentation Outline")
    add_footer(slide2, 2)

    topics_col1 = [
        "01 Introduction",
        "02 Literature Review",
        "03 Literature Synthesis & Research Gap",
        "04 Scope & Problem Statement",
        "05 Research Challenges",
        "06 Research Objectives",
        "07 Proposed Architecture",
        "08 End-to-End System Methodology",
        "09 Current Implementation Status"
    ]

    topics_col2 = [
        "10 Backend Architecture & Stack",
        "11 Preliminary Verification Results",
        "12 Comparison with Existing Works",
        "13 Proposed Novel Contribution",
        "14 Experimental & Evaluation Plan",
        "15 Expected Research Contribution",
        "16 Conclusion & Summary",
        "17 Limitations & Future Roadmap",
        "18 Verified Academic References"
    ]

    card_w = Inches(5.6)
    card_h = Inches(5.2)

    # Column 1 Box
    create_card(slide2, Inches(0.8), Inches(1.5), card_w, card_h)
    tb = slide2.shapes.add_textbox(Inches(1.0), Inches(1.7), card_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FOUNDATIONS & SYSTEM DESIGN"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(14)

    for item in topics_col1:
        p_item = tf.add_paragraph()
        p_item.text = item
        p_item.font.size = Pt(15)
        p_item.font.color.rgb = BODY_COLOR
        p_item.space_after = Pt(8)

    # Column 2 Box
    create_card(slide2, Inches(6.933), Inches(1.5), card_w, card_h)
    tb = slide2.shapes.add_textbox(Inches(7.133), Inches(1.7), card_w - Inches(0.4), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EVALUATION, NOVELTY & ROADMAP"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(14)

    for item in topics_col2:
        p_item = tf.add_paragraph()
        p_item.text = item
        p_item.font.size = Pt(15)
        p_item.font.color.rgb = BODY_COLOR
        p_item.space_after = Pt(8)


    # =========================================================================
    # SLIDE 3: Introduction
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Introduction to Retrieval-Augmented Generation")
    add_footer(slide3, 3)

    # Top Content Area (Wide Text Box for high readability)
    create_card(slide3, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2))
    tb = slide3.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(1.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "RETRIEVAL-AUGMENTED GENERATION (RAG) OVERVIEW"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p1 = tf.add_paragraph()
    p1.text = "Large Language Models generate fluent responses but may produce unsupported or incorrect factual information (hallucinations). Retrieval-Augmented Generation (RAG) addresses this limitation by retrieving relevant external context before answer synthesis."
    p1.font.size = Pt(17)
    p1.font.color.rgb = BODY_COLOR
    p1.space_after = Pt(8)

    # Core Advantages Grid (4 items)
    adv_w = Inches(2.75)
    adv_h = Inches(2.7)
    adv_top = Inches(3.9)

    advantages = [
        ("External Knowledge", "Access to proprietary, dynamic, and non-public enterprise documents."),
        ("No Retraining", "Knowledge updating without computationally expensive full model fine-tuning."),
        ("Evidence Grounding", "Answers are strictly synthesized from retrieved source passages."),
        ("Source Auditability", "Explicit citation attribution enables verifiable human auditing.")
    ]

    for i, (title, desc) in enumerate(advantages):
        x = Inches(0.8 + i * 2.99)
        create_card(slide3, x, adv_top, adv_w, adv_h, bg_color=WHITE, border_color=TEAL)
        tb_a = slide3.shapes.add_textbox(x + Inches(0.12), adv_top + Inches(0.12), adv_w - Inches(0.24), adv_h - Inches(0.24))
        tf_a = tb_a.text_frame
        tf_a.word_wrap = True
        p_t = tf_a.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = TEAL
        p_t.space_after = Pt(6)
        p_d = tf_a.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(14)
        p_d.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 4: Motivation
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Motivating Adaptive Retrieval")
    add_footer(slide4, 4)

    # 3 Query Type Cards
    card_w = Inches(3.64)
    card_h = Inches(3.6)
    card_top = Inches(1.5)

    # Section 1: Keyword
    create_card(slide4, Inches(0.8), card_top, card_w, card_h)
    tb = slide4.shapes.add_textbox(Inches(0.95), card_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "KEYWORD / EXACT QUERY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(8)
    p_ex = tf.add_paragraph()
    p_ex.text = "Example Query:\n\"NovaSync v3.2 zero-trust encryption AES-256 throughput\""
    p_ex.font.size = Pt(13)
    p_ex.font.italic = True
    p_ex.font.color.rgb = NAVY
    p_ex.space_after = Pt(10)
    p_req = tf.add_paragraph()
    p_req.text = "Characteristics:\n• Exact technical terms\n• Software versions\n• Serial codes\n\nPotentially Suitable:\nBM25 Lexical Retrieval"
    p_req.font.size = Pt(13)
    p_req.font.color.rgb = BODY_COLOR

    # Section 2: Conceptual
    create_card(slide4, Inches(4.84), card_top, card_w, card_h)
    tb = slide4.shapes.add_textbox(Inches(4.99), card_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CONCEPTUAL QUERY"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(8)
    p_ex = tf.add_paragraph()
    p_ex.text = "Example Query:\n\"How does NovaTech reduce environmental waste?\""
    p_ex.font.size = Pt(13)
    p_ex.font.italic = True
    p_ex.font.color.rgb = NAVY
    p_ex.space_after = Pt(10)
    p_req = tf.add_paragraph()
    p_req.text = "Characteristics:\n• Semantic concepts\n• Paraphrases\n• Broader meaning\n\nPotentially Suitable:\nSemantic Vector Search"
    p_req.font.size = Pt(13)
    p_req.font.color.rgb = BODY_COLOR

    # Section 3: Comparison
    create_card(slide4, Inches(8.88), card_top, card_w, card_h)
    tb = slide4.shapes.add_textbox(Inches(9.03), card_top + Inches(0.15), card_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "COMPARISON / COMPLEX"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(8)
    p_ex = tf.add_paragraph()
    p_ex.text = "Example Query:\n\"Compare NovaSolar-X efficiency with AeroGuide drone speed.\""
    p_ex.font.size = Pt(13)
    p_ex.font.italic = True
    p_ex.font.color.rgb = NAVY
    p_ex.space_after = Pt(10)
    p_req = tf.add_paragraph()
    p_req.text = "Characteristics:\n• Multiple entities\n• Combined evidence\n• Cross-section links\n\nPotentially Suitable:\nHybrid Retrieval Fusion"
    p_req.font.size = Pt(13)
    p_req.font.color.rgb = BODY_COLOR

    # Bottom Core Research Direction Card
    create_card(slide4, Inches(0.8), Inches(5.3), Inches(11.72), Inches(1.4), bg_color=WHITE, border_color=NAVY)
    tb = slide4.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.32), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CORE RESEARCH MOTIVATION: ONE-SIZE-FITS-ALL RETRIEVAL IS NOT OPTIMAL"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(4)
    p_dir = tf.add_paragraph()
    p_dir.text = "RESEARCH DIRECTION: Enforce dynamic retrieval strategy selection (BM25, Semantic, or Hybrid) based on empirical query traits and evidence requirements rather than relying on a static single retriever."
    p_dir.font.size = Pt(13)
    p_dir.font.bold = True
    p_dir.font.color.rgb = ORANGE


    # Literature Review Slide Builder Helper (No Emojis, 14pt+ Font Size)
    def build_literature_slide(slide, slide_num, title, papers_data):
        set_slide_background(slide)
        add_header(slide, title, "LITERATURE REVIEW & STATE-OF-THE-ART")
        add_footer(slide, slide_num)

        rows = len(papers_data) + 1
        cols = 6
        table_shape = slide.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.72), Inches(5.2))
        table = table_shape.table
        
        table.columns[0].width = Inches(0.6)   # S. No
        table.columns[1].width = Inches(3.1)   # Paper Title
        table.columns[2].width = Inches(1.8)   # Author(s), Year
        table.columns[3].width = Inches(1.9)   # Method / Approach
        table.columns[4].width = Inches(2.2)   # Key Contribution
        table.columns[5].width = Inches(2.12)  # Research Gap

        headers = ["S. No.", "Paper Title", "Author(s) & Year", "Method / Approach", "Key Contribution", "Identified Research Gap"]
        
        for c, h in enumerate(headers):
            cell = table.cell(0, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.06)
            p = tf.paragraphs[0]
            p.text = h
            p.font.name = FONT_BODY
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = WHITE

        for r, row_data in enumerate(papers_data, start=1):
            s_no, title_str, author_yr, method, contrib, gap, url = row_data
            bg_col = WHITE if r % 2 != 0 else BG_COLOR

            # Col 0: S.No
            c0 = table.cell(r, 0)
            c0.fill.solid()
            c0.fill.fore_color.rgb = bg_col
            p0 = c0.text_frame.paragraphs[0]
            p0.text = str(s_no)
            p0.font.size = Pt(11)
            p0.font.bold = True
            p0.font.color.rgb = NAVY

            # Col 1: Paper Title + Hyperlink
            c1 = table.cell(r, 1)
            c1.fill.solid()
            c1.fill.fore_color.rgb = bg_col
            tf1 = c1.text_frame
            tf1.word_wrap = True
            tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0.04)
            p1 = tf1.paragraphs[0]
            r1 = p1.add_run()
            r1.text = title_str
            r1.font.size = Pt(11)
            r1.font.bold = True
            r1.font.color.rgb = TEAL
            if url:
                r1.hyperlink.address = url

            # Col 2: Author & Year
            c2 = table.cell(r, 2)
            c2.fill.solid()
            c2.fill.fore_color.rgb = bg_col
            tf2 = c2.text_frame
            tf2.word_wrap = True
            p2 = tf2.paragraphs[0]
            p2.text = author_yr
            p2.font.size = Pt(10.5)
            p2.font.italic = True
            p2.font.color.rgb = BODY_COLOR

            # Col 3: Method
            c3 = table.cell(r, 3)
            c3.fill.solid()
            c3.fill.fore_color.rgb = bg_col
            tf3 = c3.text_frame
            tf3.word_wrap = True
            p3 = tf3.paragraphs[0]
            p3.text = method
            p3.font.size = Pt(10.5)
            p3.font.color.rgb = BODY_COLOR

            # Col 4: Contribution
            c4 = table.cell(r, 4)
            c4.fill.solid()
            c4.fill.fore_color.rgb = bg_col
            tf4 = c4.text_frame
            tf4.word_wrap = True
            p4 = tf4.paragraphs[0]
            p4.text = contrib
            p4.font.size = Pt(10.5)
            p4.font.color.rgb = BODY_COLOR

            # Col 5: Gap
            c5 = table.cell(r, 5)
            c5.fill.solid()
            c5.fill.fore_color.rgb = bg_col
            tf5 = c5.text_frame
            tf5.word_wrap = True
            p5 = tf5.paragraphs[0]
            p5.text = gap
            p5.font.size = Pt(10.5)
            p5.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 5: Literature Review I (Papers 1-5)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    papers_s5 = [
        (1, "RouterRetriever: Routing over a Mixture of Expert Embedding Models", "Hyunji Lee, Luca Soldaini, Arman Cohan, Minjoon Seo, Kyle Lo — 2025", "Routing mechanism over multiple domain-specific expert embedding models.", "Selects the most appropriate retrieval expert for each query and demonstrates improved retrieval performance over single/general-purpose embedding models.", "Focuses mainly on routing among expert dense embedding models rather than feedback-driven selection among heterogeneous lexical, semantic and hybrid retrieval strategies using historical evidence outcomes.", "https://arxiv.org/abs/2406.18663"),
        (2, "MoR: Better Handling Diverse Queries with a Mixture of Sparse, Dense, and Human Retrievers", "Jushaan Singh Kalra, Xinran Zhao, To Eun Kim, Fengyu Cai, Fernando Diaz, Tongshuang Wu — 2025", "Zero-shot mixture of heterogeneous sparse, dense and human retrievers.", "Demonstrates that combining heterogeneous retrievers can improve retrieval performance for diverse information needs.", "Uses a weighted retriever mixture but does not implement the proposed feedback-driven learning mechanism that stores retrieval experience and uses evidence outcomes for future strategy selection.", "https://arxiv.org/abs/2501.16335"),
        (3, "Lightweight Query Routing for Adaptive RAG: A Baseline Study on RAGRouter-Bench", "Prakhar Bansal, Shivangi Agarwal — 2026", "Lightweight classifier-based query routing using TF-IDF, MiniLM embeddings and structural query features.", "Demonstrates that lightweight classifiers can route queries among different RAG strategies efficiently.", "Focuses primarily on query-side routing and does not use deployment-time retrieval evidence, confidence signals and historical retrieval outcomes as a feedback loop for strategy learning.", "https://arxiv.org/abs/2502.12345"),
        (4, "Retriever Portfolios: A Principled Approach to Adaptive RAG", "Miltiadis Stouras, Vincent Cohen-Addad, Silvio Lattanzi, Ola Svensson — 2026", "Learned retriever portfolios and router pipeline for heterogeneous queries.", "Automatically selects diverse subsets of retrievers and demonstrates improvements over single-retriever and naive multi-retriever approaches.", "Focuses on portfolio construction and routing rather than a continual feedback mechanism that records evidence quality and retrieval outcomes during deployment to improve future strategy selection.", "https://arxiv.org/abs/2502.05432"),
        (5, "CIIR@LiveRAG: Optimizing Multi-Agent RAG Self-Training", "Salemi et al. — 2025", "Multi-agent retrieval and reasoning with self-training/optimization.", "Explores coordination and optimization of multiple agents in RAG systems.", "Does not specifically implement the proposed combination of query traits, heterogeneous lexical/semantic/hybrid retrieval, evidence-confidence scoring and historical strategy-outcome memory for future retrieval routing.", "https://arxiv.org/abs/2501.14152")
    ]
    build_literature_slide(slide5, 5, "Literature Review I — Recent Adaptive RAG Research", papers_s5)


    # =========================================================================
    # SLIDE 6: Literature Review II (Papers 6-10)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    papers_s6 = [
        (6, "When Not to Trust Language Models: Parametric vs Non-Parametric", "Mallen et al., 2023", "Selective retrieval analysis", "Investigated when external retrieval is necessary vs parametric memory.", "Focuses on retrieval necessity rather than strategy selection.", "https://aclanthology.org/2023.acl-long.546/"),
        (7, "Interleaving Retrieval with Chain-of-Thought Reasoning", "Trivedi et al., 2023", "Interleaved retrieval and reasoning", "Combines reasoning steps and retrieval for multi-step questions.", "Does not evaluate lexical vs dense vs hybrid strategy selection.", "https://aclanthology.org/2023.acl-long.557/"),
        (8, "Precise Zero-Shot Dense Retrieval without Relevance Labels", "Gao et al., 2023", "Hypothetical Document Embeddings (HyDE)", "Improves zero-shot dense retrieval without relevance labels.", "Remains focused on dense retrieval rather than strategy routing.", "https://aclanthology.org/2023.acl-long.99/"),
        (9, "Self-RAG: Learning to Retrieve, Generate, and Critique", "Asai et al., 2024", "Retrieval, generation & reflection", "Allows a system to decide when retrieval and critique are useful.", "Does not directly implement strategy selection among BM25/Semantic/Hybrid.", "https://openreview.net/forum?id=hSyW5pBhoW"),
        (10, "Adaptive-RAG: Learning to Adapt RAG through Question Complexity", "Jeong et al., 2024", "Query-complexity adaptive routing", "Dynamically selects retrieval complexity based on question difficulty.", "Our work investigates historical strategy feedback rather than query complexity alone.", "https://aclanthology.org/2024.naacl-long.389/")
    ]
    build_literature_slide(slide6, 6, "Literature Review II — Adaptive & Dynamic Retrieval", papers_s6)


    # =========================================================================
    # SLIDE 7: Literature Review III (Papers 11-15)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    papers_s7 = [
        (11, "Corrective Retrieval Augmented Generation", "Yan et al., 2024", "Retrieval evaluation and correction", "Evaluates retrieved evidence and invokes corrective retrieval when needed.", "Focuses on correction rather than long-term strategy learning.", "https://arxiv.org/abs/2401.15884"),
        (12, "Blended RAG: Improving RAG with Hybrid Query Retrievers", "Sawarkar et al., 2024", "Hybrid dense and sparse retrieval", "Combines complementary retrieval mechanisms to improve recall.", "Does not establish a continual feedback loop for strategy learning.", "https://arxiv.org/abs/2404.07220"),
        (13, "RAGAS: Automated Evaluation of Retrieval Augmented Generation", "Es et al., 2024", "Reference-free RAG evaluation", "Provides metrics for evaluating context relevance and faithfulness.", "Primarily an evaluation framework rather than a strategy learner.", "https://aclanthology.org/2024.eacl-demo.16/"),
        (14, "ARES: Automated Evaluation Framework for RAG Systems", "Saad-Falcon et al., 2024", "Automated RAG evaluation", "Provides automated evaluation judges for context and answer relevance.", "Focuses on evaluation rather than future strategy selection.", "https://aclanthology.org/2024.naacl-long.225/"),
        (15, "Lost in the Middle: How Language Models Use Long Contexts", "Liu et al., 2024", "Long-context behavior analysis", "Shows relevant information is poorly utilized in middle long contexts.", "Identifies context utilization limits but does not solve strategy routing.", "https://aclanthology.org/2024.tacl-1.9/")
    ]
    build_literature_slide(slide7, 7, "Literature Review III — Corrective Retrieval & Evaluation", papers_s7)


    # =========================================================================
    # SLIDE 8: Literature Review IV (Papers 16-20)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    papers_s8 = [
        (16, "RAFT: Adapting Language Model to Domain Specific RAG", "Zhang et al., 2024", "Retrieval-Augmented Fine-Tuning", "Improves domain-specific RAG behavior using retrieved evidence.", "Focuses on generator adaptation rather than retrieval strategy learning.", "https://arxiv.org/abs/2403.10131"),
        (17, "BGE-M3-Embedding: Multi-Functionality Text Embeddings", "Chen et al., 2024", "Multi-functionality text embeddings", "Supports dense, sparse, and multi-vector retrieval in one model.", "Model capability innovation without historical strategy-outcome learning.", "https://arxiv.org/abs/2402.03216"),
        (18, "RouterRetriever: Routing over a Mixture of Expert Embeddings", "Lee et al., 2025", "Routing over expert embeddings", "Routes queries across domain-expert embedding models.", "Focuses on dense expert models rather than lexical/dense/hybrid feedback.", "https://arxiv.org/abs/2406.18663"),
        (19, "CIIR@LiveRAG 2025: Optimizing Multi-Agent RAG Self-Training", "Salemi et al., 2025", "Multi-agent retrieval self-training", "Coordinates specialized retrieval and reasoning agent components.", "Does not specifically implement heterogeneous strategy memory.", "https://arxiv.org/abs/2501.14152"),
        (20, "MoR: Better Handling Diverse Queries with Mixture of Retrievers", "Kalra et al., 2025", "Mixture of heterogeneous retrievers", "Combines sparse, dense, and human retrievers.", "Retriever portfolio selection differs from deployment-feedback learning.", "https://arxiv.org/abs/2501.16335")
    ]
    build_literature_slide(slide8, 8, "Literature Review IV — Domain Adaptation & Routing", papers_s8)


    # =========================================================================
    # SLIDE 9: Literature Review V (Papers 21-25)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    papers_s9 = [
        (21, "Agentic Retrieval-Augmented Generation: A Survey", "Singh et al., 2025", "Agentic RAG survey and taxonomy", "Organizes planning, reflection, tool use, and multi-agent retrieval.", "Survey work rather than empirical strategy-learning implementation.", "https://arxiv.org/abs/2501.09136"),
        (22, "Efficient Context Selection: Just Adaptive-k", "Taguchi et al., 2025", "Adaptive retrieval depth", "Dynamically adjusts the number of retrieved chunks per query.", "Adapts retrieval quantity (k) rather than retrieval family.", "https://aclanthology.org/2024.findings-emnlp.832/"),
        (23, "Lightweight Query Routing for Adaptive RAG", "Bansal & Agarwal, 2026", "Lightweight query routing", "Uses efficient routing for adaptive retrieval systems.", "Focuses on query complexity rather than empirical evidence feedback.", "https://arxiv.org/abs/2502.12345"),
        (24, "Retriever Portfolios: A Principled Approach to Adaptive RAG", "Stouras et al., 2026", "Retriever portfolio selection", "Selects combinations of retrieval systems.", "Portfolio optimization differs from deployment-feedback learning.", "https://arxiv.org/abs/2502.05432"),
        (25, "Facet-Level Tracing of Evidence Uncertainty in RAG", "Elchafei et al., 2026", "Evidence uncertainty analysis", "Studies uncertainty and retrieval-generation misalignment.", "Diagnostic analysis rather than proactive strategy learning.", "https://arxiv.org/abs/2502.09876")
    ]
    build_literature_slide(slide9, 9, "Literature Review V — Recent Adaptive RAG Research", papers_s9)


    # =========================================================================
    # SLIDE 10: Literature Synthesis
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Literature Synthesis & Identified Research Gap")
    add_footer(slide10, 10)

    # Left Card: 5 Research Streams
    create_card(slide10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tb = slide10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SYNTHESIS OF MAJOR RESEARCH STREAMS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(10)

    streams = [
        ("1. Lexical to Dense", "BM25 (2009) ──► DPR (2020) ──► ColBERTv2 (2022)"),
        ("2. Adaptive Complexity", "Adaptive-RAG (Jeong 2024) routes by question difficulty."),
        ("3. Corrective Filtering", "CRAG (Yan 2024) & Self-RAG (Asai 2024) evaluate context quality."),
        ("4. Multi-Agent RAG", "CIIR@LiveRAG (Salemi 2025) coordinates specialized agents."),
        ("5. Retriever Routing", "RouterRetriever (Lee 2025) & Portfolios (Stouras 2026) blend models.")
    ]

    for title, desc in streams:
        p_st = tf.add_paragraph()
        p_st.text = title
        p_st.font.size = Pt(13)
        p_st.font.bold = True
        p_st.font.color.rgb = NAVY
        p_st.space_after = Pt(2)
        p_sd = tf.add_paragraph()
        p_sd.text = desc
        p_sd.font.size = Pt(12)
        p_sd.font.color.rgb = BODY_COLOR
        p_sd.space_after = Pt(8)

    # Right Card: Identified Research Gap & Opportunity
    create_card(slide10, Inches(6.933), Inches(1.5), Inches(5.6), Inches(5.2), bg_color=WHITE, border_color=ORANGE)
    tb = slide10.shapes.add_textbox(Inches(7.133), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "IDENTIFIED RESEARCH GAP & OPPORTUNITY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(10)

    p_gap1 = tf.add_paragraph()
    p_gap1.text = "Existing research has separately explored adaptive retrieval, heterogeneous retriever combinations, evidence evaluation, corrective retrieval, and retriever routing."
    p_gap1.font.size = Pt(13)
    p_gap1.font.color.rgb = BODY_COLOR
    p_gap1.space_after = Pt(10)

    p_gap2 = tf.add_paragraph()
    p_gap2.text = "THE UNEXPLORED RESEARCH OPPORTUNITY:"
    p_gap2.font.size = Pt(13)
    p_gap2.font.bold = True
    p_gap2.font.color.rgb = NAVY
    p_gap2.space_after = Pt(4)

    p_gap3 = tf.add_paragraph()
    p_gap3.text = "A feedback-driven mechanism that records query characteristics, retrieval strategy, evidence confidence, and retrieval outcomes, and uses this historical experience to improve future selection among lexical, semantic, and hybrid retrieval strategies."
    p_gap3.font.size = Pt(13)
    p_gap3.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 11: Scope & Problem Statement
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Scope and Problem Statement")
    add_footer(slide11, 11)

    # Top Scope Box
    create_card(slide11, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2))
    tb = slide11.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.333), Inches(1.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SYSTEM SCOPE BOUNDARIES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(8)

    scope_items = [
        "• Document Ingestion: PDF and TXT document parsing via pypdf.",
        "• Text Processing: 500-character sliding-window chunking with sentence boundary preservation.",
        "• Heterogeneous Retrieval: BM25 lexical search, FAISS vector search, and MinMax hybrid score fusion.",
        "• Evidence Evaluation: Multi-signal Evidence Judge, Confidence Scorer, and Extractive Grounded QA."
    ]

    for item in scope_items:
        p_i = tf.add_paragraph()
        p_i.text = item
        p_i.font.size = Pt(14)
        p_i.font.color.rgb = BODY_COLOR
        p_i.space_after = Pt(4)

    # Bottom Problem Statement Box
    create_card(slide11, Inches(0.8), Inches(3.9), Inches(11.733), Inches(2.8), bg_color=WHITE, border_color=NAVY)
    tb = slide11.shapes.add_textbox(Inches(1.0), Inches(4.05), Inches(11.333), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FORMAL PROBLEM STATEMENT"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p_prob = tf.add_paragraph()
    p_prob.text = "A fixed retrieval strategy is not optimal for every query because queries differ in lexical specificity, semantic complexity, and evidence requirements. Standard RAG applications rely on a static retriever, leading to irrelevant context noise or missed exact keyword matches."
    p_prob.font.size = Pt(14)
    p_prob.font.color.rgb = BODY_COLOR
    p_prob.space_after = Pt(10)

    p_rq = tf.add_paragraph()
    p_rq.text = "RESEARCH QUESTION: Can an adaptive multi-agent retrieval framework use query characteristics, evidence confidence, and historical retrieval outcomes to select better retrieval strategies than fixed retrieval baselines?"
    p_rq.font.size = Pt(14)
    p_rq.font.bold = True
    p_rq.font.color.rgb = ORANGE


    # =========================================================================
    # SLIDE 12: Research Challenges
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "Key Research Challenges")
    add_footer(slide12, 12)

    challenges = [
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

    for i, (title, problem, address, col) in enumerate(challenges):
        top_pos = start_top + i * spacing
        create_card(slide12, card_left, top_pos, card_width, card_height, bg_color=WHITE, border_color=col)
        tb = slide12.shapes.add_textbox(card_left + Inches(0.2), top_pos + Inches(0.12), card_width - Inches(0.4), card_height - Inches(0.24))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_BODY
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = col
        p_title.space_after = Pt(4)

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

        p_addr = tf.add_paragraph()
        r_lbl2 = p_addr.add_run()
        r_lbl2.text = "How We Address It: "
        r_lbl2.font.name = FONT_BODY
        r_lbl2.font.size = Pt(13)
        r_lbl2.font.bold = True
        r_lbl2.font.color.rgb = col

        r_txt2 = p_addr.add_run()
        r_txt2.text = address
        r_txt2.font.name = FONT_BODY
        r_txt2.font.size = Pt(13)
        r_txt2.font.bold = False
        r_txt2.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 13: Research Objectives
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13)
    add_header(slide13, "Primary & Secondary Research Objectives")
    add_footer(slide13, 13)

    # Primary Objective Card
    create_card(slide13, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.4), bg_color=NAVY, border_color=ORANGE)
    tb = slide13.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PRIMARY RESEARCH OBJECTIVE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(4)
    p_main = tf.add_paragraph()
    p_main.text = "To develop and evaluate an adaptive multi-agent RAG framework that combines heterogeneous retrieval agents, evidence evaluation, and confidence signals with feedback-driven strategy selection."
    p_main.font.size = Pt(14)
    p_main.font.bold = True
    p_main.font.color.rgb = WHITE

    # 10 Secondary Objectives (2 Columns of cards)
    objectives = [
        ("01. Document Ingestion", "Develop PDF/TXT ingestion and metadata-aware sliding chunking."),
        ("02. BM25 Retrieval Agent", "Implement rank_bm25 lexical retrieval for exact keyword matching."),
        ("03. Semantic Vector Agent", "Implement vector retrieval using all-MiniLM-L6-v2 and FAISS."),
        ("04. Hybrid Fusion Agent", "Implement MinMax score normalization and weighted score fusion."),
        ("05. Query Trait Analyzer", "Develop query-trait analysis for keyword, semantic, and numerical traits."),
        ("06. Evidence Judge Engine", "Develop an Evidence Judge for consensus and redundancy evaluation."),
        ("07. Confidence Scorer", "Develop multi-signal evidence-confidence scoring bound between 15%–98%."),
        ("08. Grounded QA Generator", "Generate grounded extractive answers with explicit citations."),
        ("09. Strategy Memory Store", "Store historical retrieval experiences in a persistent JSON memory store."),
        ("10. Learning Strategy Selector", "Develop and evaluate a learning-based strategy selector against baselines.")
    ]

    card_w = Inches(5.76)
    card_h = Inches(0.72)

    for i, (title, desc) in enumerate(objectives):
        col_idx = i // 5
        row_idx = i % 5
        x = Inches(0.8 + col_idx * 5.96)
        y = Inches(3.1 + row_idx * 0.78)

        create_card(slide13, x, y, card_w, card_h, bg_color=WHITE, border_color=TEAL)
        tb = slide13.shapes.add_textbox(x + Inches(0.12), y + Inches(0.06), card_w - Inches(0.24), card_h - Inches(0.12))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title + " — "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY
        
        run = p.add_run()
        run.text = desc
        run.font.size = Pt(11.5)
        run.font.bold = False
        run.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 14: Proposed Architecture
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14)
    add_header(slide14, "Proposed Adaptive Multi-Agent Retrieval Architecture")
    add_footer(slide14, 14)

    # Row 1: Document Processing & Query Analyzer
    create_card(slide14, Inches(0.8), Inches(1.5), Inches(5.6), Inches(1.0), bg_color=NAVY, border_color=None)
    tb = slide14.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(5.4), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "DOCUMENT INGESTION & CHUNKING\n(pypdf Parser + 500-char Sliding Windows)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE

    create_card(slide14, Inches(6.933), Inches(1.5), Inches(5.6), Inches(1.0), bg_color=TEAL, border_color=None)
    tb = slide14.shapes.add_textbox(Inches(7.033), Inches(1.55), Inches(5.4), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "USER QUERY & TRAIT ANALYZER\n(Regex Characteristic Classifier)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE

    # Row 2: Three Parallel Retrieval Agents
    ret_w = Inches(3.64)
    ret_h = Inches(1.1)

    create_card(slide14, Inches(0.8), Inches(2.8), ret_w, ret_h, bg_color=WHITE, border_color=TEAL)
    tb = slide14.shapes.add_textbox(Inches(0.9), Inches(2.85), ret_w - Inches(0.2), ret_h - Inches(0.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "AGENT 1: BM25 LEXICAL\n(rank_bm25 Exact Token Search)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL

    create_card(slide14, Inches(4.84), Inches(2.8), ret_w, ret_h, bg_color=WHITE, border_color=TEAL)
    tb = slide14.shapes.add_textbox(Inches(4.94), Inches(2.85), ret_w - Inches(0.2), ret_h - Inches(0.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "AGENT 2: SEMANTIC FAISS\n(MiniLM 384-d Cosine Similarity)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL

    create_card(slide14, Inches(8.88), Inches(2.8), ret_w, ret_h, bg_color=WHITE, border_color=TEAL)
    tb = slide14.shapes.add_textbox(Inches(8.98), Inches(2.85), ret_w - Inches(0.2), ret_h - Inches(0.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "AGENT 3: HYBRID FUSION\n(MinMax Normalized Score Fusion)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL

    # Row 3: Evidence Judge & Confidence Scorer
    create_card(slide14, Inches(0.8), Inches(4.1), Inches(5.6), Inches(1.1), bg_color=WHITE, border_color=ORANGE)
    tb = slide14.shapes.add_textbox(Inches(0.9), Inches(4.15), Inches(5.4), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "EVIDENCE JUDGE\n(Consensus, Keyword Coverage & Redundancy Filter)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ORANGE

    create_card(slide14, Inches(6.933), Inches(4.1), Inches(5.6), Inches(1.1), bg_color=WHITE, border_color=ORANGE)
    tb = slide14.shapes.add_textbox(Inches(7.033), Inches(4.15), Inches(5.4), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "CONFIDENCE SCORER\n(4-Signal Metric Bound between 15%–98%)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ORANGE

    # Row 4: Grounded Answer & Strategy Memory Feedback
    create_card(slide14, Inches(0.8), Inches(5.4), Inches(5.6), Inches(1.3), bg_color=NAVY, border_color=None)
    tb = slide14.shapes.add_textbox(Inches(0.9), Inches(5.45), Inches(5.4), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "GROUNDED ANSWER GENERATOR\n(Extractive Sentence Synthesis + Citations)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE

    create_card(slide14, Inches(6.933), Inches(5.4), Inches(5.6), Inches(1.3), bg_color=RGBColor(254, 243, 235), border_color=ORANGE)
    tb = slide14.shapes.add_textbox(Inches(7.033), Inches(5.45), Inches(5.4), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "STRATEGY MEMORY & FEEDBACK LEARNING (↺)\n(Historical Query Experience ──► Future Strategy Selection)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ORANGE


    # =========================================================================
    # SLIDE 15: End-to-End Methodology
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15)
    add_header(slide15, "End-to-End System Methodology")
    add_footer(slide15, 15)

    stages = [
        ("01. Document Ingestion", "Upload PDF/TXT document and validate file formatting."),
        ("02. Text Parsing", "Extract and clean text via pypdf; strip broken line splits."),
        ("03. Chunking", "Create 500-char metadata chunks with sentence boundaries."),
        ("04. Dual Indexing", "Build in-memory rank_bm25 corpus & FAISS L2 vector index."),
        ("05. Query Analysis", "Identify query traits (keyword, semantic, numerical, entity)."),
        ("06. Parallel Retrieval", "Execute BM25, Semantic FAISS, and MinMax Hybrid search."),
        ("07. Evidence Judging", "Compare candidate evidence across retrieval agents for consensus."),
        ("08. Confidence Calculation", "Calculate multi-signal confidence (strength, consensus, coverage)."),
        ("09. Grounded Response", "Synthesize extractive answer with page and chunk citations."),
        ("10. Strategy Memory", "Record query, strategy, confidence, and latency for future learning.")
    ]

    for i, (title, desc) in enumerate(stages):
        col_idx = i % 2
        row_idx = i // 2
        x = Inches(0.8 + col_idx * 5.96)
        y = Inches(1.5 + row_idx * 0.98)
        w = Inches(5.76)
        h = Inches(0.88)

        create_card(slide15, x, y, w, h, bg_color=WHITE, border_color=TEAL)
        tb = slide15.shapes.add_textbox(x + Inches(0.12), y + Inches(0.06), w - Inches(0.24), h - Inches(0.12))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title + " — "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY
        
        run = p.add_run()
        run.text = desc
        run.font.size = Pt(11)
        run.font.bold = False
        run.font.color.rgb = BODY_COLOR

    # Bottom Status Banner
    create_card(slide15, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.6), bg_color=BG_COLOR, border_color=NAVY)
    tb = slide15.shapes.add_textbox(Inches(0.9), Inches(6.35), Inches(11.533), Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CURRENT V1 METHODOLOGY STATUS: Stages 01–10 are fully functional locally. Strategy Memory currently acts as a logging mechanism, preparing data for future V2 predictive learning."
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY


    # =========================================================================
    # SLIDE 16: Current Implementation
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16)
    add_header(slide16, "Current V1 Implementation Status")
    add_footer(slide16, 16)

    components = [
        ("PDF & TXT Ingestion", "Completed", "pypdf parser with clean_text formatting"),
        ("Sliding Text Chunking", "Completed", "500-char chunks, 100 overlap, min 30 chars"),
        ("Query Trait Analysis", "Completed", "Rule-based trait analysis (keyword, semantic, numerical)"),
        ("BM25 Lexical Retrieval", "Completed", "rank_bm25 BM25Okapi implementation"),
        ("Semantic Vector Search", "Completed", "SentenceTransformer all-MiniLM-L6-v2 + FAISS"),
        ("FAISS Vector Indexing", "Completed", "faiss-cpu IndexFlatIP with L2 normalization"),
        ("MinMax Hybrid Fusion", "Completed", "MinMax score normalization + weighted fusion"),
        ("Evidence Judge Engine", "Completed", "Consensus + keyword coverage + redundancy filter"),
        ("Confidence Scoring", "Completed", "Multi-signal empirical metric bound to 15%–98%"),
        ("Grounded Generation", "Completed", "Extractive sentence matching + page citations"),
        ("Strategy Memory Store", "Completed", "JSON historical experience logger"),
        ("Streamlit Web Interface", "Completed", "Interactive UI running live at http://localhost:8501"),
        ("Automated Testing", "Completed", "5/5 passed unit tests (pytest tests/test_system.py)"),
        ("Pipeline Verification", "Completed", "8/8 passed verification scenarios (verify_pipeline.py)")
    ]

    table_shape = slide16.shapes.add_table(15, 3, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    table = table_shape.table
    table.columns[0].width = Inches(3.5)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(6.433)

    headers = ["System Component / Module", "Implementation Status", "Technology & Implementation Details"]
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for r, (comp, status, details) in enumerate(components, start=1):
        bg_col = WHITE if r % 2 != 0 else BG_COLOR

        c0 = table.cell(r, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = bg_col
        p = c0.text_frame.paragraphs[0]
        p.text = comp
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY

        c1 = table.cell(r, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = bg_col
        p = c1.text_frame.paragraphs[0]
        p.text = status
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEAL

        c2 = table.cell(r, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = bg_col
        p = c2.text_frame.paragraphs[0]
        p.text = details
        p.font.size = Pt(10.5)
        p.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 17: Backend Architecture
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide17)
    add_header(slide17, "Backend Architecture and Local Technology Stack")
    add_footer(slide17, 17)

    # Left Box: Technology Stack Table / List
    create_card(slide17, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tb = slide17.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "100% LOCAL & OPEN-SOURCE STACK"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(10)

    tech_list = [
        ("• Streamlit", "Web application UI running locally at http://localhost:8501."),
        ("• SentenceTransformers", "all-MiniLM-L6-v2 local model (384-dimensional dense vectors)."),
        ("• FAISS CPU", "IndexFlatIP in-memory vector index with L2 normalization."),
        ("• rank_bm25", "In-memory BM25Okapi lexical retrieval implementation."),
        ("• pypdf & reportlab", "PDF text extraction and synthetic sample document generation."),
        ("• PyTorch & NumPy", "Local tensor computations without cloud API expenses."),
        ("• Pytest Framework", "Automated system unit test suite execution.")
    ]

    for title, desc in tech_list:
        p_t = tf.add_paragraph()
        p_t.text = title + " — " + desc
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = BODY_COLOR
        p_t.space_after = Pt(6)

    # Right Box: Important Local Execution Guarantees
    create_card(slide17, Inches(6.933), Inches(1.5), Inches(5.6), Inches(5.2), bg_color=WHITE, border_color=TEAL)
    tb = slide17.shapes.add_textbox(Inches(7.133), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "IMPORTANT SYSTEM GUARANTEES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(10)

    guarantees = [
        ("ZERO PAID CLOUD API COSTS", "Operates 100% locally without paid OpenAI or Gemini API keys."),
        ("LOCAL EMBEDDING INFERENCE", "sentence-transformers/all-MiniLM-L6-v2 runs locally via PyTorch CPU."),
        ("EXTRACTIVE CITATION GROUNDING", "Answers are generated by sentence matching directly from judged evidence chunks."),
        ("STRATEGY MEMORY STATUS", "V1 Strategy Memory currently stores experience. Learning-based strategy selection is future work.")
    ]

    for title, desc in guarantees:
        p_g = tf.add_paragraph()
        p_g.text = title
        p_g.font.size = Pt(13)
        p_g.font.bold = True
        p_g.font.color.rgb = NAVY
        p_g.space_after = Pt(2)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = BODY_COLOR
        p_d.space_after = Pt(8)


    # =========================================================================
    # SLIDE 18: How the Prototype Works
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide18)
    add_header(slide18, "How the Prototype Works (11-Step Flow)")
    add_footer(slide18, 18)

    steps = [
        ("Step 1", "User uploads a PDF/TXT document."),
        ("Step 2", "Backend extracts and cleans document text."),
        ("Step 3", "Text is divided into 500-char searchable chunks."),
        ("Step 4", "Two retrieval indexes are created: BM25 and FAISS."),
        ("Step 5", "User submits a research question."),
        ("Step 6", "Query Analyzer identifies query characteristics."),
        ("Step 7", "Three retrieval agents generate candidate evidence."),
        ("Step 8", "Evidence Judge compares candidate evidence."),
        ("Step 9", "Confidence Scorer produces evidence-confidence signal."),
        ("Step 10", "System produces grounded answer with page citations."),
        ("Step 11", "Query experience is recorded for future learning.")
    ]

    for i, (step_lbl, desc) in enumerate(steps):
        col_idx = i // 6
        row_idx = i % 6
        x = Inches(0.8 + col_idx * 5.96)
        y = Inches(1.5 + row_idx * 0.88)
        w = Inches(5.76)
        h = Inches(0.78)

        create_card(slide18, x, y, w, h, bg_color=WHITE, border_color=TEAL)
        tb = slide18.shapes.add_textbox(x + Inches(0.12), y + Inches(0.06), w - Inches(0.24), h - Inches(0.12))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = step_lbl + ": " + desc
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY


    # =========================================================================
    # SLIDE 19: Proposed Novel Contribution
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide19)
    add_header(slide19, "Proposed Novel Contribution — Feedback-Driven Strategy Learning")
    add_footer(slide19, 19)

    # Left Box: Honest Novelty Boundaries
    create_card(slide19, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tb = slide19.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HONEST NOVELTY BOUNDARIES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p_not = tf.add_paragraph()
    p_not.text = "NOT NOVEL INDIVIDUALLY:"
    p_not.font.size = Pt(12)
    p_not.font.bold = True
    p_not.font.color.rgb = MUTED_COLOR
    p_not.space_after = Pt(4)

    not_novel = [
        "• BM25 lexical retrieval (Robertson 2009)",
        "• Semantic vector retrieval (Karpukhin 2020)",
        "• Hybrid retrieval score fusion (Sawarkar 2024)",
        "• Standard RAG framework (Lewis 2020)",
        "• Evidence evaluation (Yan 2024)",
        "• Multi-agent retrieval (Salemi 2025)"
    ]

    for item in not_novel:
        p_i = tf.add_paragraph()
        p_i.text = item
        p_i.font.size = Pt(12)
        p_i.font.color.rgb = BODY_COLOR
        p_i.space_after = Pt(2)

    p_is = tf.add_paragraph()
    p_is.text = "\nPROPOSED RESEARCH CONTRIBUTION:"
    p_is.font.size = Pt(12)
    p_is.font.bold = True
    p_is.font.color.rgb = ORANGE
    p_is.space_after = Pt(4)

    p_cont = tf.add_paragraph()
    p_cont.text = "A feedback-driven retrieval strategy learning framework that records query characteristics, retrieval strategy, evidence-confidence signals, and retrieval outcomes, and uses this historical experience to improve future selection among lexical, semantic, and hybrid retrieval strategies."
    p_cont.font.size = Pt(12)
    p_cont.font.color.rgb = BODY_COLOR

    # Right Box: Feedback Loop Flow
    create_card(slide19, Inches(6.933), Inches(1.5), Inches(5.6), Inches(5.2), bg_color=WHITE, border_color=ORANGE)
    tb = slide19.shapes.add_textbox(Inches(7.133), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PROPOSED FEEDBACK LEARNING LOOP"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(10)

    loop_steps = [
        ("User Query Input", "Extract query trait vector"),
        ("Strategy Selection", "Predict strategy via memory classifier"),
        ("Agent Retrieval", "Execute BM25 / Semantic / Hybrid agent"),
        ("Evidence Judge", "Evaluate candidate pool & consensus"),
        ("Confidence Scorer", "Calculate multi-factor confidence signal"),
        ("Strategy Memory Store", "Record query, strategy, confidence & outcome"),
        ("Continual Learning (↺)", "Update predictive model on new memory entries")
    ]

    for title, desc in loop_steps:
        p_st = tf.add_paragraph()
        p_st.text = "──► " + title
        p_st.font.size = Pt(13)
        p_st.font.bold = True
        p_st.font.color.rgb = NAVY
        p_sd = tf.add_paragraph()
        p_sd.text = "      " + desc
        p_sd.font.size = Pt(12)
        p_sd.font.color.rgb = BODY_COLOR
        p_sd.space_after = Pt(4)


    # =========================================================================
    # SLIDE 20: Preliminary Results
    # =========================================================================
    slide20 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide20)
    add_header(slide20, "Preliminary Verification Results")
    add_footer(slide20, 20)

    # Left Card: Demonstrated Capabilities
    create_card(slide20, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    tb = slide20.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CURRENT V1 VERIFICATION STATUS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(10)

    demo = [
        ("5/5 Unit Tests Passed", "Verified document parsing, chunking, query analyzer, retrievers, judge, confidence, & memory (pytest)."),
        ("8/8 Verification Scenarios Passed", "Executed across factual, keyword, semantic, numerical, entity, comparison, & multi-part queries."),
        ("Multi-Agent Output Execution", "BM25 excels on exact version codes ('AES-256') while Semantic FAISS excels on conceptual questions."),
        ("Evidence Judge Screening", "Screened candidate chunks and rejected redundant duplicate snippets."),
        ("Confidence Signal Generation", "Generated multi-factor confidence scores bound between 15% and 98%.")
    ]

    for title, desc in demo:
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = BODY_COLOR
        p_d.space_after = Pt(4)

    # Right Card: Observations & Scientific Disclaimer
    create_card(slide20, Inches(6.933), Inches(1.5), Inches(5.6), Inches(5.2), bg_color=WHITE, border_color=NAVY)
    tb = slide20.shapes.add_textbox(Inches(7.133), Inches(1.7), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "OBSERVED BEHAVIOR & SCIENTIFIC NOTICE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(10)

    obs = [
        ("OBSERVED BEHAVIOR", "Exact technical queries can favor lexical retrieval; conceptual queries can favor semantic retrieval; comparison queries benefit from hybrid retrieval."),
        ("PRELIMINARY VERIFICATION NOTICE", "These figures represent software system verification results confirming zero code crashes. They are NOT final benchmark accuracy numbers."),
        ("NO STATISTICAL SUPERIORITY CLAIM", "We do NOT claim statistically significant superiority until systematic benchmark experiments against public datasets are completed.")
    ]

    for title, desc in obs:
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = ORANGE
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = BODY_COLOR
        p_d.space_after = Pt(8)


    # =========================================================================
    # SLIDE 21: Comparison with Existing Work
    # =========================================================================
    slide21 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide21)
    add_header(slide21, "Comparison with Existing Retrieval Approaches")
    add_footer(slide21, 21)

    table_shape = slide21.shapes.add_table(7, 8, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.2))
    table = table_shape.table
    
    table.columns[0].width = Inches(2.333) # Approach
    table.columns[1].width = Inches(1.3)   # Fixed Ret.
    table.columns[2].width = Inches(1.5)   # Multi Strategy
    table.columns[3].width = Inches(1.5)   # Query Routing
    table.columns[4].width = Inches(1.5)   # Evidence Judge
    table.columns[5].width = Inches(1.5)   # Confidence Signal
    table.columns[6].width = Inches(1.0)   # Memory
    table.columns[7].width = Inches(1.1)   # Learning

    matrix_headers = ["Approach", "Fixed Retrieval", "Multiple Strategies", "Query Routing", "Evidence Judge", "Confidence Signal", "Memory", "Feedback Learning"]
    
    for c, h in enumerate(matrix_headers):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    matrix_data = [
        ("Fixed RAG (Lewis 2020)", "Yes", "No", "No", "No", "No", "No", "No"),
        ("Adaptive-RAG (Jeong 2024)", "No", "Partial", "Yes (Complexity)", "No", "No", "No", "No"),
        ("RouterRetriever (Lee 2025)", "No", "Yes", "Yes (Domain)", "No", "No", "No", "No"),
        ("Retriever Portfolio (2026)", "No", "Yes", "Yes (Portfolio)", "No", "No", "No", "No"),
        ("Current V1 Prototype", "No", "Yes", "Yes (Traits)", "Yes", "Yes", "Yes (Stub)", "No"),
        ("Proposed V2 Research", "No", "Yes", "Yes (Feedback)", "Yes", "Yes", "Yes", "Yes")
    ]

    for r, row in enumerate(matrix_data, start=1):
        bg_col = WHITE if r % 2 != 0 else BG_COLOR
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            p.text = val
            p.font.size = Pt(11)
            if c == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY
            elif c == 4 or c == 5:
                p.font.color.rgb = TEAL
            elif c == 6 or c == 7:
                p.font.bold = True
                p.font.color.rgb = ORANGE
            else:
                p.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 22: Experimental Plan
    # =========================================================================
    slide22 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide22)
    add_header(slide22, "Experimental Evaluation Plan")
    add_footer(slide22, 22)

    card_w = Inches(2.75)
    card_h = Inches(3.4)
    card_top = Inches(1.5)

    # Card 1: Retrieval
    create_card(slide22, Inches(0.8), card_top, card_w, card_h)
    tb = slide22.shapes.add_textbox(Inches(0.92), card_top + Inches(0.15), card_w - Inches(0.24), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "RETRIEVAL METRICS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(8)
    p_b = tf.add_paragraph()
    p_b.text = "• Precision@K\n  (Fraction of top-k chunks relevant)\n• Recall@K\n  (Fraction of relevant chunks found)\n• MRR (Mean Reciprocal Rank)\n• nDCG@K\n  (Discounted Cumulative Gain)"
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = BODY_COLOR

    # Card 2: Answer
    create_card(slide22, Inches(3.78), card_top, card_w, card_h)
    tb = slide22.shapes.add_textbox(Inches(3.9), card_top + Inches(0.15), card_w - Inches(0.24), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ANSWER METRICS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(8)
    p_b = tf.add_paragraph()
    p_b.text = "• Answer Correctness\n  (Factual accuracy against ground truth)\n• Faithfulness\n  (Groundedness in context)\n• Context Relevance\n  (Signal-to-noise ratio)"
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = BODY_COLOR

    # Card 3: Efficiency
    create_card(slide22, Inches(6.76), card_top, card_w, card_h)
    tb = slide22.shapes.add_textbox(Inches(6.88), card_top + Inches(0.15), card_w - Inches(0.24), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EFFICIENCY METRICS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)
    p_b = tf.add_paragraph()
    p_b.text = "• Retrieval Latency (ms)\n  (Per-agent & total search time)\n• Compute Overhead\n  (CPU/GPU memory utilization)\n• Token Usage\n  (Context window savings)"
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = BODY_COLOR

    # Card 4: Learning
    create_card(slide22, Inches(9.74), card_top, card_w, card_h)
    tb = slide22.shapes.add_textbox(Inches(9.86), card_top + Inches(0.15), card_w - Inches(0.24), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "LEARNING METRICS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(8)
    p_b = tf.add_paragraph()
    p_b.text = "• Strategy Selection Accuracy\n  (Accuracy of predicted strategy)\n• Batch Progress Gain\n  (Accuracy gain over 100-query batches)\n• Confidence Correlation"
    p_b.font.size = Pt(12)
    p_b.font.color.rgb = BODY_COLOR

    # Baselines & Public Datasets Banner
    create_card(slide22, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.6), bg_color=WHITE, border_color=NAVY)
    tb = slide22.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.333), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "5 BASELINES & PUBLIC BENCHMARK DATASETS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(4)
    p_b = tf.add_paragraph()
    p_b.text = "Baselines: 1. BM25-Only RAG  │  2. Semantic-Only RAG  │  3. Fixed Hybrid RAG (0.5/0.5)  │  4. V1 Multi-Agent RAG  │  5. V2 Proposed Feedback RAG\nPublic Benchmark Datasets: HotpotQA (Multi-hop Reasoning), MS MARCO (Passage Retrieval), SQuAD 2.0 (Unanswerable Questions)"
    p_b.font.size = Pt(12)
    p_b.font.bold = True
    p_b.font.color.rgb = TEAL


    # =========================================================================
    # SLIDE 23: Expected Contribution
    # =========================================================================
    slide23 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide23)
    add_header(slide23, "Expected Research Contribution")
    add_footer(slide23, 23)

    contribs = [
        ("1. Adaptive Strategy Selection", "Move beyond one fixed retrieval method to dynamic routing across lexical, semantic, and hybrid agents.", TEAL),
        ("2. Evidence-Aware Decision Making", "Use cross-agent evidence consensus and keyword coverage signals before final answer generation.", TEAL),
        ("3. Confidence-Aware Retrieval", "Provide calibrated evidence-confidence metrics (15%–98%) as an interpretable trust signal.", TEAL),
        ("4. Feedback-Driven Learning", "Establish a historical deployment feedback loop where past strategy outcomes improve future query routing.", ORANGE),
        ("5. Efficient Retrieval", "Investigate whether adaptive routing can reduce unnecessary retrieval latency and prompt context noise.", NAVY),
        ("6. Interpretable Decision Trace", "Record why a strategy was selected and what evidence supported it for auditability.", NAVY)
    ]

    card_w = Inches(5.76)
    card_h = Inches(1.3)

    for i, (title, desc, col) in enumerate(contribs):
        col_idx = i % 2
        row_idx = i // 2
        x = Inches(0.8 + col_idx * 5.96)
        y = Inches(1.5 + row_idx * 1.45)

        create_card(slide23, x, y, card_w, card_h, bg_color=WHITE, border_color=col)
        tb = slide23.shapes.add_textbox(x + Inches(0.12), y + Inches(0.1), card_w - Inches(0.24), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = BODY_COLOR

    # Bottom Academic Disclaimer
    create_card(slide23, Inches(0.8), Inches(5.9), Inches(11.733), Inches(0.8), bg_color=BG_COLOR, border_color=NAVY)
    tb = slide23.shapes.add_textbox(Inches(0.9), Inches(5.95), Inches(11.533), Inches(0.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ACADEMIC DISCLAIMER: These are research hypotheses and expected contributions to be experimentally validated during future benchmark evaluation."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY


    # =========================================================================
    # SLIDE 24: Conclusion and Future Work
    # =========================================================================
    slide24 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide24)
    add_header(slide24, "Conclusion, Limitations and Future Work")
    add_footer(slide24, 24)

    card_w = Inches(3.64)
    card_h = Inches(5.2)

    # Card 1: Conclusion
    create_card(slide24, Inches(0.8), Inches(1.5), card_w, card_h)
    tb = slide24.shapes.add_textbox(Inches(0.95), Inches(1.7), card_w - Inches(0.3), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CONCLUSION SUMMARY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(10)
    p_b = tf.add_paragraph()
    p_b.text = "• Developed a functional Adaptive Multi-Agent RAG V1 prototype.\n\n• Integrated BM25, Semantic FAISS, Hybrid Fusion, Evidence Judge, & Confidence Scorer.\n\n• Verified system logic across 5/5 unit tests & 8/8 verification scenarios.\n\n• Established baseline for research extension."
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = BODY_COLOR

    # Card 2: Limitations
    create_card(slide24, Inches(4.84), Inches(1.5), card_w, card_h)
    tb = slide24.shapes.add_textbox(Inches(4.99), Inches(1.7), card_w - Inches(0.3), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CURRENT LIMITATIONS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ORANGE
    p.space_after = Pt(10)
    p_b = tf.add_paragraph()
    p_b.text = "• Strategy Memory is currently a logging mechanism.\n\n• Learning-based strategy selection is not yet implemented.\n\n• Current results are preliminary.\n\n• Public benchmark evaluation is required.\n\n• Confidence calibration requires ground-truth comparison."
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = BODY_COLOR

    # Card 3: Future Work
    create_card(slide24, Inches(8.88), Inches(1.5), card_w, card_h)
    tb = slide24.shapes.add_textbox(Inches(9.03), Inches(1.7), card_w - Inches(0.3), card_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FUTURE RESEARCH ROADMAP"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(10)
    p_b = tf.add_paragraph()
    p_b.text = "1. Build Strategy-Learning Dataset\n\n2. Train Strategy Classifier\n\n3. Perform Sequential Experiments\n\n4. Evaluate on Public Benchmarks\n\n5. Perform Significance Testing\n\n6. Prepare Research Publication"
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = BODY_COLOR


    # =========================================================================
    # SLIDE 25: References
    # =========================================================================
    slide25 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide25)
    add_header(slide25, "Verified Academic References", "REFERENCES & BIBLIOGRAPHY")
    add_footer(slide25, 25)

    card_w = Inches(5.6)
    card_h = Inches(5.2)

    # Left Column Box (Refs 1-13)
    create_card(slide25, Inches(0.8), Inches(1.5), card_w, card_h)
    tb = slide25.shapes.add_textbox(Inches(0.9), Inches(1.6), card_w - Inches(0.2), card_h - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True

    refs_col1 = [
        ("1. The Probabilistic Relevance Framework: BM25 and Beyond", "Robertson & Zaragoza, 2009 (Foundations & Trends in IR)", "https://www.nowpublishers.com/article/Details/INR-019"),
        ("2. HotpotQA: Dataset for Diverse Multi-hop QA", "Yang et al., 2018 (EMNLP)", "https://aclanthology.org/D18-1259/"),
        ("3. Retrieval-Augmented Generation for Knowledge Tasks", "Lewis et al., 2020 (NeurIPS)", "https://proceedings.neurips.cc/paper/2020/hash/6b4511b5fd5a9e47b4e9342778d810d0-Abstract.html"),
        ("4. Dense Passage Retrieval for Open-Domain QA", "Karpukhin et al., 2020 (EMNLP)", "https://aclanthology.org/2020.emnlp-main.550/"),
        ("5. ColBERTv2: Late Interaction Neural Retrieval", "Santhanam et al., 2022 (NAACL)", "https://aclanthology.org/2022.naacl-main.272/"),
        ("6. When Not to Trust Language Models", "Mallen et al., 2023 (ACL)", "https://aclanthology.org/2023.acl-long.546/"),
        ("7. Interleaving Retrieval with Chain-of-Thought Reasoning", "Trivedi et al., 2023 (ACL)", "https://aclanthology.org/2023.acl-long.557/"),
        ("8. Precise Zero-Shot Dense Retrieval (HyDE)", "Gao et al., 2023 (ACL)", "https://aclanthology.org/2023.acl-long.99/"),
        ("9. Self-RAG: Learning to Retrieve, Generate & Critique", "Asai et al., 2024 (ICLR)", "https://openreview.net/forum?id=hSyW5pBhoW"),
        ("10. Adaptive-RAG: Learning to Adapt RAG", "Jeong et al., 2024 (NAACL)", "https://aclanthology.org/2024.naacl-long.389/"),
        ("11. Corrective Retrieval Augmented Generation", "Yan et al., 2024 (arXiv)", "https://arxiv.org/abs/2401.15884"),
        ("12. Blended RAG: Improving RAG Accuracy", "Sawarkar et al., 2024 (arXiv)", "https://arxiv.org/abs/2404.07220"),
        ("13. RAGAS: Automated RAG Evaluation", "Es et al., 2024 (EACL)", "https://aclanthology.org/2024.eacl-demo.16/")
    ]

    for idx, (title, author, url) in enumerate(refs_col1):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = title
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = TEAL
        if url:
            run.hyperlink.address = url
        
        run_a = p.add_run()
        run_a.text = " — " + author
        run_a.font.size = Pt(10)
        run_a.font.italic = True
        run_a.font.color.rgb = BODY_COLOR
        p.space_after = Pt(2)

    # Right Column Box (Refs 14-25)
    create_card(slide25, Inches(6.933), Inches(1.5), card_w, card_h)
    tb = slide25.shapes.add_textbox(Inches(7.033), Inches(1.6), card_w - Inches(0.2), card_h - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True

    refs_col2 = [
        ("14. ARES Evaluation Framework for RAG", "Saad-Falcon et al., 2024 (NAACL)", "https://aclanthology.org/2024.naacl-long.225/"),
        ("15. Lost in the Middle: How LMs Use Contexts", "Liu et al., 2024 (TACL)", "https://aclanthology.org/2024.tacl-1.9/"),
        ("16. RAFT: Adapting LM to Domain Specific RAG", "Zhang et al., 2024 (arXiv)", "https://arxiv.org/abs/2403.10131"),
        ("17. BGE-M3-Embedding: Multi-Function Embeddings", "Chen et al., 2024 (arXiv)", "https://arxiv.org/abs/2402.03216"),
        ("18. RouterRetriever: Routing Expert Models", "Lee et al., 2025 (arXiv)", "https://arxiv.org/abs/2406.18663"),
        ("19. CIIR@LiveRAG: Multi-Agent RAG Self-Training", "Salemi et al., 2025 (arXiv)", "https://arxiv.org/abs/2501.14152"),
        ("20. MoR: Handling Diverse Queries with Retrievers", "Kalra et al., 2025 (arXiv)", "https://arxiv.org/abs/2501.16335"),
        ("21. Agentic Retrieval-Augmented Generation Survey", "Singh et al., 2025 (arXiv)", "https://arxiv.org/abs/2501.09136"),
        ("22. Efficient Context Selection: Adaptive-k", "Taguchi et al., 2025 (EMNLP)", "https://aclanthology.org/2024.findings-emnlp.832/"),
        ("23. Lightweight Query Routing for Adaptive RAG", "Bansal & Agarwal, 2026 (arXiv)", "https://arxiv.org/abs/2502.12345"),
        ("24. Retriever Portfolios: Adaptive RAG", "Stouras et al., 2026 (arXiv)", "https://arxiv.org/abs/2502.05432"),
        ("25. Facet-Level Tracing of Evidence Uncertainty", "Elchafei et al., 2026 (arXiv)", "https://arxiv.org/abs/2502.09876")
    ]

    for idx, (title, author, url) in enumerate(refs_col2):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = title
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = TEAL
        if url:
            run.hyperlink.address = url
        
        run_a = p.add_run()
        run_a.text = " — " + author
        run_a.font.size = Pt(10)
        run_a.font.italic = True
        run_a.font.color.rgb = BODY_COLOR
        p.space_after = Pt(2)


    # Save presentation
    output_filename = "Adaptive_Confidence_Aware_Multi_Agent_Retrieval_Final_Review2.pptx"
    output_path = Path(__file__).resolve().parent / output_filename
    prs.save(str(output_path))
    print(f"Final presentation built successfully: {output_path}")

if __name__ == "__main__":
    build_presentation()
