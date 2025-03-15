from flask import Flask, jsonify, request, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recyclehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define the Listing model with an image_filename field
class Listing(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # using UUID as string
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # e.g., "sell", "exchange", "donate"
    material = db.Column(db.String(50), nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)  # For storing the image file name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'action': self.action,
            'material': self.material,
            'created_at': self.created_at.isoformat() + 'Z',
            'image_url': url_for('uploaded_file', filename=self.image_filename, _external=True) if self.image_filename else None
        }

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to RecycleHub Marketplace API'})

# Endpoint to serve uploaded images
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Retrieve all listings
@app.route('/listings', methods=['GET'])
def get_listings():
    listings = Listing.query.all()
    return jsonify([listing.to_dict() for listing in listings])

# Create a new listing with an optional image upload
@app.route('/listings', methods=['POST'])
def create_listing():
    # Use multipart/form-data for file upload along with form fields.
    title = request.form.get('title')
    description = request.form.get('description')
    location = request.form.get('location')
    action = request.form.get('action')
    material = request.form.get('material')

    # Validate required fields
    if not all([title, description, location, action, material]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Process the image file if provided
    file = request.files.get('image')
    image_filename = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_filename = filename
    elif file:
        return jsonify({'error': 'File type not allowed'}), 400

    # Create the listing record
    listing_id = str(uuid4())
    new_listing = Listing(
        id=listing_id,
        title=title,
        description=description,
        location=location,
        action=action,
        material=material,
        image_filename=image_filename
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

    # Update text fields (image update can be added similarly)
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

if __name__ == '__main__':
    app.run(debug=True)
