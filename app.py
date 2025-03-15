from flask import Flask, jsonify, request, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# ---------------------
# Configuration
# ---------------------

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recyclehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize database
db = SQLAlchemy(app)

# ---------------------
# Helper Functions
# ---------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------
# Models
# ---------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # One-to-many relationship: one user can create many listings
    listings = db.relationship('Listing', backref='creator', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() + 'Z'
        }

class Listing(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # using UUID as string
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # e.g., "sell", "exchange", "donate"
    material = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)  # For storing the image file name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign key linking to the user who created the listing
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'action': self.action,
            'material': self.material,
            'created_at': self.created_at.isoformat() + 'Z',
            'user_id': self.user_id,
        }
        if self.image_filename:
            data['image_url'] = url_for('uploaded_file', filename=self.image_filename, _external=True)
        # Optionally include creator's username if needed:
        if self.creator:
            data['username'] = self.creator.username
        return data

# ---------------------
# Routes / Endpoints
# ---------------------

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to RecycleHub Marketplace API'})

# Serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Endpoint to retrieve all users (for testing)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# User signup endpoint
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if user already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'User already exists'}), 400

    password_hash = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

# Retrieve all listings
@app.route('/listings', methods=['GET'])
def get_listings():
    listings = Listing.query.all()
    return jsonify([listing.to_dict() for listing in listings])

# Create a new listing with optional image upload and user association
@app.route('/listings', methods=['POST'])
def create_listing():
    # Expecting multipart/form-data for file upload
    title = request.form.get('title')
    description = request.form.get('description')
    location = request.form.get('location')
    action = request.form.get('action')
    material = request.form.get('material')
    user_id = request.form.get('user_id')  # In a production app, derive this from authentication

    if not all([title, description, location, action, material, user_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user_id'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Process the image file if provided
    file = request.files.get('image')
    image_filename = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_filename = filename
    elif file:
        return jsonify({'error': 'File type not allowed'}), 400

    new_listing = Listing(
        id=str(uuid4()),
        title=title,
        description=description,
        location=location,
        action=action,
        material=material,
        image_filename=image_filename,
        user_id=user_id
    )
    db.session.add(new_listing)
    db.session.commit()
    return jsonify(new_listing.to_dict()), 201

# Retrieve a specific listing by ID
@app.route('/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if listing:
        return jsonify(listing.to_dict())
    return jsonify({'error': 'Listing not found'}), 404

# Update an existing listing (for simplicity, image update is not handled here)
@app.route('/listings/<listing_id>', methods=['PUT'])
def update_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404

    listing.title = request.form.get('title', listing.title)
    listing.description = request.form.get('description', listing.description)
    listing.location = request.form.get('location', listing.location)
    listing.action = request.form.get('action', listing.action)
    listing.material = request.form.get('material', listing.material)

    db.session.commit()
    return jsonify(listing.to_dict())

# Delete a listing
@app.route('/listings/<listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    db.session.delete(listing)
    db.session.commit()
    return jsonify({'message': 'Listing deleted'}), 200

# ---------------------
# Main Application Runner
# ---------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
