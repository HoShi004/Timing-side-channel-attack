import time
import matplotlib.pyplot as plt

from vulnerable_checker import check_password as vulnerable_check
from timing_attack_fix import check_password as secure_check
from vulnerable_checker import real_secret


# make test guesses automatically from the real secret
guesses = []

for i in range(len(real_secret) + 1):
    correct_part = real_secret[:i]
    remaining = "X" * (len(real_secret) - i)
    guess = correct_part + remaining
    guesses.append(guess)

# number of times each guess is measured 
sample = 10 
vulnerable_times = []
secure_times = []

for guess in guesses:
    vulnerable_measurements = []
    secure_measurements = []

    for _ in range(sample):
        start = time.perf_counter()
        vulnerable_check(guess)
        end = time.perf_counter()
        vulnerable_measurements.append(end - start)

        start = time.perf_counter()
        secure_check(guess)
        end = time.perf_counter()
        secure_measurements.append(end - start)

    vulnerable_average = sum(vulnerable_measurements)/len(vulnerable_measurements)
    secure_average = sum(secure_measurements)/len(secure_measurements)

    vulnerable_times.append(vulnerable_average)
    secure_times.append(secure_average)


# draw vulnerable timing line
plt.plot(
    guesses,
    vulnerable_times,
    marker = "o",
    linewidth=2.5
)

# draw secure timing line
plt.plot(
    guesses,
    secure_times,
    marker = "o",
    linewidth=2.5
)

# graph labels
plt.xlabel("Password Guess")
plt.ylabel("Time Taken (seconds)")
plt.title("Timing Side Channel: Vulnerable vs Secure Comparison")

# put line names at the end instead of using a legend box
plt.text(
    len(guesses) - 1,
    vulnerable_times[-1],
    "  Vulnerable",
    va="center",
    fontweight="bold"
)

plt.text(
    len(guesses) - 1,
    secure_times[-1],
    "  Secure",
    va="center",
    fontweight="bold"
)

# rotate password guesses
plt.xticks(rotation=45)

# cleaner graph look
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("timing_comparison.png", dpi=300, bbox_inches="tight")
plt.show()