from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

def create_resume_pdf(resume_text, template="Professional"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    base_styles = getSampleStyleSheet()

    # Customize styles based on template
    if template == "Modern":
        heading_style = ParagraphStyle(
            "Heading",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=colors.HexColor("#005f73"),
            spaceAfter=8
        )
        normal_style = ParagraphStyle(
            "Normal",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.black
        )
        bullet_style = ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leftIndent=12,
            bulletIndent=6,
            textColor=colors.HexColor("#0A9396")
        )
        
    elif template == "Creative":
        heading_style = ParagraphStyle(
            "Heading",
            parent=base_styles["Heading2"],
            fontName="Courier-Bold",
            fontSize=15,
            textColor=colors.HexColor("#1C1C1C"),
            spaceAfter=10
        )
        normal_style = ParagraphStyle(
            "Normal",
            parent=base_styles["Normal"],
            fontName="Courier",
            fontSize=10,
            textColor=colors.HexColor("#333333")
        )
        bullet_style = ParagraphStyle(
            "Bullet",
            parent=base_styles["Normal"],
            fontName="Courier",
            fontSize=10,
            leftIndent=12,
            bulletIndent=6,
            textColor=colors.HexColor("#4A90E2")
        )
    else:  # Default = Professional
        heading_style = base_styles["Heading2"]
        normal_style = base_styles["Normal"]
        bullet_style = base_styles["Bullet"]

    # Build the PDF
    flowables = []
    for line in resume_text.split("\n"):
        if line.strip() == "":
            flowables.append(Spacer(1, 10))
        elif line.strip().endswith(":"):
            flowables.append(Paragraph(f"<b>{line.strip()}</b>", heading_style))
        elif line.strip().startswith("-"):
            flowables.append(Paragraph(line.strip(), bullet_style))
        else:
            flowables.append(Paragraph(line.strip(), normal_style))

    doc.build(flowables)
    buffer.seek(0)
    return buffer



