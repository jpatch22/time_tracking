import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from data.data_manager import DataManager

class SummaryTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.data_manager = DataManager()

        # Create a dropdown to select the summary range (e.g., last 7 days, month, year)
        self.range_var = tk.StringVar()
        self.range_combobox = ttk.Combobox(self, textvariable=self.range_var)
        self.range_combobox['values'] = ["Last 7 Days", "Last Month", "Last Year"]
        self.range_combobox.set("Last 7 Days")
        self.range_combobox.grid(row=0, column=0, padx=10, pady=10)
        self.range_combobox.bind("<<ComboboxSelected>>", self.update_chart)

        # Plot area for displaying the summary data
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

        self.update_chart()

    def update_chart(self, event=None):
        # Determine the range for the summary
        summary_range = self.range_var.get()
        if summary_range == "Last 7 Days":
            data = self.data_manager.get_last_7_days_summary()
        elif summary_range == "Last Month":
            data = self.data_manager.get_last_30_days_summary()
        elif summary_range == "Last Year":
            data = self.data_manager.get_last_365_days_summary()
        else:
            data = []

        # Clear the chart and draw new data
        self.ax.clear()
        if data:
            for day, activities in data.items():
                self.ax.bar(day, [sum(activities.values())], label=f"{day}")
            self.ax.set_title(f'{summary_range} Summary')
            self.ax.set_ylabel('Total Hours')
            self.ax.legend()
        else:
            self.ax.text(0.5, 0.5, "No Data Available", fontsize=12, ha='center')

        self.canvas.draw()

