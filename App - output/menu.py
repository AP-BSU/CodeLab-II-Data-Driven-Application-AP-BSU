import tkinter as tk
from PIL import Image, ImageTk
import threading
import vlc
import requests
import subprocess

def create_main_menu():
    # Initialize the main Tkinter window
    root = tk.Tk()
    root.title("Main Menu")
    root.attributes("-fullscreen", True)  # Enable fullscreen mode
    root.configure(bg="#173759")  # Set background color

    # Function to close the application
    def exit_app(event=None):
        # Exit fullscreen mode and close the application
        root.attributes("-fullscreen", False)
        root.destroy()

    # Bind Escape key to exit fullscreen
    root.bind("<Escape>", exit_app)

    # Button click placeholder functions
    def start_app():
        # Load the game.py script seamlessly
        root.destroy()  # Close current GUI
        subprocess.run(["python", r"game.py"])  # Run the next script

    def show_tutorial():
        # Display a large image as an overlay
        overlay = tk.Toplevel(root)
        overlay.attributes("-fullscreen", True)  # Make it fullscreen
        overlay.configure(bg="#000000")  # Black background

        # Load and display the tutorial image
        try:
            tutorial_image = Image.open(r"C:\Users\User\Downloads\ADRIAN\Receiver\Office\BSU\BSU(Y2) - 2024 - 2025\CodeLab2\Works\SA2\App\assets\images\menu-overlay.png")  # Replace with your tutorial image file path
            tutorial_image = tutorial_image.resize((800, 600))  # Resize to fit the screen
            tutorial_photo = ImageTk.PhotoImage(tutorial_image)

            tutorial_label = tk.Label(overlay, image=tutorial_photo, bg="#000000")
            tutorial_label.image = tutorial_photo  # Keep a reference to avoid garbage collection
            tutorial_label.pack(expand=True)

        except Exception as e:
            print(f"Error loading tutorial image: {e}")
            tk.Label(overlay, text="Tutorial Image Not Found", font=("Lucida Console", 24, "bold"),
                     bg="#000000", fg="white").pack(expand=True)

        # Bind click anywhere on the screen to close the overlay
        overlay.bind("<Button-1>", lambda e: overlay.destroy())

    def quit_app():
        # Handle the Quit button click and close the application
        root.destroy()

    # Check Internet Connection
    def check_connection():
        # Check if the user is connected to the internet and update the status label
        try:
            requests.get("https://www.google.com", timeout=5)
            connection_label.config(text="Connection: Online", fg="green")
        except requests.ConnectionError:
            connection_label.config(text="Connection: Not Connected", fg="red")

    # Play sound function
    def play_hover_sound():
        # Play a sound effect when the button is hovered using vlc
        threading.Thread(target=lambda: vlc.MediaPlayer(
            r"On click-menufx.mp3"  # Replace with your hover sound file
        ).play()).start()

    # Styles for buttons
    button_style = {
        "font": ("Lucida Console", 28, "bold"),  # Increased font size
        "fg": "yellow",
        "bg": "#444444",
        "relief": "flat",
        "bd": 0,
        "activebackground": "#555555",
        "cursor": "hand2",
        "width": 30,  # Wider button
    }

    # Load and display the logo
    try:
        logo_image = Image.open(r"C:\Users\User\Downloads\ADRIAN\Receiver\Office\BSU\BSU(Y2) - 2024 - 2025\CodeLab2\Works\SA2\App\assets\images\Gamelogob.png")  # Replace with your logo file path
        logo_image = logo_image.resize((600, 200))  # Adjust size for the larger logo
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(root, image=logo_photo, bg="#173759")
        logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
        logo_label.pack(pady=30)  # Space above and below the logo
    except Exception as e:
        print(f"Error loading logo: {e}")
        logo_label = tk.Label(root, text="Logo Here", font=("Lucida Console", 24, "bold"), bg="#173759", fg="white")
        logo_label.pack(pady=30)

    # Create a frame with dashed border to enclose the buttons
    border_frame = tk.Frame(
        root,
        bg="#173759",
        highlightbackground="white",
        highlightcolor="white",
        highlightthickness=3,
        bd=0,
    )
    border_frame.pack(pady=20)

    # Function to create a button with hover sound effects
    def create_hover_button(parent, text, command):
        # Create a button inside the dashed border container with hover sound effect
        button = tk.Button(parent, text=text, command=command, **button_style)
        button.bind("<Enter>", lambda e: play_hover_sound())  # Play sound on hover
        button.pack(pady=15, ipadx=30, ipady=15)  # Add spacing and scaling
        return button

    # Add buttons inside the dashed border container
    create_hover_button(border_frame, "Start", start_app)
    create_hover_button(border_frame, "Tutorial", show_tutorial)
    create_hover_button(border_frame, "Quit", quit_app)

    # Internet connection status label
    connection_label = tk.Label(
        root, text="Checking connection...", font=("Lucida Console", 20), bg="#173759", fg="white"
    )
    connection_label.pack(pady=15)  # Space between label and buttons

    # Check the connection status
    threading.Thread(target=check_connection).start()

    # Start the Tkinter main event loop
    root.mainloop()


if __name__ == "__main__":
    create_main_menu()
