import  time, st7789,math
from machine import Pin, SPI

############## TUTAJ STWÓRZ OBEIKT SPI ###############

spi = machine.SPI(0, 40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
IPS = st7789.ST7789(spi, 240, 320, reset=Pin(21,Pin.OUT), dc=Pin(16, Pin.OUT),rotation = 3)
IPS.init()

##################=====================################

def pointer_poly(length, radius):
    return [
        (0, 0),
        (-radius, radius),
        (-radius, int(length * 0.3)),
        (-1, length),
        (1, length),
        (radius, int(length * 0.3)),
        (radius, radius),
        (0,0)
    ]



ym = 150         #środek po y
xm= 160          #środek po x 
r = 140          #Zewnętrzny promień pierścienia 
odcinek = 20     #Długość pierścienia (Rysowana do Wewnątrz)
wskazowka = 40   #Długość wskazówki 
# 
# @micropython.native
def speedometer_plus():
    for i in range(math.pi*r):
        kolor_zmienna = int(i*81/(r))           #Konwertowanie ilości iteracji, aby zawsze k było w przedzaile [0-255]
        kolor = st7789.color565( 0+ kolor_zmienna   ,20,      255 - kolor_zmienna)
        
        #Ta część musi być po obliczeniu koloru 
        i += math.pi * r/2       #Zrotowanie rysowania koła (Pozmieniaj wartości i zobacz co się dzieje) 
        math.sqrt((1 - math.cos((i)/r))/2)
  
  
        ####### POLYGON #####
        IPS.polygon(pointer_poly(-wskazowka,1),
                    -int(r*math.sin((i+3)/r)) +xm + int(2 * math.sin(i/r)),
                    int(r*math.cos((i+3)/r)) + ym - int(2*math.cos(i/r)) ,
                    st7789.GREEN,
                    (i)/(r) )
        

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
        #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
        IPS.line(-int(r*math.sin((i)/r)) +xm-1        ,
         int(r*math.cos(i/r)) + ym  ,
         -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)-1) ,
         int(r*math.cos(i/r)) + ym - int(odcinek*math.cos((i)/r)), kolor)
        
        
        #Czyszczenie po wskazówce
        IPS.line(-int(r*math.sin((i-2)/r)) +xm + int(odcinek * math.sin((i-2)/r))  ,
             int(r*math.cos((i-2)/r)) + ym - int(odcinek*math.cos((i-2)/r)) ,
             -int(r*math.sin((i-2)/r)) +xm + int(odcinek * math.sin((i-2)/r)) + int((wskazowka -odcinek+5) * math.sin((i-2)/r)) ,
             int(r*math.cos((i-2)/r)) + ym - int(odcinek*math.cos((i-2)/r))- int((wskazowka -odcinek+5)*math.cos((i-2)/r)),
                 st7789.BLACK)
        
        IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r))  ,
             int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r)) -1,
             -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r)) ,
             int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r))- int((wskazowka -odcinek+5)*math.cos(i/r)) -1,
                 st7789.BLACK)
        
        IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) -1 ,
             int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r)) ,
             -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r))-1 ,
             int(r*math.cos(i/r)) + ym - int(odcinek*math.cos(i/r))- int((wskazowka -odcinek+5)*math.cos(i/r)) ,
                 st7789.BLACK)        




def speedometer_minus():
    for i in range(math.pi*r):
        kolor_zmienna = int(i*81/(r))     #Konwertowanie ilości iteracji, aby zawsze k było w przedzaile [0-255]
        kolor = st7789.BLACK
        
        #Ta część musi być po obliczeniu koloru 
        i -= math.pi * r/2       #Zrotowanie rysowania koła (Pozmieniaj wartości i zobacz co się dzieje) 
        math.sqrt((1 - math.cos((i)/r))/2)
  
        rotacja =(-i)/(r)   
        if rotacja <0:
            rotacja += 2*math.pi 
        ####### POLYGON #####
        IPS.polygon(pointer_poly(+wskazowka,1),
                    -int(r*math.sin((i+3)/r)) +xm + int(2 * math.sin(i/r)),
                    -int(r*math.cos((i+3)/r)) + ym +int(2* math.cos(i/r)) ,
                    st7789.GREEN,
                    rotacja )
      
        
        #Rysowanie lini pomiędzy 2 obręczami 
        IPS.line(-int(r*math.sin(i/r)) +xm,
             -int(r*math.cos(i/r)) + ym ,
             -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) ,
             -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos(i/r)), kolor)
        #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
        IPS.line(-int(r*math.sin((i)/r)) +xm        ,
         -int(r*math.cos(i/r)) + ym  ,
         -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)) ,
         -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos((i)/r))+1, kolor)
        #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
        IPS.line(-int(r*math.sin((i)/r)) +xm+1       ,
         -int(r*math.cos(i/r)) + ym  ,
         -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin((i)/r)+1) ,
         -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos((i)/r)), kolor)
        
        
        #Czyszczenie po wskazówce
        IPS.line(-int(r*math.sin((i-3)/r)) +xm + int(odcinek * math.sin((i-3)/r))  ,
             -int(r*math.cos((i-3)/r)) + ym + int(odcinek*math.cos((i-3)/r)) ,
             -int(r*math.sin((i-3)/r)) +xm + int(odcinek * math.sin((i-3)/r)) + int((wskazowka -odcinek+5) * math.sin((i-3)/r)) ,
             -int(r*math.cos((i-3)/r)) + ym + int(odcinek*math.cos((i-3)/r))+ int((wskazowka -odcinek+5)*math.cos((i-3)/r)),
                 st7789.BLACK)
        
        IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r))   ,
            -int(r*math.cos(i/r)) + ym + int(odcinek*math.cos(i/r)),
            -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r)) ,
            -int(r*math.cos(i/r)) + ym +int(odcinek*math.cos(i/r))+ int((wskazowka -odcinek+5)*math.cos(i/r))+1 ,
                 st7789.BLACK)
        
        IPS.line(-int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) +1 ,
             -int(r*math.cos(i/r)) + ym +int(odcinek*math.cos(i/r)) ,
             -int(r*math.sin(i/r)) +xm + int(odcinek * math.sin(i/r)) + int((wskazowka -odcinek+5) * math.sin(i/r))+1 ,
             -int(r*math.cos(i/r)) +ym + int(odcinek*math.cos(i/r))+int((wskazowka -odcinek+5)*math.cos(i/r)) ,
                 st7789.BLACK)        


for i in range(4):       
    start = time.ticks_us()
    speedometer_plus()
    delta = time.ticks_diff(time.ticks_us(), start)                
    print('Zamkniecie licznika w: '+ str(delta/1000000)+ ' s')
    start = time.ticks_us()
    speedometer_minus()
    delta = time.ticks_diff(time.ticks_us(), start)                
    print('Zwolnienie do 0 w: '+ str(delta/1000000)+ ' s')