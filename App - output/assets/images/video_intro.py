import cv2
import tkinter as tk
import subprocess
from screeninfo import get_monitors

# Function to wait for user input to start
def wait_for_enter():
    def start_app(event=None):
        root.destroy()  # Close the waiting screen and proceed

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    label = tk.Label(
        root,
        text="Press Enter to start the application...",
        font=("Arial", 24),
        fg="white",
        bg="black",
    )
    label.pack(expand=True)

    root.bind("<Return>", start_app)
    root.mainloop()

# Function to play video using OpenCV
def play_video(video_path):
    """
    Plays the given video file using OpenCV in fullscreen.
    The user can press the spacebar to skip the video.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    monitor = get_monitors()[0]
    screen_width, screen_height = monitor.width, monitor.height

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to fit the screen
        frame = cv2.resize(frame, (screen_width, screen_height))
        cv2.imshow("App Intro", frame)

        if cv2.waitKey(25) & 0xFF == ord(' '):  # Spacebar to skip
            print("Video skipped.")
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to launch the main menu
def launch_main_menu():
    subprocess.run(["python", r"CodeLab2\Works\SA2\App\assets\main_menu.py"])  # Call the second file

# Main program
if __name__ == "__main__":
    wait_for_enter()  # Step 1: Wait for user input
    play_video(r"CodeLab2\Works\SA2\App\assets\Intro.mp4")  # Step 2: Play the intro video
    launch_main_menu()  # Step 3: Launch the main menu
