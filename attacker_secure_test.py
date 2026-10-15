import time
import string

from timing_attack_fix import check_password, real_secret
characters = string.ascii_letters + string.digits 

known = ""
# number of times each guess will be tested
sample = 5

for position in range(len(real_secret)):
    best_char = ""
    longest_time = 0

    for char in characters:
        remaining = len(real_secret) - len(known) - 1
        guess = known + char + "X" *remaining

        measurement = []
        for _ in range(sample):
            start = time.perf_counter()
            check_password(guess)
            end = time.perf_counter()
            elapsed_time = end - start
            measurement.append (elapsed_time)
        average_time = sum(measurement) / len(measurement)   

        # if this character has the longest average time, save it as the most likely correct char
        if average_time > longest_time:
            longest_time = average_time
            best_char = char
    known += best_char
    print("Recovered words so far:", known )

print()
print("Final word: ", known)
print("Actual word: ", real_secret)
print("Attack successful: ", known == real_secret, "\n")
