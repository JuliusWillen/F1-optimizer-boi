import tkinter as tk
from tkinter import ttk, filedialog
from itertools import combinations, product
from data import ConstructorData, DriverData

class F1TeamOptimizerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("F1 Team Optimizer")
        self.window.geometry("800x500")

        self.driver_data = None
        self.constructor_data = None
        self.budget_cap = 100

        self.create_widgets()

    def create_widgets(self):
        # Create title label
        label_title = ttk.Label(self.window, text="F1 Team Optimizer", font=("Arial", 16, "bold"))
        label_title.pack(pady=20)

        # Create frame for file selection
        frame_file_selection = ttk.Frame(self.window)
        frame_file_selection.pack()

        # Create label and entry for driver data file
        label_driver_data = ttk.Label(frame_file_selection, text="Driver Data File:")
        label_driver_data.grid(row=0, column=0, padx=5, pady=5)

        self.entry_driver_data = ttk.Entry(frame_file_selection, width=40)
        self.entry_driver_data.grid(row=0, column=1, padx=5, pady=5)

        button_browse_driver_data = ttk.Button(frame_file_selection, text="Browse", command=self.browse_driver_data_file)
        button_browse_driver_data.grid(row=0, column=2, padx=5, pady=5)

        # Create label and entry for constructor data file
        label_constructor_data = ttk.Label(frame_file_selection, text="Constructor Data File:")
        label_constructor_data.grid(row=1, column=0, padx=5, pady=5)

        self.entry_constructor_data = ttk.Entry(frame_file_selection, width=40)
        self.entry_constructor_data.grid(row=1, column=1, padx=5, pady=5)

        button_browse_constructor_data = ttk.Button(frame_file_selection, text="Browse", command=self.browse_constructor_data_file)
        button_browse_constructor_data.grid(row=1, column=2, padx=5, pady=5)

        # Create label and entry for budget cap
        label_budget_cap = ttk.Label(frame_file_selection, text="Budget Cap (in millions):")
        label_budget_cap.grid(row=2, column=0, padx=5, pady=5)

        self.entry_budget_cap = ttk.Entry(frame_file_selection, width=10)
        self.entry_budget_cap.insert(tk.END, self.budget_cap)
        self.entry_budget_cap.grid(row=2, column=1, padx=5, pady=5)

        # Create calculate button
        button_calculate = ttk.Button(self.window, text="Calculate", command=self.reload_calculation)
        button_calculate.pack(pady=10)

        # Create treeview for displaying results
        self.treeview_results = ttk.Treeview(self.window, columns=("Drivers", "Constructors", "Points", "Cost (in millions)"))
        self.treeview_results.heading("Drivers", text="Drivers")
        self.treeview_results.heading("Constructors", text="Constructors")
        self.treeview_results.heading("Points", text="Points")
        self.treeview_results.heading("Cost (in millions)", text="Cost (in millions)")
        self.treeview_results["show"] = "headings"
        self.treeview_results.pack(padx=10, pady=10)
        
    def browse_driver_data_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.entry_driver_data.delete(0, tk.END)
        self.entry_driver_data.insert(tk.END, filename)

    def browse_constructor_data_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.entry_constructor_data.delete(0, tk.END)
        self.entry_constructor_data.insert(tk.END, filename)

    def reload_calculation(self):
        # Load driver and constructor data
        driver_data_file = self.entry_driver_data.get()
        constructor_data_file = self.entry_constructor_data.get()
        self.budget_cap = float(self.entry_budget_cap.get())

        self.driver_data = DriverData(driver_data_file)
        self.constructor_data = ConstructorData(constructor_data_file)

        # Set number of selections
        num_driver_selections = 5
        num_constructor_selections = 2

        # Generate all possible combinations of drivers and constructors
        team_combinations = product(combinations(self.driver_data.get_drivers(), num_driver_selections),
                                    combinations(self.constructor_data.get_constructors(), num_constructor_selections))

        # Calculate point total and cost total for each combination
        combinations_data = []
        for drivers, constructors in team_combinations:
            driver_points = sum(self.driver_data.get_drivers()[driver][0] for driver in drivers)
            constructor_points = sum(self.constructor_data.get_constructors()[constructor][0] for constructor in constructors)
            point_total = driver_points + constructor_points

            driver_costs = sum(self.driver_data.get_drivers()[driver][1] for driver in drivers)
            constructor_costs = sum(self.constructor_data.get_constructors()[constructor][1] for constructor in constructors)
            cost_total = round(driver_costs + constructor_costs, 2)

            if cost_total <= self.budget_cap:
                combinations_data.append((drivers, constructors, point_total, cost_total))

        # Sort combinations by point total in descending order
        combinations_data.sort(key=lambda x: x[2], reverse=True)

        # Clear the treeview
        self.treeview_results.delete(*self.treeview_results.get_children())

        # Display top 5 teams in the treeview
        for i, (drivers, constructors, points, cost) in enumerate(combinations_data[:5], start=1):
            driver_names = ", ".join(drivers)
            constructor_names = ", ".join(constructors)
            self.treeview_results.insert("", tk.END, values=(driver_names, constructor_names, points, cost))

    def run(self):
        # Run the GUI main loop
        self.window.mainloop()


if __name__ == "__main__":
    gui = F1TeamOptimizerGUI()
    gui.run()
