from app import app, db
from models import Customer, Parcel, Courier, TrackingUpdate

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add test couriers
        couriers = [
            Courier(
                name="John Doe",
                phone="+1234567890",
                status="available"
            ),
            Courier(
                name="Jane Smith",
                phone="+1987654321",
                status="available"
            )
        ]
        
        for courier in couriers:
            db.session.add(courier)
            
        db.session.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")