import random
import string
import time

import requests

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
NAMES = 10               # Default number of usernames to save per platform
LENGTH = 5               # Random username length for generated names
FILE = "valid.txt"      # File where valid usernames are saved
WEBHOOK_URL = "https://discord.com/api/webhooks/1539287436801347584/RlpxN5zAQIu59t-FRIPnLGFrLzAIRi1pZuevdJwUpUQgK62dWhAmbw520uUrIvEVhAUZ"
BIRTHDAY = "1999-04-20" # Used only for Roblox validation
MAX_FAILURES = 10        # Stop a platform if it keeps failing repeatedly
MAX_TAKEN_IN_ROW = 100   # Stop automatically after 100 consecutive unavailable usernames
SUPPORTED_PLATFORMS = ["roblox", "twitter", "tiktok", "twitch", "youtube", "discord"]
TARGET_PLATFORMS = SUPPORTED_PLATFORMS

# -----------------------------------------------------------------------------
# Terminal colors
# -----------------------------------------------------------------------------
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    GRAY = "\033[90m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def make_pronounceable_username(length):
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    result = []

    for i in range(length):
        if i == 0:
            choices = consonants if random.random() < 0.7 else vowels
            letter = random.choice(choices)
        else:
            prev_is_vowel = result[-1] in vowels
            if prev_is_vowel:
                letter = random.choice(consonants)
            else:
                letter = random.choice(vowels) if random.random() < 0.45 else random.choice(consonants)

        result.append(letter)

    if all(ch not in vowels for ch in result):
        result[random.randrange(length)] = random.choice(vowels)

    return "".join(result)


def make_username(length, pronounceable=False):
    if pronounceable:
        return make_pronounceable_username(length)

    letters = string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def save_username(username, platform):
    with open(FILE, "a+", encoding="utf-8") as f:
        f.write(f"`{username}` is available on {platform}\n")


def clear_valid_file():
    with open(FILE, "w", encoding="utf-8") as f:
        f.write("")


def print_success(platform, username, found_count):
    message = f"`{username}` is available on {platform}"
    print(f"{bcolors.OKBLUE}[{found_count}/{NAMES}] [+] {message}{bcolors.ENDC}")


def print_taken(platform, username):
    print(f"{bcolors.FAIL}[-] {platform}: {username} is taken{bcolors.ENDC}")


# -----------------------------------------------------------------------------
# Platform-specific checks
# -----------------------------------------------------------------------------
def check_roblox_username(username):
    url = (
        "https://auth.roblox.com/v1/usernames/validate"
        f"?request.username={username}&request.birthday={BIRTHDAY}"
    )
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json().get("code") == 0


def check_twitter_username(username):
    # X/Twitter pages are not a guaranteed API, so this is a best-effort check.
    for base in ("https://x.com", "https://twitter.com"):
        url = f"{base}/{username}"
        response = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        text = response.text.lower()

        if response.status_code == 404:
            return True
        if "this account doesn't exist" in text or "page not found" in text or "user not found" in text:
            return True

    return False


def check_tiktok_username(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=8)
    text = response.text.lower()

    if response.status_code == 404:
        return True
    if "couldn't find this account" in text or "user not found" in text or "page not found" in text:
        return True
    return False


def check_twitch_username(username):
    url = f"https://www.twitch.tv/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=8)
    text = response.text.lower()

    if response.status_code == 404:
        return True
    if "page not found" in text or "channel not found" in text or "this channel does not exist" in text:
        return True
    return False


def check_youtube_username(username):
    url = f"https://www.youtube.com/@{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=8)
    text = response.text.lower()

    if response.status_code == 404:
        return True
    if "channel not found" in text or "this channel does not exist" in text or "page not found" in text:
        return True
    if '"robots"' in text and 'noindex' in text:
        return True
    return False


def check_discord_username(username):
    # Discord does not provide a public username availability API.
    # This is a placeholder so the script keeps the same structure.
    return False


def prompt_for_platforms():
    while True:
        answer = input(
            "Which site(s) do you want to check? "
            "Options: roblox, twitter, tiktok, twitch, youtube, discord, or all. "
            "Separate with commas: "
        ).strip().lower()

        if not answer:
            print("No site entered. Try again.")
            continue

        raw_values = [value.strip() for value in answer.replace(" ", "").split(",")]

        if "all" in raw_values:
            return SUPPORTED_PLATFORMS

        normalized = []
        for value in raw_values:
            if value == "x":
                value = "twitter"
            if value not in SUPPORTED_PLATFORMS:
                print(f"Invalid site: {value}. Valid choices: {', '.join(SUPPORTED_PLATFORMS)}")
                break
            if value not in normalized:
                normalized.append(value)
        else:
            return normalized


