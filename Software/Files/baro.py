from machine import Pin, I2C   ,lightsleep, PWM                     
import time , gc, sys, math
sys.path.insert(0, '/Libraries/Barometer')            # Uzyskanie dostępu do biblioteki barometru
from mpl3115a2 import MPL3115A2                       # Zimportowanie z biblioteki klasy MPL3115A2
i2cbus = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)# Towrzenie obietki I2C dla MPL3115A2
mpl = MPL3115A2(i2cbus, mode=MPL3115A2.ALTITUDE)      # Tworzenie obiektu MPL3115A2 pod nazwą mpl



while True:
    h = mpl.altitude()
    t = mpl.temperature()
    print(str(h) + '      ' + str(t)
          
          
          
          )
    time.sleep_ms(300)