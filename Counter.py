import cv2
import numpy as np
import pyvirtualcam
import time

# Countdown Timer: 30 minutes (in seconds)
COUNTDOWN_SECONDS = 30 * 60  # 30 minutes

width = 320
height = 180

# Function to generate countdown text frame
def generate_frame(time_left):
    # Create a blank canvas (black background)
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Format time as mm:ss
    minutes = time_left // 60
    seconds = time_left % 60
    time_str = f"{minutes:02d}:{seconds:02d}"

    # Draw the countdown text on the frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    font_color = (255, 255, 255)  # White color
    thickness = 8
    text_size = cv2.getTextSize(time_str, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2

    # Put the timer text on the frame
    cv2.putText(frame, time_str, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)

    # Convert to RGB (for pyvirtualcam)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

def main():

    fps = 30  # Ensure FPS is explicitly set

    with pyvirtualcam.Camera(width=width, height=height, fps=fps, fmt=pyvirtualcam.PixelFormat.RGB) as cam:
        print(f"Virtual camera started: {cam.device}")

        start_time = time.time()
        while True:
            elapsed_time = int(time.time() - start_time)
            time_left = COUNTDOWN_SECONDS - elapsed_time

            if time_left < 0:
                print("Countdown finished!")
                break

            frame = generate_frame(time_left)
            cam.send(frame)
            cam.sleep_until_next_frame()

if __name__ == "__main__":
    main()
