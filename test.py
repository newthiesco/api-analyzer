import requests

BASE_URL = "http://127.0.0.1:8000"

# Get agency sizes
resp = requests.get(f"{BASE_URL}/api/v1/agencies/size")
data = resp.json()
print("Agency Sizes:")
print(data)

# Trigger manual update
update = requests.get(f"{BASE_URL}/api/v1/update").json()
print("\nManual Update Result:")
print(update)

# Check health
health = requests.get(f"{BASE_URL}/api/v1/health").json()
print("\nHealth Check:")
print(health)
