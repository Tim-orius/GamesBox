import tkinter as tk
from tkinter import messagebox

import random

from agent import Agent
from game_grid import GameGrid
from game_ui import GameUI


class Frame:
    """Wrapper of the game ui and initialisation for the menus."""
    def __init__(self, root):
        """GameUI + GameGrid Wrapper.

        :param root: tkinter object
        """
        # General game variables
        self.root = root
        self.grid = GameGrid()
        self.ui = GameUI(root, self.grid)

        # Auto-play variables
        self.perform_auto_play = False
        self.agent = None
        self.depth = 7
        self.ai_auto_play = True

        # Setup Game & UI
        self.root.geometry("500x500")
        self.ui.grid_config()
        self.key_binds()
        self.menu_setup()

        # Start the game
        self.restart()

    def menu_setup(self):
        """General menu setup"""
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.game_menu = tk.Menu(self.menu)
        self.options_menu = tk.Menu(self.menu)

        self.menu.add_cascade(label="Game", menu=self.game_menu)
        self.menu.add_cascade(label="Options", menu=self.options_menu)

        self.game_menu.add_command(label="Restart", command=lambda: self.restart())
        self.game_menu.add_command(label="Game options", command=lambda: self.game_options())
        self.game_menu.add_command(label="AI options", command=lambda: self.ai_options())
        self.game_menu.add_command(label="Add Custom Value", command=lambda: self.add_custom_value())

        self.options_menu.add_command(label="Adjust Frame Size", command=lambda: self.frame_size_options())
        self.options_menu.add_command(label="Help", command=lambda: self.help())

    def key_binds(self):
        """Setup key binds"""
        self.root.bind("<Up>", lambda event: self.move(0))
        self.root.bind("<Down>", lambda event: self.move(1))
        self.root.bind("<Left>", lambda event: self.move(2))
        self.root.bind("<Right>", lambda event: self.move(3))
        self.root.bind("<Escape>", lambda event: self.restart())
        self.root.bind("<Return>", lambda event: self.toggle_auto_play())

    def restart(self):
        """Restart game"""
        self.ui.restart()
        self.grid.restart(spawn_no=2)
        self.ui.setup()

    def move(self, direction):
        """Perform move"""
        success = self.grid.move(direction)
        if success:
            self.ui.update()
        else:
            if self.ui.grid.check_game_over():
                self.end()

    def end(self):
        """Game over"""
        self.ui.end()

    def game_options(self):
        """Open the game options window."""
        # Create secondary (or popup) window.
        self.game_opts_window = tk.Toplevel()
        self.game_opts_window.title("Game Options")
        self.game_opts_window.configure(bg='lightblue')
        self.game_opts_window.minsize(400, 250)

        # Use current values from the instance attributes
        current_base_number = str(self.grid.base_number)
        current_percentage = str(self.grid.percent_double_base_on_spawn)

        # Base number option
        self.base_number_option_label = tk.Label(self.game_opts_window,
                                                 text="Base number (1-2):",
                                                 bg='lightblue',
                                                 font=('Arial', 10))
        self.base_number_option_label.pack(pady=(20, 0))
        self.base_number_option = tk.Entry(self.game_opts_window,
                                           font=('Arial', 12),
                                           width=10)
        self.base_number_option.insert(0, current_base_number)  # Set default value from self.base_number
        self.base_number_option.pack(pady=5)

        # Percentage option
        self.percentage_option_label = tk.Label(self.game_opts_window,
                                                text="Percentage for double values spawning (0-100):",
                                                bg='lightblue',
                                                font=('Arial', 10))
        self.percentage_option_label.pack(pady=(20, 0))
        self.percentage_option = tk.Entry(self.game_opts_window,
                                          font=('Arial', 12),
                                          width=10)
        self.percentage_option.insert(0, current_percentage)  # Set default value from self.percentage
        self.percentage_option.pack(pady=5)

        # Buttons frame for better organization
        button_frame = tk.Frame(self.game_opts_window, bg='lightblue')
        button_frame.pack(pady=20)

        button_cancel = tk.Button(
            button_frame,
            text="Cancel",
            command=self.game_opts_window.destroy,
            bg='red',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_cancel.pack(side=tk.LEFT, padx=(10, 5))

        button_save = tk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_options(False),
            bg='orange',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_save.pack(side=tk.LEFT, padx=5)

        button_ok = tk.Button(
            button_frame,
            text="OK",
            command=lambda: self.save_options(True),
            bg='green',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_ok.pack(side=tk.LEFT, padx=(5, 10))

        # Bind Enter key for saving options (same behavior as pressing OK)
        self.game_opts_window.bind('<Return>', lambda event: self.save_options(True))

        # Set focus on the base number entry
        self.base_number_option.focus_set()

    def save_options(self, ok_pressed:bool):
        base_number_str = self.base_number_option.get()
        percentage_str = self.percentage_option.get()

        if not base_number_str.isdigit() or not percentage_str.isdigit():
            messagebox.showerror("Input Error", "Please enter valid integers for both fields.")
            return

        base_number = int(base_number_str)
        percentage = int(percentage_str)

        if not (1 <= base_number <= 2):
            messagebox.showerror("Input Error", "Base number must be between 1 and 2.")
            return
        if not (0 <= percentage <= 100):
            messagebox.showerror("Input Error", "Percentage must be between 0 and 100.")
            return

        # Process the options here
        old_base = self.grid.base_number
        self.grid.base_number = base_number
        self.grid.percent_double_base_on_spawn = percentage

        if ok_pressed:
            self.game_opts_window.destroy()

        if old_base != base_number:
            self.restart()

    def add_custom_value(self):
        """Prompt user for a custom value to add to the board"""
        self.custom_value_window = tk.Toplevel()
        self.custom_value_window.title("Add Custom Value")

        # Set a minimum size for the window
        self.custom_value_window.minsize(300, 200)

        # Customize the background color
        self.custom_value_window.configure(bg='lightblue')

        # Checkbox for power input (default checked)
        self.power_input_var = tk.BooleanVar(value=True)  # Default checked
        power_checkbox = tk.Checkbutton(
            self.custom_value_window,
            text="Power instead of raw value",
            variable=self.power_input_var,
            bg='lightblue',  # Match the window's background
            font=('Arial', 10)
        )
        power_checkbox.pack(pady=(20, 10))

        # Input Field
        label = tk.Label(self.custom_value_window, text="Enter custom value (must be a power of the base number):",
                         bg='lightblue', font=('Arial', 10))
        label.pack(pady=(10, 0))

        self.custom_value_entry = tk.Entry(self.custom_value_window, font=('Arial', 12), width=30)
        self.custom_value_entry.pack(pady=5, padx=10)

        # Buttons frame for better organization
        button_frame = tk.Frame(self.custom_value_window, bg='lightblue')
        button_frame.pack(pady=20)

        button_cancel = tk.Button(
            button_frame,
            text="Cancel",
            command=self.custom_value_window.destroy,
            bg='red',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_cancel.pack(side='left', padx=(0, 10))

        button_add = tk.Button(
            button_frame,
            text="Add",
            command=self.process_custom_value,
            bg='green',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_add.pack(side='left')

        # Bind Enter key to the process_custom_value method
        self.custom_value_window.bind('<Return>', lambda event: self.process_custom_value())

        # Optionally, focus on the entry field for convenience
        self.custom_value_entry.focus_set()

    def process_custom_value(self):
        """Process the value entered by the user and add it to the board."""
        custom_value_str = self.custom_value_entry.get()

        if self.power_input_var.get():
            # Validate as power
            if not custom_value_str.isdigit():
                messagebox.showerror("Input Error", "Please enter a valid integer.")
                return

            power = int(custom_value_str)

            # Calculate the actual custom value
            custom_value = self.grid.base_number ** power
        else:
            # Validate as raw value
            if not custom_value_str.isdigit():
                messagebox.showerror("Input Error", "Please enter a valid integer.")
                return

            custom_value = int(custom_value_str)

        # Check if the value is compliant with base number
        if custom_value < self.grid.base_number or custom_value % self.grid.base_number != 0:
            messagebox.showerror("Input Error", f"Value must be a power of the base number {self.grid.base_number}.")
            return

        # Call spawn method with custom_value
        self.grid.spawn(spawn_no=1, custom_value=custom_value)
        self.ui.update()
        self.custom_value_window.destroy()

    def frame_size_options(self):
        """Open the frame size adjustment window."""
        # Create an adjustment window
        self.frame_size_window = tk.Toplevel()
        self.frame_size_window.title("Frame Size Adjustment")
        self.frame_size_window.configure(bg='lightblue')
        self.frame_size_window.minsize(300, 150)

        # Label to show current frame size
        self.frame_size_label = tk.Label(self.frame_size_window,
                                         text=f"Current Frame Size: {self.grid.frame_size}",
                                         bg='lightblue',
                                         font=('Arial', 12))
        self.frame_size_label.pack(pady=(20, 20))

        # Frame size adjustment buttons
        button_frame_size_adjust = tk.Frame(self.frame_size_window, bg='lightblue')
        button_frame_size_adjust.pack(pady=5)

        button_decrease_frame_size = tk.Button(
            button_frame_size_adjust,
            text="-",
            command=self.decrease_frame_size,
            bg='orange',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_decrease_frame_size.pack(side=tk.LEFT, padx=(0, 5))

        button_increase_frame_size = tk.Button(
            button_frame_size_adjust,
            text="+",
            command=self.increase_frame_size,
            bg='green',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_increase_frame_size.pack(side=tk.LEFT, padx=(5, 0))

        # Close button for the frame size window
        close_button = tk.Button(self.frame_size_window,
                                 text="Close",
                                 command=self.frame_size_window.destroy, bg='red', fg='white', font=('Arial', 10, 'bold')
                                 )
        close_button.pack(pady=(20, 10))

    def increase_frame_size(self):
        """Increase the frame size by 1."""
        self.grid.frame_size += 1
        self.frame_size_label.config(text=f"Current Frame Size: {self.grid.frame_size}")

        self.ui.grid_config()
        self.restart()

    def decrease_frame_size(self):
        """Decrease the frame size by 1, but do not go below 4."""
        if self.grid.frame_size > 4:
            self.grid.frame_size -= 1
            self.frame_size_label.config(text=f"Current Frame Size: {self.grid.frame_size}")

            self.ui.grid_config()
            self.restart()
        else:
            messagebox.showwarning("Frame Size Error", "Frame size cannot be less than 4.")

    def help(self):
        """Open help window with explanation of game, controls, and options."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("800x600")
        help_window.configure(bg='lightblue')

        help_text = (
            "2048 Game Help\n\n"
            "Objective:\n"
            "Combine tiles with the same numbers to reach the 2048 tile.\n\n"
            "Controls:\n"
            "- Use arrow keys to move the tiles:\n"
            "  Up: Move tiles up\n"
            "  Down: Move tiles down\n"
            "  Left: Move tiles left\n"
            "  Right: Move tiles right\n"
            "- Press 'Escape' to restart the game.\n\n"
            "Options:\n"
            "- Base number (1-4): Set the base number for the tiles.\n"
            "- Percentage for double values spawning (0-100): Control how often double base numbers are spawned.\n\n"
            "Custom Value:\n"
            "- You can add a custom value to the board using the 'Add Custom Value' option.\n"
            "- Ensure it's a power of the base number if the checkbox is checked."
        )

        text_area = tk.Text(help_window, bg='lightblue', fg='black', font=('Arial', 12), wrap=tk.WORD)
        text_area.insert(tk.END, help_text)
        text_area.config(state=tk.DISABLED)
        text_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Close button for the help window
        close_button = tk.Button(help_window, text="Close", command=help_window.destroy, bg='red', fg='white', font=('Arial', 10, 'bold'))
        close_button.pack(pady=10)

    def ai_options(self):
        """Open the AI options window."""
        # Create secondary (or popup) window.
        self.ai_opts_window = tk.Toplevel()
        self.ai_opts_window.title("AI Options")
        self.ai_opts_window.configure(bg='lightblue')
        self.ai_opts_window.minsize(400, 250)

        # Depth option
        self.depth_option_label = tk.Label(self.ai_opts_window,
                                           text="AI Search Depth:",
                                           bg='lightblue',
                                           font=('Arial', 10))
        self.depth_option_label.pack(pady=(20, 0))
        self.depth_option = tk.Entry(self.ai_opts_window,
                                     font=('Arial', 12),
                                     width=10)
        self.depth_option.insert(0, str(getattr(self, 'depth', 1)))  # Default value or current depth
        self.depth_option.pack(pady=5)

        # AI method selection
        ai_method = 'ai' if self.ai_auto_play else 'random'
        self.ai_method_var = tk.StringVar(value=ai_method)
        random_radio = tk.Radiobutton(self.ai_opts_window,
                                      text="Random",
                                      variable=self.ai_method_var,
                                      value='random',
                                      bg='lightblue',
                                      font=('Arial', 10))
        random_radio.pack(pady=(10, 0))

        ai_search_radio = tk.Radiobutton(self.ai_opts_window,
                                         text="AI Search",
                                         variable=self.ai_method_var,
                                         value='ai',
                                         bg='lightblue',
                                         font=('Arial', 10))
        ai_search_radio.pack()

        # Buttons frame for better organization
        button_frame = tk.Frame(self.ai_opts_window, bg='lightblue')
        button_frame.pack(pady=20)

        button_cancel = tk.Button(
            button_frame,
            text="Cancel",
            command=self.ai_opts_window.destroy,
            bg='red',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_cancel.pack(side=tk.LEFT, padx=(10, 5))

        button_save = tk.Button(
            button_frame,
            text="Save",
            command=self.save_ai_options,
            bg='orange',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        button_save.pack(side=tk.LEFT, padx=5)

        # Bind Enter key for saving options (same behavior as pressing Save)
        self.ai_opts_window.bind('<Return>', lambda event: self.save_ai_options())

        # Set focus on depth entry
        self.depth_option.focus_set()

    def save_ai_options(self):
        """Save the AI options and close the window."""
        depth_str = self.depth_option.get()

        if not depth_str.isdigit():
            messagebox.showerror("Input Error", "Please enter a valid integer for depth.")
            return

        depth = int(depth_str)
        # Save the depth to the instance
        self.depth = depth

        # You can set a variable for the AI method selection
        if self.ai_method_var.get() == 'ai':
            self.ai_auto_play = True
        else:
            self.ai_auto_play = False

        self.ai_opts_window.destroy()

    def toggle_auto_play(self):
        """Toggle the automatic play on and off."""
        if not self.perform_auto_play:
            print("----------------------------------------------------------------------------------------------------------------")
            print("AUTO PLAY ACTIVATED")
            print("----------------------------------------------------------------------------------------------------------------")
            if self.agent is None:
                self.agent = Agent(ui=self.ui)

            self.perform_auto_play = True
            self.auto_play()
        else:
            print("----------------------------------------------------------------------------------------------------------------")
            print("AUTO PLAY DEACTIVATED")
            print("----------------------------------------------------------------------------------------------------------------")
            self.perform_auto_play = False

    def auto_play(self):
        """Automatically perform random moves while auto_playing."""
        if self.perform_auto_play:
            game_over = False

            # AI or Random
            if self.ai_auto_play:
                _, direction = self.agent.step(grid=self.ui.grid, depth=self.depth)
            else:
                direction = random.randint(0, 3)

            # Check for game over via ai
            if direction == -1:
                game_over = True
            else:
                # Perform move
                self.move(direction)
                # check for game over after move
                if self.grid.check_game_over():
                    game_over = True

            # Game over
            if game_over:
                self.perform_auto_play = False
                print("----------------------------------------------------------------------------------------------------------------")
                print("AUTO PLAY GAME OVER")
                print("----------------------------------------------------------------------------------------------------------------")
                self.end()

            # Schedule the next move
            self.root.after(300, self.auto_play)

