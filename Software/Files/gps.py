from machine import Pin, UART, I2C
#Import utime library to implement delay
import utime, time


from micropyGPS import MicropyGPS
#https://github.com/inmcm/micropyGPS

##########################################################
#GPS Module UART Connection
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
##########################################################


##########################################################
TIMEZONE = 5
my_gps = MicropyGPS(TIMEZONE)
##########################################################

def convert(parts):
    if (parts[0] == 0):
        return None
        
    data = parts[0]+(parts[1]/60.0)
    # parts[2] contain 'E' or 'W' or 'N' or 'S'
    if (parts[2] == 'S'):
        data = -data
    if (parts[2] == 'W'):
        data = -data

    data = '{0:.6f}'.format(data) # to 6 decimal places
    return str(data)
##########################################################

##########################################################
while True:
    #_________________________________________________
    length = gps_module.any()
    if length>0:
        b = gps_module.read(length)
        for x in b:
            msg = my_gps.update(chr(x))
    #_________________________________________________
    latitude = convert(my_gps.latitude)
    longitude = convert(my_gps.longitude)
    #_________________________________________________
    if (latitude == None and latitude == None):
        print('empty')
    #_________________________________________________
    t = my_gps.timestamp
    #t[0] => hours : t[1] => minutes : t[2] => seconds
    gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
    
    gpsdate = my_gps.date_string('long')
    speed = my_gps.speed_string('kph') #'kph' or 'mph' or 'knot'
    #_________________________________________________
    print('Lat:', latitude)
    print('Lng:', longitude)
    print('time:', gpsTime)
    print('Date:', gpsdate)
    print('speed:', speed)  
    time.sleep_ms(500)
##########################################################