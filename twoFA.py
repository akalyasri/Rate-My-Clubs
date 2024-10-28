from flask import Flask, jsonify, request
import pyotp
import io
import base64
import qrcode

app = Flask(__name__)

# Dummy user storage
users = {}

@app.route('/signup', methods=['POST'])
def signup():
    # Get user data (username, password) from request
    data = request.get_json()
    username = data['username']

    # Generate a new secret key for the user
    secret = pyotp.random_base32()

    # Save the user with the secret (this is just a demo, you'd use a DB in production)
    users[username] = {'secret': secret, 'password': data['password']}

    # Generate the TOTP provisioning URL for Google Authenticator
    totp = pyotp.TOTP(secret)
    otp_auth_url = totp.provisioning_uri(username, issuer_name="ClubReviewApp")

    # Generate QR code for the URL
    qr = qrcode.make(otp_auth_url)

    # Convert QR code to base64 so we can send it to the frontend
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Return the base64 QR code to display in frontend
    return jsonify({
        'message': 'User registered successfully!',
        'qr_code_base64': qr_code_base64
    })

def generate_qr_code(user_email):
    # Generate a QR code based on user email or any other information
    secret = pyotp.random_base32()  # Generate a secret key
    qr_data = f"otpauth://totp/{user_email}?secret={secret}&issuer=ClubReviewApp"
    qr = qrcode.make(qr_data)
    
    # Convert QR code to base64
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return qr_code_base64  # Return the QR code as base64

if __name__ == '__main__':
    app.run(debug=True)
