import customtkinter as ctk

class AboutWindow(ctk.CTkToplevel):
    """
    A Toplevel window to display information about the Banker's Algorithm
    and the concept of deadlock.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("About Banker's Algorithm")
        self.geometry("700x550")
        self.grab_set() # Make the window modal (blocks interaction with main window until closed)
        self.resizable(False, False) # Prevent resizing for fixed content

        # Configure grid for expansion
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a scrollable textbox for the information content
        info_textbox = ctk.CTkTextbox(self, wrap="word", corner_radius=10, font=("Cascadia Code", 13))
        info_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Define the information text
        about_text = """
How Banker's Algorithm Works
-------------------------------

The Banker's Algorithm is a resource allocation and deadlock avoidance algorithm.
It tests for safety by simulating the allocation of predetermined maximum possible
amounts of all resources. It then performs a "safe-state" check to test for
possible deadlock conditions for all other pending activities before deciding
whether a resource allocation should be allowed.

The algorithm works as follows:

1.  **Define Matrices:**
    -   **Allocation:** A matrix showing how many resources of each type are
        currently allocated to each process.
    -   **Max:** A matrix defining the maximum number of resources of each type
        that each process may request over its lifetime.
    -   **Available:** A vector indicating the number of resources of each type
        that are currently available in the system (unallocated).
    -   **Need:** A matrix representing the remaining resources each process needs
        to complete its execution. It's calculated as: `Need = Max - Allocation`.

2.  **Safety Check Algorithm:**
    a.  **Initialization:**
        - Create a `Work` vector, initialized with the values from `Available`.
        - Create a boolean `Finish` vector for all processes, initially set to `False` for all.

    b.  **Find a Process:**
        - Search for a process `Pi` that meets two conditions:
            1.  `Finish[i]` is `False` (the process has not yet completed).
            2.  `Need[i]` is less than or equal to `Work` (the process's remaining
                resource needs can be satisfied by the currently available resources).

    c.  **No Such Process:**
        - If no such process `Pi` is found, proceed to step (e).

    d.  **Simulate Allocation and Release:**
        - If such a process `Pi` is found:
            -   'Pretend' to allocate resources to this process.
            -   Update `Work`: Add the resources currently allocated to `Pi`
                back to `Work` (`Work = Work + Allocation[i]`). This simulates `Pi`
                finishing and releasing its resources.
            -   Set `Finish[i]` to `True`.
            -   Go back to step (b) to find the next process that can execute.

    e.  **Check Final State:**
        - After the loop, check if `Finish[i]` is `True` for all processes.
        - If all processes are finished, the system is in a **safe state**, and
          the sequence of processes found is a safe sequence.
        - Otherwise, the system is in an **unsafe state (deadlock)**.

---
Example:
---
Let's say we have:
Processes = 3, Resources = 2

Allocation:
P0: [1, 0]
P1: [1, 1]
P2: [0, 1]

Max:
P0: [3, 2]
P1: [2, 2]
P2: [3, 1]

Available: [1, 0]

1.  **Calculate Need:**
    Need P0: [2, 2]
    Need P1: [1, 1]
    Need P2: [3, 0]

2.  **Run Safety Check:**
    -   Initial Work = [1, 0]
    -   Check P0: Need [2, 2] > Work [1, 0]. Cannot satisfy.
    -   Check P1: Need [1, 1] > Work [1, 0]. Cannot satisfy.
    -   Check P2: Need [3, 0] > Work [1, 0]. Cannot satisfy.

    **Result:** No process can be satisfied. System is in a **DEADLOCK** state.
