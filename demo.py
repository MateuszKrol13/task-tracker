import requests

BASE = "http://127.0.0.1:5050/"

response = requests.get(BASE + "tasks" )
print(response.json())
input()

response =requests.patch(BASE + "tasks/1")
print("Entries length: ")
input()

response = requests.post(BASE + "tasks", json={
    "title": "restAPI task",
    "due": "tomorrow",
    "time_est" : "3 hours",
    "description" : "Lorem Ipsum...",
    "priority" : -2,
})
print(response)
