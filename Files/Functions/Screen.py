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
start = 0
delta = 0
b = st7789.color565(50,100,255)
gold =  st7789.color565(179 , 139 , 91 )
start = 0
class Display():
#### Dodatkowe zmienne do wykrycia zniamy aby nastąpiło czyszczenie przed pokazaniem nowych danych
    zmiana_czasu               = 0
    wyswietlana_predkosc       = 0  
    wyswietlana_cadence        = 0
#### Zmienne do speedometera ###
    wyswietlana_cadence_speedometer  = 0   
    wyswietlana_predkosc_speedometer = 0 
    wejscie  = True
    speed    = 0
    roznica  = 0
    prog     = 0
    pochodna = True
    poprzednia_pochodna = True   
    pozycja = 0
    pozycja_x = 0
    pozycja_y = 0
    speedometer_stop = False
    dlugosc_smugi = 0
    aktualna_pozycja = 0 
    dlugosc_wskaznia = 0
##### Do zmiany koloru
    wybor_motywu_obrecz = 0
    wybor_motywu_speedo = 0
    wybor_motywu_czas = 0
    wybor_motywu_dyst = 0
    kolor_czcionki = 0
    kolor_podrozy = 0
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
        ###=== Interwały ===###

        if obj_menu.interwal_czas_start_0 == True:
            self.interwal_czas(obj_menu,obj_licznik)
            
        elif obj_menu.interwal_dystans_start_0 == True:
            self.interwal_dstans(obj_menu,obj_licznik)  
        
        ###=== Spedometer ===###    
        if obj_menu.warunek_ktory_wyswietlacz ==0:  
            self.wyswietlanie_speedometera(obj_menu,obj_licznik, 160,180,157)
      
        ###=== Cała reszta ===###    
        else:
            if self.wejscie == False: #Jeżeli wyszliśmy z funkcji #Spedometer to czyścimy jednorazowo screena
                if obj_menu.interwal_czas_start_0 == True:
                    IPS.fill_rect(0,0,320,132,st7789.BLACK)
                    IPS.fill_rect(240,193,80,38,st7789.BLACK)
                    IPS.fill_rect(0,132,120,108,st7789.BLACK)
                    IPS.fill_rect(120,109,30,30, st7789.BLACK)
                    IPS.fill_rect(220,115,100,42,st7789.BLACK)
                    IPS.fill_rect(310,155,10,30,st7789.BLACK)
                    IPS.fill_rect(120,132,20,5,st7789.BLACK)
                elif  obj_menu.interwal_dystans_start_0 == True:
                    IPS.fill_rect(0,0,320,181,st7789.BLACK)
                else:
                    IPS.fill(st7789.BLACK)
                #Dodac funkcje ustawiajacą na defultowe wartosci eby po ponowym wejsciu do speedometera dzialalo jak nalezy
                self.wejscie = True
                              
            self.show_speed(obj_licznik.current_speed)
            self.show_cadence(obj_licznik.current_cadence)
            if obj_menu.zmiana_przycisk == True:
                gc.collect() # Just in case, bo nie ma framebuffera  
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
 
    def funkcja_wyswietlacz_1(self,obj_licznik,obj_menu): #Total dystans   
        self.show_picture(obj_menu)
        IPS.text(font_32, str(round(obj_licznik.counter * obj_licznik.obwod_kola/1000000,1)) + ' Km'    , 5    ,110,  self.motyw_czcionki(self.kolor_czcionki))
        IPS.text(font_32, str(round(obj_licznik.counter_podroz * obj_licznik.obwod_kola/1000000,1))  , 5   ,150,   self.motyw_czcionki((self.kolor_czcionki-1)))
        
    def funkcja_wyswietlacz_2(self,obj_licznik,obj_menu): #Przewyzszenia
        self.show_picture(obj_menu)
        IPS.text(font_32, str(round(obj_licznik.przeywzszenia,1)) + ' m' ,          5    ,110,self.motyw_czcionki(self.kolor_czcionki))
        IPS.text(font_32, str(round(obj_licznik.przeywzszenia_podroz,1)) ,    5    ,150,self.motyw_czcionki((self.kolor_czcionki-1)))        
        
    def funkcja_wyswietlacz_3(self,obj_licznik,obj_menu): #Max speed
        self.show_picture(obj_menu)
        IPS.text(font_32, str(round(obj_licznik.v_max,1))+ ' Km/h' ,        5    ,110,self.motyw_czcionki(self.kolor_czcionki))
        IPS.text(font_32, str(round(obj_licznik.v_max_podroz,1)) , 5    ,150,self.motyw_czcionki((self.kolor_czcionki-1)))
        
    def funkcja_wyswietlacz_4(self,obj_licznik,obj_menu): #Czas
        self.show_picture(obj_menu)
        obj_licznik.rtc_czas()
        if self.zmiana_czasu != obj_licznik.rtc_czas_podroz[3]:
            IPS.fill_rect(0,109,120,72, st7789.BLACK)
            IPS.fill_rect(120,109,30,30, st7789.BLACK)
            IPS.fill_rect(120,140,9,31, st7789.BLACK)
            self.zmiana_czasu = obj_licznik.rtc_czas_podroz[3]
            
        IPS.text(font_32, str(obj_licznik.rtc_czas_total[0]) +':'+ str(obj_licznik.rtc_czas_total[1])+':'
        +str(obj_licznik.rtc_czas_total[2])+':'+str(obj_licznik.rtc_czas_total[3]) , 0    ,108,self.motyw_czcionki(self.kolor_czcionki), 1)
        if obj_licznik.rtc_czas_podroz[0] == 0:
            IPS.text(font_32,  str(obj_licznik.rtc_czas_podroz[1])+':'
            +str(obj_licznik.rtc_czas_podroz[2])+':'+str(obj_licznik.rtc_czas_podroz[3]) , 0    ,145,self.motyw_czcionki((self.kolor_czcionki-1)))
        else:      
            IPS.draw(romand, str(obj_licznik.rtc_czas_podroz[0]) +':'+ str(obj_licznik.rtc_czas_podroz[1])+':'
            +str(obj_licznik.rtc_czas_podroz[2])+':'+str(obj_licznik.rtc_czas_podroz[3]) , 0   ,164,self.motyw_czcionki((self.kolor_czcionki-1)),0.75)
                    
    def funkcja_wyswietlacz_5(self,obj_licznik,obj_menu): #Srednia predkosc 
        self.show_picture(obj_menu)
        IPS.text(font_32,str(round(obj_licznik.v_srednie_t(),1))+ ' Km/h'  ,5    ,110,self.motyw_czcionki(self.kolor_czcionki))
        if obj_licznik.v_srednie_p() == None:
            pass
        else:
            IPS.text(font_32, str(round(obj_licznik.v_srednie_p(),1)) ,5    ,150,self.motyw_czcionki((self.kolor_czcionki-1)))
                
    def show_picture(self, obj_menu):
        if obj_menu.zmiana_przycisk == True:
            gc.collect() # Just in case, bo nie ma framebuffera
            micropython.alloc_emergency_exception_buf(100)
            IPS.fill_rect(0,0,160,105, st7789.BLACK)
            if obj_menu.warunek_ktory_wyswietlacz ==1:
                IPS.jpg('/Libraries/Pictures/total.jpg',30,0, st7789.SLOW)           #105x105
            elif obj_menu.warunek_ktory_wyswietlacz ==2:
                IPS.jpg( '/Libraries/Pictures/przewyzszenia.jpg' ,30,0, st7789.SLOW) #118x98
            elif obj_menu.warunek_ktory_wyswietlacz ==3:              
                IPS.jpg('/Libraries/Pictures/v_max.jpg' ,11,0, st7789.SLOW)          #138x101
            elif obj_menu.warunek_ktory_wyswietlacz ==4:              
                IPS.jpg('/Libraries/Pictures/czas.jpg' ,29,0, st7789.SLOW)           #102x105
            elif obj_menu.warunek_ktory_wyswietlacz ==5:                
                IPS.jpg('/Libraries/Pictures/v_sr.jpg',10,0, st7789.SLOW )           #140x102                  
            obj_menu.zmiana_przycisk = False
        else:
            pass
    
    def show_speed(self,predkosc):
        gc.collect() # Just in case, bo nie ma framebuffera               
        if self.wyswietlana_predkosc != predkosc:
            gc.collect() # Just in case, bo nie ma framebuffera    
            speed = int(predkosc)
            if speed > 9:
                x = 280
            else:
                x = 225    
            IPS.fill_rect(164,20,156,90,st7789.BLACK)
            IPS.draw(romand, str(speed), 160, 60,self.motyw_czcionki(self.kolor_czcionki), 3.1)
            IPS.draw(romand, str(round((round(predkosc,1)- speed)*10)), x, 47, self.motyw_czcionki(self.kolor_czcionki), 1.9)
            self.wyswietlana_predkosc = predkosc
        else:
            pass       
 

    def show_speed_speedometer(self,predkosc, obj_menu):
                  
        if self.wyswietlana_predkosc_speedometer != predkosc:
            gc.collect() # Just in case, bo nie ma framebuffera   
            speed = int(predkosc)     
            zaokraglenie = round((round(predkosc,1)- speed)*10)
            if zaokraglenie == 10:
                zaokraglenie = 9         
            
            self.flaga_speed_0 = False  
            if obj_menu.interwal_czas_start_0 == True:
                if speed > 9:
                    x = 78
                else:
                    x = 47
                IPS.fill_rect(0,185,120,55,st7789.BLACK)
                IPS.draw(romand, str(speed), 1, 215, self.motyw_czcionki(self.kolor_czcionki), 2)
                IPS.draw(romand, str(zaokraglenie), x, 203, self.motyw_czcionki(self.kolor_czcionki), 1)          
            elif obj_menu.interwal_dystans_start_0 == True:     
                if speed > 9:
                    x = 187
                else:
                    x = 155
                IPS.fill_rect(107,95,105,51,st7789.BLACK)
                IPS.draw(romand, str(speed), 109, 122, self.motyw_czcionki(self.kolor_czcionki), 2)
                IPS.draw(romand, str(zaokraglenie), x, 110, self.motyw_czcionki(self.kolor_czcionki), 1)    
            else:
                if speed > 9:
                    x = 200
                else:
                    x = 155
                IPS.fill_rect(105,118,125,65,st7789.BLACK)
                IPS.draw(romand, str(speed), 102, 152, self.motyw_czcionki(self.kolor_czcionki), 2.6)
                IPS.draw(romand, str(zaokraglenie), x, 137, self.motyw_czcionki(self.kolor_czcionki), 1.3)
                
            self.wyswietlana_predkosc_speedometer = predkosc
        else:
            pass     
    def show_cadence(self,cadence):
        if self.wyswietlana_cadence != cadence:
            IPS.fill_rect(220,115,100,42,st7789.BLACK)
            IPS.draw(romand, str(round(cadence)), 219, 138, self.motyw_czcionki(self.kolor_czcionki), 1.8)
            self.wyswietlana_cadence = cadence
        else:
            pass
 
    def show_cadence_speedometer(self,cadence, obj_menu):
        if self.wyswietlana_cadence_speedometer != cadence:
            if obj_menu.interwal_czas_start_0 == True:
                IPS.fill_rect(240,193,80,38,st7789.BLACK)
                IPS.draw(romand, str(round(cadence)), 240, 212, self.motyw_czcionki(self.kolor_czcionki), 1.3)
                               
            elif obj_menu.interwal_dystans_start_0 == True:
                IPS.fill_rect(182,146,73,35,st7789.BLACK)
                IPS.draw(romand, str(round(cadence)), 180, 167, self.motyw_czcionki(self.kolor_czcionki), 1.3)                       
                
            else:              
                IPS.fill_rect(115,194,95,40,st7789.BLACK)
                if cadence < 10:
                    x_prim = 1
                elif cadence < 100 and cadence > 10:
                    x_prim = 2
                else:
                    x_prim = 3                   
                IPS.draw(romand, str(round(cadence)), int(160 - x_prim*16), 215, self.motyw_czcionki(self.kolor_czcionki), 1.6)
            self.wyswietlana_cadence_speedometer = cadence
        else:
            pass
 
