import RPi.GPIO as GPIO
import time

SERVO_PIN = 18

def drop_payload():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(2.5)
    
    print("Activating servo for payload release...")
    pwm.ChangeDutyCycle(7.5)  # Adjust angle for drop
    time.sleep(1)
    pwm.ChangeDutyCycle(2.5)  # Reset position
    time.sleep(1)
    
    pwm.stop()
    GPIO.cleanup()
