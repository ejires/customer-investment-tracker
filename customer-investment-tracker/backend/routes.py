from flask import Blueprint, request, jsonify

routes = Blueprint('routes', __name__)

# Sample customer data
customers = []

# Get all customers
@routes.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200

# Add a new customer
@routes.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"msg": "Missing name or email"}), 400
    
    new_customer = {
        "id": len(customers) + 1,
        "name": data['name'],
        "email": data['email']
    }
    customers.append(new_customer)
    
    return jsonify(new_customer), 201
if __name__ == "__main__":
    app.run(debug=True)

# Update customer
@routes.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = next((cust for cust in customers if cust["id"] == id), None)
    if not customer:
        return jsonify({"msg": "Customer not found"}), 404
    
    data = request.get_json()
    customer.update(data)
    return jsonify(customer), 200

# Delete customer
@routes.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    global customers
    customers = [cust for cust in customers if cust["id"] != id]
    return '', 204

