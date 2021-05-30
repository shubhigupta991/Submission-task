import requests

url = 'http://127.0.0.1:8000/extract?src=https://storage.googleapis.com/bizupimg/profile_photo/918208896427%20GOODWELL%20LOGO.png'
response = requests.get(url)
response.json()