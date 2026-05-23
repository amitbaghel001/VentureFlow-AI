"""
EXIMIUS AI — PDF Export
Generates institutional-quality investment memo PDFs via ReportLab.
"""

import io
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ── Colour palette ────────────────────────────────────────────────────────────
VOID       = colors.HexColor("#050810")
SURFACE    = colors.HexColor("#0D1117")
CARD       = colors.HexColor("#0F1629")
BORDER     = colors.HexColor("#1A2744")
INDIGO     = colors.HexColor("#4F6EF7")
CYAN       = colors.HexColor("#00D4FF")
EMERALD    = colors.HexColor("#10B981")
AMBER      = colors.HexColor("#F59E0B")
ROSE       = colors.HexColor("#F43F5E")
WHITE      = colors.HexColor("#F0F4FF")
GREY       = colors.HexColor("#8892B0")
DARK_GREY  = colors.HexColor("#4A5568")

# ── Style builders ────────────────────────────────────────────────────────────

def _build_styles() -> dict[str, ParagraphStyle]:
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=28,
            textColor=WHITE,
            alignment=TA_CENTER,
            leading=34,
            spaceAfter=6,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName="Helvetica",
            fontSize=10,
            textColor=GREY,
            alignment=TA_CENTER,
            leading=14,
            spaceAfter=4,
        ),
        "section_label": ParagraphStyle(
            "section_label",
            fontName="Helvetica-Bold",
            fontSize=7,
            textColor=INDIGO,
            leading=10,
            spaceBefore=16,
            spaceAfter=6,
            leftIndent=0,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=GREY,
            leading=15,
            alignment=TA_JUSTIFY,
            spaceAfter=4,
        ),
        "body_white": ParagraphStyle(
            "body_white",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=WHITE,
            leading=15,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=9,
            textColor=GREY,
            leading=14,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=3,
        ),
        "score_label": ParagraphStyle(
            "score_label",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=CYAN,
            leading=12,
        ),
        "rec_invest": ParagraphStyle(
            "rec_invest",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=EMERALD,
            leading=16,
        ),
        "rec_pass": ParagraphStyle(
            "rec_pass",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=ROSE,
            leading=16,
        ),
        "rec_monitor": ParagraphStyle(
            "rec_monitor",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=AMBER,
            leading=16,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=7,
            textColor=DARK_GREY,
            alignment=TA_CENTER,
            leading=10,
        ),
    }


def _hr() -> HRFlowable:
    return HRFlowable(
        width="100%", thickness=0.5, color=BORDER, spaceAfter=8, spaceBefore=4
    )


def _section(label: str, styles: dict) -> Paragraph:
    return Paragraph(label.upper(), styles["section_label"])


def _bullet_list(items: list[str], styles: dict) -> list[Paragraph]:
    return [Paragraph(f"• {item}", styles["bullet"]) for item in items]


def _score_row(label: str, score: int, styles: dict) -> Table:
    """Single score bar as a mini table."""
    filled = int(score / 5)  # out of 20 cells
    bar = "█" * filled + "░" * (20 - filled)
    data = [[
        Paragraph(label, styles["bullet"]),
        Paragraph(f'<font color="#4F6EF7">{bar}</font>  {score}', styles["score_label"]),
    ]]
    tbl = Table(data, colWidths=[70 * mm, 110 * mm])
    tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return tbl


# ── Main export function ──────────────────────────────────────────────────────

