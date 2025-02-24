import tkinter as tk
from tkinter import ttk
import time
from hardware.io_controller import IOController
from hardware.display_utils import DisplayManager

class TestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Behavioral System Test Interface")
        
        # Initialize hardware
        self.io = IOController()
        self.display_manager = DisplayManager(self.io.display_left, self.io.display_right)
        
        # Create GUI elements
        self.create_widgets()
        
        # Start update loop
        self.update_states()
        
    def create_widgets(self):
        # Input states frame
        states_frame = ttk.LabelFrame(self.root, text="Input States", padding="5")
        states_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.state_labels = {
            'right_lever': ttk.Label(states_frame, text="Right Lever: OFF"),
            'left_lever': ttk.Label(states_frame, text="Left Lever: OFF"),
            'nose_poke': ttk.Label(states_frame, text="Nose Poke: OFF")
        }
        
        # In simulation mode, add toggle buttons
        if hasattr(self.io, '_simulated_states'):
            for i, (key, label) in enumerate(self.state_labels.items()):
                label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
                ttk.Button(
                    states_frame, 
                    text="Toggle", 
                    command=lambda k=key: self.toggle_input(k)
                ).grid(row=i, column=1, padx=5, pady=2)
        else:
            for i, (key, label) in enumerate(self.state_labels.items()):
                label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
        
        # Display control frame
        display_frame = ttk.LabelFrame(self.root, text="Display Control", padding="5")
        display_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        ttk.Button(display_frame, text="Test Pattern", 
                  command=self.display_manager.draw_test_pattern).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(display_frame, text="Clear Displays", 
                  command=self.display_manager.clear_displays).grid(row=0, column=1, padx=5, pady=2)

    def toggle_input(self, input_name):
        if hasattr(self.io, '_simulated_states'):
            self.io._simulated_states[input_name] = not self.io._simulated_states[input_name]
        
    def update_states(self):
        # Update input states
        states = self.io.get_input_states()
        for key, state in states.items():
            self.state_labels[key].config(text=f"{key.replace('_', ' ').title()}: {'ON' if state else 'OFF'}")
        
        # Schedule next update
        self.root.after(1000, self.update_states)

if __name__ == "__main__":
    root = tk.Tk()
    # Set window size and position
    root.geometry("300x250+100+100")  # width x height + x_position + y_position
    app = TestGUI(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nExiting...")
        root.quit() 