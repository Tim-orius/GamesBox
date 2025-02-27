import tkinter as tk


class ColorMapper:
    def __init__(self):
        pass

    def get_color(self, value):
        """

        :param value:
        :return:
        """
        if value < 1:
            r = g = b = 255
        elif value == 1:
            r = 0
            g = 255
            b = 0
        elif value < 9:
            # Moving from red (RGB: 255, 0, 0) to blue (RGB: 0, 0, 255)
            r = 255
            g = int(255 * (1 - (value / 10)))
            b = 0
        elif value == 99:
            r = 255
            g = 0
            b = 255
        else:
            r = g = b = 255

        return self.rgb_to_hex(r, g, b)

    def rgb_to_hex(self, r, g, b):
        return f'#{r:02X}{g:02X}{b:02X}'


class ColorStrip:
    def __init__(self):
        self.color_mapper = ColorMapper()

    def create_strip(self, max_value):
        window = tk.Tk()
        window.title("Minesweeper Color Strip")

        # Create a canvas and make it resizable
        canvas = tk.Canvas(window)
        canvas.pack(fill=tk.BOTH, expand=True)

        rectangle_width = 50

        for i in range(max_value + 1):
            color = self.color_mapper.get_color(i)

            # Create the rectangle for the color strip
            x1 = i * rectangle_width
            x2 = x1 + rectangle_width
            canvas.create_rectangle(x1, 0, x2, 100, fill=color, outline=color)

            # Get hex code and value
            hex_code = color

            # Draw the hex code and value text on the rectangle
            canvas.create_text((x1 + x2) / 2, 50, text=f"{hex_code}\n{i}", fill="black", font=("Arial", 10), anchor="center")

        # Configure the canvas to expand as the window resizes
        window.geometry(f"{rectangle_width * (max_value + 1)}x100")  # Initial window size
        window.mainloop()


def main():
    max_value = 8  # Based on Minesweeper rules, max tile number is usually 8
    color_strip = ColorStrip()

    # Create a color strip for Minesweeper
    print("Displaying Minesweeper color strip...")
    color_strip.create_strip(max_value)


if __name__ == "__main__":
    main()