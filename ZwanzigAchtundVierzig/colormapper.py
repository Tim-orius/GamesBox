import tkinter as tk


class ColorMapper:
    def __init__(self, base=2):
        self.base = base

    def get_color(self, exponent):
        # Determine the color based on the exponent value
        if exponent < 10:
            # Scale from beige/yellow (RGB: 255, 255, 224) to red (RGB: 255, 0, 0)
            r = 255
            g = int(255 * (1 - (exponent / 15)))
            b = 0
        elif exponent < 19:
            # Moving from red (RGB: 255, 0, 0) to blue (RGB: 0, 0, 255)
            r = int(255 * (1 - ((exponent - 10) / 15)))
            g = 0
            b = int(255 * ((exponent - 10) / 15))
        else:
            # Moving from blue (RGB: 0, 0, 255) to green (RGB: 0, 255, 0)
            r = 0
            g = int(255 * ((exponent - 20) / 15))
            b = int(255 * (1 - ((exponent - 20) / 15)))

        # Make sure the colors are within the valid range
        r = min(max(r, 0), 255)
        g = min(max(g, 0), 255)
        b = min(max(b, 0), 255)

        return self.rgb_to_hex(r, g, b)

    def rgb_to_hex(self, r, g, b):
        return f'#{r:02X}{g:02X}{b:02X}'

    def get_value_color(self, value):
        if value == 0:
            return "#FFFFFF"  # White for zero
        elif value < 0:
            return "#000000"  # Black for negative values

        # Calculate the exponent based on the base
        exponent = 0
        while value >= self.base:
            value //= self.base
            exponent += 1

        # Get the color based on the exponent
        return self.get_color(exponent)


class ColorStrip:
    def __init__(self, base=2):
        self.color_mapper = ColorMapper(base)

    def create_strip(self, max_exponent):
        window = tk.Tk()
        window.title(f"Color Strip for Base {self.color_mapper.base}")

        # Create a canvas and make it resizable
        canvas = tk.Canvas(window)
        canvas.pack(fill=tk.BOTH, expand=True)

        rectangle_width = 50

        for i in range(max_exponent + 1):
            value = self.color_mapper.base ** i
            color = self.color_mapper.get_value_color(value)

            # Create the rectangle for the color strip
            x1 = i * rectangle_width
            x2 = x1 + rectangle_width
            canvas.create_rectangle(x1, 0, x2, 100, fill=color, outline=color)

            # Get hex code and exponent
            hex_code = color

            # Draw the hex code and exponent text on the rectangle
            canvas.create_text((x1 + x2) / 2, 50, text=f"{hex_code}\n{i}", fill="black", font=("Arial", 10), anchor="center")

        # Configure the canvas to expand as window resizes
        window.geometry(f"{rectangle_width * (max_exponent + 1)}x100")  # Initial window size
        window.mainloop()


def main():
    base = 2
    strip_len = 25
    color_strip = ColorStrip(base=base)

    # Create a color strip for base 2
    print(f"Displaying color strip for base {base}...")
    color_strip.create_strip(strip_len)

if __name__ == "__main__":
    main()