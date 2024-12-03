from garminconnect import Garmin
from dotenv import load_dotenv
import os
import datetime

# Replace with your Garmin Connect credentials
load_dotenv()
email = os.getenv('GARMIN_EMAIL')
password = os.getenv('GARMIN_PASSWORD')

# Initialize Garmin client
client = Garmin(email, password)
client.login()

# Fetch activities
activities = client.get_activities(0, 10)  # Fetches the first 10 activities
for activity in activities:
    print(activity)

