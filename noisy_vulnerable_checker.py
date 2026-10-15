import time 
import random

real_secret = "Hello1234"

def compare_function(user_input, real_secret):
    if len(user_input)!=len(real_secret):
        return False

    for i in range(len(real_secret)):
        if user_input[i] != real_secret[i]:
            return False
        # intentional delay after each correct character
        # creates timing leak for my demo
        time.sleep(0.05 + random.uniform(0,0.01)) 

    return True

def check_password(password):
    return compare_function(password, real_secret)

if __name__ == "__main__":
    while True:
        attacker_guess = input("Enter your guess: ")
        
        # start measuring how long the code took
        start = time.perf_counter()
        result = check_password(attacker_guess)
        end = time.perf_counter()
        elapsed_time = end - start
        print("Password Correct:", result)
        print(f"Time Taken: {elapsed_time:.6f} seconds\n")