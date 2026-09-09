"""
Script to generate a pristine 3-Page Academic / Evaluation PDF Report for:
GenAI TAE 1: "Multi-Agent AI System for Personalized Health Coaching"
Authors / Group Project

Structure:
Page 1: 1. Introduction (Background, Problem Statement, Objectives, Multi-Agent Paradigm)
Page 2: 2. Methodology (System Architecture, Deterministic Engine, Agent Coordination, LLM Prompting)
Page 3: 3. Result (Work Done) (Implementation, Streamlit UI, Case Study Output, Evaluation, Conclusion)
"""

import os
import sys

def build_pdf(filename="GenAI_TAE1_Health_Coach_Report.pdf"):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
    )
    from reportlab.pdfgen import canvas

    # Page Geometry & Canvas for Running Headers/Footers
    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_decorations(num_pages)
                super().showPage()
            super().save()

        def draw_decorations(self, page_count):
            self.saveState()
            
            # Header Bar
            self.setFillColor(colors.HexColor("#0F172A")) # Dark Slate
            self.setFont("Helvetica-Bold", 8)
            self.drawString(40, 762, "GENAI TAE 1 : COURSE PROJECT EVALUATION REPORT")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(572, 762, "Multi-Agent Personalized Health Coaching")
            
            # Header Line
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(40, 755, 572, 755)

            # Footer Line
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(40, 42, 572, 42)

            # Footer text
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, 30, "AI Agents for Personalized Health & Wellness | Academic Submission")
            self.drawRightString(572, 30, f"Page {self._pageNumber} of {page_count}")
            
            self.restoreState()

    # Document setup with precise margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Custom typography & styles
    primary_color = colors.HexColor("#1E3A8A")   # Deep Blue
    secondary_color = colors.HexColor("#0D9488") # Teal
    dark_slate = colors.HexColor("#0F172A")
    body_color = colors.HexColor("#334155")
    card_bg = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=0,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=secondary_color,
        alignment=0,
        spaceAfter=6
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569")
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=15,
        textColor=primary_color,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=dark_slate,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.2,
        textColor=body_color,
        alignment=4, # Justified
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.3,
        leading=10.8,
        textColor=body_color,
        leftIndent=12,
        spaceAfter=2.5
    )

    code_callout = ParagraphStyle(
        'CodeCallout',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=dark_slate
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, META, & SECTION 1: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("AI Agents for Personalized Health Coaching", title_style))
    story.append(Paragraph("A Multi-Agent Generative AI Architecture with Deterministic Health Calculation Engines", subtitle_style))
    
    # Metadata Badge Box
    meta_table_data = [[
        Paragraph("<b>Course:</b> Generative AI (GenAI) — TAE 1", meta_style),
        Paragraph("<b>Framework:</b> Python, Streamlit, LLM APIs", meta_style),
        Paragraph("<b>Architecture:</b> Coordinator-Subagent Multi-Agent", meta_style)
    ]]
    meta_table = Table(meta_table_data, colWidths=[180, 175, 177])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 0.75, border_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # SECTION 1: INTRODUCTION
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=5, spaceBefore=1))

    story.append(Paragraph("<b>1.1 Background & Motivation</b>", h2_style))
    story.append(Paragraph(
        "Modern health and wellness management is inherently multi-faceted, requiring coordinated insights across clinical nutrition, physiological exercise science, and behavioral lifestyle recovery. Generic conversational Large Language Models (LLMs) often struggle in personalized wellness guidance due to a lack of domain compartmentalization, arithmetic inaccuracy in calculating metabolic requirements (such as BMR, TDEE, and macronutrient targets), and the generation of conflicting or generic advice without strict constraint enforcement.",
        body_style
    ))
    story.append(Paragraph(
        "To overcome these limitations, this project introduces a <b>Hybrid Multi-Agent Generative AI Framework</b> specifically engineered for personalized health coaching. By pairing a deterministic mathematical engine with autonomous domain-specialized agents (Nutrition, Fitness, and Lifestyle) under a Master Coordinator Agent, the system provides mathematically grounded, hyper-personalized, and safe daily health recommendations.",
        body_style
    ))

    story.append(Paragraph("<b>1.2 Problem Statement</b>", h2_style))
    story.append(Paragraph(
        "Monolithic single-agent chatbots present severe vulnerabilities when applied to wellness coaching:",
        body_style
    ))
    story.append(Paragraph("• <b>Domain Hallucination:</b> Unspecialized LLMs intermingle calorie calculation with exercise splits, leading to mathematically invalid diet regimens and dangerous macro ratios.", bullet_style))
    story.append(Paragraph("• <b>Lack of Contextual Grounding:</b> Off-the-shelf chatbots fail to persistently respect user constraints (such as vegetarian/vegan dietary habits, metabolic baselines, and age limitations).", bullet_style))
    story.append(Paragraph("• <b>Single Point of Failure:</b> Unstructured prompting lacks modular fallback mechanisms when external LLM API rate limits or network latencies occur.", bullet_style))

    story.append(Paragraph("<b>1.3 Key Objectives & Scope</b>", h2_style))
    story.append(Paragraph(
        "The primary objectives of this GenAI TAE 1 project include:",
        body_style
    ))
    story.append(Paragraph("1. <b>Multi-Agent Orchestration:</b> Formulate an asynchronous Coordinator-Subagent architecture that intelligently parses user queries and dispatches sub-tasks to dedicated specialist agents.", bullet_style))
    story.append(Paragraph("2. <b>Deterministic + Stochastic Hybridization:</b> Integrate scientific physiological formulas (Mifflin-St Jeor equation, TDEE activity multipliers, BMI classification) to ground LLM reasoning in verified clinical mathematics.", bullet_style))
    story.append(Paragraph("3. <b>Dual-Engine LLM Fallback:</b> Enable seamless execution with high-performance LLMs (Google Gemini 2.5/1.5 Flash, Groq LLaMA-3) along with an intelligent offline rule-based fallback engine.", bullet_style))
    story.append(Paragraph("4. <b>Interactive Clinical Dashboard:</b> Implement an intuitive, reactive Streamlit web interface with real-time biometric metrics, dynamic agent badges, and persistent state management.", bullet_style))

    # Page Break to Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: SECTION 2: METHODOLOGY
    # =========================================================================
    story.append(Paragraph("2. Methodology", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=5, spaceBefore=1))

    story.append(Paragraph("<b>2.1 System Architecture & Data Pipeline</b>", h2_style))
    story.append(Paragraph(
        "The system employs a hierarchical <b>Coordinator-Subagent Pattern</b>. When a user submits an inquiry alongside their profile metadata (Age, Gender, Height, Weight, Goal, Diet Preference, Activity Level), the input is processed through a sequential two-stage pipeline:",
        body_style
    ))

    # Architecture Summary Table
    arch_data = [
        [Paragraph("<b>Component Layer</b>", table_header), Paragraph("<b>Module / File</b>", table_header), Paragraph("<b>Functional Responsibility</b>", table_header)],
        [Paragraph("<b>1. Deterministic Engine</b>", table_cell), Paragraph("<code>utils/health_calc.py</code>", code_callout), Paragraph("Calculates BMI, BMR (Mifflin-St Jeor), TDEE, caloric shifts (-400/+300 kcal), and water intake.", table_cell)],
        [Paragraph("<b>2. Master Coordinator</b>", table_cell), Paragraph("<code>agents/coordinator_agent.py</code>", code_callout), Paragraph("Semantic intent routing, agent activation filtering, and multi-agent response synthesis.", table_cell)],
        [Paragraph("<b>3. Nutrition Specialist</b>", table_cell), Paragraph("<code>agents/nutrition_agent.py</code>", code_callout), Paragraph("Macro distributions, meal plans (Veg/Vegan/Non-Veg), and micronutrient timing.", table_cell)],
        [Paragraph("<b>4. Fitness Specialist</b>", table_cell), Paragraph("<code>agents/fitness_agent.py</code>", code_callout), Paragraph("Resistance/Cardio training splits, sets/reps, warm-up, and recovery protocols.", table_cell)],
        [Paragraph("<b>5. Lifestyle Specialist</b>", table_cell), Paragraph("<code>agents/lifestyle_agent.py</code>", code_callout), Paragraph("Circadian alignment, sleep hygiene protocols, hydration schedules, and box-breathing.", table_cell)],
        [Paragraph("<b>6. Storage & State</b>", table_cell), Paragraph("<code>utils/storage.py</code>", code_callout), Paragraph("Persistent JSON serialization of user profile biometric states and conversational history.", table_cell)]
    ]
    arch_table = Table(arch_data, colWidths=[110, 140, 282])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2.2 Deterministic Health Calculation Formulas</b>", h2_style))
    story.append(Paragraph(
        "To prevent arithmetic inaccuracies common in standard LLMs, biometric calculations are computed using exact clinical formulas before being injected into prompt contexts:",
        body_style
    ))
    story.append(Paragraph("• <b>Basal Metabolic Rate (BMR) [Mifflin-St Jeor Equation]:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<i>Men:</i> BMR = (10 × weight<sub>kg</sub>) + (6.25 × height<sub>cm</sub>) − (5 × age) + 5", code_callout))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<i>Women:</i> BMR = (10 × weight<sub>kg</sub>) + (6.25 × height<sub>cm</sub>) − (5 × age) − 161", code_callout))
    story.append(Paragraph("• <b>Total Daily Energy Expenditure (TDEE):</b> TDEE = BMR × Activity Multiplier [1.2 (Sedentary) to 1.9 (Extra Active)].", bullet_style))
    story.append(Paragraph("• <b>Caloric & Macro Targets:</b> Weight Loss applies a 400 kcal deficit (35% Protein, 40% Carb, 25% Fat); Muscle Gain applies a +300 kcal surplus (30% Protein, 45% Carb, 25% Fat).", bullet_style))

    story.append(Paragraph("<b>2.3 Coordinator Dispatch Logic & Prompt Engineering</b>", h2_style))
    story.append(Paragraph(
        "The Coordinator Agent evaluates incoming user prompts against semantic keyword patterns. Queries containing diet terms trigger the Nutrition Agent; exercise queries activate the Fitness Agent; sleep/hydration queries trigger the Lifestyle Agent. General queries simultaneously invoke all three sub-agents for comprehensive holistic coaching. Each agent is governed by strict system prompts enforcing safety constraints, dietary compliance, and explicit non-medical disclaimers.",
        body_style
    ))

    # Page Break to Page 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: SECTION 3: RESULT (WORK DONE) & CONCLUSION
    # =========================================================================
    story.append(Paragraph("3. Result (Work Done)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=5, spaceBefore=1))

    story.append(Paragraph("<b>3.1 Implemented Artifacts & User Interface</b>", h2_style))
    story.append(Paragraph(
        "The full multi-agent application was implemented, tested, and validated. The frontend features a sleek dark-themed <b>Glassmorphism UI</b> built with Streamlit and modern CSS typography (`Outfit`), offering high interactivity and visual clarity:",
        body_style
    ))
    story.append(Paragraph("• <b>Sidebar Biometric Onboarding:</b> Users input personal metrics (Age, Gender, Height, Weight, Activity, Diet, Goal, API Key) with instant real-time metric updates.", bullet_style))
    story.append(Paragraph("• <b>Live Biometric Metric Cards:</b> Displays BMI badge with health category, BMR, TDEE, Calorie Goal, and Daily Hydration target in Liters.", bullet_style))
    story.append(Paragraph("• <b>Interactive Multi-Agent Chat Console:</b> Displays transparent agent badges (🏷️ Nutrition Agent, 🏋️ Fitness Agent, 🌿 Lifestyle Agent) showing which agents contributed to each response.", bullet_style))

    story.append(Paragraph("<b>3.2 Sample Execution & Multi-Agent Collaboration Trace</b>", h2_style))

    # Sample Output Callout Box
    sample_box_data = [[
        Paragraph(
            "<b>Input User Query:</b> <i>\"I am a 22-year-old vegetarian wanting to build lean muscle. Give me a full daily plan.\"</i><br/>"
            "<b>Orchestration Result:</b> Coordinator identified cross-domain requirements and activated all 3 Specialist Agents.<br/>"
            "• <b>Nutrition Agent:</b> Calculated 2,450 kcal (+300 surplus), 183g Protein (Paneer, Tofu, Greek Yogurt, Dal, Whey), 275g Carbs, 68g Healthy Fats with timed meal schedules.<br/>"
            "• <b>Fitness Agent:</b> 4-day Hypertrophy split (Compound Push/Pull/Legs), 4 sets x 8-12 reps with 90s rest, warm-up and cool-down routines.<br/>"
            "• <b>Lifestyle Agent:</b> 3.4L hydration schedule, 8-hour sleep hygiene with 45-min blue light cutoff, and 4-4-4-4 box breathing.",
            ParagraphStyle('SampleText', parent=styles['Normal'], fontName='Helvetica', fontSize=7.8, leading=10.2, textColor=dark_slate)
        )
    ]]
    sample_box = Table(sample_box_data, colWidths=[532])
    sample_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(sample_box)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>3.3 Evaluation & Key Performance Highlights</b>", h2_style))
    
    # Comparison / Highlights Table
    comp_data = [
        [Paragraph("<b>Evaluation Metric</b>", table_header), Paragraph("<b>Standard Generic Chatbot</b>", table_header), Paragraph("<b>Proposed Multi-Agent System</b>", table_header)],
        [Paragraph("<b>Macro Accuracy</b>", table_cell), Paragraph("Approximated / Inconsistent arithmetic", table_cell), Paragraph("100% Grounded in Mifflin-St Jeor & exact grams", table_cell)],
        [Paragraph("<b>Dietary Adherence</b>", table_cell), Paragraph("Frequently hallucinates non-veg items", table_cell), Paragraph("Strict filtering strictly adhering to user diet", table_cell)],
        [Paragraph("<b>Offline Resilience</b>", table_cell), Paragraph("Fails completely without active API", table_cell), Paragraph("Smart deterministic rule fallback engine", table_cell)],
        [Paragraph("<b>Safety Protocols</b>", table_cell), Paragraph("Vague or missing warnings", table_cell), Paragraph("Enforced non-medical clinical disclaimer", table_cell)]
    ]
    comp_table = Table(comp_data, colWidths=[120, 206, 206])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>3.4 Conclusion & Future Work</b>", h2_style))
    story.append(Paragraph(
        "The project successfully demonstrates the effectiveness of multi-agent collaborative architectures for specialized Generative AI applications. By decoupling clinical nutrition, strength coaching, and behavioral lifestyle recovery into dedicated sub-agents backed by deterministic mathematical verification, the system achieves superior accuracy, personalization, and safety compared to conventional single-agent LLMs. Future extensions include wearable IoT integration (smartwatch heart-rate sync), continuous vision-based food meal calorie scanning, and long-term reinforcement learning from user feedback.",
        body_style
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    out_pdf = "GenAI_TAE1_Health_Coach_Report.pdf"
    if len(sys.argv) > 1:
        out_pdf = sys.argv[1]
    build_pdf(out_pdf)