def generate_memo_pdf(memo_data: dict[str, Any], startup_data: dict[str, Any] | None = None) -> bytes:
    """
    Generate a professional investment memo PDF.
    Returns raw bytes suitable for st.download_button.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = _build_styles()
    story = []

    company = memo_data.get("company_name", "Unknown Company")
    date_str = datetime.now().strftime("%B %d, %Y")
    recommendation = memo_data.get("investment_recommendation", "MONITOR").upper()

    # ── COVER SECTION ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph("EXIMIUS AI", ParagraphStyle(
        "brand", fontName="Helvetica-Bold", fontSize=9,
        textColor=INDIGO, alignment=TA_CENTER, spaceAfter=8,
    )))
    story.append(Paragraph("INVESTMENT COMMITTEE MEMORANDUM", ParagraphStyle(
        "ic_label", fontName="Helvetica", fontSize=8,
        textColor=GREY, alignment=TA_CENTER, spaceAfter=20,
        letterSpacing=2,
    )))
    story.append(_hr())
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(company, styles["cover_title"]))
    story.append(Paragraph(
        memo_data.get("deal_stage", "Early Stage"), styles["cover_sub"]
    ))
    story.append(Paragraph(f"Memo Date: {date_str}", styles["cover_sub"]))
    story.append(Spacer(1, 6 * mm))

    # Recommendation badge
    rec_style_map = {
        "INVEST":  styles["rec_invest"],
        "PASS":    styles["rec_pass"],
        "MONITOR": styles["rec_monitor"],
    }
    rec_style = rec_style_map.get(recommendation, styles["rec_monitor"])
    icons = {"INVEST": "▲ INVEST", "PASS": "▼ PASS", "MONITOR": "◈ MONITOR"}
    story.append(Paragraph(icons.get(recommendation, recommendation), rec_style))
    story.append(Spacer(1, 6 * mm))
    story.append(_hr())
    story.append(Spacer(1, 4 * mm))

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────
    story.append(_section("Executive Summary", styles))
    story.append(Paragraph(memo_data.get("executive_summary", ""), styles["body"]))
    story.append(Spacer(1, 3 * mm))

    # ── SCORE BREAKDOWN (if startup data provided) ────────────────────────────
    if startup_data and startup_data.get("score_breakdown"):
        story.append(_section("Investment Scoring", styles))
        sb = startup_data["score_breakdown"]
        dim_map = {
            "market_opportunity": "Market Opportunity",
            "product_differentiation": "Product Differentiation",
            "team_signals": "Team Signals",
            "traction_quality": "Traction Quality",
            "competitive_positioning": "Competitive Positioning",
        }
        for key, label in dim_map.items():
            val = sb.get(key, 50)
            story.append(_score_row(label, val, styles))
        story.append(Paragraph(
            f"Composite Investment Score: {startup_data.get('investment_score', 0)}/100",
            styles["score_label"],
        ))
        story.append(Spacer(1, 3 * mm))

    # ── MARKET OPPORTUNITY ────────────────────────────────────────────────────
    story.append(_section("Market Opportunity", styles))
    story.append(Paragraph(memo_data.get("market_opportunity", ""), styles["body"]))

    # ── PRODUCT & TECHNOLOGY ──────────────────────────────────────────────────
    story.append(_section("Product & Technology", styles))
    story.append(Paragraph(memo_data.get("product_technology", ""), styles["body"]))

    # ── TEAM ASSESSMENT ───────────────────────────────────────────────────────
    story.append(_section("Team Assessment", styles))
    story.append(Paragraph(memo_data.get("team_assessment", ""), styles["body"]))

    # ── TRACTION ──────────────────────────────────────────────────────────────
    story.append(_section("Traction & Validation", styles))
    story.append(Paragraph(memo_data.get("traction_metrics", ""), styles["body"]))

    # ── COMPETITIVE LANDSCAPE ─────────────────────────────────────────────────
    story.append(_section("Competitive Landscape", styles))
    story.append(Paragraph(memo_data.get("competitive_landscape", ""), styles["body"]))

    # ── BULL / BEAR ───────────────────────────────────────────────────────────
    story.append(_section("Bull Case", styles))
    story.append(Paragraph(memo_data.get("bull_case", ""), styles["body"]))

    story.append(_section("Bear Case", styles))
    story.append(Paragraph(memo_data.get("bear_case", ""), styles["body"]))

    # ── KEY RISKS ─────────────────────────────────────────────────────────────
    story.append(_section("Key Risks", styles))
    for risk in memo_data.get("key_risks", []):
        story.append(Paragraph(f"• {risk}", styles["bullet"]))

    # ── RECOMMENDATION ────────────────────────────────────────────────────────
    story.append(_section("Investment Recommendation", styles))
    story.append(Paragraph(icons.get(recommendation, recommendation), rec_style))
    story.append(Paragraph(memo_data.get("recommendation_rationale", ""), styles["body"]))
    story.append(Spacer(1, 3 * mm))

    # ── PROPOSED TERMS ────────────────────────────────────────────────────────
    if memo_data.get("proposed_terms_notes"):
        story.append(_section("Proposed Terms", styles))
        story.append(Paragraph(memo_data["proposed_terms_notes"], styles["body"]))

    # ── DILIGENCE QUESTIONS ───────────────────────────────────────────────────
    story.append(_section("Key Diligence Questions", styles))
    for i, q in enumerate(memo_data.get("key_diligence_questions", []), 1):
        story.append(Paragraph(f"{i}. {q}", styles["bullet"]))

    # ── NEXT STEPS ────────────────────────────────────────────────────────────
    story.append(_section("Next Steps", styles))
    for step in memo_data.get("next_steps", []):
        story.append(Paragraph(f"• {step}", styles["bullet"]))

    story.append(Spacer(1, 8 * mm))
    story.append(_hr())
    story.append(Paragraph(
        f"Generated by EXIMIUS AI · {date_str} · Confidential — Internal Use Only",
        styles["footer"],
    ))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
