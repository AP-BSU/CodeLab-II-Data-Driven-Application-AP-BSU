import tkinter as tk
from tkinter import messagebox
import random
import requests
from PIL import Image, ImageTk
import pygame
from threading import Thread
import time
import os
import sys

# API URL and constants
TRIVIA_API = "https://opentdb.com/api.php?amount=1&type=multiple"
MAX_QUESTIONS = 7
BACKUP_FILE = r"backup.txt"  # Path to the backup file

# Initialize pygame for sound effects
pygame.init()
pygame.mixer.init()

# File paths for assets
BACKGROUND_IMAGE = r"wireframe-game.png"
WIN_SOUND = r"Win_fx.mp3"
LOSE_SOUND = r"LossFx.mp3"
MUSIC_FILES = [r"tension-fxB.mp3", 
               r"tension-fxC.mp3"]

# Fetch a question and options from the Trivia API
def fetch_trivia_question():
    # Fetch data from the API
    try:
        response = requests.get(TRIVIA_API, timeout=5)
        if response.status_code == 200:
            data = response.json()["results"][0]
            question = data["question"]
            correct_answer = data["correct_answer"]
            options = data["incorrect_answers"] + [correct_answer]
            random.shuffle(options)  # Shuffle options
            return question, correct_answer, options
    except requests.RequestException:
        pass
    return None, None, []  # Return empty data on failure

# Fetch a question and options from the backup file
def fetch_backup_question():
    # Load question data from the backup file
    try:
        with open(BACKUP_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                line = random.choice(lines).strip()
                parts = line.split(",")  # Split the line into parts
                if len(parts) == 5:
                    question = parts[0]
                    correct_answer = parts[1]
                    options = parts[1:]  # Include correct and wrong answers
                    return question, correct_answer, options
    except FileNotFoundError:
        pass
    return None, None, []  # Return empty data on failure

# Play background music in a loop
def play_music():
    music = random.choice(MUSIC_FILES)
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)  # Loop music indefinitely

# Stop background music
def stop_music():
    pygame.mixer.music.stop()

# Main application class for the game
class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)  # Set fullscreen mode
        self.question_number = 1  # Initialize question count
        self.score = 0  # Initialize score

        # Load and set the background image
        self.bg_image = ImageTk.PhotoImage(Image.open(BACKGROUND_IMAGE).resize(
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        ))
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Main container for game UI
        self.main_container = tk.Frame(self.root, bg="black", highlightthickness=0)
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=700)

        # Start the game immediately
        self.start_game()

    # Start the game logic
    def start_game(self):
        self.question_number = 1  # Reset question number
        self.score = 0  # Reset score
        self.clear_screen()  # Clear UI
        play_music()  # Play background music
        self.show_question()  # Show the first question

    # Restart the application
    def restart_game(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)  # Restart the Python script

    # Display the next question
    def show_question(self):
        if self.question_number > MAX_QUESTIONS:
            self.end_game()  # End game if max questions reached
            return

        # Try fetching from API, fallback to backup file if API fails
        question, correct_answer, options = fetch_trivia_question()
        if not question or not correct_answer:
            question, correct_answer, options = fetch_backup_question()

        # Handle case when no questions are available
        if not question or not correct_answer:
            messagebox.showinfo("Trivia Failsafe", "No question available. You win this round!")
            self.score += 10
            self.question_number += 1
            self.show_question()
            return

        self.correct_answer = correct_answer  # Store correct answer
        self.clear_screen()  # Clear UI

        # Display timer above the question
        self.timer_label = tk.Label(
            self.main_container, text="", font=("Lucida Console", 18), fg="white", bg="black"
        )
        self.timer_label.pack(pady=10)

        # Display the question text
        tk.Label(
            self.main_container,
            text=question,
            font=("Lucida Console", 20),
            bg="black",
            fg="white",
            wraplength=900,
        ).pack(pady=20)

        # Create a grid layout for answer options
        options_frame = tk.Frame(self.main_container, bg="black")
        options_frame.pack(pady=20)
        for i, option in enumerate(options):
            tk.Button(
                options_frame,
                text=option,
                font=("Lucida Console", 18),
                bg="gray",
                fg="white",
                command=lambda opt=option: self.check_answer(opt),  # Pass the selected answer
                width=30,
                height=2,
            ).grid(row=i // 2, column=i % 2, padx=10, pady=10)

        self.start_timer(25)  # Start countdown timer

    # Start the countdown timer
    def start_timer(self, seconds):
        self.time_left = seconds  # Initialize timer

        def countdown():
            while self.time_left > 0:
                self.timer_label.config(text=f"Time Left: {self.time_left}s")
                time.sleep(1)
                self.time_left -= 1
            if self.time_left == 0:
                self.end_game("Time's up! Game Over!")  # End game on timeout

        Thread(target=countdown, daemon=True).start()  # Run timer in a separate thread

    # Check if the selected answer is correct
    def check_answer(self, selected):
        stop_music()  # Stop background music
        if selected == self.correct_answer:
            pygame.mixer.Sound(WIN_SOUND).play()  # Play win sound
            self.score += 10  # Increment score
            self.question_number += 1  # Move to next question
            self.show_question()
        else:
            pygame.mixer.Sound(LOSE_SOUND).play()  # Play lose sound
            self.end_game("Incorrect answer. Game Over!")  # End game on incorrect answer

    # End the game and display final message
    def end_game(self, message="Thank you for playing!"):
        stop_music()  # Stop background music
        self.clear_screen()  # Clear UI
        tk.Label(
            self.main_container,
            text=message,
            font=("Lucida Console", 24),
            fg="yellow",
            bg="black",
        ).pack(pady=50)
        tk.Button(
            self.main_container,
            text="Play Again",
            font=("Lucida Console", 18),
            bg="blue",
            fg="white",
            width=20,
            command=self.start_game,  # Restart the game logic
        ).pack(pady=10)
        tk.Button(
            self.main_container,
            text="Quit",
            font=("Lucida Console", 18),
            bg="red",
            fg="white",
            width=20,
            command=self.root.quit,  # Exit the application
        ).pack(pady=10)

    # Clear all widgets from the UI container
    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