#===================================== SPEEDOMETER ====================================================#    
         
    def wyswietlanie_speedometera(self,obj_menu, obj_licznik,xm,ym,r):
        global start
        if self.wejscie == True: #Jeżeli wchodzimy do funkcji pierwszy raz
            self.wejscie_speedometer(obj_menu)
            self.obrecz_speedometer(ym,xm,r+4,3) # Rysowanie obręczy od speedometera
            self.wejscie = False                                       # Ustawienie flagi wejścia na False
            
        self.show_cadence_speedometer(obj_licznik.current_cadence ,obj_menu) # Wyświetlamy kadencję 
        self.show_speed_speedometer  (obj_licznik.current_speed   ,obj_menu) # Wyświetlamy aktualną prędkość
         
        if self.speed != obj_licznik.current_speed :                # Jeżeli otrzymaliśmy nową wartość chwilową
            self.roznica = obj_licznik.current_speed - self.speed   # Obliczamy rónicę pomiędzy poprzednią, a nową wartością prędkości
            ##== Gdy prędkość powyżej 50   ==##  
            if obj_licznik.current_speed >50:                       # Zakres speedometera wynosi 50km, jeżeli prędkość jest większa to brawo, zamknąłeś licznik
                if self.speed <= 50:                                # Jeżeli poprzednia wartość, była pmniejsza niż 50 to różnica wynosi różnice pomiędzy poprzednią wartościa a Max_v
                    self.roznica = 50 - self.speed                  # Nadpisujemy nową wartość różnicy jeżeli aktualna prędkość wynosi więcej niż 50  
                elif self.speed > 50:                               # Jeżeli poprzednia wartość, była większa niż 50 to generalnie nie robimy nic, bo zapitalasz nieźle
                    self.roznica = 0
            self.speed = obj_licznik.current_speed                  # Przypisanie zmiennej speed aktualnej prędkości
            
            # Obliczamy aktualną pozycję speedometera [Co innego niż poprzednia prędkości chwilowa!]:
            self.aktualna_pozycja = self.pozycja*50/(r*math.pi)     # Aktualna pozycja jeżeli poprzednio zwiększaliśmy wartość
            if self.pochodna == False:
                self.aktualna_pozycja = 50 -self.aktualna_pozycja   # Jeżeli prędzej odejmowaliśmy, to liczmy od drugiej strony        
            if self.pochodna == True and self.aktualna_pozycja <= self.speed:    # Znaczy, że wciaz chcemy rosnąć 
                self.roznica = 0
            elif self.pochodna == False and self.aktualna_pozycja >= self.speed: # Znaczy, że wciąż chcemy maleć 
                self.roznica = -1              
            
            
            if self.roznica >= 0:                                   # Nowa wartość jest większa niż poprzednia
                self.prog = math.pi*r*self.speed/50                 # Prog to pozycja do ktorej chcemy dojsc i na niej przestac.
                if self.prog > math.pi*r:                           # Jeżeli prędkość jest większa niż 50 km to ustawiamy prog na 50 km 
                    self.prog = math.pi*r
                self.pochodna = True                                # Ustawiamy flagę na True, bo mamy wzroty 

            elif self.roznica < 0:                                  # Nowa wartość jest mniejsza niż poprzednia
                self.prog = math.pi*r*(50 -self.speed)/50
                if self.prog < 1:                                   # Jeżeli zwalniamy z ponad 50 i jedziemy ponad 50 to prog wtedy byłby ujemny, wiec ustawiamy go na 1
                    self.prog = 1
                self.pochodna = False                               # Ustawiamy flagę na False, bo mamy spadki 
                
            if self.pochodna != self.poprzednia_pochodna:           # Wykrycie zmiany kierunu
            # Będziemy wywoływać inną funkcję która iteruje się od drugiej strony, dodatkowo - 4 aby zamalować wskaźnik
                self.pozycja = round(math.pi*r - self.pozycja -4)   # Zmieniamy wartość pozycji
        
            self.poprzednia_pochodna = self.pochodna                # Przypisanie poprzedniej wartości pochodnej         
            self.speedometer_stop = False

    
            
        if self.speedometer_stop == False:                          # Jeżeli 'mamy pozwolenie' na rysowanie                           
                self.smuga_i_wsk(obj_menu,obj_licznik,xm,ym,r)
                

    def smuga_i_wsk(self,obj_menu,obj_licznik,xm,ym,r):
        if self.pozycja >= self.prog:
            self.speedometer_stop = True    
        ## Dane do smugi    
        if self.pochodna == True: 
            x1 = -round(r*math.cos(self.pozycja/r)) + xm   
            x2 = x1 + round(self.dlugosc_wskaznia*math.cos(self.pozycja/r))
        ## Dane do wskaźnika       
            x_wsk = -round(r*math.cos((self.pozycja+3)/r)) + xm
            rotacja = ((self.pozycja/r) +math.pi/2)              # Rotujemy od pi/2 do 3*pi/2
        ## Dane do koloru         
            pozycja_kolor = (self.pozycja/500)*255
        else:
        ## Dane do smugi  
            x1 = round(r*math.cos(self.pozycja/r)) + xm
            x2 = x1 - round(self.dlugosc_wskaznia*math.cos(self.pozycja/r))
        ## Dane do wskaźnika    
            x_wsk =  round(r*math.cos((self.pozycja+3)/r)) + xm
            rotacja = (-(self.pozycja/r) + 3*math.pi/2)          # Rotujemy od 3*pi/2 do pi/2
        ## Dane do koloru    
            pozycja_kolor = 255*(math.pi *r-self.pozycja)/500
       
        y1 = -round(r*math.sin(self.pozycja/r)) + ym
        y2 = y1 + round(self.dlugosc_wskaznia*math.sin(self.pozycja/r))
        # [x1,y1] przechowują wsp. zewnętrzne do smugi
        # [x2,y2] przechowują wsp. wewnętrzne do smugi
        # [x_wsk,y_wsk] przechowują wsp.  do wskaźnika
        y_wsk =   -round(r*math.sin((self.pozycja+3)/r)) + ym
                  
            
        ####### Rysowanie wskaźnika #####
        IPS.polygon(self.wskaznik(-self.dlugosc_wskaznia+1 ,1),  x_wsk,  y_wsk,
                    self.kolor_obreczy_i_int(self.wybor_motywu_obrecz, pozycja_kolor), rotacja )

        ####### Rysowanie smugi #####
        self.draw_line(x1,y1,x2,y2,pozycja_kolor)


        self.pozycja += 1 # przesuwamy się o jedną pozycję dalej 

    @micropython.native
    def draw_line(self,x1,y1,x2,y2,pozycja_kolor):
        if y1 == y2:                 # Nie można dzielić przez 0 
            a = 0
        else:
            a = (x1-x2)/(y1 - y2)    # Teoretycznie wzór wygląda inaczej, ale to jest dobrze         
        dlugosc_po_x = abs(x1 - x2)  # Wyliczamy różnice po x i y
        dlugosc_po_y = abs(y1 - y2)
        wybor = self.wybor_motywu_speedo 
        
        

        
        if dlugosc_po_y >= dlugosc_po_x:  # prędkość  [12.5 - 37.5]
            skala = self.dlugosc_wskaznia/dlugosc_po_y
            dlugosc_lini = range(dlugosc_po_y+ 1)
