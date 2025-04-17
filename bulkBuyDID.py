from __future__ import absolute_import, division, print_function
import os
import time
import telnyx
from dotenv import load_dotenv
from pathlib import Path

# Load API Key from .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

telnyx.api_key = os.getenv("TELNYX_API_KEY")
if not telnyx.api_key:
    print("TELNYX_API_KEY not found in .env file.")
    exit(1)

# Area codes to search
AREA_CODES = [
    "763", "612", "952",       # Minnesota
    "305", "786", "954", "561",  # Florida
    "512", "737", "210", "254",  # Texas
    "813", "656", "727", "941", "239",  # Florida
    "706", "762", "478", "770",  # Georgia
    "503", "971", "541", "458"   # Oregon
]

# Search for available numbers
found_numbers = []
print("Searching for available numbers...\n")

for area_code in AREA_CODES:
    try:
        result = telnyx.AvailablePhoneNumber.list(
            filter={
                "country_code": "US",
                "national_destination_code": area_code,
                "phone_number_type": "local",
                "features": "voice",
                "best_effort": True,
                "limit": 1
            }
        )
        if result.data:
            phone_number = result.data[0]["phone_number"]
            found_numbers.append(phone_number)
            print("Found for area code {}: {}".format(area_code, phone_number))
        else:
            print("No number found for area code {}".format(area_code))
    except Exception as e:
        print("Error searching for area code {}: {}".format(area_code, e))

# Confirm purchase
if not found_numbers:
    print("\nNo numbers found. Exiting.")
    exit(0)

print("\nSummary of numbers to purchase:")
for number in found_numbers:
    print(" - {}".format(number))

confirm = input("\nDo you want to order all of these numbers? (y/n): ").strip().lower()
if confirm != "y":
    print("Order cancelled.")
    exit(0)

# Place orders one by one
print("\nPlacing orders...\n")
for number in found_numbers:
    try:
        order = telnyx.NumberOrder.create(
            phone_numbers=[{"phone_number": number}],
            customer_reference="BULK-BUY"
        )
        print("Order placed: {} | Order ID: {}".format(number, order.id))
    except Exception as e:
        print("Failed to order {}: {}".format(number, e))
    time.sleep(5)

print("\nAll orders processed.")

