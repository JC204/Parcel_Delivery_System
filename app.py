from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Customer, Parcel, Courier, TrackingUpdate
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parcel_delivery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/parcels/track/<tracking_number>', methods=['GET'])
def track_parcel(tracking_number):
    parcel = Parcel.query.filter_by(tracking_number=tracking_number).first()
    
    if not parcel:
        return jsonify({'error': 'Parcel not found'}), 404
    
    # Get tracking updates
    updates = [
        {
            'id': update.id,
            'status': update.status,
            'location': update.location,
            'description': update.description,
            'timestamp': update.timestamp.isoformat()
        }
        for update in parcel.tracking_updates
    ]
    
    return jsonify({
        'id': parcel.id,
        'tracking_number': parcel.tracking_number,
        'status': parcel.status,
        'weight': parcel.weight,
        'description': parcel.description,
        'created_at': parcel.created_at.isoformat(),
        'sender': {
            'id': parcel.sender.id,
            'name': parcel.sender.name,
            'email': parcel.sender.email,
            'phone': parcel.sender.phone,
            'address': parcel.sender.address
        },
        'recipient': {
            'id': parcel.recipient.id,
            'name': parcel.recipient.name,
            'email': parcel.recipient.email,
            'phone': parcel.recipient.phone,
            'address': parcel.recipient.address
        },
        'courier': {
            'id': parcel.courier.id,
            'name': parcel.courier.name,
            'phone': parcel.courier.phone
        } if parcel.courier else None,
        'tracking_updates': updates
    })

@app.route('/api/parcels', methods=['POST'])
def create_parcel():
    data = request.get_json()
    
    try:
        # Create sender
        sender = Customer(
            name=data['sender']['name'],
            email=data['sender']['email'],
            phone=data['sender']['phone'],
            address=data['sender']['address']
        )
        db.session.add(sender)
        
        # Create recipient
        recipient = Customer(
            name=data['recipient']['name'],
            email=data['recipient']['email'],
            phone=data['recipient']['phone'],
            address=data['recipient']['address']
        )
        db.session.add(recipient)
        
        # Generate tracking number
        tracking_number = str(uuid.uuid4())[:8].upper()
        
        # Create parcel
        parcel = Parcel(
            tracking_number=tracking_number,
            status='pending',
            weight=data['weight'],
            description=data['description'],
            sender=sender,
            recipient=recipient,
            created_at=datetime.utcnow()
        )
        db.session.add(parcel)
        
        # Add initial tracking update
        initial_update = TrackingUpdate(
            parcel=parcel,
            status='pending',
            location='Warehouse',
            description='Parcel registered in the system',
            timestamp=datetime.utcnow()
        )
        db.session.add(initial_update)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Parcel created successfully',
            'tracking_number': tracking_number
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/parcels/<tracking_number>/assign-courier', methods=['POST'])
def assign_courier(tracking_number):
    data = request.get_json()
    courier_id = data.get('courier_id')
    
    if not courier_id:
        return jsonify({'error': 'Courier ID is required'}), 400
        
    try:
        parcel = Parcel.query.filter_by(tracking_number=tracking_number).first()
        if not parcel:
            return jsonify({'error': 'Parcel not found'}), 404
            
        courier = Courier.query.get(courier_id)
        if not courier:
            return jsonify({'error': 'Courier not found'}), 404
            
        if courier.status != 'available':
            return jsonify({'error': 'Courier is not available'}), 400
            
        # Assign courier and update status
        parcel.courier = courier
        parcel.status = 'assigned'
        courier.status = 'busy'
        
        # Add tracking update
        update = TrackingUpdate(
            parcel=parcel,
            status='assigned',
            location='Warehouse',
            description=f'Assigned to courier: {courier.name}',
            timestamp=datetime.utcnow()
        )
        db.session.add(update)
        
        db.session.commit()
        
        return jsonify({'message': 'Courier assigned successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/parcels/<tracking_number>/update', methods=['POST'])
def add_tracking_update(tracking_number):
    data = request.get_json()
    
    try:
        parcel = Parcel.query.filter_by(tracking_number=tracking_number).first()
        if not parcel:
            return jsonify({'error': 'Parcel not found'}), 404
            
        # Add tracking update
        update = TrackingUpdate(
            parcel=parcel,
            status=data['status'],
            location=data['location'],
            description=data['description'],
            timestamp=datetime.utcnow()
        )
        db.session.add(update)
        
        # Update parcel status
        parcel.status = data['status']
        
        # If delivered, update courier status
        if data['status'] == 'delivered' and parcel.courier:
            parcel.courier.status = 'available'
        
        db.session.commit()
        
        return jsonify({'message': 'Tracking update added successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/couriers', methods=['GET'])
def get_available_couriers():
    couriers = Courier.query.filter_by(status='available').all()
    return jsonify([{
        'id': courier.id,
        'name': courier.name,
        'phone': courier.phone,
        'status': courier.status
    } for courier in couriers])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)