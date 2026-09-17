import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

def generate_sample_pdf(pdf_path: Path):
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    story = []
    
    # Title Header
    story.append(Paragraph("NovaTech Research & Product Knowledge Base", title_style))
    story.append(Paragraph("Confidential Internal Technical Documentation | Version 4.2 | Published 2025", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=15))
    
    # Section 1
    story.append(Paragraph("1. Executive Summary & Company Overview", section_style))
    story.append(Paragraph(
        "NovaTech AI Labs is a leading deep-tech research enterprise founded in 2021 and headquartered in Boston, Massachusetts. "
        "The company specializes in next-generation renewable energy technology, autonomous edge robotics, and secure distributed protocols. "
        "In Q1 2025, NovaTech successfully completed its $45 million Series B funding round, led by Horizon CleanTech Ventures. "
        "NovaTech's mission is to accelerate global industrial sustainability and intelligent automation through adaptive multi-agent systems and novel material science.",
        body_style
    ))
    
    # Section 2
    story.append(Paragraph("2. NovaSolar-X Quantum Solar Panel Specifications", section_style))
    story.append(Paragraph(
        "The NovaSolar-X (Model NS-520-QX) represents NovaTech's flagship photovoltaic innovation. Utilizing silicon-perovskite tandem cells, "
        "the module achieves a record-setting operational efficiency of 28.4%. Key technical specifications include:",
        body_style
    ))
    
    table_data = [
        ["Parameter", "Specification Value"],
        ["Peak Power Output", "520 Watts"],
        ["Cell Architecture", "Silicon-Perovskite Tandem"],
        ["Energy Conversion Efficiency", "28.4%"],
        ["Operating Temperature Range", "-40°C to +85°C"],
        ["Annual Degradation Rate", "0.35% per year"],
        ["Standard Warranty", "30-Year Performance Guarantee"]
    ]
    t = Table(table_data, colWidths=[200, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # Section 3
    story.append(Paragraph("3. Project AeroGuide: Autonomous Drone Swarm Research", section_style))
    story.append(Paragraph(
        "Project AeroGuide focuses on decentralized search-and-rescue operations using autonomous micro-drone swarms. "
        "Each AeroGuide unit is powered by the custom NV-X2 Edge AI Neural Processor, allowing real-time spatial mapping and obstacle avoidance. "
        "The drones communicate via a peer-to-peer mesh network without relying on centralized GPS or cloud connectivity. "
        "Key operational parameters: Maximum flight duration is 45 minutes, maximum top speed is 65 km/h, and the integrated payload includes dual-spectrum thermal optical sensors and solid-state LiDAR.",
        body_style
    ))
    
    # Section 4
    story.append(Paragraph("4. Financial Highlights & Key Leadership", section_style))
    story.append(Paragraph(
        "During Q3 2025, NovaTech reported record quarterly revenue of $18.4 million, representing a 42% year-over-year growth. "
        "The company maintains a high commitment to innovation, allocating 34% of overall revenue directly to research and development (R&D). "
        "NovaTech is guided by Chief Executive Officer Dr. Aris Vance and Chief Technology Officer Elena Rostova. "
        "Strategic milestones include expanding product distribution into European Union markets by Q2 2026.",
        body_style
    ))
    
    # Section 5
    story.append(Paragraph("5. Environmental Sustainability & Zero-Carbon Manufacturing", section_style))
    story.append(Paragraph(
        "NovaTech operates under a strict Zero-Carbon Manufacturing Initiative. The target is achieving 100% renewable energy across all manufacturing facilities by 2027. "
        "Current facilities feature closed-loop water recycling systems that cut industrial wastewater by 82%. "
        "All NovaSolar-X module frames are constructed using 100% recycled structural aluminum, significantly lowering the embodied carbon footprint.",
        body_style
    ))
    
    # Section 6
    story.append(Paragraph("6. NovaSync v3.2 Distributed Data Protocol", section_style))
    story.append(Paragraph(
        "NovaSync v3.2 is NovaTech's proprietary distributed data synchronization protocol engineered for low-latency IoT communication. "
        "It employs zero-trust AES-256 end-to-end encryption and a lightweight consensus algorithm termed Proof-of-State. "
        "Benchmark testing demonstrates sub-12 millisecond network latency and high throughput reaching up to 10 Gbps across multi-region clusters.",
        body_style
    ))
    
    doc.build(story)
    print(f"Sample PDF successfully generated at: {pdf_path}")

def generate_sample_questions(txt_path: Path):
    questions_content = """# NovaTech Research Knowledge Base - Recommended Test Questions

1. [Factual] What is the warranty period and energy efficiency of the NovaSolar-X solar panel?
2. [Keyword-Heavy] NovaSync v3.2 zero-trust encryption AES-256 throughput latency Proof-of-State
3. [Semantic] How does NovaTech ensure its green manufacturing processes protect the environment and reduce waste?
4. [Numerical] What is the Q3 2025 revenue figure and the percentage of revenue allocated to R&D?
5. [Entity] Who are the CEO and CTO of NovaTech, and where is the enterprise headquartered?
6. [Comparison] Compare the operational characteristics of the NovaSolar-X solar panel with the AeroGuide drone swarm system.
7. [Multi-Section Integration] How do NovaTech's sustainability goals align with its financial investments and upcoming 2026 European expansion milestones?
8. [Disagreement-Prone] What battery flight duration, top speed, and neural processor specs are defined for NovaTech's autonomous products?
"""
    txt_path.write_text(questions_content, encoding='utf-8')
    print(f"Sample test questions generated at: {txt_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    pdf_out = base_dir / "NovaTech_Research_Knowledge_Base.pdf"
    txt_out = base_dir / "test_questions.txt"
    generate_sample_pdf(pdf_out)
    generate_sample_questions(txt_out)
