"""
This Python code generates a QR code from a given URL and saves the image 
in the same directory as the script. The main functions of the code are:

1.URL for QR code: The URL to be encoded in the QR code is specified as the variable `url`.
   The user can change this URL directly in the code.

2.QR code settings: 
   - `version=1`: Defines the size of the QR code (the higher the number, the larger the QR code).
   - `error_correction=qrcode.constants.ERROR_CORRECT_L`: Specifies the degree of error correction, 
     which can recover up to 7% of the data.
   - `box_size=10`: Specifies the size of the individual boxes in the QR code.
   - `border=4`: Specifies the width of the border around the QR code.

3.Image generation: The QR code is created with a black fill and white background 
   and saved as a PNG image.

4.Image storage location: 
   - The image is saved in the same directory as the script.
   - The save path is determined dynamically with `os.path`.
"""
import qrcode
import os

url = "ENTER-HERE-THE_URL"

qr = qrcode.QRCode(
    version=1,  
    error_correction=qrcode.constants.ERROR_CORRECT_L,  
    box_size=10,  
    border=4, 
)

qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill="black", back_color="white")

script_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_directory, "qr_code.png")

img.save(image_path)

print(f"QR code image has been saved at: {image_path}")