#             start = time.ticks_us() # get millisecond counter 
        ### Ta część kodu zajmuję najwięcej czasu, ok 8ms z 11 ms okresu  ###
            for i in dlugosc_lini:
                arg1 = i * skala     # Konwetujemy zmienną arg1 zgodnie ze skalą aby zachować odpowiedni fade
                x_prim = round(i*a)  # Wyliczam nachylenie prostej, zapisuje do zmiennej lokalnej w celach optymalizacji 
                # Zamazywanie za sobą smugi, bez konieczności wywoływania funkcji od koloru oraz realizacja 'cofania'   
                if arg1 <= self.dlugosc_smugi and self.pochodna == True:
                    IPS.pixel(x1+x_prim   ,y1 + i,    Display.kolor_smugi(wybor,arg1,pozycja_kolor))
                    IPS.pixel(x1+x_prim +1,y1 + i,    Display.kolor_smugi(wybor,arg1,pozycja_kolor))
                else:
                    IPS.pixel(x1+x_prim   ,y1 + i,    st7789.BLACK)
                    IPS.pixel(x1+x_prim +1,y1 + i,    st7789.BLACK)  
#             delta = time.ticks_diff(time.ticks_us(), start) # compute time difference
#             print(delta)
        else: # prędkość  [0- 12.5) u (37.5 - 50]
            if y1 != y2:             # Nie można dzielić przez 0 
                a = 1/a
                 
            skala = self.dlugosc_wskaznia/dlugosc_po_x
            dlugosc_lini = range(dlugosc_po_x + 1)
            for i in dlugosc_lini:
                arg1 = i * skala      
                y_prim  = round(i*a)   
                # Zamazywanie za sobą smugi, bez konieczności wywoływania funkcji od koloru
                # Oraz realizacja 'cofania'     
                if arg1 <= self.dlugosc_smugi and self.pochodna == True :
                    
                    if x1 <= x2:
                        IPS.pixel(x1+i,y1 + y_prim,   Display.kolor_smugi(wybor,arg1,pozycja_kolor))  # 1 ćwiartka
                        IPS.pixel(x1+i,y1 + y_prim-1, Display.kolor_smugi(wybor,arg1,pozycja_kolor))  
                    else:
                        IPS.pixel(x1-i,y1 - y_prim,  Display.kolor_smugi(wybor,arg1,pozycja_kolor))    # 4 ćwiartka
                        IPS.pixel(x1-i,y1 - y_prim+1, Display.kolor_smugi(wybor,arg1,pozycja_kolor))   
                else:
                    if x1 <= x2 :
                        IPS.pixel(x1+i,y1 + y_prim,   st7789.BLACK)  # 1 ćwiartka
                        IPS.pixel(x1+i,y1 + y_prim-1, st7789.BLACK)  
                    else:
                        IPS.pixel(x1-i,y1 - y_prim,   st7789.BLACK)  # 4 ćwiartka
                        IPS.pixel(x1-i,y1 - y_prim+1, st7789.BLACK)
                        
                        
