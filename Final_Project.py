# Necessary Imports
from gpiozero import MotionSensor, LED
from picamera import PiCamera
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time
import smtplib

# Email configurations
email_provider = "mms.att.net"
email_address = "doctorfrogster@gmail.com"
email_password = "H8o15l12y25."
phone_number = "8593825226"
smtp_server = "smtp.gmail.com"
photo_path = ""
smtp_port = 587

# Setup GPIO pins
motion_sensor = MotionSensor(6)
led = LED(26, active_high=False)

# Setup camera
camera = PiCamera()
camera.resolution = (3280,2464)

# Function to take a timestamped picture and save it to pi files
def take_picture():
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"/home/pi/Downloads/motion_{timestamp}.jpg"
    camera.capture(filename)
    print(f"Picture taken: {filename}")
    return filename

# Email functions similar to sendip
def send_email(photo_path):
    if email_provider == "8593825226@txt.att":
        print("Please configure your email provider.")
        return
    subject = "Motion Detected!"
    body = "Motion detected on PI Sensor!"

    # Create message
    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = f"{phone_number}@{email_provider}"
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Attach photo if path is provided
    if photo_path:
        with open(photo_path, 'rb') as f:
            img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename=photo_path)
        message.attach(img)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, f"{phone_number}@{email_provider}", message.as_string())
            print("Email notification sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

while True:
    motion_sensor.wait_for_motion()
    print("Motion detected")

    led.on()
    photo_path = take_picture()
    send_email(photo_path)
    time.sleep(.5)
    photo_path = take_picture()
    send_email(photo_path)
    time.sleep(.5)
    photo_path = take_picture()
    send_email(photo_path)
    time.sleep(.5)
    photo_path = take_picture()
    send_email(photo_path)
    time.sleep(1)
    led.off()
    time.sleep(5)