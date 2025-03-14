from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recyclehub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Listing model
class Listing(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # using UUID as string
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # e.g., "sell", "exchange", "donate"
    material = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'action': self.action,
            'material': self.material,
            'created_at': self.created_at.isoformat() + 'Z'
        }

# Create tables before the first request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to RecycleHub Marketplace API'})

# Retrieve all listings
@app.route('/listings', methods=['GET'])
def get_listings():
    listings = Listing.query.all()
    return jsonify([listing.to_dict() for listing in listings])

# Create a new listing
@app.route('/listings', methods=['POST'])
def create_listing():
    data = request.get_json()
    listing_id = str(uuid4())
    new_listing = Listing(
        id=listing_id,
        title=data.get('title'),
        description=data.get('description'),
        location=data.get('location'),
        action=data.get('action'),
        material=data.get('material')
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

# Update an existing listing
@app.route('/listings/<listing_id>', methods=['PUT'])
def update_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    data = request.get_json()
    listing.title = data.get('title', listing.title)
    listing.description = data.get('description', listing.description)
    listing.location = data.get('location', listing.location)
    listing.action = data.get('action', listing.action)
    listing.material = data.get('material', listing.material)
    
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
    # Create tables explicitly before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)