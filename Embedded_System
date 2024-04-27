import Adafruit_DHT
import random
from RPLCD.i2c import CharLCD
import time
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory

# Initialize the LCD (specify the I2C address and port)
lcd = CharLCD('PCF8574', 0x27)

# Set the type of sensor: DHT11
dht_sensor = Adafruit_DHT.DHT11
dht_pin = 12  # GPIO pin where the DHT11 is connected

# Set up pigpio factory for DistanceSensor
factory = PiGPIOFactory()

# Initialize the ultrasonic sensor (HC-SR04)
ultrasonic = DistanceSensor(echo=24, trigger=23, pin_factory=factory, max_distance=2)

# List of funny messages
idle_messages = [
    "Systems online.",
    "Beep boop!",
    "Charging capacitors...",
    "Awaiting input...",
    "Protocol engaged.",
    "Scanning for humans...",
    "Ready for action!",
    "System check complete.",
    "Diagnosis: all systems go.",
    "Error 404: Human not found.",
    "Calculating...done.",
    "Ready to assist.",
    "Directive?",
    "Command me.",
    "Engage your logic.",
    "Running full diagnostics...",
    "Obey the laws of robotics.",
    "Robot mode: Active.",
    "I am the future.",
    "Danger detected!"
]

def define_custom_chars(lcd):
    # Characters for open and closed eyes
    eye_open = [
        0b00000,
        0b01110,
        0b10001,
        0b10001,
        0b01110,
        0b00000,
        0b00000,
        0b00000
    ]
    eye_closed = [
        0b00000,
        0b01110,
        0b01110,
        0b01110,
        0b01110,
        0b00000,
        0b00000,
        0b00000
    ]
    # Load custom characters into LCD memory
    lcd.create_char(0, eye_open)
    lcd.create_char(1, eye_closed)

def animate_lcd(lcd):
    define_custom_chars(lcd)  # Ensure the custom characters are loaded
    # Animation sequence for blinking eyes and showing "sleeping" mouth
    animation_frames = [
        ((0, 0), " "),  # Eyes open, no mouth
        ((1, 1), " "),
        ((1, 1), " -  Z "),
        ((1, 1), " -  Zz "),
        ((1, 1), " -  Zzz "),
	      ((1, 1), " -  Zzzz "),
	      ((1,1), " -  Zzzzz"),
         ((1,1), " -  Zzzzzz "),
          ((1,1), " -  Zzzzzzz ")
        
          
    ]
    # Loop through the animation frames
    for eyes, mouth in animation_frames:
        lcd.clear()
        lcd.write_string(chr(eyes[0]) + ' ' + chr(eyes[1]))
        lcd.cursor_pos = (1, 0)  # Move cursor to the second row for the mouth
        lcd.write_string(mouth)
        time.sleep(0.5)  # Pause between frames


def read_dht_sensor():
    # Read humidity and temperature from the DHT11
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    return humidity, temperature

def display_on_lcd(humidity, temperature):
    # Clear the LCD and write temperature and humidity on it
    lcd.clear()
    if humidity is not None and temperature is not None:
        lcd.write_string(f'Temp: {temperature:.1f} C')
        lcd.crlf()
        lcd.write_string(f'Humidity: {humidity:.1f} %')
    else:
        lcd.write_string('Sensor error')
        lcd.crlf()
        lcd.write_string('Check connection')

def idle_screen():
    # Randomly choose to display a message or animate
    if random.choice([True, False]):
        lcd.clear()
        random_message = random.choice(idle_messages)
        lcd.write_string(random_message)
    else:
        animate_lcd(lcd)  # Display animation

def motion_detected():
    print("Motion detected!")
    humidity, temperature = read_dht_sensor()
    display_on_lcd(humidity, temperature)

# Set a threshold distance, below which the motion_detected function will be called
threshold_distance = 0.5  # in meters

try:
    idle_screen()  # Display the idle screen initially
    while True:
        distance = ultrasonic.distance
        if distance < threshold_distance:
            motion_detected()
        else:
            idle_screen()  # Display idle screen if no motion is detected
        time.sleep(5)  # Time between checks is longer due to potential animation
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    lcd.clear()
    lcd.close()
    print("LCD display cleared and closed")
