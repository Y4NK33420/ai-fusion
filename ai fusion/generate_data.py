# generate_data.py
from app import app, db, MedicalItems
from random import randint, uniform

def generate_data():
    with app.app_context():
        # Fictitious medical item names
        item_names = ["Surgical Masks", "Gloves", "Antibiotics", "Bandages", "Scalpels", "Thermometers", "Blood Pressure Monitors", "IV Bags", "Stethoscopes", "Syringes"]

        # Generate 10 fictitious items and add them to the database
        for i in range(10):
            # Generate random latitude and longitude
            latitude = uniform(-90, 90)
            longitude = uniform(-180, 180)

            new_item = MedicalItems(
                item_name=item_names[randint(0, len(item_names) - 1)],
                quantity=randint(1, 1000),
                location='Hospital ' + str(i + 1),
                hub_name='Hub ' + str(i + 1),
                latitude=latitude,
                longitude=longitude,
                urgency='High' if randint(0, 1) == 1 else 'Low'
            )
            db.session.add(new_item)

        # Commit the changes to the database
        db.session.commit()

        print("Data added successfully!")

if __name__ == '__main__':
    generate_data()
