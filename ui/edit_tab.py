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
        self.activity_var = tk.StringVar()  # To store the activity name
        self.category_var = tk.StringVar()  # To store the category name
        self.duration_var = tk.DoubleVar()
        self.selected_activity = tk.StringVar()

        # Select Date - with Combobox and manual Entry
        ttk.Label(self, text="Select or Input Date:").grid(row=0, column=0, padx=10, pady=5)

        # Date Combobox
        self.date_combobox = ttk.Combobox(self, textvariable=self.date_var)
        self.update_dates()
        self.date_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.date_combobox.bind("<<ComboboxSelected>>", self.update_activity_list)

        # Manual Date Entry Field
        ttk.Label(self, text="Or Enter Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        self.manual_date_entry = ttk.Entry(self, textvariable=self.date_var)  # Bind same variable to sync
        self.manual_date_entry.grid(row=1, column=1, padx=10, pady=5)
        self.manual_date_entry.bind("<Return>", self.update_activity_list)  # Bind the Enter key to trigger update

        # Category Entry
        ttk.Label(self, text="Category:").grid(row=2, column=0, padx=10, pady=5)
        self.category_entry = ttk.Entry(self, textvariable=self.category_var)
        self.category_entry.grid(row=2, column=1, padx=10, pady=5)

        # Activity Name Entry
        ttk.Label(self, text="Activity Name:").grid(row=3, column=0, padx=10, pady=5)
        self.activity_entry = ttk.Entry(self, textvariable=self.activity_var)
        self.activity_entry.grid(row=3, column=1, padx=10, pady=5)

        # Duration Entry
        ttk.Label(self, text="Duration (hours):").grid(row=4, column=0, padx=10, pady=5)
        ttk.Entry(self, textvariable=self.duration_var).grid(row=4, column=1, padx=10, pady=5)

        # List of Activities
        ttk.Label(self, text="Activities on Selected Date:").grid(row=5, column=0, padx=10, pady=5)
        self.activity_listbox = tk.Listbox(self, listvariable=self.selected_activity, selectmode=tk.SINGLE)
        self.activity_listbox.grid(row=5, column=1, padx=10, pady=5)
        self.activity_listbox.bind("<<ListboxSelect>>", self.populate_activity_details)

        # Buttons for Add, Edit, Remove Actions
        ttk.Button(self, text="Add Record", command=self.add_record).grid(row=6, column=0, pady=10)
        ttk.Button(self, text="Edit Record", command=self.edit_record).grid(row=6, column=1, pady=10)
        ttk.Button(self, text="Remove Record", command=self.remove_record).grid(row=6, column=2, pady=10)

    def update_dates(self):
        """Updates the combobox with available dates from the database."""
        dates = self.data_manager.get_dates()
        self.date_combobox['values'] = dates

    def update_activity_list(self, event=None):
        """Updates the activity list based on the selected or entered date."""
        selected_date = self.date_var.get()
        self.activity_listbox.delete(0, tk.END)  # Clear the listbox first
        if selected_date:
            activities = self.data_manager.get_activities_by_date(selected_date)
            if activities:
                for activity, category, duration in activities:
                    self.activity_listbox.insert(tk.END, f"{category}: {activity} ({duration} hrs)")
            else:
                self.activity_listbox.insert(tk.END, "No activities found")

    def populate_activity_details(self, event=None):
        """Populates activity details when an activity is selected."""
        try:
            index = self.activity_listbox.curselection()[0]
            selected = self.activity_listbox.get(index)
            if "No activities found" in selected:
                return

            category_activity, duration = selected.split(" (")
            category, activity_name = category_activity.split(": ")
            duration = float(duration.split()[0])

            self.category_var.set(category.strip())
            self.activity_var.set(activity_name.strip())
            self.duration_var.set(duration)
        except IndexError:
            pass

    def add_record(self):
        """Adds a new record."""
        selected_date = self.date_var.get()
        category = self.category_var.get()
        activity = self.activity_var.get()
        duration = self.duration_var.get()

        # Validate all fields
        if not selected_date:
            messagebox.showwarning("Input Error", "Please enter a valid date.")
        elif not category:
            messagebox.showwarning("Input Error", "Please enter a category.")
        elif not activity:
            messagebox.showwarning("Input Error", "Please enter an activity name.")
        elif duration <= 0:
            messagebox.showwarning("Input Error", "Please enter a valid duration.")
        else:
            try:
                self.data_manager.add_activity(selected_date, activity, duration, category=category)
                self.update_activity_list()  # Refresh the list
                messagebox.showinfo("Success", "Activity added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add activity: {str(e)}")

    def edit_record(self):
        """Edits an existing record."""
        selected_date = self.date_var.get()
        activity = self.activity_var.get()
        category = self.category_var.get()
        duration = self.duration_var.get()

        if selected_date and activity and duration > 0:
            try:
                self.data_manager.edit_activity(selected_date, activity, category, duration)
                self.update_activity_list()  # Refresh the list
                messagebox.showinfo("Success", "Activity edited successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to edit activity: {str(e)}")
        else:
            messagebox.showwarning("Input Error", "Please select an activity and fill all fields correctly.")

    def remove_record(self):
        """Removes a selected record."""
        selected_date = self.date_var.get()
        if selected_date:
            try:
                index = self.activity_listbox.curselection()[0]
                selected = self.activity_listbox.get(index)
                if "No activities found" in selected:
                    return

                activity_name = selected.split(": ")[1].split(" (")[0].strip()

                self.data_manager.remove_activity(selected_date, activity_name)
                self.update_activity_list()  # Refresh the list
                messagebox.showinfo("Success", "Activity removed successfully!")
            except IndexError:
                messagebox.showwarning("Input Error", "Please select an activity to remove.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove activity: {str(e)}")

