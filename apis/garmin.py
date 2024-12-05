from garminconnect import Garmin
from dotenv import load_dotenv
import os

class GarminRequest:
    def __init__(self):
        load_dotenv()
        email = os.getenv('GARMIN_EMAIL')
        password = os.getenv('GARMIN_PASSWORD')

        # Initialize Garmin client
        self.client = Garmin(email, password)
        self.client.login()

    def request_date(self, date):
        """
        Input date datetime format
        Returns List[Tuple(name, duration)]
        """
        activities = self.client.get_activities_by_date(date.isoformat(), date.isoformat())
        print(activities)
        res = []
        for a in activities:
            res.append((a["activityName"], a["duration"] / 60 / 60))
        return res

