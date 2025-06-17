import customtkinter as ctk
from tkinter import messagebox
import random
from windows import AboutWindow, ResultsWindow
from banker_logic import run_bankers_algorithm_logic

class DeadlockDetectorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Deadlock Detection & Prevention System")
        self.geometry("1000x800") # Set initial window size
        ctk.set_appearance_mode("dark") # Set default theme to dark mode
        ctk.set_default_color_theme("blue") # Set default color theme

        # --- Class Variables for Child Windows ---
        # Keep track of Toplevel windows to prevent multiple instances or manage focus
        self.about_window = None
        self.results_window = None

        # --- Core Application Variables ---
        self.num_processes = 0 # Stores the number of processes (n)
        self.num_resources = 0 # Stores the number of resource types (m)
        
        # Lists to hold references to the CTkEntry widgets for matrix input
        self.allocation_entries = [] # 2D list of Entry widgets for Allocation matrix
        self.max_entries = []        # 2D list of Entry widgets for Max Need matrix
        self.available_entries = []  # 1D list of Entry widgets for Available resources

        # --- Build Main GUI Layout ---
        self.create_main_gui_layout()
        
        # Initialize matrix input fields with default values on startup
        # This populates the grid for 5 processes and 3 resources initially.
        self.create_matrix_inputs()

    def create_main_gui_layout(self):
        """
        Sets up the main frame and essential widgets for the application's input interface.
        """
        # Main container frame for the entire application content
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # --- Top Section: Title and About Button ---
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=(10,0))
        top_frame.grid_columnconfigure(0, weight=1) # Allows title to expand horizontally
        
        title_label = ctk.CTkLabel(top_frame, text="Banker's Algorithm Simulator", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, pady=10)

        # About button to open the info window
        about_btn = ctk.CTkButton(top_frame, text="i", command=self.open_about_window,
                                  width=30, height=30, corner_radius=15,
                                  font=ctk.CTkFont(size=18, weight="bold"))
        about_btn.grid(row=0, column=1, padx=10, sticky="e")

        # --- Input Frame for Processes and Resources Count ---
        input_dim_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        input_dim_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(input_dim_frame, text="Processes:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(20, 5), pady=10)
        self.processes_entry = ctk.CTkEntry(input_dim_frame, width=50)
        self.processes_entry.pack(side="left", padx=5, pady=10)
        self.processes_entry.insert(0, "5") # Default value for convenience

        ctk.CTkLabel(input_dim_frame, text="Resources:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(20, 5), pady=10)
        self.resources_entry = ctk.CTkEntry(input_dim_frame, width=50)
        self.resources_entry.pack(side="left", padx=5, pady=10)
        self.resources_entry.insert(0, "3") # Default value for convenience

        # Button to generate/update the matrix input fields based on dimensions
        self.create_matrices_btn = ctk.CTkButton(input_dim_frame, text="Generate Fields", command=self.create_matrix_inputs)
        self.create_matrices_btn.pack(side="right", padx=20, pady=10)
        
        # --- Frame to hold the dynamic matrix input grids ---
        self.matrix_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.matrix_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # --- Status Message Label ---
        # Displays feedback to the user (e.g., "Safe state detected", "Input Error")
        self.status_label = ctk.CTkLabel(self.main_frame, text="Enter values and run the algorithm.",
                                         font=ctk.CTkFont(size=16), justify="center")
        self.status_label.pack(pady=20, padx=20)

    def open_about_window(self):
        """
        Opens the AboutWindow, ensuring only one instance is active at a time.
        """
        # Check if the about window exists and is still open
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(self) # Create new instance if not
        else:
            self.about_window.focus() # Bring existing window to front

    def create_matrix_inputs(self):
        """
        Dynamically generates or regenerates the input fields for the Allocation,
        Max Need, and Available matrices based on the current number of processes
        and resources entered by the user.
        """
        try:
            # Get dimensions from entry fields
            self.num_processes = int(self.processes_entry.get())
            self.num_resources = int(self.resources_entry.get())
            
            # Basic validation: dimensions must be positive
            if self.num_processes <= 0 or self.num_resources <= 0:
                messagebox.showerror("Invalid Input", "Number of processes and resources must be positive integers.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for processes and resources.")
            return

        # Clear any existing matrix input widgets from the frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Configure the grid layout for the matrix_frame
        # Column 0 for Allocation, Column 1 for Max Need, Column 2 for Controls
        self.matrix_frame.grid_columnconfigure(0, weight=1)
        self.matrix_frame.grid_columnconfigure(1, weight=1)
        self.matrix_frame.grid_columnconfigure(2, weight=1, minsize=250) # Give controls more space

        # --- Allocation Matrix Input ---
        alloc_frame = ctk.CTkFrame(self.matrix_frame, corner_radius=10)
        alloc_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(alloc_frame, text="Allocation Matrix", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        # Call helper to create grid of entry widgets
        self.allocation_entries = self._create_grid_of_entries(alloc_frame, self.num_processes, self.num_resources, "P")

        # --- Max Need Matrix Input ---
        max_frame = ctk.CTkFrame(self.matrix_frame, corner_radius=10)
        max_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(max_frame, text="Max Need Matrix", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        # Call helper to create grid of entry widgets
        self.max_entries = self._create_grid_of_entries(max_frame, self.num_processes, self.num_resources, "P")
        
        # --- Controls Frame (Available Resources & Action Buttons) ---
        controls_frame = ctk.CTkFrame(self.matrix_frame, corner_radius=10)
        controls_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Available Resources Input Section
        avail_frame = ctk.CTkFrame(controls_frame, corner_radius=10)
        avail_frame.pack(pady=10, padx=10, fill='x')
        ctk.CTkLabel(avail_frame, text="Available Resources", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        # _create_grid_of_entries returns a list of lists, but for Available, we only need the first (and only) row.
        self.available_entries = self._create_grid_of_entries(avail_frame, 1, self.num_resources, "R")[0]

        # Action Buttons Section
        buttons_frame = ctk.CTkFrame(controls_frame, fg_color="transparent") # Transparent for cleaner look
        buttons_frame.pack(pady=20, padx=20, fill='x', expand=True)

        calculate_btn = ctk.CTkButton(buttons_frame, text="Check for Deadlock", command=self.run_bankers_algorithm,
                                      font=ctk.CTkFont(size=16, weight="bold"))
        calculate_btn.pack(side="top", fill="x", ipady=10, pady=5) # ipady adds internal padding

        randomize_btn = ctk.CTkButton(buttons_frame, text="Randomize Inputs", command=self.randomize_fields,
                                      fg_color="#D35400", hover_color="#E67E22") # Custom colors for distinction
        randomize_btn.pack(side="top", fill="x", pady=5)
        
        reset_btn = ctk.CTkButton(buttons_frame, text="Reset All", command=self.reset_fields,
                                  fg_color="#7f8c8d", hover_color="#95a5a6") # Custom colors for distinction
        reset_btn.pack(side="top", fill="x", pady=5)

    def _create_grid_of_entries(self, parent_frame, rows, cols, row_label_prefix="R"):
        """
        Helper method to create a grid of CTkEntry widgets with row/column labels
        within a specified parent frame.
        
        Args:
            parent_frame (ctk.CTkFrame): The frame where the grid will be packed.
            rows (int): Number of rows for the grid.
            cols (int): Number of columns for the grid.
            row_label_prefix (str): Prefix for row labels (e.g., "P" for process, "R" for resource).
        
        Returns:
            list[list[ctk.CTkEntry]]: A 2D list (matrix) of the created Entry widgets.
        """
        grid_container_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        grid_container_frame.pack(pady=5, padx=5)
        
        entries_matrix = [] # This will store references to all entry widgets

        # Create column headers (R0, R1, R2...)
        for j in range(cols):
            col_label = ctk.CTkLabel(grid_container_frame, text=f"R{j}", font=ctk.CTkFont(size=12, weight="bold"))
            col_label.grid(row=0, column=j+1, padx=5, pady=2) # Column 0 is reserved for row labels

        # Create rows of entry widgets with optional row labels (P0, P1...)
        for i in range(rows):
            current_row_entries = []
            if rows > 1: # Only add row labels if it's a multi-row matrix (like Allocation or Max Need)
                row_label = ctk.CTkLabel(grid_container_frame, text=f"{row_label_prefix}{i}", font=ctk.CTkFont(size=12, weight="bold"))
                row_label.grid(row=i+1, column=0, padx=5, pady=2)
            
            # Create entry widgets for each cell in the current row
            for j in range(cols):
                entry_widget = ctk.CTkEntry(grid_container_frame, width=50, justify='center')
                entry_widget.grid(row=i+1, column=j+1, padx=5, pady=5)
                entry_widget.insert(0, "0") # Default value for each entry
                current_row_entries.append(entry_widget)
            
            entries_matrix.append(current_row_entries) # Add the current row's entries to the main matrix
        
        return entries_matrix

    def get_matrix_values(self, entries_list):
        """
        Parses integer values from a 2D list of CTkEntry widgets (for Allocation/Max matrices).
        Performs basic validation for non-negative integers.

        Args:
            entries_list (list[list[ctk.CTkEntry]]): A 2D list of Entry widgets.

        Returns:
            list[list[int]] or None: The parsed 2D list of integers, or None if validation fails.
        """
        parsed_matrix = []
        try:
            for r_idx, row_entries in enumerate(entries_list):
                current_row_values = []
                for c_idx, entry_widget in enumerate(row_entries):
                    value = int(entry_widget.get())
                    if value < 0:
                        messagebox.showerror("Input Error", f"Negative value found at row {r_idx}, column {c_idx}. All matrix values must be non-negative.")
                        return None
                    current_row_values.append(value)
                parsed_matrix.append(current_row_values)
            return parsed_matrix
        except ValueError:
            messagebox.showerror("Input Error", "All matrix fields must contain valid non-negative integers.")
            return None
        except IndexError:
            # This handles cases where matrix dimensions might have changed unexpectedly.
            messagebox.showerror("Input Error", "Matrix dimensions mismatch with entered values. Please re-generate fields using 'Generate Fields' button.")
            return None

    def get_vector_values(self, entries_list):
        """
        Parses integer values from a 1D list of CTkEntry widgets (for Available resources).
        Performs basic validation for non-negative integers.

        Args:
            entries_list (list[ctk.CTkEntry]): A 1D list of Entry widgets.

        Returns:
            list[int] or None: The parsed list of integers, or None if validation fails.
        """
        parsed_vector = []
        try:
            for idx, entry_widget in enumerate(entries_list):
                value = int(entry_widget.get())
                if value < 0:
                    messagebox.showerror("Input Error", f"Negative value found for resource {idx}. All available resource values must be non-negative.")
                    return None
                parsed_vector.append(value)
            return parsed_vector
        except ValueError:
            messagebox.showerror("Input Error", "All available resource fields must contain valid non-negative integers.")
            return None
        except IndexError:
            # This handles cases where vector length might have changed unexpectedly.
            messagebox.showerror("Input Error", "Available resources count mismatch. Please re-generate fields using 'Generate Fields' button.")
            return None

    def reset_fields(self):
        """
        Resets all input fields (Allocation, Max Need, Available) to a default value of '0'.
        Updates the status label to inform the user.
        """
        # Iterate through all Allocation matrix entries and set to '0'
        for row_entries in self.allocation_entries:
            for entry_widget in row_entries:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, '0')
        
        # Iterate through all Max Need matrix entries and set to '0'
        for row_entries in self.max_entries:
            for entry_widget in row_entries:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, '0')
        
        # Iterate through all Available resources entries and set to '0'
        for entry_widget in self.available_entries:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, '0')
            
        self.status_label.configure(text="Fields reset. Enter new values.",
                                     text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])

    def randomize_fields(self):
        """
        Populates all input fields (Allocation, Max Need, Available) with random
        non-negative integer values. Ensures Max is always >= Allocation.
        Updates the status label.
        """
        # Ensure dimensions are set before attempting to randomize
        if self.num_processes == 0 or self.num_resources == 0:
            messagebox.showinfo("Info", "Please set valid dimensions (Processes & Resources) first, then click 'Generate Fields'.")
            return

        # Randomize values for Allocation and Max Need matrices
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                alloc_val = random.randint(0, 5) # Random value for allocation (0-5)
                self.allocation_entries[i][j].delete(0, 'end')
                self.allocation_entries[i][j].insert(0, str(alloc_val))
                
                max_val = random.randint(alloc_val, alloc_val + 5) # Max must be >= current allocation
                self.max_entries[i][j].delete(0, 'end')
                self.max_entries[i][j].insert(0, str(max_val))
        
        # Randomize values for Available resources
        for j in range(self.num_resources):
            avail_val = random.randint(3, 10) # Random value for available resources (3-10)
            self.available_entries[j].delete(0, 'end')
            self.available_entries[j].insert(0, str(avail_val))
            
        self.status_label.configure(text="Random values generated. Click 'Check for Deadlock'.", text_color="yellow")

    def run_bankers_algorithm(self):
        """
        Gathers input data from the GUI, performs necessary validations,
        then calls the core Banker's Algorithm logic, and finally displays
        the results in a dedicated results window.
        """
        # 1. Gather input values from the GUI entry widgets
        current_allocation = self.get_matrix_values(self.allocation_entries)
        current_max_need = self.get_matrix_values(self.max_entries)
        current_initial_available = self.get_vector_values(self.available_entries)

        # If any of the input parsing functions returned None, an error message
        # has already been displayed, so stop execution here.
        if current_allocation is None or current_max_need is None or current_initial_available is None:
            return 

        # 2. Perform additional input validation: Check if matrix dimensions match expected counts
        # This is a crucial check after parsing, to ensure data integrity before algorithm execution.
        is_dimensions_valid = True
        if len(current_allocation) != self.num_processes or \
           (self.num_processes > 0 and len(current_allocation[0]) != self.num_resources):
            is_dimensions_valid = False
        if len(current_max_need) != self.num_processes or \
           (self.num_processes > 0 and len(current_max_need[0]) != self.num_resources):
            is_dimensions_valid = False
        if len(current_initial_available) != self.num_resources:
            is_dimensions_valid = False

        if not is_dimensions_valid:
            messagebox.showerror("Input Error", "Matrix dimensions do not match the set number of processes/resources. Please click 'Generate Fields' and verify inputs.")
            return

        # 3. Pre-check: Ensure Max Need is always greater than or equal to Allocation
        # A process cannot request less than what it's already been given.
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                if current_max_need[i][j] < current_allocation[i][j]:
                    messagebox.showerror("Input Error", f"Error: Max Need for P{i} R{j} ({current_max_need[i][j]}) must be >= Allocation for P{i} R{j} ({current_allocation[i][j]}).")
                    return # Stop if this crucial condition is violated

        # 4. Call the core Banker's Algorithm logic (from banker_logic.py)
        # This function performs the actual safety check and generates simulation steps.
        need_matrix, simulation_steps, safe_sequence, is_safe_state = \
            run_bankers_algorithm_logic(current_allocation, current_max_need, 
                                        current_initial_available, self.num_processes, self.num_resources)

        # 5. Display results in the ResultsWindow
        # If a ResultsWindow is already open, destroy it first to ensure fresh content.
        if self.results_window is not None and self.results_window.winfo_exists():
            self.results_window.destroy() 
        
        # Create and show the new ResultsWindow with all algorithm outputs
        self.results_window = ResultsWindow(current_initial_available, need_matrix, 
                                            simulation_steps, safe_sequence, is_safe_state, self)
        self.results_window.focus() # Bring the results window to the foreground

        # 6. Update the status label on the main window based on the algorithm's outcome
        if is_safe_state:
            self.status_label.configure(text="Safe state detected. Results shown in new window.", text_color="cyan")
        else:
            self.status_label.configure(text="Deadlock detected! Results shown in new window.", text_color="red")


if __name__ == "__main__":
    app = DeadlockDetectorApp()
    app.mainloop()
