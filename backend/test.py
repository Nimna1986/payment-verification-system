from app.services.ocr_service import extract_text
from app.services.payment_parser import parse_payment_text


image_path = "uploads/payment_3.jpeg"

text = extract_text(image_path)

print("===== OCR RESULT =====")
print(text)
print("======================")

payment_data = parse_payment_text(text)

print()
print("===== PARSED PAYMENT =====")
print(payment_data)
print("==========================")