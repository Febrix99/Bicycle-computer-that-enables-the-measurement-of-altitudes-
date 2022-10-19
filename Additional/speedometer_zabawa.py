import  time, st7789,math
from machine import Pin, SPI

############## TUTAJ STWÓRZ OBEIKT SPI ###############
# np:
spi = machine.SPI(0, 40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
IPS = st7789.ST7789(spi, 240, 320, reset=Pin(21,Pin.OUT), dc=Pin(16, Pin.OUT),rotation = 3)
IPS.init()
#
##################=====================################

ym = 200       #środek po y
xm= 160        #środek po x 
r = 160        #Zewnętrzny promień pierścienia 
odcinek = 30   #Długość pierścienia (Rysowana do Wewnątrz)

print(abs(odcinek - r))
@micropython.native
def speedometer():
    for i in range(math.pi * r):
        kolor_zmienna = int(i*81/(r))           #Konwertowanie ilości iteracji, aby zawsze k było w przedzaile [0-255]
        kolor = st7789.color565( 0+ kolor_zmienna   ,20,      255 - kolor_zmienna)
        
        #Ta część musi być po obliczeniu koloru 
        i += math.pi * r/2       #Zrotowanie rysowania koła (Pozmieniaj wartości i zobacz co się dzieje) 
        math.sqrt((1 - math.cos((i)/r))/2)
  
        #Rysowanie lini pomiędzy 2 obręczami 
        IPS.line(-int(r*math.sin(i/r)) +xm        ,
             int(r*math.cos(i/r)) + ym ,
             -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) ,
             int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r)), kolor)
        #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
        IPS.line(-int(r*math.sin((i)/r)) +xm        ,
         int(r*math.cos(i/r)) + ym-1  ,
         -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)) ,
         int(r*math.cos(i/r)) + ym - int(odcinek*math.cos((i)/r))-1, kolor)
        
start = time.ticks_us()
speedometer()
delta = time.ticks_diff(time.ticks_us(), start)                
print('Zamkniecie licznika w: '+ str(delta/1000000)+ ' s')