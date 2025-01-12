import tkinter as tk

def create_main_menu():
    """
    #Creates the main menu with fullscreen mode, black background,
    and a single white button in the center.
    """
    root = tk.Tk()
    root.title("Main Menu")
    root.attributes("-fullscreen", True)  # Start in fullscreen
    root.configure(bg="black")  # Set background color to black

    # Function to close the app
    def exit_app(event=None):
        root.attributes("-fullscreen", False)
        root.destroy()

    # Bind Escape key to close the app
    root.bind("<Escape>", exit_app)

    # Add a white button in the center
    button = tk.Button(
        root,
        text="Click Me",
        font=("Arial", 16),
        bg="white",
        command=lambda: print("Button Clicked!")
    )
    button.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    create_main_menu()
