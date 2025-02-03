from flask import Flask, request, jsonify
import requests
import math

app = Flask(__name__)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(digit) for digit in str(n)]
    return sum(digit ** len(digits) for digit in digits) == n

def digit_sum(n):
    return sum(int(digit) for digit in str(n))

def get_fun_fact(number):
    response = requests.get(f"http://numbersapi.com/{number}/math")
    return response.text if response.status_code == 200 else "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = int(request.args.get('number'))
    except (ValueError, TypeError):
        return jsonify({"number": request.args.get('number'), "error": True}), 400

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("odd" if number % 2 else "even")

    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": number == sum([i for i in range(1, number) if number % i == 0]),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
