import qrcode
import os
from PIL import Image
from qrcode.constants import ERROR_CORRECT_L
import qrcode.constants

def generate_general_qr():
    # The URL the QR should link to
    scan_url ="http://127.0.0.1:8000/check-in/"  # Use your localhost URL for testing
    folder = "media/qrcodes"  # Folder to store the image
    os.makedirs(folder, exist_ok=True)

    # qr =qrcode.QRCode(
    #     version= 1,
    #     box_size= 10,
    #     border=4,
    #     error_correction=qrcode.constants.ERROR_CORRECT_L
    # )
    # qr.add_data(scan_url)
    # qr.make(fit=True)


    img = qrcode.make(scan_url)
    file_path = os.path.join(folder, "general_qrcode.png")
    img.save(file_path)  # type: ignore
    
    print("✅ QR saved!")

    
generate_general_qr()
