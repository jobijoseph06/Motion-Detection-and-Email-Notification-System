import glob
import os
import cv2
import time
from emailing import send_email
from threading import Thread

# Initialize the webcam
cap = cv2.VideoCapture(0)
time.sleep(1)  # Allow the camera to warm up

# Variables to store the first frame and motion detection status
first_frame = None
status_list = []
count = 1
email_done = False  # Flag to track if email has been sent

# Function to clean up all images in the "images" folder
def clean():
    images = glob.glob("images/*.png")  # Get all PNG files in the folder
    for image in images:
        os.remove(image)  # Remove each image

# Wrapper function for sending email and setting the completion flag
def send_email_wrapper(image_path):
    global email_done
    send_email(image_path)  # Call the email sending function
    email_done = True  # Set the flag to indicate email sending is done

# Main loop to capture video and process frames
while True:
    status = 0  # Initialize the motion status as no motion
    check, frame = cap.read()  # Capture the current frame

    # Convert the frame to grayscale for processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)  # Apply Gaussian blur

    # Store the first frame if it's not set
    if first_frame is None:
        first_frame = gray_frame_gau

    # Compute the difference between the first frame and the current frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Apply a threshold to highlight regions of motion
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded frame to fill in gaps
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Find contours of the motion regions
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in contours:
        # Ignore small movements by checking contour area
        if cv2.contourArea(i) < 5000:
            continue

        # Draw a rectangle around the detected motion
        x, y, w, h = cv2.boundingRect(i)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        # If motion is detected, update status and save the frame
        if rectangle.any():
            status = 1  # Motion detected
            cv2.imwrite(f"images/{count}.png", frame)  # Save the frame
            count += 1  # Increment the image counter
            all_images = glob.glob("images/*.png")  # Get all saved images
            index = int(len(all_images) / 2)  # Pick the middle image
            image_with_object = all_images[index]

    # Track the last two motion statuses
    status_list.append(status)
    status_list = status_list[-2:]

    # If motion stops (transition from 1 to 0), trigger email and cleanup
    if status_list[0] == 1 and status_list[1] == 0:
        if not email_done:  # Ensure no duplicate email threads
            # Start the email sending thread
            email_thread = Thread(target=send_email_wrapper, args=(image_with_object,))
            email_thread.start()

    # Once email is sent, trigger cleanup
    if email_done:
        email_done = False  # Reset the flag for the next email
        clean_thread = Thread(target=clean)  # Start the cleanup thread
        clean_thread.start()

    # Display the video with motion detection rectangles
    cv2.imshow("Video", frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
