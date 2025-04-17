import os
import time
import telnyx
from dotenv import load_dotenv
from pathlib import Path

# === Load Environment ===
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

telnyx.api_key = os.getenv("TELNYX_API_KEY")
if not telnyx.api_key:
    print("❌ TELNYX_API_KEY not found in .env")
    exit(1)

# === Area codes to search and buy from ===
AREA_CODES = [
    "763", "612", "952",     # Minnesota
    "305", "786", "954", "561",  # Florida (Miami/Fort Lauderdale/Palm Beach)
    "512", "737", "210", "254",  # Texas (Austin, San Antonio)
    "813", "656", "727", "941", "239",  # Florida (Tampa/Sarasota)
    "706", "762", "478", "770",  # Georgia
    "503", "971", "541", "458"   # Oregon
]

# === Step 1: Search numbers ===
found_numbers = []

print("�� Searching for available numbers in each area code...\n")

for code in AREA_CODES:
    try:
        result = telnyx.AvailablePhoneNumber.list(
            filter={
                "country_code": "US",
                "national_destination_code": code,
                "phone_number_type": "local",
                "features": "voice",
                "best_effort": True,
                "limit": 1
            }
        )
        if result.data:
            phone_number = result.data[0]["phone_number"]
            found_numbers.append(phone_number)
            print(f"✅ {code}: {phone_number}")
        else:
            print(f"❌ No number found for {code}")
    except Exception as e:
        print(f"❌ Error searching {code}: {e}")

# === Step 2: Confirm ===
if not found_numbers:
    print("\n❌ No numbers found — nothing to order.")
    exit(1)

print("\n�� Summary of numbers to purchase:")
for num in found_numbers:
    print(f"  - {num}")

confirm = input("\n�� Do you want to purchase all of these numbers? (y/n): ").strip().lower()
if confirm != "y":
    print("❌ Purchase cancelled.")
    exit(0)

# === Step 3: Order numbers with delay ===
print("\n�� Placing orders...")

for number in found_numbers:
    try:
        order = telnyx.NumberOrder.create(
            phone_numbers=[{"phone_number": number}],
            customer_reference="BULK-BUY"
        )
        print(f"✅ Ordered: {number} | Order ID: {order.id}")
    except Exception as e:
        print(f"❌ Failed to order {number}: {e}")
    time.sleep(5)

print("\n�� Done! All orders processed.")

