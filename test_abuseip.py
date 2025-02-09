from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Get API Key and LINE Token from environment variables
API_KEY = os.getenv("ABUSEIPDB_API_KEY")
LINE_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

# API endpoint for blacklist data
url = "https://api.abuseipdb.com/api/v2/blacklist"

# Request headers for API call
headers = {
    "Key": API_KEY,
    "Accept": "application/json"
}

# Send GET request to API
response = requests.get(url, headers=headers)

# Check the response status
if response.status_code == 200:
    data = response.json()
    # Check if there are any dangerous IPs in the response
    if "data" in data:
        ip_count = len(data["data"])  # Number of IPs found
        print(f"Found a total of {ip_count} dangerous IP addresses")

        for ip_data in data["data"]:
            ip_address = ip_data["ipAddress"]
            abuse_confidence_score = ip_data["abuseConfidenceScore"]
            print(f"IP: {ip_address} - Abuse Confidence Score: {abuse_confidence_score}%")

            # Function to send LINE notifications
            def send_line_notify(message):
                url = "https://notify-api.line.me/api/notify"
                headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
                # title = "🚨 IP Status Alert"
                data = {"message": f"{message}"} 
                response = requests.post(url, headers=headers, data=data)
                if response.status_code == 200:
                    print("✅ Notification sent via LINE")
                else:
                    print("❌ Failed to send notification")

            # Send notification based on abuse confidence score
            if abuse_confidence_score > 50:
                send_line_notify(f"🚨 Dangerous IP found! IP: {ip_address}, Risk: {abuse_confidence_score}%")
            else:
                send_line_notify(f"🟢 This IP is safe: {ip_address}")
    else:
        print("❌ No dangerous IPs found in the API response")
else:
    print(f"❌ Error fetching data from API: {response.status_code}")
    print("API message:", response.text)
