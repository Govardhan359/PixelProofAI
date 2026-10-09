import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def generate_report_pdf(analysis):
    buffer = io.BytesIO()
    
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "PixelProof AI - Forensic Analysis Report")
    
    # Draw a line below the title
    p.setLineWidth(1)
    p.line(50, height - 60, width - 50, height - 60)
    
    # Define bounding box for image
    img_x = 50
    img_y = height - 330
    img_width = 250
    img_height = 250
    
    # Image (Left column)
    if analysis.image:
        try:
            img = ImageReader(analysis.image.path)
            # By supplying both width and height with preserveAspectRatio, 
            # reportlab fits it perfectly inside the bounding box and anchors at the bottom-left of the box.
            p.drawImage(img, img_x, img_y, width=img_width, height=img_height, preserveAspectRatio=True)
            p.rect(img_x, img_y, img_width, img_height, stroke=1, fill=0)
        except Exception:
            p.setFont("Helvetica", 10)
            p.drawString(img_x, img_y + int(img_height/2), "(Image preview unavailable)")
            
    # Information (Right Column)
    text_start_x = 330
    current_y = height - 90
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(text_start_x, current_y, "File Information")
    current_y -= 25
    
    p.setFont("Helvetica", 10)
    # Truncate long UUIDs or filenames so they don't overrun page
    short_id = str(analysis.id)[:18] + "..." if len(str(analysis.id)) > 18 else str(analysis.id)
    p.drawString(text_start_x, current_y, f"Report ID: {short_id}")
    current_y -= 20
    
    from django.utils import timezone
    local_time = timezone.localtime(analysis.created_at)
    p.drawString(text_start_x, current_y, f"Date: {local_time.strftime('%A, %b %d %Y, %H:%M')}")
    current_y -= 20
    
    short_name = analysis.original_filename[:35] + "..." if len(analysis.original_filename) > 35 else analysis.original_filename
    p.drawString(text_start_x, current_y, f"Source File: {short_name}")
    current_y -= 40
    
    # Model Findings (Right Column continued)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(text_start_x, current_y, "Model Verdict")
    current_y -= 25
    
    p.setFont("Helvetica-Bold", 12)
    if analysis.predicted_class == 'human':
        p.setFillColorRGB(0.1, 0.6, 0.1) # Greenish
        pred_str = "Genuine Pattern (Human)"
    else:
        p.setFillColorRGB(0.8, 0.1, 0.1) # Reddish
        pred_str = "AI Generated (Artificial)"
        
    p.drawString(text_start_x, current_y, f"Prediction: {pred_str}")
    p.setFillColorRGB(0, 0, 0) # Reset to black
    current_y -= 25
    
    p.setFont("Helvetica", 11)
    if analysis.ai_percentage:
        p.drawString(text_start_x, current_y, f"AI Likelihood: {analysis.ai_percentage}%")
    current_y -= 20
    
    p.setFont("Helvetica", 10)
    p.drawString(text_start_x, current_y, f"Engine: {analysis.model_identifier}")
    current_y -= 20
    p.drawString(text_start_x, current_y, f"Version: {analysis.model_version}")
    current_y -= 20
    p.drawString(text_start_x, current_y, f"Inference Latency: {round(analysis.inference_duration, 4)}s")
    
    # Line Above Disclaimer
    p.line(50, 80, width - 50, 80)
    
    # Disclaimer at bottom
    p.setFont("Helvetica-Oblique", 9)
    p.setFillColorRGB(0.4, 0.4, 0.4)
    text = (
        "Disclaimer: This technical report constitutes a probabilistic model prediction based on "
        "learned detector constraints. It is strictly not an absolute proof of authenticity or fraud. "
    )
    p.drawString(50, 60, text)
    p.drawString(50, 48, "Outputs reflect feature alignment scores and should be used exclusively for forensic research prioritization.")
    
    # Close the PDF object cleanly
    p.showPage()
    p.save()
    
    # File buffer rewind
    buffer.seek(0)
    return buffer.read()
