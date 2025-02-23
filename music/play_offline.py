import os
import time
import subprocess
import RPi.GPIO as GPIO
import signal
import sys
from waveshare_PCF8563 import PCF8563

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Set up GPIO pin 27 as an output
led_pin = 27
GPIO.setup(led_pin, GPIO.OUT)

# Define the directories for the playlists
morning_playlist_dir = "~/music/morning"
evening_playlist_dir = "~/music/evening"

# Initialize the PCF8563 RTC
rtc = PCF8563.PCF8563()
rtc.Init()

# Function to play a playlist
def play_playlist(directory):
    if not os.path.exists(directory) or not any(filename.endswith(".mp3") for filename in os.listdir(directory)):
        return

    filenames = [filename for filename in sorted(os.listdir(directory)) if filename.endswith(".mp3")]
    for filename in filenames:
        file_path = os.path.join(directory, filename)
        try:
            subprocess.run(["mpg123", file_path], check=True)
            print(f"Playing file {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error playing file {file_path}: {e}")

# Function to get the current time from the PCF8563 RTC
def get_current_time():
    time_data = rtc.Get_Time()  # Returns [seconds, minutes, hours]
    return {
        "hour": time_data[2],
        "minute": time_data[1],
        "second": time_data[0]
    }

# Signal handler for script termination
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

# Main function to check the time and play the appropriate playlist
def main():
    morning_played = False
    evening_played = False
    GPIO.output(led_pin, GPIO.HIGH)
    print("LED is ON")
    
    while True:
        current_time = get_current_time()
        hour = current_time["hour"]
        minute = current_time["minute"]

        # Play morning playlist at 9:00 AM
        if hour == 9 and minute == 0 and not morning_played:
            try:
                print(f"Playing morning playlist at {hour:02d}:{minute:02d}")
                play_playlist(morning_playlist_dir)
                morning_played = True
                evening_played = False
            except Exception as e:
                print(f"Error playing morning playlist: {e}")

        # Play evening playlist at 6:30 PM
        elif hour == 18 and minute == 30 and not evening_played:
            try:
                print(f"Playing evening playlist at {hour:02d}:{minute:02d}")
                play_playlist(evening_playlist_dir)
                evening_played = True
                morning_played = False
            except Exception as e:
                print(f"Error playing evening playlist: {e}")

        # Reset flags at midnight
        elif hour == 0 and minute == 0:
            morning_played = False
            evening_played = False

        # Sleep for 20 seconds before checking the time again
        time.sleep(20)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting gurbaani audio player")
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")