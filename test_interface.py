import tkinter as tk
from tkinter import ttk
import time
from PIL import Image, ImageDraw

from hardware.io_controller import IOController

class TestInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Behavioral System Test Interface")
        
        # Configure style
        self.setup_styles()
        
        # Initialize hardware interface
        self.io = IOController()
        
        # Create GUI elements
        self.create_widgets()
        
        # Configure window
        self.root.geometry("400x300")  # Set window size
        self.root.resizable(False, False)  # Fix window size
        
        # Start polling inputs
        self.poll_inputs()
    
    def setup_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('State.TLabel', font=('Helvetica', 10), padding=5)
        style.configure('StateValue.TLabel', 
                       font=('Helvetica', 10, 'bold'), 
                       padding=5,
                       width=10,
                       anchor='center')
        style.configure('Controls.TButton', 
                       font=('Helvetica', 10),
                       padding=10)
    
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title = ttk.Label(main_frame, 
                         text="System Status Monitor",
                         style='Header.TLabel')
        title.pack(pady=(0, 20))
        
        # Input state indicators
        self.state_frame = ttk.LabelFrame(main_frame, 
                                        text="Input States",
                                        padding="10")
        self.state_frame.pack(fill="x", pady=(0, 20))
        
        # Grid configuration
        self.state_frame.columnconfigure(1, weight=1)
        
        # Right Lever
        ttk.Label(self.state_frame, 
                 text="Right Lever:",
                 style='State.TLabel').grid(row=0, column=0, sticky="e")
        self.right_lever_state = ttk.Label(self.state_frame,
                                         text="up",
                                         style='StateValue.TLabel')
        self.right_lever_state.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Left Lever
        ttk.Label(self.state_frame,
                 text="Left Lever:",
                 style='State.TLabel').grid(row=1, column=0, sticky="e")
        self.left_lever_state = ttk.Label(self.state_frame,
                                        text="up",
                                        style='StateValue.TLabel')
        self.left_lever_state.grid(row=1, column=1, sticky="ew", padx=5)
        
        # Nose Poke
        ttk.Label(self.state_frame,
                 text="Nose Poke:",
                 style='State.TLabel').grid(row=2, column=0, sticky="e")
        self.nose_poke_state = ttk.Label(self.state_frame,
                                       text="empty",
                                       style='StateValue.TLabel')
        self.nose_poke_state.grid(row=2, column=1, sticky="ew", padx=5)
        
        # Add some vertical spacing between rows
        for row in range(3):
            ttk.Frame(self.state_frame).grid(row=row, column=0, pady=5)
        
        # Display controls
        self.display_frame = ttk.LabelFrame(main_frame,
                                          text="Display Controls",
                                          padding="10")
        self.display_frame.pack(fill="x")
        
        # Button container for horizontal layout
        button_frame = ttk.Frame(self.display_frame)
        button_frame.pack(pady=5)
        
        self.test_button = ttk.Button(button_frame,
                                    text="Test Pattern",
                                    style='Controls.TButton',
                                    command=self.test_displays)
        self.test_button.pack(side='left', padx=5)
        
        self.clear_button = ttk.Button(button_frame,
                                     text="Clear Displays",
                                     style='Controls.TButton',
                                     command=self.clear_displays)
        self.clear_button.pack(side='left', padx=5)
    
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
    
    def test_displays(self):
        """Draw test pattern on both displays"""
        # Create test pattern
        image = Image.new('1', (128, 64), 0)  # '1' = binary mode
        draw = ImageDraw.Draw(image)
        
        # Draw some test patterns
        draw.rectangle([0, 0, 127, 63], outline=1)  # Border
        draw.line([0, 0, 127, 63], fill=1)  # Diagonal line
        draw.line([0, 63, 127, 0], fill=1)  # Diagonal line
        draw.rectangle([32, 16, 96, 48], fill=1)  # Center rectangle
        
        # Display on both screens
        self.io.display_left.image(image)
        self.io.display_right.image(image)
        self.io.display_left.show()
        self.io.display_right.show()

def main():
    root = tk.Tk()
    app = TestInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main() 