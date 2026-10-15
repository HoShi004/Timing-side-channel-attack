from flask import Flask, request, jsonify
import time
import random
import hmac

app = Flask(__name__)

real_secret = "Hello1234"


# vulnerable comparison function
def compare_function(user_input, real_secret):

    if len(user_input) != len(real_secret):
        return False

    for i in range(len(real_secret)):

        if user_input[i] != real_secret[i]:
            return False

        # intentional timing leak + small random noise
        time.sleep(0.05 + random.uniform(0, 0.01))

    return True


# secure comparison function
def secure_compare(user_input, real_secret):
    return hmac.compare_digest(user_input, real_secret)


# vulnerable API endpoint
@app.route("/check", methods=["POST"])
def check_password():

    data = request.get_json()

    password = data.get("password", "")

    result = compare_function(password, real_secret)

    return jsonify({
        "correct": result
    })


# secure API endpoint
@app.route("/check-secure", methods=["POST"])
def check_password_secure():

    data = request.get_json()

    password = data.get("password", "")

    result = secure_compare(password, real_secret)

    return jsonify({
        "correct": result
    })


if __name__ == "__main__":
    app.run(port=5000)