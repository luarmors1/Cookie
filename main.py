import requests
from colorama import Fore, Style

def exit_program():
    print("exitting program")
    exit()


def ask(prompt):
    answer = input(Fore.RED + "SHADOW-TOOLS>> " + Style.RESET_ALL + prompt)
    if answer.strip().casefold() == "exit":
        print("Exiting the program.")
        exit()
    return answer

print(Fore.CYAN + r"  /$$$$$$  /$$                       /$$                        " + Style.RESET_ALL)
print(Fore.CYAN + r" /$$__  $$| $$                      | $$                        " +    Fore.RED +"    [0] dc tokens" + Style.RESET_ALL)
print(Fore.CYAN + r"| $$  \__/| $$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$  /$$  /$$  /$$" +    Fore.RED +"    [1] lookup" + Style.RESET_ALL)
print(Fore.CYAN + r"|  $$$$$$ | $$__  $$ |____  $$ /$$__  $$ /$$__  $$| $$ | $$ | $$" +    Fore.RED +"    [2] spam" + Style.RESET_ALL)
print(Fore.CYAN + r" \____  $$| $$  \ $$  /$$$$$$$| $$  | $$| $$  \ $$| $$ | $$ | $$" +    Fore.RED +"    [3] delete" + Style.RESET_ALL)
print(Fore.CYAN + r" /$$  \ $$| $$  | $$ /$$__  $$| $$  | $$| $$  | $$| $$ | $$ | $$" +    Fore.RED +"    [4] edit" + Style.RESET_ALL)
print(Fore.CYAN + r"|  $$$$$$/| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$/|  $$$$$/$$$$/" +    Fore.RED +"    [5] raid (fixing)" + Style.RESET_ALL)
print(Fore.CYAN + r" \______/ |__/  |__/ \_______/ \_______/ \______/  \_____/\___/" +    Fore.RED +"     [6] exit" + Style.RESET_ALL) 
print("                                                                 ")                                                                                                                               
source = ask("enter your choice :").strip()

if source == "0":
    token = ask("enter your discord token :").strip()
    try:
        discord_token = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": token},
            timeout=10,
        )
        discord_token.raise_for_status()
        token_data = discord_token.json()
        print(f"connected to : {token_data.get('username')}")
        print(f"display name : {token_data.get('global_name')}")
        print(f"user id : {token_data.get('id')}")
    except requests.RequestException as exc:
        print(f"Invalid token or request failed: {exc}")

elif source == "1":
    webhook = ask("enter your webhook url :")
    discord_webhook = requests.get(webhook)
    webhook_data = discord_webhook.json()
    creator = webhook_data.get("user")
    print(f"Webhook connected to {webhook_data['name']}")
    print(f"Webhook ID: {webhook_data['id']}")
    if creator and creator.get("username"):
        print(f"created by : {creator['user']['username']}")
    else:
        print("username data failed to fetch")

elif not source.isdigit() or int(source) > 6:
    print("choose a number 0-6")
elif source == "2":
    webhook = ask("enter your webhook url :")
    message = ask("enter your message :")
    count = int(ask("amount of messages to send :"))
    send = {"content": message}
    for i in range(count):
        requests.post(webhook, json=send)
        print(f"sent message {i+1} of {count}")

elif source == "3":
    webhook = ask("enter your webhook url :")
    response = requests.get(webhook)
    data = response.json()
    webhook_name = data.get("name")
    new_name = f"{webhook_name} is gone :("
    requests.patch(webhook, json={"name": new_name})
    message = "webhook deleted. don't be sad im gone, be happy it started."
    send = {"content": message}
    requests.post(webhook, json=send)
    requests.delete(webhook)
    print("webhook deleted successfully")

elif source == "4":
    webhook = ask("enter your webhook url :")
    new_name = ask("enter new name for the webhook :")
    edit_data = {"name": new_name,}
    requests.patch(webhook, json=edit_data)
    message = f'webhook name changed to "{new_name}"!'
    send = {"content": message}
    requests.post(webhook, json=send)
    print(edit_data['name'] + " webhook edited successfully")

elif source == "5":
    webhooks = ask("enter webhooks spaced by commas :")
    choices = [item.strip() for item in webhooks.split(",") if item.strip()]
    with open("webhooks.txt", "w", encoding="utf-8") as file:
        for choice in choices:
            file.write(choice + "\n")
    message = "# R-A-I-D-E-D B-Y S-H-A-D-O-W https://discord.gg/duQJPVKDDY # R-A-I-D-E-D B-Y S-H-A-D-O-W https://discord.gg/duQJPVKDDY # R-A-I-D-E-D B-Y S-H-A-D-O-W https://discord.gg/duQJPVKDDY # R-A-I-D-E-D B-Y S-H-A-D-O-W https://discord.gg/duQJPVKDDY # R-A-I-D-E-D B-Y S-H-A-D-O-W https://discord.gg/duQJPVKDDY # R-A-I-D-E-D B-Y S-H-A-D-O-W https://discord.gg/duQJPVKDDY"
    send = {"content": message}
    print(f"you added {len(choices)} webhooks")
    answer = ask("wanna raid now?: ")
    if answer == "yes":
        count = int(ask("how many times to send raid messages :"))
        for i in range(count):
            with open("webhooks.txt", "r", encoding="utf-8") as file:
                webhook = file.readlines()
            requests.post(webhook, json=send)
            print(f"messages sent! {i+1} of {count}")
elif source == "6":
    exit_program()