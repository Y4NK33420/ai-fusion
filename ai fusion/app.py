from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import geodesic



app = Flask(__name__, static_folder = 'templates\static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_inventory.db'
db = SQLAlchemy(app)

# Define the models
class MedicalItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    hub_name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    urgency = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item_name = request.form['item_name']
        quantity = int(request.form['quantity'])
        location = request.form['location']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        urgency = request.form['urgency']

        # Find the closest hub
        closest_hub = find_closest_hub(location, latitude, longitude, quantity, urgency)

        # Render template with results
        return render_template('result.html', closest_hub=closest_hub)

    # Fetch available items from the inventory
    items = MedicalItems.query.all()

    return render_template('index.html', items=items)

def find_closest_hub(location, user_latitude, user_longitude, required_quantity, urgency):
    # Fetch all hubs from the database
    hubs = MedicalItems.query.distinct(MedicalItems.hub_name).all()
    
    # Initialize variables for storing nearest hub details
    nearest_hub_distance = float('inf')
    nearest_hub = None

    for hub in hubs:
        # Check if the hub has the required items in sufficient quantity and meets the urgency level
        if hub.quantity >= required_quantity and hub.urgency == urgency:
            hub_distance = calculate_distance((hub.latitude, hub.longitude), (user_latitude, user_longitude))

            # Update the nearest hub if this hub is closer
            if hub_distance < nearest_hub_distance:
                nearest_hub_distance = hub_distance
                nearest_hub = {
                    'hub_name': hub.hub_name,
                    'distance': hub_distance
                }

    return nearest_hub

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
