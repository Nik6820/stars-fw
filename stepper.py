import RPi.GPIO as GPIO
import time
import threading

PUL = 17
DIR = 27

STEPS_PER_REV = 200 * 8   # 200 шагов * микрошаг 1/8 (как на DIP-переключателях)
MIN_RPM = 1
MAX_RPM = 150

rpm = 30                  # стартовая скорость, об/мин

GPIO.setmode(GPIO.BCM)
GPIO.setup(PUL, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DIR, GPIO.OUT, initial=GPIO.LOW)

def read_speed():
    global rpm
    while True:
        text = input("Новая скорость (об/мин): ")
        try:
            value = float(text)
        except ValueError:
            print("Нужно число")
            continue
        rpm = max(MIN_RPM, min(MAX_RPM, value))
        print(f"Скорость: {rpm} об/мин")

threading.Thread(target=read_speed, daemon=True).start()

GPIO.output(DIR, GPIO.HIGH)   # направление; GPIO.LOW для обратного
time.sleep(0.01)

try:
    while True:
        # половина периода импульса в секундах
        delay = 60 / (rpm * STEPS_PER_REV) / 2
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()