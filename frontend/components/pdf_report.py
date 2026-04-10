from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable
import os
from datetime import datetime


def generate_pdf_report(filename, prediction, confidence, decision,latency, spectrogram_path):

    output_path = "deepfake_report.pdf"
    doc = SimpleDocTemplate(output_path)

    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>AI Deepfake Audio Forensic Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    # Metadata
    elements.append(Paragraph(f"File Name: {filename}", styles["Normal"]))
    elements.append(Paragraph(f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))

    # Prediction Results
    elements.append(Paragraph(f"Prediction: <b>{prediction}</b>", styles["Normal"]))
    elements.append(Paragraph(f"Confidence: {confidence*100:.2f}%", styles["Normal"]))
    elements.append(Paragraph(f"Final Decision: <b>{decision}</b>", styles["Normal"]))
    elements.append(Paragraph(f"Inference Time: {latency:.3f} seconds", styles["Normal"]))
    elements.append(Spacer(1, 0.4 * inch))

    # Spectrogram
    if os.path.exists(spectrogram_path):
        elements.append(Paragraph("Forensic Spectrogram:", styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Image(spectrogram_path, width=5 * inch, height=3 * inch))

    elements.append(Spacer(1, 0.5 * inch))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(
        "This report was generated using a Hybrid CNN + Transformer "
        "Deepfake Detection Model for forensic security analysis.",
        styles["Normal"]
    ))

    doc.build(elements)

    return output_path