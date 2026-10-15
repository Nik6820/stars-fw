from rpi_hardware_pwm import HardwarePWM
import RPi.GPIO as GPIO

DIR = 27
PWM_CHANNEL = 0    # 0 = GPIO 18 (или GPIO 12), 1 = GPIO 19 (или GPIO 13)

STEPS_PER_REV = 200 * 32   # 200 шагов * микрошаг 1/32
MIN_RPM, MAX_RPM = 1, 150

def rpm_to_hz(rpm):
    return rpm * STEPS_PER_REV / 60

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT, initial=GPIO.HIGH)   # GPIO.LOW для обратного направления

pwm = HardwarePWM(pwm_channel=PWM_CHANNEL, hz=rpm_to_hz(30), chip=0)
pwm.start(50)      # скважность 50%

try:
    while True:
        try:
            rpm = max(MIN_RPM, min(MAX_RPM, float(input("Новая скорость (об/мин): "))))
        except ValueError:
            print("Нужно число")
            continue
        pwm.change_frequency(rpm_to_hz(rpm))
        print(f"Скорость: {rpm} об/мин ({rpm_to_hz(rpm):.0f} Гц)")
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

