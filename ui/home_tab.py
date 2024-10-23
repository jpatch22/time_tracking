import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from data.data_manager import DataManager

class HomeTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
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

        self.ax.clear()
        categories = list(data.keys())
        activities = {}
        
        # Collect the activity names and their corresponding durations under each category
        for category, activities_data in data.items():
            for activity, duration in activities_data:
                if activity not in activities:
                    activities[activity] = [0] * len(categories)
                activities[activity][categories.index(category)] = duration

        # Plot stacked bar chart
        bottom_values = [0] * len(categories)
        for activity, durations in activities.items():
            self.ax.bar(categories, durations, bottom=bottom_values, label=activity)
            bottom_values = [bottom_values[i] + durations[i] for i in range(len(durations))]

        self.ax.set_title('Stacked Time Spent Today by Categories')
        self.ax.set_ylabel('Hours')
        self.ax.legend()
        self.canvas.draw()

