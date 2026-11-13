import qrcode
import cv2

url = "https://github.com/Abhijeet0848/NewsScope"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=16,
    border=2,
)
qr.add_data(url)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
qr_img.save("docs/github_qr_flat.png")
print(f"Generated clean flat QR code for '{url}', size={qr_img.size}")

# Verify decoding
detector = cv2.QRCodeDetector()
val, _, _ = detector.detectAndDecode(cv2.imread("docs/github_qr_flat.png"))
print("Decoded verification:", val)
assert val == url, f"Decoded mismatch! Expected {url}, got {val}"
print("VERIFICATION PASSED: QR code decodes 100% to", url)
