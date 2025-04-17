# 📞 Telnyx Bulk Number Ordering Script

This Python script automates the process of:

✅ Searching for available phone numbers from a list of area codes  
✅ Displaying and confirming the list of available numbers  
✅ Purchasing numbers **one by one** with a 5-second delay between each  
✅ Requires **only a valid Telnyx API key** — no connections or messaging profiles

---

## 📦 Features

- Loads Telnyx API credentials from `.env`
- Searches 1 number per custom area code (e.g. `305`, `512`, etc.)
- Uses `best_effort=true` to get fallback numbers if primary area code is exhausted
- Prompts for single confirmation before buying
- Orders each number with a 5-second delay
- Minimal dependencies: Telnyx SDK + dotenv

---

## 🔧 Requirements

- Python 3.7+
- Telnyx API key (you can get it from your [Telnyx Portal](https://portal.telnyx.com/))

Install dependencies:

```bash
pip install telnyx python-dotenv
````

Create a .env file in the same directory:
````
TELNYX_API_KEY=your_telnyx_api_key_here

````
✅ Notes
best_effort=true means Telnyx may return nearby or overlay area codes

You can customize the AREA_CODES list inside the script

This version does not require connection_id, messaging_profile_id, or billing_group_id

Ideal for sandbox/dev or default routing setups

📌 Coming Soon (optional features)
 CSV logging of orders and failures

 Retry logic for failed area codes

 Dry run / preview mode

 CLI flags to select exact or best-effort only
