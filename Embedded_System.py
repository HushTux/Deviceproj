import Adafruit_DHT
import random
import requests
from RPLCD.i2c import CharLCD
import time
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory

# Initialize the LCD (specify the I2C address and port)
lcd = CharLCD('PCF8574', 0x27)

# Set the type of sensor: DHT11
dht_sensor = Adafruit_DHT.DHT11
dht_pin = 26  # GPIO pin where the DHT11 is connected

# Set up pigpio factory for DistanceSensor
factory = PiGPIOFactory()

# Initialize the ultrasonic sensor (HC-SR04)
ultrasonic = DistanceSensor(echo=24, trigger=23, pin_factory=factory, max_distance=2)

# List of funny messages for the idle screen
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

# Define custom characters for LCD (like eyes open and closed)
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

# Define an animation for the LCD (like blinking eyes)
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
        ((1, 1), " -  Zzzzz"),
        ((1, 1), " -  Zzzzzz "),
        ((1, 1), " -  Zzzzzzz ")
    ]
    # Loop through the animation frames
    for eyes, mouth in animation_frames:
        lcd.clear()
        lcd.write_string(chr(eyes[0]) + ' ' + chr(eyes[1]))
        lcd.cursor_pos = (1, 0)  # Move cursor to the second row for the mouth
        lcd.write_string(mouth)
        time.sleep(0.5)  # Pause between frames

# Function to read from the DHT sensor
def read_dht_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)
    return humidity, temperature

# Function to display sensor readings on the LCD
def display_on_lcd(humidity, temperature):
    lcd.clear()
    if humidity is not None and temperature is not None:
        lcd.write_string(f'Temp: {temperature:.1f} C')
        lcd.crlf()
        lcd.write_string(f'Humidity: {humidity:.1f} %')
    else:
        lcd.write_string('Sensor error')
        lcd.crlf()
        lcd.write_string('Check connection')

# Function to handle what to do when in idle state
def idle_screen():
    if random.choice([True, False]):
        lcd.clear()
        random_message = random.choice(idle_messages)
        lcd.write_string(random_message)
    else:
        animate_lcd(lcd)

# Function to handle what to do when motion is detected
def motion_detected():
    humidity, temperature = read_dht_sensor()
    display_on_lcd(humidity, temperature)
    send_data_to_server(humidity, temperature)

# Function to send the sensor data to the Flask server
def send_data_to_server(humidity, temperature):
    server_url = 'http://192.168.1.197:5000/update'
    try:
        response = requests.post(server_url, json={'temperature': temperature, 'humidity': humidity})
        print('Data sent to server:', response.text)
    except requests.exceptions.RequestException as e:
        print('Failed to send data to server:', e)

# Main loop
try:
    idle_screen()
    while True:
        if ultrasonic.distance < 0.5:  # Threshold distance set to 0.5 meters
            motion_detected()
        else:
            idle_screen()
        time.sleep(5)  # Wait 5 seconds between checks
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    lcd.clear()
    lcd.close()
    print("LCD display cleared and closed")
