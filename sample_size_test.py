import time
import string
import matplotlib.pyplot as plt

from noisy_vulnerable_checker import check_password, real_secret

characters = string.ascii_letters + string.digits + string.punctuation

sample_sizes = [1, 3, 5]
trials = 3

success_rates = []

for sample in sample_sizes:

    successful_attack = 0

    for trial in range(trials):

        known = ""

        for position in range(len(real_secret)):

            best_char = ""
            longest_time = 0

            for char in characters:

                remaining = len(real_secret) - len(known) - 1
                guess = known + char + "X" * remaining

                measurements = []

                for _ in range(sample):

                    start = time.perf_counter()
                    check_password(guess)
                    end = time.perf_counter()

                    measurements.append(end - start)

                average_time = sum(measurements) / len(measurements)

                if average_time > longest_time:
                    longest_time = average_time
                    best_char = char

            known += best_char

        if known == real_secret:
            successful_attack += 1

        print()
        print(
            "Sample:", sample, "\n",
            "Trial:", trial + 1, "\n",
            "Recovered:", known, "\n",
            "Success:", known == real_secret
        )

    success_rate = (successful_attack / trials) * 100
    success_rates.append(success_rate)

    print()
    print(
        "Sample size:", sample, "\n",
        "Successful attacks:", successful_attack, "/", trials, "\n",
        "Success rate:", success_rate, "%\n"
    )

print("Finished testing. Generating graph...")

plt.plot(
    sample_sizes,
    success_rates,
    marker="o",
    linewidth=2.5
)

plt.xlabel("Sample Size")
plt.ylabel("Attack Success Rate (%)")
plt.title("Effect of Sample Size on Noisy Timing Attack")

plt.xticks(sample_sizes)
plt.ylim(0, 100)

ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

plt.savefig(
    "sample_size_success_rate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()