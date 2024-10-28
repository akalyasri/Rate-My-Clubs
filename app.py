from flask import Flask, render_template, request, redirect, url_for
from qrCode import generate_qr_code as generate_review_qr_code
from twoFA import generate_qr_code as generate_2fa_qr_code
from database import create_app, db, User, Club, Review  # Adjusted import for database setup

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.db'  # Set your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_email = request.form.get('email')

        # Generate a 2FA QR code
        qr_code_path = generate_2fa_qr_code(user_email)

        return render_template('2fa.html', qr_code_path=qr_code_path)

    return render_template('signup.html')  # Render the signup page for GET requests

@app.route('/2fa-handler', methods=['POST'])
def twofa_handler():
    code = request.form['2fa-code']
    # Verify the 2FA code logic goes here...
    return redirect(url_for('home'))  # Redirect to home or appropriate page

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_review', methods=['POST'])
def submit_review():
    club_name = request.form.get('club_name')
    rating = request.form.get('rating')
    review = request.form.get('review')

    # Use your database logic to save the review
    # Ensure you have a valid club ID instead of club_name
    club = Club.query.filter_by(name=club_name).first()
    if club:  # Check if the club exists
        new_review = Review(club_id=club.id, rating=rating, comment=review)
        db.session.add(new_review)
        db.session.commit()

    return redirect(url_for('home'))

def get_clubs(college_name, location):
    # Using SQLAlchemy to query the database
    return Club.query.filter(
        Club.name.ilike(f'%{college_name}%'),
        Club.location.ilike(f'%{location}%')
    ).all()

@app.route('/search', methods=['POST'])
def search():
    college_name = request.form.get('college_name')
    location = request.form.get('location')
    
    clubs = get_clubs(college_name, location)
    
    return render_template('results.html', college_name=college_name, location=location, clubs=clubs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    