import tkinter as tk
from hardware.io_controller import IOController
import time

class TestInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Behavioral System Test Interface")
        
        # Initialize hardware interface
        self.io = IOController()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start polling inputs
        self.poll_inputs()
    
    def create_widgets(self):
        # Input state indicators
        self.state_frame = tk.LabelFrame(self.root, text="Input States", padx=5, pady=5)
        self.state_frame.pack(padx=10, pady=10, fill="x")
        
        # Right Lever
        tk.Label(self.state_frame, text="Right Lever:").grid(row=0, column=0, sticky="e")
        self.right_lever_state = tk.Label(self.state_frame, text="up", width=10)
        self.right_lever_state.grid(row=0, column=1, padx=5)
        
        # Left Lever
        tk.Label(self.state_frame, text="Left Lever:").grid(row=1, column=0, sticky="e")
        self.left_lever_state = tk.Label(self.state_frame, text="up", width=10)
        self.left_lever_state.grid(row=1, column=1, padx=5)
        
        # Nose Poke
        tk.Label(self.state_frame, text="Nose Poke:").grid(row=2, column=0, sticky="e")
        self.nose_poke_state = tk.Label(self.state_frame, text="empty", width=10)
        self.nose_poke_state.grid(row=2, column=1, padx=5)
        
        # Display controls
        self.display_frame = tk.LabelFrame(self.root, text="Display Controls", padx=5, pady=5)
        self.display_frame.pack(padx=10, pady=10, fill="x")
        
        self.clear_button = tk.Button(self.display_frame, text="Clear Displays", command=self.clear_displays)
        self.clear_button.pack(pady=5)
    
    def update_state_display(self, states):
        # Update lever states (True = pressed/down, False = released/up)
        self.right_lever_state.config(text="down" if states['right_lever'] else "up")
        self.left_lever_state.config(text="down" if states['left_lever'] else "up")
        
        # Update nose poke state (True = empty, False = poked)
        self.nose_poke_state.config(text="empty" if states['nose_poke'] else "poke!")
    
    def poll_inputs(self):
        # Get current states
        states = self.io.get_input_states()
        self.update_state_display(states)
        
        # Schedule next poll (10ms = 100Hz refresh rate)
        self.root.after(10, self.poll_inputs)
    
    def clear_displays(self):
        self.io.clear_displays()

def main():
    root = tk.Tk()
    app = TestInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main() 