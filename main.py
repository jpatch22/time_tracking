import tkinter as tk
from tkinter import ttk
from ui.home_tab import HomeTab
from ui.edit_tab import EditTab
from ui.summary_tab import SummaryTab
from apis.garmin import GarminRequest

class TimeTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Time Tracker App")
        self.geometry("800x600")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        self.garminRequest = GarminRequest()

        # Adding tabs
        self.home_tab = HomeTab(self.notebook, self.garminRequest)
        self.edit_tab = EditTab(self.notebook, self.garminRequest)
        self.summary_tab = SummaryTab(self.notebook)

        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.edit_tab, text="Edit Data")
        self.notebook.add(self.summary_tab, text="Summary")
        # Bind the tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        # Call the update method for each specific tab when it's selected
        if tab_text == "Home":
            self.home_tab.update_chart()  # Refresh chart on home tab
        elif tab_text == "Edit Data":
            self.edit_tab.update_activity_list()  # Refresh activity list on edit tab
        elif tab_text == "Summary":
            self.summary_tab.update_chart()  # Refresh chart on summary tab


if __name__ == "__main__":
    app = TimeTrackerApp()
    app.mainloop()

