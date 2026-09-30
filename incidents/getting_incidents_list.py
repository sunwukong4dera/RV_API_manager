from requests import get

response = get('https://link/api/v2/incidents/')
print(response.json())



