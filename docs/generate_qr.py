import qrcode
from PIL import Image

# URL to encode
url = "https://github.com/Abhijeet0848/NewsLens"

# Create clean, flat, high-contrast QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=16,
    border=2,
)
qr.add_data(url)
qr.make(fit=True)

# Generate flat image
qr_img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
qr_img.save("docs/github_qr_flat.png")
print(f"Generated clean flat QR code for '{url}', size={qr_img.size}")
