import sqlite3
from datetime import date, timedelta

class DataManager:
    def __init__(self):
        self.conn = sqlite3.connect('time_records.db')
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Create activities table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    category TEXT,
                    activity TEXT,
                    duration REAL
                )
            ''')

            # Create categories table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE
                )
            ''')

    def add_today_activity(self, category, activity, duration):
        today = str(date.today())
        self.add_activity(today, activity, duration, category)

    def add_activity(self, selected_date, activity, duration, category=None):
        with self.conn:
            self.conn.execute('''
                INSERT INTO activities (date, category, activity, duration) VALUES (?, ?, ?, ?)
            ''', (selected_date, category if category else "", activity, duration))

    def edit_activity(self, selected_date, activity, duration):
        with self.conn:
            self.conn.execute('''
                UPDATE activities SET duration=? WHERE date=? AND activity=?
            ''', (duration, selected_date, activity))

    def remove_activity(self, selected_date, activity):
        with self.conn:
            self.conn.execute('''
                DELETE FROM activities WHERE date=? AND activity=?
            ''', (selected_date, activity))

    def get_today_activities_grouped_by_category(self):
        today = str(date.today())
        cursor = self.conn.execute('''
            SELECT category, activity, SUM(duration) FROM activities WHERE date=? GROUP BY category, activity
        ''', (today,))
        data = {}
        for category, activity, duration in cursor.fetchall():
            if category not in data:
                data[category] = []
            data[category].append((activity, duration))
        return data

    def get_dates(self):
        cursor = self.conn.execute('''
            SELECT DISTINCT date FROM activities ORDER BY date DESC
        ''')
        return [row[0] for row in cursor.fetchall()]

    def get_activities_by_date(self, selected_date):
        cursor = self.conn.execute('''
            SELECT activity, duration FROM activities WHERE date=?
        ''', (selected_date,))
        return cursor.fetchall()

    # New Summary Methods for Different Time Ranges
    def get_last_7_days_summary(self):
        last_7_days = str(date.today() - timedelta(days=7))
        cursor = self.conn.execute('''
            SELECT date, category, SUM(duration) FROM activities
            WHERE date >= ? GROUP BY date, category ORDER BY date ASC
        ''', (last_7_days,))
        data = cursor.fetchall()
        summary = {}
        for record_date, category, duration in data:
            if record_date not in summary:
                summary[record_date] = {}
            summary[record_date][category] = duration
        return summary

    def get_last_30_days_summary(self):
        last_30_days = str(date.today() - timedelta(days=30))
        cursor = self.conn.execute('''
            SELECT date, category, SUM(duration) FROM activities
            WHERE date >= ? GROUP BY date, category ORDER BY date ASC
        ''', (last_30_days,))
        data = cursor.fetchall()
        summary = {}
        for record_date, category, duration in data:
            if record_date not in summary:
                summary[record_date] = {}
            summary[record_date][category] = duration
        return summary

    def get_last_365_days_summary(self):
        last_365_days = str(date.today() - timedelta(days=365))
        cursor = self.conn.execute('''
            SELECT date, category, SUM(duration) FROM activities
            WHERE date >= ? GROUP BY date, category ORDER BY date ASC
        ''', (last_365_days,))
        data = cursor.fetchall()
        summary = {}
        for record_date, category, duration in data:
            if record_date not in summary:
                summary[record_date] = {}
            summary[record_date][category] = duration
        return summary

    # Category Methods
    def add_category(self, category_name):
        try:
            with self.conn:
                self.conn.execute('''
                    INSERT INTO categories (name) VALUES (?)
                ''', (category_name,))
        except sqlite3.IntegrityError:
            pass  # Category already exists

    def get_categories(self):
        cursor = self.conn.execute('''
            SELECT name FROM categories
        ''')
        return [row[0] for row in cursor.fetchall()]

    def search_categories(self, search_term):
        cursor = self.conn.execute('''
            SELECT name FROM categories WHERE name LIKE ?
        ''', (f'%{search_term}%',))
        return [row[0] for row in cursor.fetchall()]

    def close(self):
        self.conn.close()

