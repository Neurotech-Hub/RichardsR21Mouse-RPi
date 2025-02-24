from PIL import Image, ImageDraw, ImageFont
import os

class DisplayManager:
    def __init__(self, display_left, display_right):
        self.display_left = display_left
        self.display_right = display_right
        self.width = 128
        self.height = 64
        
        # Create blank images for drawing
        self.image_left = Image.new("1", (self.width, self.height))
        self.image_right = Image.new("1", (self.width, self.height))
        
        # Create drawing objects
        self.draw_left = ImageDraw.Draw(self.image_left)
        self.draw_right = ImageDraw.Draw(self.image_right)
        
        # Load a font - modified for cross-platform compatibility
        try:
            # Try system fonts in different locations
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "C:/Windows/Fonts/arial.ttf"  # Windows
            ]
            for path in font_paths:
                if os.path.exists(path):
                    self.font = ImageFont.truetype(path, 16)
                    break
            else:
                self.font = ImageFont.load_default()
        except:
            self.font = ImageFont.load_default()

    def draw_test_pattern(self, side="both"):
        if side in ["left", "both"]:
            self.draw_left.rectangle((0, 0, self.width, self.height), outline=1, fill=0)
            self.draw_left.text((5, 5), "Left Display", font=self.font, fill=1)
            self.draw_left.rectangle((20, 30, 108, 50), outline=1, fill=1)
            self.display_left.image(self.image_left)
            self.display_left.show()
            
        if side in ["right", "both"]:
            self.draw_right.rectangle((0, 0, self.width, self.height), outline=1, fill=0)
            self.draw_right.text((5, 5), "Right Display", font=self.font, fill=1)
            self.draw_right.ellipse((20, 30, 108, 50), outline=1, fill=1)
            self.display_right.image(self.image_right)
            self.display_right.show()
            
    def clear_displays(self):
        self.draw_left.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw_right.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.display_left.image(self.image_left)
        self.display_right.image(self.image_right)
        self.display_left.show()
        self.display_right.show() 