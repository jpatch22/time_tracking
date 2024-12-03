import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from data.data_manager import DataManager
import numpy as np
from datetime import date, datetime

class HomeTab(ttk.Frame):
    def __init__(self, parent, garminRequest):
        super().__init__(parent)
        self.garminRequest = garminRequest
        self.data_manager = DataManager()

        self.activity_var = tk.StringVar()
        self.duration_var = tk.DoubleVar()
        self.category_var = tk.StringVar()

        # Dropdown for categories
        ttk.Label(self, text="Category:").grid(row=0, column=0, padx=10, pady=10)
        self.category_combobox = ttk.Combobox(self, textvariable=self.category_var)
        self.update_categories()
        self.category_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.category_combobox.bind("<KeyRelease>", self.on_category_search)

        # Button to add new category
        ttk.Button(self, text="Add New Category", command=self.add_category).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(self, text="Sync Garmin Activities", command=self.sync_garmin).grid(row=1, column=2, padx=10, pady=10)

        # Entry for recording new activity
        ttk.Label(self, text="Activity Name:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Entry(self, textvariable=self.activity_var).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self, text="Duration (hours):").grid(row=2, column=0, padx=10, pady=10)
        ttk.Entry(self, textvariable=self.duration_var).grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self, text="Add Record", command=self.add_record).grid(row=3, column=0, columnspan=3, pady=10)

        # Plot area for displaying current day's stacked bar chart
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3)

        self.update_chart()
    
    def on_category_search(self, event):
        search_term = self.category_var.get().lower()
        categories = self.data_manager.search_categories(search_term)
        self.category_combobox['values'] = categories

    def sync_garmin(self):
        selected_date = str(date.today())
        parsed_data = None
        try:
            parsed_data = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except:
            messagebox.showwarning("Input Error", "Please enter a valid date.")
            return
        activities = self.garminRequest.request_date(parsed_data)
        existingActivities = self.data_manager.get_activities_by_date(selected_date)
        try:
            for a in activities:
                actTuple = ("", a[0], a[1])
                print(actTuple)
                if actTuple in existingActivities:
                    continue
                self.data_manager.add_activity(selected_date, "", a[1], category=a[0])
                self.update_chart()  # Refresh the list
            messagebox.showinfo("Success", "Sync with Garmin Successful")
        except:
            messagebox.showinfo("Failure", "Something went wrong!")
    
    def add_category(self):
        new_category = self.category_var.get()
        if new_category:
            self.data_manager.add_category(new_category)
            self.update_categories()

    def update_categories(self):
        categories = self.data_manager.get_categories()
        self.category_combobox['values'] = categories

    def add_record(self):
        category = self.category_var.get()
        activity = self.activity_var.get()
        duration = self.duration_var.get()
        if activity and duration > 0 and category:
            self.data_manager.add_today_activity(category, activity, duration)
            self.update_chart()


    def update_chart(self):
        # Get today's activity data grouped by categories
        data = self.data_manager.get_today_activities_grouped_by_category()

        # Clear the previous plot
        self.ax.clear()
        
        categories = list(data.keys())
        activities = {}

        # Collect activity names and their durations by category
        for category, activities_data in data.items():
            for activity, duration in activities_data:
                if activity not in activities:
                    activities[activity] = [0] * len(categories)
                activities[activity][categories.index(category)] = duration

        # Define a color map (or you can manually assign colors if preferred)
        colors = plt.cm.get_cmap('tab20', len(categories))  # Using colormap for consistent category coloring

        # Initialize bottom positions for stacking
        bottom_values = np.zeros(len(categories))

        # Plot stacked bar chart
        for i, (activity, durations) in enumerate(activities.items()):
            bars = self.ax.bar(categories, durations, bottom=bottom_values, label=activity, color=colors(i))

            # Annotate activity name on top of each bar
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    self.ax.text(
                        bar.get_x() + bar.get_width() / 2,  # X-coordinate
                        bar.get_y() + height / 2,  # Y-coordinate (middle of the bar)
                        f'{activity}',  # Activity name as label
                        ha='center', va='center', fontsize=8, color='white', rotation=90
                    )

            # Update the bottom position for the next stacked bar
            bottom_values += durations

        # Set labels and title
        self.ax.set_title('Stacked Time Spent Today by Categories', fontsize=14)
        self.ax.set_ylabel('Hours', fontsize=12)
        self.ax.set_xticks(np.arange(len(categories)))
        self.ax.set_xticklabels(categories, fontsize=10, rotation=45, ha='right')

        # Add legend
        #self.ax.legend(title="Activities", bbox_to_anchor=(1.05, 1), loc='upper left')
        self.figure.tight_layout()

        # Draw the updated chart
        self.canvas.draw()

