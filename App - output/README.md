# README
**Begin the application by starting on start.py**

**Specification and Requirements:**

* Folder size: 14.8MB
* Internet access for API calls

**Operating System:**
Minimum: Windows 7 / macOS 10.13 / Ubuntu 18.04 or later.

**Processor**
Minimum: Dual-core processor (e.g., Intel Core i3 or AMD equivalent).

**Memory (RAM):**
Minimum: 4 GB.

**Graphics (GPU):**
Minimum: Integrated graphics (e.g., Intel UHD or AMD Radeon Vega for OpenCV).

**Storage:**
Minimum: 500 MB of free disk space (for Python, libraries, and assets like videos, images, and audio).


# Pylances used and details:

**Core libraries:** os, sys, subprocess, random, time, threading.
**GUI:** tkinter, tkinter.messagebox, PIL.Image, PIL.ImageTk.
**Media and audio:** cv2, ffpyplayer.player, vlc, pygame.
**Network:** requests.

1. start.py​menu:

* from ffpyplayer.player import MediaPlayer: For playing audio alongside video.
* import cv2: For video playback and frame processing.
* import subprocess: To run external scripts (e.g., menu.py).
* import tkinter as tk: For creating a graphical user interface (GUI).

2. menu.py​game:

* import tkinter as tk: For creating the GUI.
* from PIL import Image, ImageTk: For handling and displaying images.
* import threading: For running tasks in the background (e.g., checking internet connection).
* import vlc: For playing audio (hover sound effects).
* import requests: To check internet connectivity.
* import subprocess: To run external scripts (e.g., game.py).

3. game.py import tkinter as tk`: For creating the GUI.**

* from tkinter import messagebox: For displaying messages to the user.
* import random: For shuffling options and selecting backup questions.
* import requests: For fetching trivia questions from an API.
* from PIL import Image, ImageTk: For handling and displaying images.
* import pygame: For playing sound effects and background music.
* from threading import Thread: For running the countdown timer in the background.
* import time: For handling delays (e.g., countdown timer).
* import os: For interacting with the operating system (e.g., restarting the script).
* import sys: For restarting the script with the same Python interpreter.

# Thank you for the time to downoad and access my summative assessment!
- Adrian Garcia