############################################################################################################                           
    def kolor_obreczy_i_int(self,wybor, poz):
    ##############################== Kolor po pozycji ==############################################
            ### Z zółtego do czerwonego ##
        if wybor == 0:
            RED   = 255
            GREEN = 230 -poz * 0.9
            BLUE  = 30 - poz* 0.1
            return st7789.color565( int(RED),int(GREEN), int(BLUE))    
            ### Cimno niebieski  przez  do szkrałatnego ###
        elif wybor == 1:   
            RED   = 20 + poz*0.8
            GREEN = 0
            BLUE  = 143 -poz*0.5 
            return st7789.color565(int(RED),GREEN, int(BLUE))   
           ### Turkusowny do magneto - różowego  ###
        elif wybor == 2:
            RED   = 50 + poz * 0.8
            GREEN = 233 - poz *2/3
            BLUE  = 172  +  poz * 0.3
            return st7789.color565(int(RED),int(GREEN), int(BLUE))
           ### Żółty do ciemno zielonego   ###
        elif wybor == 3:
            RED   = 230 - poz * 0.9
            GREEN = 230 - poz *0.6
            BLUE  =  poz * 0.1
            return st7789.color565(int(RED),int(GREEN), int(BLUE))     
        elif wybor == 4:    
            RED   = 100+ poz*0.6
            GREEN = poz*0.3
            BLUE  = 0
            return st7789.color565(int(RED),int(GREEN), int(BLUE))
    ##############################== Stały kolor ==############################################    
        elif wybor == 5:
            RED   = 0
            GREEN = 255 
            BLUE  = 255
            return st7789.color565(int(RED),int(GREEN), int(BLUE))
        elif wybor == 6:
            return st7789.RED         
        elif wybor == 7:
            return st7789.WHITE        
    @micropython.native
    def kolor_smugi(wybor, arg,poz):  
        # arg1 [0 - 36]   Do fade smugi 
        # poz  [0 - 255]  Czyli po pozycji
    ##############################== Kolor po argumencie i po pozycji ==############################################     
            ### Z zółtego do czerwonego  ###
        if wybor == 0:
            RED   = 255
            GREEN = 230 -poz * 0.9
            BLUE  = 30 - poz* 0.1
            return st7789.color565( int(RED*(1- arg/60))  , int(GREEN*(1- arg/60)), int(BLUE*(1- arg/60)))
            ### Tęcza  ###
        elif wybor == 1:
            return Display.tecza(arg)
  
            ### Turkusowny do magneto - różowego ###
        elif wybor == 2:
            RED   = 50 + poz * 0.8
            GREEN = 233 - poz *2/3
            BLUE  = 172  +  poz * 0.3
            return st7789.color565(int(RED*(1- arg/72))  , int(GREEN*(1- arg/72)), int(BLUE*(1- arg/72)))
        
            ### Ciemny czerwony do krwistej pomarańczy   ###
        elif wybor == 3:
            RED   = 100+ poz*0.6
            GREEN = poz*0.3
            BLUE  = 0
            return st7789.color565(int(RED*(1- arg/72))  , int(GREEN*(1- arg/40)), int(BLUE*(1- arg/36)))
        
            ### Cimno niebieski  przez  do szkrałatnego  ###
        elif wybor == 4:
            RED   = 20 + poz*0.8
            GREEN = 0
            BLUE  = 143 -poz*0.5   
            return st7789.color565(int(RED*(1- arg/36))  , int(GREEN*(1- arg/36)), int(BLUE*(1- arg/36)))   
            ### Turkusowy ###  
        elif wybor == 5:
            RED   = 0
            GREEN = 255 
            BLUE  = 255
            return st7789.color565(int(RED*(1- arg/55))  , int(GREEN*(1- arg/55)), int(BLUE*(1- arg/55)))
            ### Jasno Zielon- żółty ###  
        elif wybor == 6:
            RED   = poz
            GREEN = 255
            BLUE  = 0 
            return st7789.color565(int(RED*(1- arg/36))  , int(GREEN*(1- arg/50)), int(BLUE*(1- arg/50)))
        
        elif wybor == 7:
            RED   = 0+ poz* 0.5
            GREEN = 255 - poz
            BLUE  = 255
            return st7789.color565(int(RED*(1- arg/80))  , int(GREEN*(1- arg/80)), int(BLUE*(1- arg/80)))
        elif wybor == 8:
            RED   = 0 + poz* 0.3
            GREEN = 255 
            BLUE  = 255 - poz
            return st7789.color565(int(RED*(1- arg/80))  , int(GREEN*(1- arg/80)), int(BLUE*(1- arg/80)))



    def motyw_czcionki(self,wybor):
        if wybor == 0:
            return st7789.BLUE
        if wybor == 1:
            return st7789.GREEN
        if wybor == 2:
            return st7789.RED
        if wybor == 3:
            return st7789.CYAN
        if wybor == 4:
            return st7789.YELLOW
        if wybor == 5:
            return st7789.WHITE
        if wybor == 6:
            return st7789.MAGENTA
        else:
            return st7789.MAGENTA        
        
    @micropython.native
    def tecza(arg):
            if arg <= 6:     
                RED   = 255
                GREEN = 0
                BLUE  = 0
            elif arg > 6 and arg <= 12:     
                RED   = 255
                GREEN = 122
                BLUE  = 0
            elif arg > 12 and arg <= 18:     
                RED   = 240
                GREEN = 255
                BLUE  = 0
            elif arg > 18 and arg <= 24:     
                RED   = 0
                GREEN = 255
                BLUE  = 0
            elif arg > 24 and arg <= 30:     
                RED   = 0
                GREEN = 0
                BLUE  = 255
            else:    
                RED   = 80
                GREEN = 0
                BLUE  = 150  
            return st7789.color565(RED,GREEN,BLUE) 
