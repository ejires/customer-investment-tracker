from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from auth import auth  # Import your `auth` blueprint
from flask import request, jsonify  # Import necessary modules
# Import database connection (assuming you're using SQLAlchemy or similar)

# Initialize Flask app
app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)
customers = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "phone": "123-456-7890"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "phone": "987-654-3210"},
    {"id": 3, "name": "Dayo Paul", "email": "segskennysp@gmail.com", "phone": "806-535-9164"}
]

@app.route('/customers/search', methods=['GET'])
def search_customers():
    query = request.args.get('q', '')  # Retrieve the search query
    print(f"Search query received: {query}")  # Debugging log

    if not query:
        return jsonify({"message": "Search query is missing"}), 400

    try:
        # Search logic: filter the customers by name or email (case insensitive)
        results = [customer for customer in customers if query.lower() in customer['name'].lower() or query.lower() in customer['email'].lower()]
        
        # If no results, return a message
        if not results:
            return jsonify({"message": "No customers found matching your query"}), 404
        
        print(f"Search results: {results}")  # Debugging log
        return jsonify(results), 200  # Return the filtered customer data
        
    except Exception as e:
        print(f"Error while searching customers: {e}")  # Log the error
        return jsonify({"message": "Failed to search customers"}), 500


# Enable CORS for all routes
CORS(app)  # This will add `Access-Control-Allow-Origin` headers to all responses

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a strong secret key
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')  # Authentication routes

# Root route for testing
@app.route('/')
def home():
    return "Welcome to the Customer Investment Tracker!"

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)














