**Motion Detection and Email Notification System**  

This project is a Python-based application that uses OpenCV for real-time motion detection and sends email notifications with a snapshot of the detected motion. The system captures video from a webcam, identifies motion using frame differencing and contour detection, and performs the following tasks:  

- **Motion Detection**: Detects significant movements in the video feed.  
- **Email Notification**: Sends an email with an image attachment of the detected motion.  
- **Automated Cleanup**: Deletes captured images after the email is sent to save storage.  
- **Multithreading**: Ensures smooth performance by handling email sending and image cleanup in separate threads.  

This project demonstrates the use of OpenCV for video processing and multithreading in Python to create an efficient motion detection and alert system.  

Feel free to customize this description based on your implementation details!
