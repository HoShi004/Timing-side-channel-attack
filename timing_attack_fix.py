import hmac

real_secret = "Hello1234"

def secure_compare(user_input, real_secret):
    return hmac.compare_digest(user_input, real_secret)

def check_password(password):
    return secure_compare(password, real_secret)