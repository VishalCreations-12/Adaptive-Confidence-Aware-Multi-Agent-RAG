import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle

def generate_sample_pdf(pdf_path: Path):
    """Generate comprehensive 12-page technical research knowledge base for NovaTech Enterprise."""
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=8
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    sec_style = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=4
    )
    sub_style = ParagraphStyle(
        'SubSecHeading',
        parent=styles['Heading3'],
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=8,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    story = []
    
    # Header
    story.append(Paragraph("NovaTech Applied Intelligence & Hardware Labs: Comprehensive Technical Compendium", title_style))
    story.append(Paragraph("Formal Technical Specification Document | Version 5.4 | Enterprise Technical Release 2025-2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=10))
    
    # 1. Corporate History & Executive Governance
    story.append(Paragraph("1. Corporate Identity, History, and Executive Governance", sec_style))
    story.append(Paragraph(
        "NovaTech Applied Intelligence Labs is a multinational deep-technology enterprise founded in October 2021 by Dr. Aris Vance and Dr. Elena Rostova. "
        "The corporate headquarters is located at 400 Technology Square, Cambridge, Massachusetts, with major secondary engineering campuses in Munich, Germany, and Zurich, Switzerland. "
        "The leadership team comprises Chief Executive Officer Dr. Aris Vance, Chief Technology Officer Dr. Elena Rostova, Chief Financial Officer Marcus Sterling, "
        "and Vice President of Advanced Hardware Systems Dr. Naoko Takahashi. "
        "As of fiscal year 2025, NovaTech employs 1,420 full-time engineers and research scientists globally, with 58% holding advanced degrees in computer science, robotics, or material physics.",
        body_style
    ))
    story.append(Paragraph(
        "NovaTech's mission statement emphasizes accelerating global industrial sustainability and intelligent automation through adaptive multi-agent software architectures, "
        "custom edge-compute silicon, and next-generation photovoltaic material science. "
        "The organization maintains strict corporate governance guided by the ISO 9001 quality management framework and ISO 27001 data security compliance.",
        body_style
    ))

    # 2. Financial Disclosures & R&D Capital Investments
    story.append(Paragraph("2. Financial Capitalization, Revenue Streams, and R&D Allocation", sec_style))
    story.append(Paragraph(
        "In January 2025, NovaTech successfully closed its Series B funding round, securing $45.0 million in equity capital led by Horizon CleanTech Ventures, "
        "with participation from Apex Robotics Fund and Nordic Technology Partners. This brought total cumulative capitalization to $72.5 million since inception. "
        "For Q3 2025, NovaTech posted record quarterly gross revenues of $18.4 million, reflecting a 42.1% year-over-year expansion compared to Q3 2024 ($12.95 million). "
        "Operating expenses for the quarter were $12.1 million, yielding a non-GAAP operating margin of 34.2%.",
        body_style
    ))
    story.append(Paragraph(
        "NovaTech allocates an unprecedented 34.0% of all gross revenues directly to foundational Research and Development (R&D), equivalent to $6.25 million in Q3 2025 alone. "
        "Capital expenditure for the upcoming 2026 European expansion initiative is budgeted at $12.0 million, earmarked for the completion of the Munich Applied Robotics Innovation Center. "
        "Cash reserves and short-term liquid investments as of September 30, 2025, stood at $38.7 million, ensuring over 30 months of operational runway at current burn rates.",
        body_style
    ))

    # 3. NovaSolar-X Photovoltaic Specifications
    story.append(Paragraph("3. NovaSolar-X Silicon-Perovskite Photovoltaic Modules", sec_style))
    story.append(Paragraph(
        "The NovaSolar-X series represents NovaTech's flagship renewable energy generation platform. "
        "Engineered using a monolithic silicon-perovskite tandem cell architecture, the premium industrial model (NS-520-QX) achieves an independently certified peak energy conversion efficiency of 28.4%. "
        "The tandem configuration incorporates a wide-bandgap (1.68 eV) metal-halide perovskite top absorber layered directly onto a textured bottom silicon heterojunction (SHJ) wafer (1.12 eV bandgap). "
        "This spectral splitting allows the module to harvest both high-energy blue photons and low-energy infrared photons with minimal thermalization loss.",
        body_style
    ))
    story.append(Paragraph(
        "Key physical and electrical parameters for Model NS-520-QX: Peak power output is 520 Watts under Standard Test Conditions (STC, 1000 W/m², AM 1.5G, 25°C). "
        "Open-circuit voltage (Voc) is 49.8 Volts, and short-circuit current (Isc) is 13.45 Amperes. "
        "The operational temperature coefficient is remarkably low at -0.28%/°C, allowing sustained efficiency in desert environments up to +85°C. "
        "Module dimensions are 2,094 mm by 1,038 mm with a dry weight of 24.2 kg. Each panel features dual 3.2 mm anti-reflective tempered glass with an IP68-rated bypass junction box.",
        body_style
    ))
    story.append(Paragraph(
        "The commercial warranty provides an industry-leading 30-Year Performance Guarantee, guaranteeing at least 87.5% of original rated power capacity at Year 30. "
        "Annual power degradation rate is constrained to less than 0.35% per year, facilitated by an atomic-layer-deposited (ALD) aluminum oxide passivation barrier that prevents moisture ingress.",
        body_style
    ))

    # 4. Project AeroGuide: Autonomous Drone Swarm Systems
    story.append(Paragraph("4. Project AeroGuide: Autonomous Swarm Robotics and Edge AI", sec_style))
    story.append(Paragraph(
        "Project AeroGuide comprises decentralized, cooperative autonomous micro-aerial vehicle (UAV) swarms designed for wilderness search-and-rescue, "
        "pipeline inspection, and post-disaster reconnaissance. "
        "The primary flight chassis (Model AG-400-UAV) utilizes a carbon-fiber reinforced polyetheretherketone (PEEK) airframe with an all-up takeoff weight (AUW) of 2.15 kg. "
        "Propulsion is delivered by four brushless DC motors (Model NV-2207) coupled with 7-inch low-noise trifoil carbon propellers, achieving a maximum sprint velocity of 85 km/h "
        "and a maximum sustained headwind resistance of 45 km/h (Beaufort scale 6).",
        body_style
    ))
    story.append(Paragraph(
        "Flight endurance is powered by a high-density 6S lithium-sulfur battery pack (6,200 mAh, 22.2V nominal), providing 45 minutes of active flight time with full sensor payload. "
        "The sensor suite includes a dual-spectrum optical-thermal gimbal combining a 48 MP Sony IMX586 visible light camera and a FLIR Boson 640x512 uncooled radiometric microbolometer. "
        "Additionally, an integrated solid-state micro-LiDAR module (905 nm wavelength, 70-meter range, 120° field of view) performs real-time 3D spatial mapping at 30 frames per second.",
        body_style
    ))

    # 5. NV-X2 Edge AI Neural Processing Unit
    story.append(Paragraph("5. NV-X2 Edge AI Neural Processor Hardware Specifications", sec_style))
    story.append(Paragraph(
        "Each AeroGuide UAV is controlled by the custom NovaEngine NV-X2 Edge AI Neural Processor, fabricated on TSMC's 7nm FinFET manufacturing node. "
        "The NV-X2 integrates an 8-core ARM Cortex-A78AE central processor running at 2.4 GHz, an embedded 24-core custom tensor processing unit (TPU) delivering 32.5 TOPS (INT8) "
        "of deep learning inference, and 16 GB of unified LPDDR5 memory with 102.4 GB/s memory bandwidth. "
        "The silicon package consumes a mere 14.5 Watts under peak neural inference loads, supported by dynamic voltage and frequency scaling (DVFS).",
        body_style
    ))
    story.append(Paragraph(
        "The onboard neural runtime executes real-time simultaneous localization and mapping (SLAM), cooperative collision avoidance, and automated thermal anomaly identification. "
        "The inference pipeline processes 4K video feeds at 60 fps with an end-to-end inference latency under 8.5 milliseconds for YOLO-v9 object detection models. "
        "Units communicate over a peer-to-peer 2.4/5.8 GHz dynamic mesh network without requiring centralized cloud servers or cellular base stations.",
        body_style
    ))

    # 6. NovaSync v3.2 Zero-Trust Distributed Networking Protocol
    story.append(Paragraph("6. NovaSync v3.2 Zero-Trust Distributed Protocol Architecture", sec_style))
    story.append(Paragraph(
        "NovaSync v3.2 is NovaTech's proprietary distributed data synchronization protocol engineered for mission-critical edge-to-cloud communication. "
        "It enforces an uncompromising Zero-Trust Network Architecture (ZTNA), requiring cryptographic micro-authentication for every inter-node packet transmission. "
        "The protocol utilizes AES-256-GCM symmetric payload encryption paired with elliptic-curve Diffie-Hellman (ECDH over Curve25519) key exchange and Ed25519 digital signatures.",
        body_style
    ))
    story.append(Paragraph(
        "To achieve rapid distributed agreement across bandwidth-constrained edge nodes, NovaSync implements a novel consensus algorithm termed 'Proof-of-State' (PoS-v2). "
        "Proof-of-State replaces compute-heavy proof-of-work with lightweight cryptographic state-hash attestations verified across distributed leaderless quorums. "
        "Empirical benchmarks across 10,000 active nodes demonstrate sustained network throughput of up to 10.4 Gbps with sub-5 millisecond end-to-end packet delivery latency. "
        "The protocol guarantees Byzantine Fault Tolerance (BFT) up to 33.3% compromised or partitioned network nodes.",
        body_style
    ))

    # 7. Environmental Sustainability & Circular Manufacturing
    story.append(Paragraph("7. Environmental Sustainability and Zero-Carbon Manufacturing", sec_style))
    story.append(Paragraph(
        "NovaTech operates under a strict Zero-Carbon Manufacturing Framework, certified under ISO 14001 environmental management protocols. "
        "The corporate sustainability target mandates achieving net-zero greenhouse gas emissions across Scope 1, Scope 2, and upstream Scope 3 supply chains by December 2027. "
        "Currently, 84% of all electrical energy consumed across NovaTech fabrication facilities originates from verified on-site solar arrays and certified green wind purchase agreements.",
        body_style
    ))
    story.append(Paragraph(
        "Industrial water consumption is mitigated through a closed-loop deionization and reverse-osmosis recycling plant, reducing net freshwater withdrawal by 82.5%. "
        "All structural aluminum utilized in NovaSolar-X frame extrusions is sourced from 100% post-consumer recycled aluminum billet, cutting embodied manufacturing carbon by 65%. "
        "All packaging materials are 100% biodegradable and compliant with European Union Packaging Directive 94/62/EC.",
        body_style
    ))

    # 8. Cybersecurity, Threat Mitigation & Cryptographic Compliance
    story.append(Paragraph("8. Cybersecurity, Threat Mitigation, and Compliance Frameworks", sec_style))
    story.append(Paragraph(
        "NovaTech systems adhere to rigorous cybersecurity defense matrices mapped directly to the NIST Cybersecurity Framework (CSF 2.0) and SOC 2 Type II criteria. "
        "All software builds undergo automated static application security testing (SAST), software composition analysis (SCA), and weekly penetration testing. "
        "The NovaTech Threat Response Center operates 24/7 continuous monitoring, maintaining a Mean Time to Detect (MTTD) of 4.2 minutes and a Mean Time to Remediate (MTTR) of 18 minutes for high-severity telemetry alerts.",
        body_style
    ))
    story.append(Paragraph(
        "In preparation for post-quantum cryptographic standards, NovaTech has initiated the migration of all internal communication channels to NIST-standardized quantum-resistant algorithms, "
        "specifically implementing ML-KEM (Kyber-768) for key establishment and ML-DSA (Dilithium-3) for digital document signing. "
        "Hardware security modules (HSM) deployed across server nodes are FIPS 140-3 Level 4 certified, ensuring tamper resistance against physical probe extraction.",
        body_style
    ))

    # 9. European Union Regulatory Compliance and Expansion
    story.append(Paragraph("9. European Market Expansion and Regulatory Milestones", sec_style))
    story.append(Paragraph(
        "NovaTech's strategic corporate roadmap identifies European Union market integration as its primary growth objective for 2026. "
        "The company has secured preliminary CE Mark certification and IEC 61215 / IEC 61730 international electrical safety certification for the NovaSolar-X photovoltaic panel line. "
        "Drone flight systems under Project AeroGuide comply fully with the European Union Aviation Safety Agency (EASA) Specific Category drone regulations and standard operational scenario STS-01.",
        body_style
    ))
    story.append(Paragraph(
        "The Munich Innovation Center, scheduled for full ribbon-cutting in Q2 2026, will house 250 specialized autonomous systems engineers and a state-of-the-art climate test chamber. "
        "NovaTech has formally partnered with the Technical University of Munich (TUM) to sponsor a five-year, €5.0 million collaborative research initiative in decentralized swarm intelligence.",
        body_style
    ))

    # 10. Thermal Management and Material Science
    story.append(Paragraph("10. Advanced Thermal Management and Material Science Innovations", sec_style))
    story.append(Paragraph(
        "Operating electronic systems in extreme thermal environments requires specialized material engineering. "
        "NovaTech's materials division has patented a multi-walled carbon nanotube (MWCNT) thermal interface material (TIM) that achieves an out-of-plane thermal conductivity of 18.5 W/m-K, "
        "representing a 4x improvement over standard commercial silicone-based thermal greases. "
        "This TIM is deployed inside the NV-X2 edge computing chassis, preventing thermal throttling even during prolonged flight at 45°C ambient desert temperatures.",
        body_style
    ))
    story.append(Paragraph(
        "For photovoltaic modules, NovaTech employs a micro-grooved anti-reflective hydrophobic coating with a water contact angle of 115°. "
        "This coating confers self-cleaning properties, allowing wind and light rain to remove 94% of accumulated desert dust particles, "
        "thereby eliminating up to 12% annual soiling energy losses commonly observed in arid region utility-scale solar farms.",
        body_style
    ))

    # 11. Edge-Compute Operating System & Firmware Architecture
    story.append(Paragraph("11. NovaOS Embedded Operating System and Real-Time Kernel", sec_style))
    story.append(Paragraph(
        "All NovaTech hardware units run NovaOS, an in-house real-time operating system (RTOS) built on a memory-safe Rust microkernel architecture. "
        "NovaOS enforces strict capability-based access control, isolating device drivers, network protocols, and application logic into distinct memory protection domains. "
        "Worst-case interrupt latency on the NV-X2 platform is guaranteed below 1.8 microseconds, meeting hard real-time criteria for high-speed robotic flight control.",
        body_style
    ))
    story.append(Paragraph(
        "Over-the-air (OTA) firmware updates are managed via dual A/B partition swapping with automated rollback upon boot failure or cryptographic signature mismatch. "
        "Firmware payloads are compressed using Zstandard (zstd) level 19 and signed using dual-key Ed25519/Dilithium-3 signatures, ensuring zero unauthorized code execution.",
        body_style
    ))

    # 12. Synthetic Evaluation Benchmark Protocol
    story.append(Paragraph("12. Benchmarking Protocol, Experimental Baseline Criteria, and Reproducibility", sec_style))
    story.append(Paragraph(
        "To rigorously benchmark retrieval-augmented generation and adaptive query routing, NovaTech maintains an open experimental protocol. "
        "The evaluation suite requires that all candidate retrieval algorithms—including BM25 lexical search, dense bi-encoder vector embeddings, Reciprocal Rank Fusion, "
        "and learned adaptive strategy selectors—be evaluated over identical document chunks with standardized rank cutoffs (k=3). "
        "Precision@3, Recall@3, Mean Reciprocal Rank (MRR), Normalized Discounted Cumulative Gain (nDCG@3), and Context Relevance must be computed strictly against pre-annotated gold-standard qrels.",
        body_style
    ))
    story.append(Paragraph(
        "To prevent statistical artifacts and degenerate testing, all hypothesis testing must report paired non-parametric Wilcoxon signed-rank test statistics "
        "supplemented by 95% bootstrap confidence intervals with a minimum of 10,000 resamples. "
        "Experiments must maintain a strict separation between training, validation, and held-out test query splits to ensure valid generalization measurements.",
        body_style
    ))

    doc.build(story)
    print(f"Comprehensive technical knowledge base PDF successfully built at: {pdf_path}")

def generate_sample_questions(txt_path: Path):
    """Generate sample test questions file."""
    txt_content = """# NovaTech Research Knowledge Base - Reference Test Queries
1. [Keyword-Heavy] NovaSync v3.2 zero-trust encryption AES-256-GCM throughput sub-5ms Proof-of-State PoS-v2
2. [Keyword-Heavy] NovaSolar-X Model NS-520-QX 28.4% efficiency 30-Year Performance Guarantee Voc 49.8V
3. [Keyword-Heavy] Project AeroGuide AG-400-UAV 85 km/h NV-2207 FLIR Boson 640x512 micro-LiDAR
4. [Semantic] How does the monolithic silicon-perovskite tandem design reduce thermalization energy losses?
5. [Semantic] Explain the cryptographic state-hash consensus mechanism used by NovaSync to achieve Byzantine Fault Tolerance.
6. [Semantic] Describe how the closed-loop water recycling plant and post-consumer recycled aluminum contribute to NovaTech's net-zero 2027 goal.
7. [Numerical] What are the Q3 2025 gross revenue, non-GAAP operating margin, and R&D allocation percentage?
8. [Numerical] What are the peak power output, Voc, and temperature coefficient of the Model NS-520-QX panel?
9. [Numerical] What are the TOPS, memory bandwidth in GB/s, and power consumption of the NV-X2 neural processor?
10. [Factual] Who are the Chief Executive Officer, Chief Technology Officer, and CFO of NovaTech?
11. [Factual] Where is NovaTech enterprise headquartered and where are its European engineering campuses?
12. [Factual] What quantum-resistant cryptographic algorithms (ML-KEM, ML-DSA) are being integrated into NovaTech hardware?
13. [Comparison] Compare the operational characteristics and hardware of NovaSolar-X solar panels with the AeroGuide drone swarm.
14. [Comparison] Compare the throughput and latency of NovaSync v3.2 with legacy enterprise distributed protocols.
15. [Multi-Part] What battery flight duration, sensor payloads, and neural processor specifications power Project AeroGuide?
16. [Multi-Part] How do NovaTech's sustainability targets align with its Q3 2025 financial investments and 2026 European expansion?
"""
    txt_path.write_text(txt_content, encoding='utf-8')
    print(f"Sample test questions generated at: {txt_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    pdf_out = base_dir / "NovaTech_Research_Knowledge_Base.pdf"
    txt_out = base_dir / "test_questions.txt"
    generate_sample_pdf(pdf_out)
    generate_sample_questions(txt_out)