############################################################################################################             
                 
    def wskaznik(self,length, radius):
        return [
            (0, 0),
            (-radius, radius),
            (0, length),
            (radius, radius),
            (0,0)
                ]
 
    def wejscie_speedometer(self,obj_menu):
        if obj_menu.interwal_czas_start_0 == True:       # Czyszczenie dla interwału czasowego 
            IPS.fill_rect(0,0,320,132,st7789.BLACK)
            IPS.fill_rect(0,132,120,108,st7789.BLACK)
            IPS.fill_rect(120,109,30,30, st7789.BLACK)          
            IPS.fill_rect(164,20,156,90,st7789.BLACK)
            IPS.fill_rect(220,115,100,42,st7789.BLACK)
            IPS.fill_rect(120,132,20,5,st7789.BLACK)
        elif  obj_menu.interwal_dystans_start_0 == True:    # Czyszczenie dla interwału dystansowego
            IPS.fill_rect(0,0,320,181,st7789.BLACK)
        else:
            IPS.fill(st7789.BLACK)                          # Standardowe czyszczenie całego ekranu
        self.speed   = 0                                    # Ustawiamy zmienne na defoult aby odpowiednio działało                             
        self.pozycja = 0 
        self.pochodna = True
        self.poprzednia_pochodna = True
        self.prog = 0

    def obrecz_speedometer(self,ym,xm,r,odcinek):
        ####### Rysowanie wskaźnika #####
        kolor = self.kolor_obreczy_i_int(self.wybor_motywu_obrecz,0)
        IPS.polygon(self.wskaznik(-self.dlugosc_wskaznia+1 ,1),  xm-r,  ym-1, kolor, math.pi/2 )
        IPS.polygon(self.wskaznik(-self.dlugosc_wskaznia+1 ,1),  xm-r,  ym-2, kolor, math.pi/2 )
        for i in range(math.pi*r):
            x = 255*i/(math.pi*r)
            kolor = self.kolor_obreczy_i_int(self.wybor_motywu_obrecz,x )
            #Rysowanie lini pomiędzy 2 obręczami 
            IPS.line(-int(r*math.cos(i/r)) +xm        ,
                 -int(r*math.sin(i/r)) + ym ,
                 -int(r*math.cos(i/r)) +xm + int(odcinek * math.cos(i/r)) ,
                 -int(r*math.sin(i/r)) + ym + int(odcinek*math.sin(i/r)), kolor)
            #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y wyżej aby wypełnić luki (np dla 45 stopni)  
            IPS.line(-int(r*math.cos((i)/r)) +xm        ,
             -int(r*math.sin(i/r)) + ym-1  ,
             -int(r*math.cos(i/r)) +xm + int(odcinek * math.cos((i)/r)) ,
             -int(r*math.sin(i/r)) + ym + int(odcinek*math.sin((i)/r)-1), kolor) 
        
  
                   
