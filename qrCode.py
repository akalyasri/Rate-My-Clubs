import qrcode

def generate_qr_code(user_email):
    # Generate a QR code based on user email or any other information
    qr_data = f"otpauth://totp/{user_email}?secret=your-secret-key"
    qr = qrcode.make(qr_data)
    qr.save(f"{user_email}_qrcode.png")  # Save the QR code as a PNG file

    return f"{user_email}_qrcode.png"

    pass
