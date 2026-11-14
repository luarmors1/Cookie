import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_json(url, payload=None):
	data = None if payload is None else json.dumps(payload).encode("utf-8")
	headers = {"Content-Type": "application/json"} if data is not None else {}
	request = Request(url, data=data, headers=headers)
	with urlopen(request, timeout=15) as response:
		return json.load(response)


def main():
	username = input("Type Roblox username here - ").strip()
	if not username:
		print("Username cannot be empty.")
		return

	try:
		results = get_json(
			"https://users.roblox.com/v1/usernames/users",
			{"usernames": [username], "excludeBannedUsers": True},
		).get("data", [])
		if not results:
			print("Roblox username not found.")
			return

		user = results[0]
		friend_data = get_json(
			f"https://friends.roblox.com/v1/users/{user['id']}/friends/count"
		)
	except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
		print(f"Could not retrieve Roblox account information: {error}")
		return

	print(f"Username: {user['name']}")
	print(f"Display name: {user['displayName']}")
	print(f"Friends: {friend_data['count']}")
	answer = input("Want to unfriend everyone? (yes/no): ").strip().lower()
	if answer == "yes":
		print("This script only reports public information and cannot unfriend anyone.")
		print("No friends were removed. Manage your friends through Roblox directly.")
	elif answer == "no":
		print("No changes made.")
	else:
		print("Please answer yes or no. No changes made.")


if __name__ == "__main__":
	main()
