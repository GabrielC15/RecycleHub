from flask import Flask, jsonify, request
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)

# In-memory store for listings
listings = {}

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to RecycleHub Marketplace API'})

# Retrieve all listings
@app.route('/listings', methods=['GET'])
def get_listings():
    return jsonify(list(listings.values()))

# Create a new listing
@app.route('/listings', methods=['POST'])
def create_listing():
    data = request.get_json()
    
    # Generate a unique ID for the listing
    listing_id = str(uuid4())
    
    # Create a new listing with required fields
    new_listing = {
        'id': listing_id,
        'title': data.get('title'),
        'description': data.get('description'),
        'location': data.get('location'),  # Address or geo-coordinates
        'action': data.get('action'),        # e.g., "sell", "exchange", "donate"
        'material': data.get('material'),    # e.g., "aluminum", "glass", etc.
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    listings[listing_id] = new_listing
    return jsonify(new_listing), 201

# Retrieve a single listing by ID
@app.route('/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    listing = listings.get(listing_id)
    if listing:
        return jsonify(listing)
    return jsonify({'error': 'Listing not found'}), 404

# Update an existing listing
@app.route('/listings/<listing_id>', methods=['PUT'])
def update_listing(listing_id):
    listing = listings.get(listing_id)
    if not listing:
        return jsonify({'error': 'Listing not found'}), 404
    
    data = request.get_json()
    # Update only provided fields
    listing['title'] = data.get('title', listing['title'])
    listing['description'] = data.get('description', listing['description'])
    listing['location'] = data.get('location', listing['location'])
    listing['action'] = data.get('action', listing['action'])
    listing['material'] = data.get('material', listing['material'])
    
    return jsonify(listing)

# Delete a listing
@app.route('/listings/<listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    if listing_id in listings:
        del listings[listing_id]
        return jsonify({'message': 'Listing deleted'}), 200
    return jsonify({'error': 'Listing not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