#===================================== INTERWAŁY ====================================================#
    
     
    def interwal_dstans(self,obj_menu,obj_licznik):
        ###=== Część odpowiedzialna czyszczenie danych po cyklu ===###
        if obj_menu.czyszczenie == True:
            if obj_menu.dodatkowe_czyszczenie == True:
                IPS.fill(st7789.BLACK)
                obj_menu.dodatkowe_czyszczenie = False 
            IPS.rect(0,185,320,55,st7789.color565(20,20,20))
            IPS.rect(1,186,318,53,st7789.color565(20,20,20))
            IPS.rect(2,187,316,51,st7789.color565(20,20,20))
            IPS.fill_rect(3,188,314,49,st7789.color565(20,20,20))
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
                    obj_menu.Odmierzanie_grafiki += 1                     # Przesunięcie się o jedą pozycje dalej           
                    pozycja_kolor = 255 *obj_menu.Odmierzanie_grafiki/314  # Wyliczenie argumentu od koloru 
                    IPS.vline(2 + obj_menu.Odmierzanie_grafiki , 188, 49
                              ,self.kolor_obreczy_i_int(self.wybor_motywu_dyst,pozycja_kolor))
                    
            elif obj_menu.cykle %2 == 0:
                if  obj_menu.odliczanie *obj_licznik.obwod_kola/1000 <  obj_menu.interwal_dystans_pause  * (1 - obj_menu.Odmierzanie_grafiki /314):
                    obj_menu.Odmierzanie_grafiki += 1                      # Przesunięcie się o jedą pozycje dalej 
                    
                    pozycja_kolor = 255 *obj_menu.Odmierzanie_grafiki/314  # Wyliczenie argumentu od koloru 
                    IPS.vline(2 + obj_menu.Odmierzanie_grafiki , 188, 49
                              ,self.kolor_obreczy_i_int(self.wybor_motywu_dyst,pozycja_kolor))

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
            obj_menu.podsumowanie = True    # Włączamy przycisk
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
                    
                    pozycja_kolor = 255 *obj_menu.Odmierzanie_grafiki/314  # Wyliczenie argumentu od koloru 
                    self.rysowanie_czasu(obj_menu.Odmierzanie_grafiki,self.kolor_obreczy_i_int(self.wybor_motywu_czas,pozycja_kolor))

            elif obj_menu.cykle %2 == 0:
                if  obj_menu.odliczanie <  obj_menu.interwal_pause  * (1 - obj_menu.Odmierzanie_grafiki /314):
                    obj_menu.Odmierzanie_grafiki += 1
                    
                    pozycja_kolor = 255 *obj_menu.Odmierzanie_grafiki/314  # Wyliczenie argumentu od koloru 
                    self.rysowanie_czasu(obj_menu.Odmierzanie_grafiki,self.kolor_obreczy_i_int(self.wybor_motywu_czas,pozycja_kolor))
                    
                    
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
        obj_menu.zmiana_przycisk = True                   # Aby od razu wyświetliły się dane 
 
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
                self.wejscie = True            # Ustawiamy flagę wejścia na True 
                gc.collect()                   # Just in case 
                break
            ##== Pokazanie danych ==##
            else:
                #== Rysujemy tylko, gdy przycisk został naciśnięty ==#
                if obj_menu.zmiana_przycisk == True:         
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

                     
                    obj_menu.zmiana_przycisk = False
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
        
    

    