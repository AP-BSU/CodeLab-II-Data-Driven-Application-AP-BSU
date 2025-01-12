from ffpyplayer.player import MediaPlayer
import cv2
import subprocess
import tkinter as tk

def play_video_with_ffpyplayer(video_path, next_file):
    """
    Plays a video with audio using OpenCV and ffpyplayer.
    Ensures video and audio are played at normal speed.
    """
    def get_audio_frame(player):
        """
        Extracts and synchronizes audio with video.
        """
        audio_frame, val = player.get_frame()
        if val != 'eof' and audio_frame is not None:
            img, t = audio_frame
        return val

    def skip_video(event=None):
        """
        Stops the video and transitions to the next Python file.
        """
        cap.release()
        player.close_player()
        cv2.destroyAllWindows()
        root.destroy()
        subprocess.run(["python", next_file])

    # OpenCV video capture and ffpyplayer audio player
    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)

    # Get the video's FPS (Frames Per Second)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 25  # Default fallback if FPS is not available
    frame_time_ms = int(1000 / fps)  # Frame time in milliseconds

    # Create Tkinter window
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.bind("<space>", skip_video)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to fit screen
        frame = cv2.resize(frame, (root.winfo_screenwidth(), root.winfo_screenheight()))
        cv2.imshow("Video Player", frame)

        # Synchronize audio
        get_audio_frame(player)

        # Delay to match the frame rate
        if cv2.waitKey(frame_time_ms) & 0xFF == 32:  # Spacebar pressed
            skip_video()

    # Finish playback
    skip_video()

if __name__ == "__main__":
    video_path = r"Intro.mp4"  # Replace with the actual path to the video
    next_file = r"menu.py"    # Replace with the actual path to the next Python file
    play_video_with_ffpyplayer(video_path, next_file)
