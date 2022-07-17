
from machine import Pin, SPI, Timer, PWM, ADC
import framebuf
import time
import math
from imu import MPU6050
from machine import Pin, I2C
from time import sleep



i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

licznikPin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)


# New driver received from WaveShare on 10th July 2021
class LCD_1inch8(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 160
        self.height = 128
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        

        self.WHITE =   0xFFFF
        self.BLACK  =  0x0000
        self.GREEN   =  0x001F
        self.BLUE    =  0xF800
        self.RED   = 0x07E0

        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36);
        self.write_data(0x70);
        
        self.write_cmd(0x3A);
        self.write_data(0x05);

         #ST7735R Frame Rate
        self.write_cmd(0xB1);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB2);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB3);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);
        self.write_data(0x01);
        self.write_data(0x2C);
        self.write_data(0x2D);

        self.write_cmd(0xB4); #Column inversion
        self.write_data(0x07);

        #ST7735R Power Sequence
        self.write_cmd(0xC0);
        self.write_data(0xA2);
        self.write_data(0x02);
        self.write_data(0x84);
        self.write_cmd(0xC1);
        self.write_data(0xC5);

        self.write_cmd(0xC2);
        self.write_data(0x0A);
        self.write_data(0x00);

        self.write_cmd(0xC3);
        self.write_data(0x8A);
        self.write_data(0x2A);
        self.write_cmd(0xC4);
        self.write_data(0x8A);
        self.write_data(0xEE);

        self.write_cmd(0xC5); #VCOM
        self.write_data(0x0E);

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0);
        self.write_data(0x0f);
        self.write_data(0x1a);
        self.write_data(0x0f);
        self.write_data(0x18);
        self.write_data(0x2f);
        self.write_data(0x28);
        self.write_data(0x20);
        self.write_data(0x22);
        self.write_data(0x1f);
        self.write_data(0x1b);
        self.write_data(0x23);
        self.write_data(0x37);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x02);
        self.write_data(0x10);

        self.write_cmd(0xe1);
        self.write_data(0x0f);
        self.write_data(0x1b);
        self.write_data(0x0f);
        self.write_data(0x17);
        self.write_data(0x33);
        self.write_data(0x2c);
        self.write_data(0x29);
        self.write_data(0x2e);
        self.write_data(0x30);
        self.write_data(0x30);
        self.write_data(0x39);
        self.write_data(0x3f);
        self.write_data(0x00);
        self.write_data(0x07);
        self.write_data(0x03);
        self.write_data(0x10);

        self.write_cmd(0xF0); #Enable test command
        self.write_data(0x01);

        self.write_cmd(0xF6); #Disable ram power save mode
        self.write_data(0x00);

            #sleep out
        self.write_cmd(0x11);
        #DEV_Delay_ms(120);

        #Turn on the LCD display
        self.write_cmd(0x29);


    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0xA0)
    
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x82)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
# ==============End of driver setup==============================
def colour(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    return colour



# zmienne potrzebne do kodu 


obwod_kola = 2155 # Dla obręczy 27.5 cala [mm]
counter = 0 #Zmienna zliczająca ilość pełnych obrotów koła
Pin17_state = 0 #Zmienna potrzebna do rozwiązania problemu drgania styków
finish = 0 # Czas po jakim zostały zliczone wsyzstkie pełne obroty koła
current_speed = 0 #Prędkość aktualna 
ilosc_impulsow = 2 #Zmienna która determinuje w zależności od ostatniej prędkości chwilowej ile należy zliczyć impulsów aby wyświetlenie kolejnej wartości mieściło się w granicach czasowych 
zmienna_modulo = 1 #Dodatkowa zmienna potrzeba do zliczania pełnych obortów koła służąca do wyliczania wartości bezwzględnej ze zmiennej "ilosc_impulsow"
counter_counterow =0 #Wynik operacji modulo potrzebny do wyliczenia prędkości chwilowej 
flaga = 0 #Zmienna potrzeba do wykrycia stanu, że w ciągu 3 sekund nie zostały zliczone wszystkie impulsy 
time_beetwen = 0 # czas pomiędzy osatnim dczytem prędkości chwilowej 
flaga_2 = 0
proporcja = 0 # współczynnik pomiędzy 0-1 który poprawia jakość prędkości chwilowej podczas "sytuacji awaryjnej" 
ay = 0 #Zmienna do której zosataje przypisywana wartość sinusa kąta nachylenia
ay_kat =0
przeywzszenia = 0

def counterTask(pin):   #Funkcja realizująca przerwanie 
    global counter, Pin17_state,  finish, current_speed,ilosc_impulsow,counter_counterow, zmienna_modulo, ay, flaga, time_beetwen, flaga_2, proporcja, ay_kat,przeywzszenia
    if (licznikPin.value() == 1) and (Pin17_state == 0 ):
       
        Pin17_state = 1
        counter += 1
  
  
        # Odzytanie wartości sinusa kąta nachylenia
        ay=round(imu.accel.y,3)  
        if ay>=1:
            ay = 1
            
        ay_kat = 180* math.asin(ay)/math.pi
        
        if ay_kat > 2:
            przeywzszenia += ay * obwod_kola/ 1000
        
          
        # Warunek gdy przez ponad 3 sekundy nie została zmieniona prędkość chwilowa         
        if flaga == 1 and current_speed != 0:
            okres_obortu = (obwod_kola*3.6)/current_speed
            proporcja = time_beetwen/okres_obortu
            if proporcja >= 1:
                proporcja = 1
            flaga = 0 
            flaga_2 =1
        
        
        # 
        zmienna_modulo += 1
        counter_counterow = zmienna_modulo % ilosc_impulsow
  
        if counter_counterow == 0:        
            finish = time.ticks_ms()
                     
            if flaga_2 == 0:
                current_speed = ilosc_impulsow*3.6*obwod_kola/time_beetwen #  3.6  (m/s => km/h)
                flaga_2 = 0
                
            elif flaga_2 == 1: 
                current_speed =(ilosc_impulsow + proporcja -1 )*obwod_kola*3.6/time_beetwen #3.6  (m/s => km/h)
                flaga_2 = 0
                
            zmienna_modulo = 0
            proporcja = 0
             
            # Zależności dla porządanej ilości impiulsów od poprzedniej prędkości chwilowej  
            if current_speed <= 9:
                 ilosc_impulsow =1
            elif current_speed <=13.63 and current_speed> 9:
                 ilosc_impulsow =2
            elif current_speed <= 18.21 and current_speed>13.63:
                 ilosc_impulsow =3
            elif current_speed <= 22.86   and current_speed>18.21:
                 ilosc_impulsow =4
            elif current_speed <=27.35    and current_speed> 22.86:
                 ilosc_impulsow = 5
            elif current_speed <32.5     and current_speed> 27.35:
                 ilosc_impulsow =6
            elif current_speed <= 37.5   and current_speed> 30.5:
                 ilosc_impulsow =7
            elif current_speed <= 43   and current_speed> 37.5:
                 ilosc_impulsow =8
            elif current_speed <= 55   and current_speed> 43:
                 ilosc_impulsow =9
            elif current_speed > 55:
                 ilosc_impulsow =11
        
    elif (licznikPin.value() == 0) and (Pin17_state == 1 ):
        Pin17_state = 0
        
    licznikPin.irq(handler=counterTask)
    
    
licznikPin.irq(trigger = Pin.IRQ_FALLING, handler = counterTask)  #Wywołwanie przerwania 



 
if __name__=='__main__':
    
    
    while True:
             
        time_beetwen = time.ticks_diff(time.ticks_ms(),finish)

        if time_beetwen > 3000 and counter_counterow == 0: # osobny if, po to, żeby 'time_beetwen' był większy niż 3s, czyli pierwszy impuls z koła nie dał dużej prędkości chwilowej
            current_speed = 0
            zmienna_modulo = 0
            
        if time_beetwen > 3000 and counter_counterow > 0:
            
            finish = time.ticks_ms()
            current_speed = counter_counterow*3.6*obwod_kola/time_beetwen
            zmienna_modulo = 0
            counter_counterow = 0
            flaga = 1 #Flaga alarmująca o tym, że w 3 sekundy nie zostały zliczone wszystkie impulsy
            
            # Zależności dla porządanej ilości impiulsów od poprzedniej prędkości chwilowej  
            if current_speed <= 9:
                 ilosc_impulsow =1
            elif current_speed <=13.63 and current_speed> 9:
                 ilosc_impulsow =2
            elif current_speed <= 18.21 and current_speed>13.63:
                 ilosc_impulsow =3
            elif current_speed <= 22.86   and current_speed>18.21:
                 ilosc_impulsow =4
            elif current_speed <=27.35    and current_speed> 22.86:
                 ilosc_impulsow = 5
            elif current_speed <32.5     and current_speed> 27.35:
                 ilosc_impulsow =6
            elif current_speed <= 37.5   and current_speed> 30.5:
                 ilosc_impulsow =7
            elif current_speed <= 43   and current_speed> 37.5:
                 ilosc_impulsow =8
            elif current_speed <= 55   and current_speed> 43:
                 ilosc_impulsow =9
            elif current_speed > 55:
                 ilosc_impulsow =11
                
        
        
           
        

        LCD = LCD_1inch8()
        #color BRG

        LCD.text('Kat: '+(str(round(ay_kat,1))), 10,20,colour(255,255,70))
        LCD.text("Speed: "+ str(round(current_speed,1)) , 5,80,colour(100,100,100))
        LCD.text("dystans: "+ str(round(counter*obwod_kola/1000 ,1))+ "m" , 5,95,colour(100,100,100))
        LCD.text("Przew: "+ str(round(przeywzszenia,1))+ "m" , 5,110,colour(100,100,100))

        LCD.show()
        
        cos_y = math.cos(math.asin(ay))
        a = ay/cos_y
    
               

# rysowanie wykresu    
        
        
        for x in range (1,40):
            LCD.pixel(x+ 100,50,colour(0,255,0))
            LCD.pixel( 100,-x+50,colour(0,255,0))
        
        for x in range (1,40):
           
            if a > 1:
                wsp_y = 1/a
                x = int(x*wsp_y)         
            y = int(a*x)           
            LCD.pixel(x+ 100,-y+ 50,colour(255,200,0)) 
           
        LCD.show()
        
        time.sleep(0.1)
       
   