"""
        info_textbox.insert("0.0", about_text)
        info_textbox.configure(state="disabled") # Make the textbox read-only

class ResultsWindow(ctk.CTkToplevel):
    """
    A Toplevel window to display the results of the Banker's Algorithm,
    including the Need Matrix, step-by-step simulation, and final safe sequence.
    """
    def __init__(self, initial_available, need_matrix, simulation_steps, safe_sequence, is_safe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Banker's Algorithm Results")
        self.geometry("700x800") # Set a fixed size for the results window
        self.grab_set() # Make the window modal

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a single scrollable frame to hold all content.
        # This ensures that if the content extends beyond the window height,
        # the user can scroll to see everything, including the final result.
        self.scrollable_content_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.scrollable_content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.scrollable_content_frame.grid_columnconfigure(0, weight=1) # Center content within this scrollable frame

        # --- Display Initial Available Resources ---
        ctk.CTkLabel(self.scrollable_content_frame, text="Initial Available Resources:",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(10, 5))
        ctk.CTkLabel(self.scrollable_content_frame, text=f"{initial_available}",
                     font=("Cascadia Code", 13), text_color="green").pack(pady=(0, 15))

        # --- Display Need Matrix ---
        ctk.CTkLabel(self.scrollable_content_frame, text="Need Matrix (Max - Allocation):",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(10, 5))
        need_frame = ctk.CTkFrame(self.scrollable_content_frame, corner_radius=8)
        need_frame.pack(pady=5, padx=20, fill="x")
        need_frame.grid_columnconfigure(0, weight=1) # For centering process rows

        # Iterate through the need_matrix to display each process's needs
        for i, row_data in enumerate(need_matrix):
            row_str = "  ".join(map(str, row_data))
            ctk.CTkLabel(need_frame, text=f"P{i}: [{row_str}]", font=("Cascadia Code", 12)).grid(row=i, column=0, sticky="w", padx=10, pady=2)

        # --- Display Simulation Steps ---
        ctk.CTkLabel(self.scrollable_content_frame, text="Simulation Steps:",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(20, 5))

        if simulation_steps:
            # Iterate through each step recorded during the algorithm execution
            for i, step_info in enumerate(simulation_steps):
                step_text = (
                    f"--- Step {i+1} ---\n"
                    f"  Executing Process: P{step_info['process_executed']}\n"
                    f"  Available (before): {step_info['work_before_execution']}\n"
                    f"  Resources Allocated by P{step_info['process_executed']}: {step_info['allocation']}\n"
                    f"  Available (after): {step_info['work_after_execution']}\n"
                    f"  Current Safe Sequence Progress: {' -> '.join([f'P{p}' for p in step_info['safe_sequence_progress']])}\n"
                )
                
                # Display each step's details
                step_label = ctk.CTkLabel(self.scrollable_content_frame, text=step_text, justify="left", font=("Cascadia Code", 12))
                step_label.pack(anchor="w", padx=10, pady=5)
                
                # Add a separator line after each step for visual clarity
                ctk.CTkFrame(self.scrollable_content_frame, height=1, fg_color="gray").pack(fill="x", padx=10, pady=5)
        else:
            # Message if no processes could execute (e.g., immediate unsafe state)
            ctk.CTkLabel(self.scrollable_content_frame, text="No processes could execute. The system might be in an immediate unsafe state.",
                         font=("Cascadia Code", 12), text_color="yellow").pack(pady=10)

        # --- Display Final Result ---
        ctk.CTkLabel(self.scrollable_content_frame, text="Final Result:",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(20, 5))
        
        if is_safe:
            # Format the safe sequence for display
            final_sequence_str = " -> ".join([f"P{p}" for p in safe_sequence])
            
            # Display safe state message
            ctk.CTkLabel(self.scrollable_content_frame, text="System is in a SAFE STATE.",
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="cyan").pack(pady=(0, 5))
            # Display the safe sequence
            ctk.CTkLabel(self.scrollable_content_frame, text=f"Safe Sequence: {final_sequence_str}",
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="cyan").pack(pady=(0, 10))
        else:
            # Display unsafe state (deadlock) message
            ctk.CTkLabel(self.scrollable_content_frame, text="DEADLOCK DETECTED.",
                         font=ctk.CTkFont(size=16, weight="bold"), text_color="red").pack(pady=(0, 5))
            ctk.CTkLabel(self.scrollable_content_frame, text="The system is in an unsafe state. No safe sequence found.",
                         font=ctk.CTkFont(size=14), text_color="red").pack(pady=(0, 10))