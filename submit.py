import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

SWARMS_API_KEY = os.getenv("SWARMS_API_KEY")
SOLANA_PUBLIC_KEY = os.getenv("SOLANA_PUBLIC_KEY")
SOLANA_PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")

headers = {
    "Authorization": f"Bearer {SWARMS_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Origin": "https://swarms.world",
    "Referer": "https://swarms.world/"
}

response = requests.get(
    "https://swarms.world/api/query-agents",
    headers=headers,
    timeout=30
)

print(f"Status: {response.status_code}")
print(response.text[:500])
