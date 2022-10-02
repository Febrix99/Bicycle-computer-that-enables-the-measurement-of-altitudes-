import  time, math, sys, gc, random ,micropython, st7789,machine
from machine import Pin, SPI
sys.path.insert(0, '/Functions')
sys.path.insert(0, '/Libraries/Font_room')
from Menu import  Menu
import romand                     # Wektoroowa czcionka
import vga1_bold_16x32 as font_32 # Wysoka_duża

#################################################################################################
spi = machine.SPI(0, 40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
IPS = st7789.ST7789(spi, 240, 320, reset=Pin(21,Pin.OUT), dc=Pin(16, Pin.OUT),rotation = 3)
IPS.init()
#################################################################################################
b = st7789.color565(50,100,255)
gold =  st7789.color565(179 , 139 , 91 )         
class Display():
    zmiana_przycisk = False
    wyswietlana_predkosc = 0  
    zmiana_czasu = 0    
#### Zmienne do speedometera ###
    wejscie = True
    wyswietlana_predkosc_speedometer = 0 
    speed = 0
    polowka = 0
    prog = 0
    pochodna = True 
    poprzednia_pochodna = True
    y_prim = 0
    x_prim = 0
    przedluzenie_wykresu = False
    bramka_speedometer_plus = True
    bramka_speedometer_minus = True 
#### Zmienne do menu ###
    poprzedni_wybor = 0
    wejscie_do_menu = False
    wymazanie_prostokata = False 
    mruganie_liczb = False
    deadline = 0
    def funkcja_sleep(self):               
        pass
         
    def funkcja_startowa(self):
        pass
    


#================================ PODSTAWOWE WYSWIETLANIE =============================================#        
    ##======= Wybór Funkcji podstawowej ==============##
    def screen(self,obj_menu,obj_licznik):
        gc.collect() # Just in case, bo nie ma framebuffera
        
        
        
        ###=== Interwały ===###
        if obj_menu.interwal_czas_start_0 == True:
            self.interwal_czas(obj_menu,obj_licznik)
            
        elif obj_menu.interwal_dystans_start_0 == True:
            self.interwal_dstans(obj_menu,obj_licznik)

        
        
        ###=== Spedometer ===###    
        if obj_menu.warunek_ktory_wyswietlacz ==0:  
            self.funkcja_wyswietlacz_0(obj_licznik,obj_menu)
            
            
        ###=== Cała reszta ===###    
        else:
            if self.wejscie == False: #Jeżeli wyszliśmy z funkcji #Spedometer to czyścimy jednorazowo screena
                if obj_menu.interwal_czas_start_0 == True:
                    IPS.fill_rect(0,0,320,132,st7789.BLACK)
                    IPS.fill_rect(0,132,120,108,st7789.BLACK)
                    IPS.fill_rect(120,109,30,30, st7789.BLACK)
                    IPS.fill_rect(227,132,93,108,st7789.BLACK)
                    IPS.fill_rect(120,132,20,5,st7789.BLACK)
                elif  obj_menu.interwal_dystans_start_0 == True:
                    IPS.fill_rect(0,0,320,181,st7789.BLACK)
                else:
                    IPS.fill(st7789.BLACK)
                #Dodac funkcje ustawiajacą na defultowe wartosci eby po ponowym wejsciu do speedometera dzialalo jak nalezy
                self.wejscie = True
                              
            self.show_speed(obj_licznik.current_speed)
            if self.zmiana_przycisk == True:
                IPS.fill_rect(0,109,120,72, st7789.BLACK)
                IPS.fill_rect(120,109,30,30, st7789.BLACK)
                IPS.fill_rect(120,140,9,31, st7789.BLACK)
                
            if obj_menu.warunek_ktory_wyswietlacz ==1: #Dystans
                self.funkcja_wyswietlacz_1(obj_licznik,obj_menu)
                    
            elif obj_menu.warunek_ktory_wyswietlacz ==2: #V max
                self.funkcja_wyswietlacz_2(obj_licznik,obj_menu)
                    
            elif obj_menu.warunek_ktory_wyswietlacz==3:  #Przewyzszenia
                self.funkcja_wyswietlacz_3(obj_licznik,obj_menu)         

            elif obj_menu.warunek_ktory_wyswietlacz==4:  #Czas
                self.funkcja_wyswietlacz_4(obj_licznik,obj_menu)
                    
            elif obj_menu.warunek_ktory_wyswietlacz==5:  #Srednia predkosc
                self.funkcja_wyswietlacz_5(obj_licznik,obj_menu)
                    
            else: print("ER. glowna")
    def funkcja_wyswietlacz_0(self,obj_licznik,obj_menu):
            #nalezy czyscic screena przd wejściem, i po wyjściu
        self.wyswietlanie_speedometera(obj_menu,obj_licznik, 160,180,157)
        
    def funkcja_wyswietlacz_1(self,obj_licznik,obj_menu): #Total dystans   
        self.show_picture(obj_menu.warunek_ktory_wyswietlacz)
        IPS.text(font_32, str(round(obj_licznik.counter * obj_licznik.obwod_kola/1000000,1)) + ' Km'    , 5    ,110,  st7789.BLUE)
        IPS.text(font_32, str(round(obj_licznik.counter_podroz * obj_licznik.obwod_kola/1000000,1))  , 5   ,150,   gold)
        
    def funkcja_wyswietlacz_2(self,obj_licznik,obj_menu): #Przewyzszenia
        self.show_picture(obj_menu.warunek_ktory_wyswietlacz)
        IPS.text(font_32, str(round(obj_licznik.przeywzszenia,1)) + ' m' ,          5    ,110,st7789.BLUE)
        IPS.text(font_32, str(round(obj_licznik.przeywzszenia_podroz,1)) ,    5    ,150,gold)        
        
    def funkcja_wyswietlacz_3(self,obj_licznik,obj_menu): #Max speed
        self.show_picture(obj_menu.warunek_ktory_wyswietlacz)
        IPS.text(font_32, str(round(obj_licznik.v_max,1))+ ' Km/h' ,        5    ,110,st7789.BLUE)
        IPS.text(font_32, str(round(obj_licznik.v_max_podroz,1)) , 5    ,150,gold)
        
    def funkcja_wyswietlacz_4(self,obj_licznik,obj_menu): #Czas
        self.show_picture(obj_menu.warunek_ktory_wyswietlacz)
        obj_licznik.rtc_czas()
        if self.zmiana_czasu != obj_licznik.rtc_czas_podroz[3]:
            IPS.fill_rect(0,109,120,72, st7789.BLACK)
            IPS.fill_rect(120,109,30,30, st7789.BLACK)
            IPS.fill_rect(120,140,9,31, st7789.BLACK)
            self.zmiana_czasu = obj_licznik.rtc_czas_podroz[3]
            
        IPS.text(font_32, str(obj_licznik.rtc_czas_total[0]) +':'+ str(obj_licznik.rtc_czas_total[1])+':'
        +str(obj_licznik.rtc_czas_total[2])+':'+str(obj_licznik.rtc_czas_total[3]) , 0    ,108,st7789.BLUE, 1)
        if obj_licznik.rtc_czas_podroz[0] == 0:
            IPS.text(font_32,  str(obj_licznik.rtc_czas_podroz[1])+':'
            +str(obj_licznik.rtc_czas_podroz[2])+':'+str(obj_licznik.rtc_czas_podroz[3]) , 0    ,145,gold)
        else:      
            IPS.draw(romand, str(obj_licznik.rtc_czas_podroz[0]) +':'+ str(obj_licznik.rtc_czas_podroz[1])+':'
            +str(obj_licznik.rtc_czas_podroz[2])+':'+str(obj_licznik.rtc_czas_podroz[3]) , 0   ,164,gold,0.75)
                    
    def funkcja_wyswietlacz_5(self,obj_licznik,obj_menu): #Srednia predkosc 
        self.show_picture(obj_menu.warunek_ktory_wyswietlacz)
        IPS.text(font_32,str(round(obj_licznik.v_srednie_t(),1))+ ' Km/h'  ,5    ,110,st7789.BLUE)
        if obj_licznik.v_srednie_p() == None:
            pass
        else:
            IPS.text(font_32, str(round(obj_licznik.v_srednie_p(),1)) ,5    ,150,gold)
                
    def show_picture(self, wybor):
        if self.zmiana_przycisk == True:
            IPS.fill_rect(0,0,160,105, st7789.BLACK)
            if wybor ==1:
                IPS.jpg('/Libraries/Pictures/total.jpg',30,0, st7789.SLOW) #105x105
            elif wybor ==2:
                IPS.jpg( '/Libraries/Pictures/przewyzszenia.jpg' ,30,0)    #118x98
            elif wybor ==3:              
                IPS.jpg('/Libraries/Pictures/v_max.jpg' ,11,0)             #138x101
            elif wybor ==4:              
                IPS.jpg('/Libraries/Pictures/czas.jpg' ,29,0)              #102x105
            elif wybor ==5:                
                IPS.jpg('/Libraries/Pictures/v_sr.jpg',10,0)               #140x102                  
            self.zmiana_przycisk = False
        else:
            pass
    
    def show_speed(self,predkosc):
        if self.wyswietlana_predkosc != predkosc:
            speed = int(predkosc)
            if speed > 9:
                x = 280
            else:
                x = 225    
            IPS.fill_rect(164,20,156,90,st7789.BLACK)
            IPS.draw(romand, str(speed), 160, 60, b, 3.1)
            IPS.draw(romand, str(int((round(predkosc,1)- speed)*10)), x, 47, b, 1.9)
            self.wyswietlana_predkosc = predkosc
            IPS.draw(romand, '110', 212, 138, b, 1.8)
        else:
            pass       
        #Tutaj będzie jeszcze wyswietlanie kadencji, analogicznie jak wyzej, tylko łatwiej 
 
 
 
    def show_speed_speedometer(self,predkosc, obj_menu):     
        if self.wyswietlana_predkosc_speedometer != predkosc:
            speed = int(predkosc)
       
            if obj_menu.interwal_czas_start_0 == True:
                if speed > 9:
                    x = 78
                else:
                    x = 47
                IPS.fill_rect(0,185,120,55,st7789.BLACK)
                IPS.fill_rect(225,205,80,40,st7789.BLACK)
                IPS.draw(romand, str(speed), 1, 215, b, 2)
                IPS.draw(romand, str(int((round(predkosc,1)- speed)*10)), x, 203, b, 1)
                self.wyswietlana_predkosc_speedometer = predkosc
                IPS.draw(romand, '110', 240, 212, b, 1.3)           
            
            elif obj_menu.interwal_dystans_start_0 == True:     
                if speed > 9:
                    x = 190
                else:
                    x = 158

                IPS.fill_rect(110,95,105,89,st7789.BLACK)
                IPS.fill_rect(100,145,170,39,st7789.BLACK)
                IPS.draw(romand, str(speed), 112, 122, b, 2)
                IPS.draw(romand, str(int((round(predkosc,1)- speed)*10)), x, 110, b, 1)
                self.wyswietlana_predkosc_speedometer = predkosc
                IPS.draw(romand, '110', 180, 167, b, 1.3)
            
            
            
            else:
                if speed > 9:
                    x = 190
                else:
                    x = 158

                IPS.fill_rect(110,95,105,80,st7789.BLACK)
                IPS.draw(romand, str(speed), 112, 122, b, 2)
                IPS.draw(romand, str(int((round(predkosc,1)- speed)*10)), x, 110, b, 1)
                self.wyswietlana_predkosc_speedometer = predkosc
                IPS.draw(romand, '110', 115, 167, b, 1.3)
        else:
            pass     
## Tutaj jeszcze wyświetlanie kadencji ! 

        
#===================================== SPEEDOMETER ====================================================#
        
        
    def wyswietlanie_speedometera(self,obj_menu, obj_licznik,xm,ym,r): 
        #Dodaj wiecej argumentow tej funkcji, czyli dlugosc smugi, max value, czas jak masz szybko dzialac [0,1]

        if self.wejscie == True:
            if obj_menu.interwal_czas_start_0 == True:
                IPS.fill_rect(0,0,320,132,st7789.BLACK)
                IPS.fill_rect(0,132,120,108,st7789.BLACK)
                IPS.fill_rect(120,109,30,30, st7789.BLACK)          
                IPS.fill_rect(227,132,93,108,st7789.BLACK)
                IPS.fill_rect(120,132,20,5,st7789.BLACK)
            elif  obj_menu.interwal_dystans_start_0 == True:
                IPS.fill_rect(0,0,320,181,st7789.BLACK)
            else:
                IPS.fill(st7789.BLACK)
            self.obrecz_speedometer(ym,xm+1,r+3,2,st7789.color565(253,250,255))
            self.wejscie = False
        self.show_speed_speedometer(obj_licznik.current_speed,obj_menu)                   
        if self.speed != obj_licznik.current_speed: #Jeżeli otrzymaliśmy nową wartość chwilową
            
            if self.speed < obj_licznik.current_speed: #jeżeli nowa wartość jest większa niż poprzednia
                if obj_licznik.current_speed <= 25:
                    self.prog = r*math.cos((obj_licznik.current_speed)*math.pi/50)
                    self.polowka = False 
                elif obj_licznik.current_speed > 25:
                    self.polowka = True
                    self.prog  = r*math.cos((obj_licznik.current_speed- 25)*math.pi/50)
                    if self.prog <= 1:
                        self.prog = 1
                self.pochodna = True  

            
            elif self.speed > obj_licznik.current_speed: #jeżeli nowa wartość jest mniejsza niż poprzednia
                if obj_licznik.current_speed <= 25:      
                    self.prog = r*math.sin((obj_licznik.current_speed)*math.pi/50)
                    self.polowka = True
                    if self.prog <= 1:
                        self.prog = 1                    
                elif obj_licznik.current_speed > 25:
                    self.polowka = False
                    self.prog  = r*math.sin((obj_licznik.current_speed- 25)*math.pi/50)
                self.pochodna = False
                
            if self.pochodna != self.poprzednia_pochodna: #Wykrycie zmiany kierunu 
                self.x_prim , self.y_prim= self.y_prim, self.x_prim,
                
            self.poprzednia_pochodna = self.pochodna
            self.speed = obj_licznik.current_speed
            if self.speed >50:
                self.speed = 50
#         if self.speed !=0 and self.speed != 50:        
#             if self.pochodna ==True:    #Wywołanie funkcji dorysowywujące     
#                 self.speedometer_plus(obj_menu,obj_licznik,xm,ym,r)
#                 
#             elif self.pochodna ==False: #Wywołanie funkcji czyszczącej 
#                 self.speedometer_minus(obj_menu,obj_licznik,xm,ym,r)
#         
        else:
            pass       
        
    @micropython.native
    def zbieranie_danych(self,x,y):
        self.x_prim = x
        self.y_prim = y
        self.przedluzenie_wykresu = False         
        self.bramka_speedometer_plus = True
        self.bramka_speedometer_minus = True
    @micropython.native
    def obrecz_speedometer(self,ym,xm,r,odcinek,kolor):
        for i in range(math.pi*r):        
            i += math.pi * r/2       #Zrotowanie rysowania koła (Pozmieniaj wartości i zobacz co się dzieje) 
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
            
    @micropython.native
    def rysownie_wskaznika_plus(self,xm,y,i,ym,x ,nachylenie,kolor,cwiartka):
        if cwiartka == 1:
            IPS.pixel(xm-y  +i          ,ym-x  +nachylenie-1   ,kolor)
            IPS.pixel(xm-y  +i          ,ym-x  +nachylenie-0   ,kolor)       
        elif cwiartka == 2:
            IPS.pixel(xm-y +nachylenie +3             ,ym-x +i -3    ,kolor)
            IPS.pixel(xm-y +nachylenie +2             ,ym-x +i -2   ,kolor)
        elif cwiartka == 3:
            IPS.pixel(xm +x -nachylenie +3           ,ym-y +i-1    ,kolor)
            IPS.pixel(xm +x -nachylenie +2           ,ym-y +i    ,kolor)            
        elif cwiartka == 4:
            IPS.pixel(xm +x -i+3          ,ym-y +nachylenie +2     ,kolor)
            IPS.pixel(xm +x -i+2          ,ym-y +nachylenie +1    ,kolor)
        else:
            pass
        
    @micropython.native
    def rysownie_wskaznika_minus(self,xm,y,i,ym,x ,nachylenie,kolor,cwiartka):
        if cwiartka == 1:
            IPS.pixel(xm+y  -i -2          ,ym-x  +nachylenie -3    ,kolor)     ## Od 50 do 37 
            IPS.pixel(xm+y  -i-1           ,ym-x  +nachylenie -2    ,kolor)
        elif cwiartka == 2:
            IPS.pixel(xm+y -nachylenie -2            ,ym-x +i +1        ,kolor) ## Od 37 do 25 
            IPS.pixel(xm+y -nachylenie -1            ,ym-x +i       ,kolor)
        elif cwiartka == 3:
            IPS.pixel(xm -x +nachylenie -3          ,ym-y +i +3   ,kolor)        ## Od 25 do 12
            IPS.pixel(xm -x +nachylenie  -2        ,ym-y +i +2   ,kolor)
        elif cwiartka == 4:
            IPS.pixel(xm -x +i           ,ym-y +nachylenie +4     ,kolor)      ## Od 12 do 0 
            IPS.pixel(xm -x +i           ,ym-y +nachylenie +5    ,kolor)
        else:
            pass
        
    @micropython.native  #przspieszenie działania funkcji o ~20%
    def rysowanie_smugi_plus(self,obj_licznik,dlugosc_odcinka,xm,ym, x, y,r, cwiartka):   
        if  cwiartka == 1 or cwiartka == 3:
            skala = math.cos(x/r)
            dlugosc_smugi =  40 * skala
        elif cwiartka == 2 or cwiartka == 4:
            skala = math.cos(y/r)
            dlugosc_smugi =  40 * skala
        red = 0  # r,g,b to zmienne do kastomizowania wyglądu    
        blue = 0        
        green = 0  
        nachylenie = 0 #O ile należy zejść w dół (w Pionie)
        odcinek = 0 #Zmienna odmierzająca odcinek (w poziomie)          
            
        for i in range(dlugosc_smugi+14):
            odcinek +=1
            if odcinek > dlugosc_odcinka:         
                nachylenie += 1 #Obnizenie wysokosci o 1, zeby dalsze odcinki rysowały się niżej 
                odcinek -= dlugosc_odcinka # odjecie dlugosci odcinka               
            if i == 10* skala: 
                blue = 10
            if i > 25 * skala:
                red += 1        
                green += 6        
                blue += 7                  
            if i > dlugosc_smugi:
                 kolor = st7789.BLACK   
            else:
                kolor = st7789.color565( 253 -i*6 - red  , 250 -i*4 - green,  255 -2*i - blue)
            if i < dlugosc_smugi +12:
                self.rysownie_wskaznika_plus(xm,y,i,ym,x ,nachylenie,st7789.color565(253,250,255) ,cwiartka)
            if cwiartka == 1:
                IPS.pixel(xm-y  +i          ,ym-x  +nachylenie +3    ,kolor)
                IPS.pixel(xm-y  +i          ,ym-x  +nachylenie +4   ,kolor)
            elif cwiartka == 2:
                IPS.pixel(xm-y +nachylenie             ,ym-x +i     ,kolor)
                IPS.pixel(xm-y +nachylenie+1           ,ym-x +i     ,kolor)
            elif cwiartka == 3:
                IPS.pixel(xm +x -nachylenie            ,ym-y +i  -1  ,kolor)
                IPS.pixel(xm +x -nachylenie-1            ,ym-y +i -1 ,kolor)
            elif cwiartka == 4:
                IPS.pixel(xm +x -i           ,ym-y +nachylenie      ,kolor)
                IPS.pixel(xm +x -i           ,ym-y +nachylenie -1  ,kolor)
            else:
                break 
                

    @micropython.native  #przspieszenie działania funkcji o ~20%
    def rysowanie_smugi_minus(self,obj_licznik,dlugosc_odcinka,xm,ym, x, y,r, cwiartka):   
        if  cwiartka == 1 or cwiartka == 3:
            skala = math.cos(x/r)
            dlugosc_smugi = 40 * skala      
        elif cwiartka == 2 or cwiartka == 4:
            skala = math.cos(y/r)
            dlugosc_smugi =  40 * skala
             
        nachylenie = 0 #O ile należy zejść w dół (w pionie) 
        odcinek = 0 #Zmienna odmierzająca odcinek (w poziomie)      
        for i in range(dlugosc_smugi+16):
            odcinek +=1
            if odcinek > dlugosc_odcinka:         
                nachylenie += 1 #Obnizenie wysokosci o 1, zeby dalsze odcinki rysowały się niżej 
                odcinek -= dlugosc_odcinka # odjecie dlugosci odcinka
            if i < dlugosc_smugi +12:
                self.rysownie_wskaznika_minus(xm,y,i,ym,x ,nachylenie,st7789.color565(253,250,255) ,cwiartka)
            if cwiartka == 1:
                IPS.pixel(xm+y  -i           ,ym-x  +nachylenie +1    ,st7789.BLACK)
                IPS.pixel(xm+y  -i           ,ym-x  +nachylenie +2  ,st7789.BLACK)
            elif cwiartka == 2:
                IPS.pixel(xm+y -nachylenie             ,ym-x +i +2       ,st7789.BLACK)
                IPS.pixel(xm+y -nachylenie +1          ,ym-x +i+2    ,st7789.BLACK)

            elif cwiartka == 3:
                IPS.pixel(xm -x +nachylenie           ,ym-y +i    ,st7789.BLACK)
                IPS.pixel(xm -x +nachylenie +1             ,ym-y +i  ,st7789.BLACK)
            elif cwiartka == 4:
                IPS.pixel(xm -x +i           ,ym-y +nachylenie      ,st7789.BLACK)
                IPS.pixel(xm -x +i            ,ym-y +nachylenie +1  ,st7789.BLACK)
               ###################################################################         
       
###########          
       
    @micropython.native              
    def speedometer_plus(self,obj_menu,obj_licznik,xm,ym,r):

        if self.bramka_speedometer_plus == True:
            f, ddF_x ,ddF_y, x,y,i =  1 - r, 1, -2* r, 0 ,r,0
            self.bramka_speedometer_plus = False      
        if y <= self.prog  and  self.polowka== False:
            self.zbieranie_danych(x,y)
            return 
        elif y <= self.prog  and self.polowka == True and i == 1:
            self.zbieranie_danych(x,y)
            return
        ######==== Rysowanie PIERWSZEJ połówki półkola ====######## 
        if x < y:
            if (f >= 0) :
                y -= 1
                ddF_y += 2
                f += ddF_y           
            x += 1;
            ddF_x += 2;
            f += ddF_x;                
            ###=== Rysowanie smóg ===###
            dlugosc_odcinka = (r/x)
            if x > self.x_prim-5 or self.przedluzenie_wykresu == True:       
                self.rysowanie_smugi_plus(obj_licznik,dlugosc_odcinka, xm, ym, x, y,r,1+(i*2))  
        ######==== Rysowanie DRUGIEJ połówki półkola ====########           
        elif x >= y : 
            ###=== Rysowanie okregu ===###
            if (f >= 0) :
                x += 1;
                ddF_y -= 2
                f += ddF_y                
            y -= 1
            ddF_x -= 2;
            f += ddF_x
            ###=== Rysowanie smóg ===###
            if y == 0:
                dlugosc_odcinka = r
            else:
                dlugosc_odcinka = (r/(y))
            
            if y < self.y_prim+5 or self.przedluzenie_wykresu  == True :
                self.rysowanie_smugi_plus(obj_licznik,dlugosc_odcinka, xm, ym, x, y,r, 2+(i*2))
        if y == 0:
            i +=1
            f, ddF_x ,ddF_y, x,y =  1 - r, 1, -2* r, 0 ,r  
            self.przedluzenie_wykresu = True
                
                    
    @micropython.native
    def speedometer_minus(self,obj_menu,obj_licznik,xm,ym,r,):
      

        
        if self.bramka_speedometer_minus == True:
            f, ddF_x ,ddF_y, x,y,i =  1 - r, 1, -2* r, 0 ,r,0
            self.bramka_speedometer_minus = False                           
        if y <= self.prog  and  self.polowka== False:
            self.zbieranie_danych(x,y)
            return         
        elif y <= self.prog  and self.polowka == True and i == 1:
            self.zbieranie_danych(x,y)
            return
        
        if x < y:   
            if (f >= 0) :
                y -= 1
                ddF_y += 2
                f += ddF_y           
            x += 1;
            ddF_x += 2;
            f += ddF_x;                
            dlugosc_odcinka = (r/x)
            if x > self.x_prim - 5 or self.przedluzenie_wykresu == True:
                self.rysowanie_smugi_minus(obj_licznik,dlugosc_odcinka, xm, ym, x, y,r,1+(i*2))                      
        elif x >= y :    
            if (f >= 0) :
                x += 1;
                ddF_y -= 2
                f += ddF_y                
            y -= 1
            ddF_x -= 2;
            f += ddF_x
            if y == 0:
                dlugosc_odcinka = r
            else:
                dlugosc_odcinka = (r/(y))
            if y < self.y_prim + 5 or self.przedluzenie_wykresu == True:
                self.rysowanie_smugi_minus(obj_licznik,dlugosc_odcinka, xm, ym, x, y,r,2+(i*2))
                
        if y == 0:
            i +=1
            f, ddF_x ,ddF_y, x,y =  1 - r, 1, -2* r, 0 ,r  
            self.przedluzenie_wykresu = True
            

#===================================== INTERWAŁY ====================================================#
    
    @micropython.native
    def interwal_dstans(self,obj_menu,obj_licznik):
        ###=== Część odpowiedzialna czyszczenie danych po cyklu ===###
        if obj_menu.czyszczenie == True:
            if obj_menu.dodatkowe_czyszczenie == True:
                IPS.fill(st7789.BLACK)
                obj_menu.dodatkowe_czyszczenie = False 
            IPS.rect(0,185,320,55,st7789.color565(20,20,20))
            IPS.rect(1,186,318,53,st7789.color565(20,20,20))
            IPS.rect(2,187,316,51,st7789.color565(20,20,20))
            IPS.fill_rect(3,188,49,st7789.color565(20,20,20))
            obj_menu.Odmierzanie_grafiki = 0
            obj_menu.czyszczenie = False
            if obj_menu.interwal_dystans_start_1 == True:
                obj_menu.deadline_interwal = time.ticks_ms()
                obj_menu.flaga_buzzer =  True
     
        ###=== Buzzer po przejechaniu cyklu (Zakkończenie i rozpoczecie nowego ===###        
        if obj_menu.flaga_buzzer ==  True and obj_menu.interwal_dystans_start_1 == True:
            obj_menu.buzzer_interwal(2)
            
        ###=== Część odpowiedzialna za pokazanie dystansu ===###
        if obj_menu.interwal_dystans_funkcja(obj_licznik) == -1:
            
            IPS.fill_rect(105,150,80,34, st7789.BLACK)
        elif obj_menu.interwal_dystans_funkcja(obj_licznik) == -2:
            obj_menu.podsumowanie = True    #Włączamy przycisk
            self.podsumowanie_interwalu(obj_menu,obj_licznik, 2) 
        else:
            
            a = len(str(obj_menu.interwal_dystans_funkcja(obj_licznik)))
            if obj_menu.zmiana_liczb != a:
                IPS.fill_rect(105,150,80,34, st7789.BLACK)
            IPS.text(font_32,str(obj_menu.interwal_dystans_funkcja(obj_licznik)),int(145- a *8 ),152,gold)           
            obj_menu.zmiana_liczb = a
            
        ###=== Część odpowiedzialna za pokazanie grafiki ===###            
        if obj_menu.interwal_dystans_start_1 == True:
            if obj_menu.cykle  %2 == 1:
                if  obj_menu.odliczanie *obj_licznik.obwod_kola/1000 <  obj_menu.interwal_dystans  * (1 - obj_menu.Odmierzanie_grafiki /314):
                    obj_menu.Odmierzanie_grafiki += 1
                    IPS.vline(2 + obj_menu.Odmierzanie_grafiki , 188, 49,
                                   st7789.color565( 20+ int(obj_menu.Odmierzanie_grafiki/2)   ,20,      180 - int(obj_menu.Odmierzanie_grafiki/2)))
                    
            elif obj_menu.cykle %2 == 0:
                if  obj_menu.odliczanie *obj_licznik.obwod_kola/1000 <  obj_menu.interwal_dystans_pause  * (1 - obj_menu.Odmierzanie_grafiki /314):
                    obj_menu.Odmierzanie_grafiki += 1
                    IPS.vline(2 + obj_menu.Odmierzanie_grafiki , 188, 49,
                                   st7789.color565( 200- int(obj_menu.Odmierzanie_grafiki/2)   ,20,      20 + int(obj_menu.Odmierzanie_grafiki/2)))

            
            
    @micropython.native
    def interwal_czas(self,obj_menu,obj_licznik):
        ###=== Część odpowiedzialna czyszczenie danych po cyklu ===###
        
        if obj_menu.czyszczenie == True:
            if obj_menu.dodatkowe_czyszczenie == True:
                IPS.fill(st7789.BLACK)
                obj_menu.dodatkowe_czyszczenie = False
            IPS.fill_circle(175,188,50,st7789.color565(20,20,20))
            IPS.fill_circle(175,188,36,st7789.BLACK)
            obj_menu.Odmierzanie_grafiki = 0
            obj_menu.czyszczenie = False
            if obj_menu.interwal_czas_start_1 == True and (obj_menu.cykle+1) < obj_menu.ilosc_cykli*2  :
                obj_menu.deadline_interwal = time.ticks_ms()
                obj_menu.flaga_buzzer =  True
                
        ###=== Buzzer po przejechaniu cyklu (Zakkończenie i rozpoczecie nowego ===###    
        if obj_menu.flaga_buzzer ==  True and obj_menu.interwal_czas_start_1 == True:
            obj_menu.buzzer_interwal(2)
            
        ###=== Część odpowiedzialna za pokazanie czasu ===###
        if obj_menu.interwal_czasowy(obj_licznik) == -1:
            IPS.fill_rect(145,173,62,34, st7789.BLACK)
        elif obj_menu.interwal_czasowy(obj_licznik) == -2:
            obj_menu.podsumowanie = True    #Włączamy przycisk
            self.podsumowanie_interwalu(obj_menu,obj_licznik, 1)
        else:
            a = len(str(obj_menu.interwal_czasowy(obj_licznik)))
            if obj_menu.zmiana_liczb != a:
                IPS.fill_rect(145,173,62,34, st7789.BLACK)
            IPS.text(font_32,str(obj_menu.interwal_czasowy(obj_licznik)),int(175- a *8 ),174,gold)           
            obj_menu.zmiana_liczb = a
            
        ###=== Część odpowiedzialna za pokazanie grafiki ===###            
        if obj_menu.interwal_czas_start_1 == True:
            if obj_menu.cykle  %2 == 1:
                if  obj_menu.odliczanie <  obj_menu.interwal_czas  * (1 - obj_menu.Odmierzanie_grafiki /314):
                    obj_menu.Odmierzanie_grafiki += 1
                    kolor = st7789.color565( 20+ int(obj_menu.Odmierzanie_grafiki/2)   ,20,      180 - int(obj_menu.Odmierzanie_grafiki/2))
                    i = obj_menu.Odmierzanie_grafiki
                    self.rysowanie_czasu(i,kolor)

            elif obj_menu.cykle %2 == 0:
                if  obj_menu.odliczanie <  obj_menu.interwal_pause  * (1 - obj_menu.Odmierzanie_grafiki /314):
                    obj_menu.Odmierzanie_grafiki += 1
                    kolor = st7789.color565( 200- int(obj_menu.Odmierzanie_grafiki/2)   ,20,      20 + int(obj_menu.Odmierzanie_grafiki/2))
                    i = obj_menu.Odmierzanie_grafiki                
                    self.rysowanie_czasu(i,kolor)
                 
    def rysowanie_czasu(self,i,kolor):
        x_sin_z =  int(50*math.sin(i/50)) +175
        y_cos_z = -int(50*math.cos(i/50)) + 188
        x_sin_w = x_sin_z - int(14*math.sin(i/50))
        y_cos_w = y_cos_z + int(14*math.cos(i/50))
        #Rysowanie lini pomiędzy 2 obręczami 
        IPS.line(x_sin_z  ,y_cos_z     ,x_sin_w ,  y_cos_w, kolor)
        #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
        IPS.line(x_sin_z , y_cos_z-1  ,x_sin_w , y_cos_w-1, kolor)          



    def podsumowanie_interwalu(self,obj_menu,obj_licznik, rodzaj): #interwal jest od rodzaju interwału
        ###== Ta część wykonuje się jednorazowo ==###
        gc.collect()                                  # Just in case 
        obj_menu.deadline_interwal = time.ticks_ms()  # Ustawienie aktualnego czasu do odmierzania buzzera 
        obj_menu.buzzer_interwal(3)                   # Wywołanie buzzera (niech już gra :)
        obj_menu.flaga_buzzer = True                  # Ustawienie flagi na True, aby wykonywała się w While
        self.zmiana_przycisk = True                   # Aby od razu wyświetliły się dane 
 
            ##== Przypisanie zmiennym lokalnym wartości ==##
        kolor_napis = st7789.color565(179 , 139 , 91 )# Zmienna lokalna (gold)
        if rodzaj == 1:
                #= Suma to ilosc przebytej drogi podczas interwału czasowego (w metrach) =#
            suma = sum(obj_menu.przejechany_dystans)*obj_licznik.obwod_kola/1000 
        elif rodzaj ==2:
                #= Suma to czas w jakim przejechane zostały interwały dystansowe (w sekundach) =#
            suma = sum(obj_menu.dlugosc_interwalu)/1000 
            
        while True:
            ##== Buzzer na zakończenie interwału ==##
            if obj_menu.flaga_buzzer == True:
                obj_menu.buzzer_interwal(3)              
            ##== Warunek wyjścia z while  ==##
            if obj_menu.przytrzymanie_przycisku(1,1200) == 1 or obj_menu.przytrzymanie_przycisku(2,1200) == 2:           
                obj_menu.reset_interwalu()     # Resetujemy dane z interwału 
                obj_menu.wyjscie_z_menu()      # Resetujemy dane z menu ( just in case,  i na pewno wracamy do głównego wyświetlania)
                IPS.fill(st7789.BLACK)         # Czyścimy ekran po sobie 
                gc.collect()                   # Just in case 
                break
            ##== Pokazanie danych ==##
            else:
                #== Rysujemy tylko, gdy przycisk został naciśnięty ==#
                if self.zmiana_przycisk == True:         
                    self.konutry_intrwal(st7789.color565(150,110,71),obj_menu)    # Rysowanie konturów interwału 
                    if obj_menu.podsumowanie_interwalu_przycisk >= obj_menu.ilosc_cykli - 3:  # Na samym dole jest podsumowanie 
                        if rodzaj == 1: # Interwał czasowy 
                            IPS.text(font_32,'Total '+ str(round(suma))+ 'm  ' + str(round(suma*3.6/(obj_menu.interwal_czas*obj_menu.ilosc_cykli),1)) ,
                                  0,204 ,kolor_napis)
                        elif rodzaj == 2: # Interwał dystansowy
                            IPS.text(font_32,'Total '+ str(round(suma))+ 's  ' + str(round(obj_menu.ilosc_cykli*obj_menu.interwal_dystans*3.6/suma,1)) ,
                                  0,204 ,kolor_napis)                      
                    przesuniecie = 40    
                    prog_1 = 4-(obj_menu.podsumowanie_interwalu_przycisk *przesuniecie)
                    prog_2 = 44-(obj_menu.podsumowanie_interwalu_przycisk *przesuniecie)
                    ###=== Nanoszenie podstawowoych infomacji na odpowiednią wysokość ===###
                    if rodzaj == 1: # Interwał czasowy 
                        IPS.text(font_32,'Czas: ' + str(obj_menu.interwal_czas),0,prog_1,kolor_napis)
                        IPS.text(font_32,'Pauza: ' + str(obj_menu.interwal_pause),160,prog_1,kolor_napis)                                      
                        IPS.text(font_32,'Nr',        4   ,prog_2   ,kolor_napis)
                        IPS.text(font_32,'Dys[m]',    60  ,prog_2   ,kolor_napis)
                        IPS.text(font_32,'Avg Km/h', 180  ,prog_2   ,kolor_napis)                        
                
                    elif rodzaj ==2: #Interwał dystansowy
                        IPS.text(font_32,'Dys: ' + str(obj_menu.interwal_dystans),0,prog_1            ,kolor_napis)
                        IPS.text(font_32,'Pauza: ' + str(obj_menu.interwal_dystans_pause),160,prog_1  ,kolor_napis)
                        IPS.text(font_32,'Nr',        4   ,prog_2   ,kolor_napis)
                        IPS.text(font_32,'Czas[s]',      52  ,prog_2   ,kolor_napis)
                        IPS.text(font_32,'Avg Km/h', 180  ,prog_2   ,kolor_napis)
                    ### tu jest źle     
                    ###=== Wyświetlanie statystyk ===###
                    for numer in range(obj_menu.ilosc_cykli):
                        #==  Warunki z odpowiednią wyskością =#
                        if obj_menu.podsumowanie_interwalu_przycisk <= 2:
                            wysokosc = 84 +(numer-obj_menu.podsumowanie_interwalu_przycisk )*40 
                        elif obj_menu.podsumowanie_interwalu_przycisk >= 3:
                            wysokosc = 4 +(numer*40)
                        #= Warunek, żeby nie nadpisywało ostatniej wartości z listy na ostatnią wyśweitlaną pozycję =#
                        if wysokosc > 204:
                            break 
                        #= Konieczny warunek, ponieważ najpierw chcemy przesunąć wszystko o 2 do góry a dopiero potem 'scrollowac' =#
                        if obj_menu.podsumowanie_interwalu_przycisk >= 3:
                              numer += obj_menu.podsumowanie_interwalu_przycisk  -2  # -2 bo bo po 3 kliknięciu chcemy przesunąć o 1 etc..                 
                        if numer >= obj_menu.ilosc_cykli:
                            break
                        IPS.text(font_32    ,str(numer+1)   ,10      ,wysokosc  ,kolor_napis)
                        #= Poszczególne dane z interwału =#
                        if rodzaj == 1: # Interwał czasowy
                            dystans = str(round(obj_menu.przejechany_dystans[numer]*obj_licznik.obwod_kola/1000))
                            srednia = str(round((obj_menu.przejechany_dystans[numer]*obj_licznik.obwod_kola*3.6)/(1000*obj_menu.interwal_czas ),1))
                            IPS.text(font_32    ,dystans       ,int(105 - len(dystans)*8)    ,wysokosc  ,kolor_napis)
                            IPS.text(font_32    ,srednia       ,int(240 - len(srednia)*8)    ,wysokosc  ,kolor_napis)   
                        
                    
                        elif rodzaj ==2: #Interwał dystansowy
                            czas = str(round(obj_menu.dlugosc_interwalu[numer]/1000))
                            srednia =str(round(obj_menu.interwal_dystans*3.6/(obj_menu.dlugosc_interwalu[numer]/1000),1))
                            IPS.text(font_32    ,czas          ,int(105 - len(czas)*8)       ,wysokosc  ,kolor_napis)
                            IPS.text(font_32    ,srednia       ,int(240 - len(srednia)*8)    ,wysokosc  ,kolor_napis)                               

                     
                    self.zmiana_przycisk = False
                    gc.collect()
                    
                else:
                    pass
                               
       
    def konutry_intrwal( self, kolor,obj_menu):
        IPS.fill(st7789.BLACK)
        if obj_menu.podsumowanie_interwalu_przycisk == 0:
            pass
        elif obj_menu.podsumowanie_interwalu_przycisk != 0:
            IPS.vline(40, 0, 40, kolor)
            IPS.vline(170, 0, 40, kolor)           
        if obj_menu.podsumowanie_interwalu_przycisk >= obj_menu.ilosc_cykli - 3:
            IPS.vline(40, 40, 200, kolor)
            IPS.vline(170, 40, 200, kolor)
        elif obj_menu.podsumowanie_interwalu_przycisk < obj_menu.ilosc_cykli - 2: 
            IPS.vline(40, 40, 240, kolor)
            IPS.vline(170, 40, 240, kolor)
          
        IPS.hline(0, 40, 320, kolor)
        IPS.hline(0, 80, 320, kolor)
        IPS.hline(0, 120, 320, kolor)
        IPS.hline(0, 160, 320, kolor)
        IPS.hline(0, 200, 320, kolor)
        
    














    
    
    
    