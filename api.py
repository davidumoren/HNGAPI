from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Helper function to check if a number is perfect
def is_perfect(n):
    if n < 2:
        return False
    sum_factors = sum(i for i in range(1, n) if n % i == 0)
    return sum_factors == n

# Helper function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    num_digits = len(digits)
    sum_powers = sum(d ** num_digits for d in digits)
    return sum_powers == n

# Helper function to calculate the sum of digits
def digit_sum(n):
    return sum(int(d) for d in str(n))

# Helper function to fetch a fun fact from the Numbers API
def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

# API endpoint to classify a number
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    # Input validation
    if not number or not number.lstrip('-').isdigit():
        return jsonify({"number": number, "error": True}), 400
    
    number = int(number)
    properties = []
    
    # Check if the number is Armstrong
    if is_armstrong(number):
        properties.append("armstrong")
    
    # Check if the number is odd or even
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    # Prepare the response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return jsonify(response), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)