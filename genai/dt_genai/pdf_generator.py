from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf_report(
    filename,
    scenario,
    analysis
):

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    # Clean markdown symbols
    clean_analysis = (
        analysis
        .replace("**", "")
        .replace("\n", "<br/>")
    )

    # Title
    content.append(
        Paragraph(
            "Decision Twin Business Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # Scenario
    content.append(
        Paragraph(
            f"<b>Scenario:</b> {scenario}",
            styles["BodyText"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # AI Analysis
    content.append(
        Paragraph(
            clean_analysis,
            styles["BodyText"]
        )
    )

    doc.build(content)

    return filename