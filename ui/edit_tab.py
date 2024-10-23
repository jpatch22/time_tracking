import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from data.data_manager import DataManager

class EditTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.data_manager = DataManager()

        # Variables to hold form data
        self.date_var = tk.StringVar()
        self.activity_var = tk.StringVar()
        self.duration_var = tk.DoubleVar()
        self.selected_activity = tk.StringVar()

        # Select Date
        ttk.Label(self, text="Select Date:").grid(row=0, column=0, padx=10, pady=5)
        self.date_combobox = ttk.Combobox(self, textvariable=self.date_var)
        self.update_dates()
        self.date_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.date_combobox.bind("<<ComboboxSelected>>", self.update_activity_list)

        # List of Activities
        ttk.Label(self, text="Activities on Selected Date:").grid(row=1, column=0, padx=10, pady=5)
        self.activity_listbox = tk.Listbox(self, listvariable=self.selected_activity, selectmode=tk.SINGLE)
        self.activity_listbox.grid(row=1, column=1, padx=10, pady=5)
        self.activity_listbox.bind("<<ListboxSelect>>", self.populate_activity_details)

        # Duration Entry
        ttk.Label(self, text="Duration (hours):").grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(self, textvariable=self.duration_var).grid(row=2, column=1, padx=10, pady=5)

        # Buttons for Add, Edit, Remove Actions
        ttk.Button(self, text="Add Record", command=self.add_record).grid(row=3, column=0, pady=10)
        ttk.Button(self, text="Edit Record", command=self.edit_record).grid(row=3, column=1, pady=10)
        ttk.Button(self, text="Remove Record", command=self.remove_record).grid(row=3, column=2, pady=10)

    def update_dates(self):
        print("update dates")
        dates = self.data_manager.get_dates()
        self.date_combobox['values'] = dates

    def update_activity_list(self, event=None):
        selected_date = self.date_var.get()
        if selected_date:
            activities = self.data_manager.get_activities_by_date(selected_date)
            self.activity_listbox.delete(0, tk.END)
            for activity, category, duration in activities:
                self.activity_listbox.insert(tk.END, f"{category}: {activity} ({duration} hrs)")

    def populate_activity_details(self, event=None):
        try:
            index = self.activity_listbox.curselection()[0]
            selected = self.activity_listbox.get(index)
            activity_name, duration = selected.split(" (")
            duration = float(duration.split()[0])

            self.activity_var.set(activity_name)
            self.duration_var.set(duration)
        except IndexError:
            pass

    def add_record(self):
        selected_date = self.date_var.get()
        activity = self.activity_var.get()
        duration = self.duration_var.get()

        if selected_date and activity and duration > 0:
            self.data_manager.add_activity(selected_date, activity, duration)
            self.update_activity_list()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields correctly.")

    def edit_record(self):
        selected_date = self.date_var.get()
        activity = self.activity_var.get()
        duration = self.duration_var.get()

        if selected_date and activity and duration > 0:
            self.data_manager.edit_activity(selected_date, activity, duration)
            self.update_activity_list()
        else:
            messagebox.showwarning("Input Error", "Please select an activity and fill all fields correctly.")

    def remove_record(self):
        selected_date = self.date_var.get()
        if selected_date:
            try:
                index = self.activity_listbox.curselection()[0]
                selected = self.activity_listbox.get(index)
                activity_name = selected.split(" (")[0]

                self.data_manager.remove_activity(selected_date, activity_name)
                self.update_activity_list()
            except IndexError:
                messagebox.showwarning("Input Error", "Please select an activity to remove.")

