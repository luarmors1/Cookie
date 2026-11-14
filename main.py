import requests

webhook = input("type webhook url: ")
print("1 webhook loaded")
webhook = input("more?: ")
if webhook.lower() == "y":
    input("type webhook url: ")
    print("2 webhooks loaded")
message = ("# R#A#I#D#E#D# B#Y# S#H#A#D#O#W#S# @everyone")
send = {"content": message}
raid = input("raid now? (y/n): ")
if raid.lower() == "y":
    print("Starting raid...")
    post = requests.post
    post(webhook, json=send)
    