# Timing Side-Channel Attack: Exploitation and Mitigation
## Overview
This project demonstrates how timing differences in password comparison can leak information about a secret.
I started with a vulnerable comparison function that checks the password character by character. Since the function stops as soon as it finds a wrong character, guesses with more correct characters take slightly longer to process.
The project then shows how this timing difference can be used to recover the secret, how random timing noise affects the attack, and how `hmac.compare_digest()` can be used as a mitigation.
The project includes:
- a vulnerable password checker
- a timing attack that recovers the secret character by character
- a noisy version of the vulnerable checker
- repeated measurements and averaging
- a sample size experiment
- a local Flask API version
- a secure comparison using `hmac.compare_digest()`


## Project Structure
- `vulnerable_checker.py` - vulnerable password comparison
- `attacker.py` - basic timing attack
- `noisy_vulnerable_checker.py` - vulnerable checker with random timing noise
- `attacker_noisy.py` - timing attack against the noisy checker
- `sample_size_test.py` - tests different sample sizes and attack success rates
- `timing_attack_fix.py` - secure comparison using `hmac.compare_digest()`
- `attacker_secure_test.py` - tests the attack against the secure comparison
- `api_server.py` - local Flask API with vulnerable and secure endpoints
- `http_attacker.py` - timing attack through HTTP requests
- `http_attacker_secure.py` - timing attack against the secure HTTP endpoint
- `comparison_graph.py` - graph comparing vulnerable and secure timing behaviour
- `requirements.txt` - required Python packages


## Vulnerable Comparison
The vulnerable checker compares the input with the real secret one character at a time.
If a character is wrong, the function immediately returns `False`.
A small delay is added after each correct character, which creates a timing difference.
For example, `HXXXXXXXX` may take longer than `AXXXXXXXX`, and `HeXXXXXXX` may take longer than `HXXXXXXXX`.
This difference can be used by the attacker to guess the secret one character at a time.


## Timing Attack
The attacker tries every possible character for the current password position.
For each guess, it:
1. measures how long the comparison takes
2. repeats the measurement several times
3. calculates the average time
4. keeps the character with the longest average time
5. moves to the next position
Using the vulnerable checker, the attack was able to recover: `Hello1234`.


## Adding Timing Noise
To make the experiment less predictable, I added a small random delay: `random.uniform(0, 0.01)`.
This creates small timing variations, so one measurement may not always be reliable.


## Sample Size Experiment
I tested different sample sizes to see whether taking more timing measurements would make the attack more reliable.
For each sample size, the attack was repeated multiple times and the success rate was recorded.
The idea was to compare whether averaging more measurements helps reduce the effect of random timing noise.


## Local HTTP API
After testing the attack directly in Python, I created a local Flask API to make the setup closer to a client-server application.
The vulnerable endpoint is: `/check`.
The attacker sends password guesses using HTTP POST requests and measures the total request time.
Everything runs locally on my own machine using: `http://127.0.0.1:5000`.


## Mitigation
For the secure version, I used: `hmac.compare_digest()`
The secure endpoint is: `/check-secure`
When I ran the same timing attack against the secure endpoint, it failed to recover the real secret.


## Results
The project showed that:
- timing differences can leak information when secrets are compared character by character
- repeated measurements can help reduce the effect of noise
- the same idea can also be tested through a local HTTP API
- using `hmac.compare_digest()` makes the timing attack unreliable


## Installation
Install the required packages with: `pip install -r requirements.txt`


## Ethical Scope
This project was created only for learning and demonstration purposes.
All attacks were performed against code and local services running on my own machine.