def prompt_for_length():
    while True:
        try:
            answer = input("How many characters? ").strip()
            length = int(answer)
            if length > 0:
                return length
            print("Length must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def prompt_for_pronounceable():
    while True:
        answer = input("pronounceable? ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please answer yes or no.")


def prompt_for_total_names():
    while True:
        try:
            answer = input("how many usernames to generate? ").strip()
            count = int(answer)
            if count > 0:
                return count
            print("Number must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def prompt_for_webhook():
    while True:
        answer = input("webhook? ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("Please answer yes or no.")


def send_usernames_to_webhook():
    if WEBHOOK_URL == "YOUR_WEBHOOK_HERE":
        print("Webhook URL not set. Replace YOUR_WEBHOOK_HERE in main.py with your actual webhook URL.")
        return False

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print("No usernames available to send.")
            return False

        response = requests.post(
            WEBHOOK_URL,
            json={"content": content},
            timeout=10,
        )
        response.raise_for_status()
        clear_valid_file()
        print(f"{bcolors.OKBLUE}[+] Sent available usernames to webhook and cleared valid.txt.{bcolors.ENDC}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"{bcolors.WARNING}[!] Failed to send usernames to webhook: {e}{bcolors.ENDC}")
        return False


def check_platform_username(username, platform):
    """Return True if the username is available.

    Roblox has a public API. Twitter/X, TikTok, Twitch, and YouTube are checked
    through public profile pages, which can be rate-limited or blocked.
    Discord does not offer a public username-availability check, so it is
    intentionally disabled here.
    """
    if platform == "roblox":
        return check_roblox_username(username)
    if platform == "twitter":
        return check_twitter_username(username)
    if platform == "tiktok":
        return check_tiktok_username(username)
    if platform == "twitch":
        return check_twitch_username(username)
    if platform == "youtube":
        return check_youtube_username(username)
    if platform == "discord":
        return check_discord_username(username)

    raise ValueError(f"Unsupported platform: {platform}")


# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
def main():
    selected_platforms = prompt_for_platforms()
    username_length = prompt_for_length()
    total_to_generate = prompt_for_total_names()
    pronounceable = prompt_for_pronounceable()
    send_webhook = prompt_for_webhook()
    print(f"{bcolors.HEADER}\nChecking: {', '.join(selected_platforms)}\nLength: {username_length}\nTotal: {total_to_generate}\nPronounceable: {pronounceable}\nWebhook: {send_webhook}{bcolors.ENDC}\n")

    if not send_webhook:
        print(f"{bcolors.WARNING}[!] Webhook disabled. Script will not send anything to Discord/webhook.{bcolors.ENDC}")

    for platform in selected_platforms:
        found = 0
        failures = 0
        taken_in_row = 0
        print(f"{bcolors.HEADER}\nChecking {platform} usernames...{bcolors.ENDC}")

        while found < total_to_generate:
            try:
                username = make_username(username_length, pronounceable=pronounceable)
                available = check_platform_username(username, platform)

                if available:
                    found += 1
                    failures = 0
                    taken_in_row = 0
                    print_success(platform, username, found)
                    save_username(username, platform)
                else:
                    taken_in_row += 1
                    print_taken(platform, username)

                    if taken_in_row >= MAX_TAKEN_IN_ROW:
                        print(f"{bcolors.WARNING}[!] 100 usernames taken in a row on {platform}. Stopping this site.{bcolors.ENDC}")
                        break

            except requests.exceptions.RequestException as e:
                failures += 1
                print(f"{bcolors.WARNING}Network error on {platform}: {e}{bcolors.ENDC}")
            except KeyboardInterrupt:
                print(f"\n{bcolors.WARNING}Interrupted by user. Stopping {platform}.{bcolors.ENDC}")
                return
            except Exception as e:
                failures += 1
                print(f"{bcolors.WARNING}Error on {platform}: {e}{bcolors.ENDC}")

            if failures >= MAX_FAILURES:
                print(f"{bcolors.WARNING}[!] Too many failures on {platform}. Stopping this site.{bcolors.ENDC}")
                break

            time.sleep(0.1)

        print(f"{bcolors.OKBLUE}[!] Finished checking {platform}.{bcolors.ENDC}\n")

    if send_webhook:
        send_usernames_to_webhook()


if __name__ == "__main__":
    main()

