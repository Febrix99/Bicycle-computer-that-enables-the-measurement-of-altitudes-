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
gold =  st7789.color565(190 , 130 , 60 ) # st7789.color565(179 , 139 , 91 )
class Display():
#### Dodatkowe zmienne do wykrycia zniamy aby nastąpiło czyszczenie przed pokazaniem nowych danych
    zmiana_czasu, speed,wyswietlana_cadence             = 0,0,0
    wyswietlana_cadence        = 0
#### Zmienne do speedometera ###
    wyswietlana_cadence_speedometer  = 0   
    wyswietlana_predkosc_speedometer = 0 
    wejscie  = True
    roznica  = 0
    prog     = 0
    pochodna = True
    poprzednia_pochodna = True   
    pozycja = 0
    pozycja_x ,pozycja_y, speedometer_stop = 0,0,False
    dlugosc_smugi,aktualna_pozycja, dlugosc_wskaznia = 0,0,0
##### Do zmiany koloru
    wybor_motywu_obrecz,wybor_motywu_speedo,wybor_motywu_czas = 0,0,0
    kolor_czcionki, kolor_podrozy ,wybor_motywu_dyst= 0,0,0 
#### Zmienne do menu ###
    poprzedni_wybor = 0
    wejscie_do_menu = False
    wymazanie_prostokata = False 
    mruganie_liczb = False
    deadline = 0
    
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
            self.wyswietlanie_speedometera(obj_menu,obj_licznik, 160,177,157)
            
        ###=== Cała reszta ===###    
        else:
            if self.wejscie == False: #Jeżeli wyszliśmy z funkcji #Spedometer to czyścimy jednorazowo screena
                if obj_menu.interwal_czas_start_0 == True:
                    Display.clear_interwal_czas(st7789.BLACK)
                elif  obj_menu.interwal_dystans_start_0 == True:
                    IPS.fill_rect(0,0,320,186,st7789.BLACK)
                else:
                    IPS.fill(st7789.BLACK)
                self.wejscie = True
                              
            self.show_cadence(obj_licznik.current_cadence,obj_menu.zmiana_przycisk)
            self.show_speed(obj_licznik.current_speed,obj_menu.zmiana_przycisk )
            if obj_menu.zmiana_przycisk == True:
                gc.collect() # Just in case, bo nie ma framebuffera  
                IPS.fill_rect(0,109,120,72, st7789.BLACK)
                IPS.fill_rect(120,109,30,30, st7789.BLACK)
                IPS.fill_rect(120,140,9,31, st7789.BLACK)
                self.show_picture(obj_menu)
                obj_menu.zmiana_przycisk = False
                
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
        IPS.text(font_32, str(round(obj_licznik.counter * obj_licznik.obwod_kola/1000000,1)) + ' Km' , 5    ,110,  self.motyw_czcionki(self.kolor_czcionki))
        IPS.text(font_32, str(round(obj_licznik.counter_podroz * obj_licznik.obwod_kola/1000000,1))  , 5   ,150,   self.motyw_czcionki((self.kolor_czcionki-1)))
        
    def funkcja_wyswietlacz_2(self,obj_licznik,obj_menu): #Przewyzszenia
        IPS.text(font_32, str(round(obj_licznik.przewyzszenia)) + ' m' ,    5    ,110,self.motyw_czcionki(self.kolor_czcionki))
        IPS.text(font_32, str(round(obj_licznik.przewyzszenia_podroz)) ,    5    ,150,self.motyw_czcionki((self.kolor_czcionki-1)))        
    def funkcja_wyswietlacz_3(self,obj_licznik,obj_menu): #Max speed
        IPS.text(font_32, str(round(obj_licznik.v_max,1))+' Km/h' ,5    ,110,self.motyw_czcionki(self.kolor_czcionki))
        IPS.text(font_32, str(round(obj_licznik.v_max_podroz,1)) , 5    ,150,self.motyw_czcionki((self.kolor_czcionki-1)))
        
    def funkcja_wyswietlacz_4(self,obj_licznik,obj_menu): #Czas
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
        IPS.text(font_32,str(round(obj_licznik.v_srednie_t(),1))+ ' Km/h'  ,5    ,110,self.motyw_czcionki(self.kolor_czcionki))
        IPS.text(font_32,str(round(obj_licznik.v_srednie_t(),1))+ ' Km/h', 5, 110, self.motyw_czcionki(self.kolor_czcionki))
        if obj_licznik.v_srednie_p() == None:
            pass
        else:
            IPS.text(font_32, str(round(obj_licznik.v_srednie_p(),1)) ,5    ,150,self.motyw_czcionki((self.kolor_czcionki-1)))
              
    def show_picture(self, obj_menu):
        if obj_menu.zmiana_przycisk == True:
            gc.collect() # Just in case, bo nie ma framebuffera
            IPS.fill_rect(0,0,160,105, st7789.BLACK)
            image_data = {
                1: ('/Libraries/Pictures/total.jpg', 30, 0),
                2: ('/Libraries/Pictures/przewyzszenia.jpg', 30, 0),
                3: ('/Libraries/Pictures/v_max.jpg', 30, 0),
                4: ('/Libraries/Pictures/czas.jpg', 29, 0),
                5: ('/Libraries/Pictures/v_sr.jpg', 10, 0),
            }
            path, x, y= image_data.get(obj_menu.warunek_ktory_wyswietlacz, (None, 0, 0))
            if path is not None:
                IPS.jpg(path, x, y, st7789.SLOW)          
    
    def clear_all(self):
        IPS.fill(st7789.BLACK)
    
    def show_speed(self, predkosc, zmiana_przycisk):
        if self.wyswietlana_predkosc != predkosc or zmiana_przycisk ==True:
            gc.collect() # Just in case, bo nie ma framebuffera
            speed = int(predkosc)
            zaokraglenie = min(round((round(predkosc,1) - speed)*10), 9)        
            aktualne_wartosci = (speed,zaokraglenie)
            x = 280 if speed > 9 else 225 
            wspolzedne_i_font_size = (160, 60, x, 45, 3.2,1.8) # x1,y1,x2,y2 font_1, font_2
            if not hasattr(self, 'poprzednie_predkosci'):
                self.poprzednie_predkosci = (speed,zaokraglenie)
            if not hasattr(self, 'poprzednie_wspolrzedne'):
                self.poprzednie_wspolrzedne = (160,x)
                
            self.draw_speed(self.poprzednie_predkosci,self.poprzednie_wspolrzedne, aktualne_wartosci, wspolzedne_i_font_size)
            self.poprzednie_predkosci = (speed,zaokraglenie)
            self.poprzednie_wspolrzedne = (160,x)
            self.wyswietlana_predkosc = predkosc
            
        else:
            pass
        



    def show_speed_speedometer(self,predkosc, obj_menu): 
        if self.wyswietlana_predkosc_speedometer != predkosc or obj_menu.powrot_menu == True:
            gc.collect() # Just in case, bo nie ma framebuffera   
            speed = int(predkosc)
            zaokraglenie = min(round((round(predkosc,1) - speed)*10), 9)  
            aktualne_wartosci = (speed,zaokraglenie)
            
            if obj_menu.interwal_czas_start_0 == True:               
                x = 85 if speed > 9 else 46
                x_1 = 1
                wspolzedne_i_font_size = (x_1, 215, x, 203,2.2,1.2) # x1,y1,x2,y2,size1,size2
                if obj_menu.powrot_menu == True:
                    self.poprzednie_wspolrzedne_1 = (x_1,x)
            elif obj_menu.interwal_dystans_start_0 == True:
                x = 195 if speed > 9 else 168
                x_1 = 109 if speed > 9 else 122
                wspolzedne_i_font_size = (x_1, 120, x, 108,2.3,1.2) # x1,y1,x2,y2,size1,size2
                if obj_menu.powrot_menu == True:
                    self.poprzednie_wspolrzedne_1 = (x_1,x)
            else:
                x = 210 if speed > 9 else 175
                x_1 = 80 if speed > 9 else 110
                wspolzedne_i_font_size = (x_1, 157, x, 141,3.2,1.8) # x1,y1,x2,y2,size1,size2
                
            if not hasattr(self, 'poprzednie_predkosci_1'):
                self.poprzednie_predkosci_1 = (speed,zaokraglenie)
            if not hasattr(self, 'poprzednie_wspolrzedne_1'):
                self.poprzednie_wspolrzedne_1 = (x_1,x)
                                               
            self.draw_speed(self.poprzednie_predkosci_1,self.poprzednie_wspolrzedne_1,aktualne_wartosci, wspolzedne_i_font_size)       
            self.poprzednie_predkosci_1 = (speed,zaokraglenie)
            self.poprzednie_wspolrzedne_1 = (x_1,x)
            self.wyswietlana_predkosc_speedometer = predkosc
            
            if obj_menu.powrot_menu == True:
                obj_menu.powrot_menu = False
                
        else:
            pass
        
        
    def draw_speed(self,poprzednie_predkosci, poprzednie_wspolrzedne,aktualne_wartosci, wspolzedne_i_font_size ):
        old_speed , old_round       = poprzednie_predkosci
        old_x, x                    = poprzednie_wspolrzedne
        speed, zaokraglenie         = aktualne_wartosci
        x1,y1,x2,y2, size_1, size_2 = wspolzedne_i_font_size
        
        IPS.draw(romand, str(old_speed)   ,old_x,y1, st7789.BLACK, size_1)
        IPS.draw(romand, str(old_round)   ,x    ,y2, st7789.BLACK, size_2)
        IPS.draw(romand, str(speed)       ,x1   ,y1, self.motyw_czcionki(self.kolor_czcionki), size_1)
        IPS.draw(romand, str(zaokraglenie),x2   ,y2, self.motyw_czcionki(self.kolor_czcionki), size_2)           
        
        
    def show_cadence(self, cadence,zmiana_przycisk):
        if self.wyswietlana_cadence != cadence or zmiana_przycisk ==True:
            showCadence = round(cadence)
            if showCadence < 10:
                x_prim = 1
            elif showCadence < 100 and showCadence > 10:
                x_prim = 2
            else:
                x_prim = 3
                
            x  = int(273 - x_prim*18)    
            if not hasattr(self, 'poprzednie_x'):
                self.poprzednie_x = x
            IPS.draw(romand, str(round(self.wyswietlana_cadence)),self.poprzednie_x , 138, st7789.BLACK, 1.8)
            IPS.draw(romand, str(showCadence), x, 138, self.motyw_czcionki(self.kolor_czcionki), 1.8)
            self.wyswietlana_cadence = cadence
            self.poprzednie_x = x
        else:
            pass
 
    def show_cadence_speedometer(self,cadence, obj_menu):
        if self.wyswietlana_cadence_speedometer != cadence or obj_menu.powrot_menu == True:

            showCadence = round(cadence)
            if showCadence < 10:
                x_prim = 1
            elif showCadence < 100 and showCadence > 10:
                x_prim = 2
            else:
                x_prim = 3
                
            if obj_menu.interwal_czas_start_0 == True:
                x = int(275 - x_prim*14)
                size = 1.4
                if obj_menu.powrot_menu == True:
                    self.poprzednie_x_1 = x
                IPS.draw(romand, str(round(self.wyswietlana_cadence_speedometer)),self.poprzednie_x_1 , 212, st7789.BLACK, size)
                IPS.draw(romand, str(showCadence), x, 212, self.motyw_czcionki(self.kolor_czcionki), size)
                               
            elif obj_menu.interwal_dystans_start_0 == True:
                x = int(225 - x_prim*13)
                size = 1.3
                if obj_menu.powrot_menu == True:
                    self.poprzednie_x_1 = x
                IPS.draw(romand, str(round(self.wyswietlana_cadence_speedometer)), self.poprzednie_x_1, 167, st7789.BLACK, size)   
                IPS.draw(romand, str(showCadence), x, 167, self.motyw_czcionki(self.kolor_czcionki), size)                       
                
            else:
                x  = int(160 - x_prim*17)
                size = 1.7
                if not hasattr(self, 'poprzednie_x_1'):
                    self.poprzednie_x_1 = x
                IPS.draw(romand, str(round(self.wyswietlana_cadence_speedometer)),self.poprzednie_x_1 , 220, st7789.BLACK, size)    
                IPS.draw(romand, str(showCadence), x , 220, self.motyw_czcionki(self.kolor_czcionki), size)
            self.wyswietlana_cadence_speedometer = cadence
            self.poprzednie_x_1 = x
        else:
            pass
    def clear_interwal_czas(kolor):
        IPS.fill_rect(0,0,320,132,kolor)
        IPS.fill_rect(235,193,85,38,kolor)
        IPS.fill_rect(0,132,120,108,kolor)
        IPS.fill_rect(120,109,30,30, kolor)
        IPS.fill_rect(220,115,100,42,kolor)
        IPS.fill_rect(310,155,10,30,kolor)
        IPS.fill_rect(120,132,20,5,kolor)
#===================================== SPEEDOMETER ====================================================#    
         
    def wyswietlanie_speedometera(self,obj_menu, obj_licznik,xm,ym,r):
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
            if self.aktualna_pozycja >= 50 and self.speed >50:
                self.speedometer_stop = True
            else:
                if self.pochodna == False:
                    self.aktualna_pozycja = 50 -self.aktualna_pozycja   # Jeżeli prędzej odejmowaliśmy, to liczmy od drugiej strony        
                if self.pochodna == True and self.aktualna_pozycja <= self.speed:    # Znaczy, że wciaz chcemy rosnąć 
                    self.roznica = 0
                elif self.pochodna == False and self.aktualna_pozycja >= self.speed: # Znaczy, że wciąż chcemy maleć 
                    self.roznica = -1              
                self.speedometer_stop = False
            
            
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
                self.pozycja = round(math.pi*r - self.pozycja-4)   # Zmieniamy wartość pozycji
                
            self.poprzednia_pochodna = self.pochodna                # Przypisanie poprzedniej wartości pochodnej         
        
        if self.speedometer_stop == False:# Jeżeli 'mamy pozwolenie' na rysowanie
            self.smuga_i_wsk(obj_menu,obj_licznik,xm,ym,r)
            
    @micropython.native
    def smuga_i_wsk(self, obj_menu, obj_licznik, xm, ym, r):
        if self.pozycja >= self.prog:
            self.speedometer_stop = True    
        pozycja_kolor = (self.pozycja / 500) * 255
        
        # Calculate sin and cos values that will be reused
        sin_pos = math.sin(self.pozycja / r)
        cos_pos = math.cos(self.pozycja / r)
        cos_pos_3 = math.cos((self.pozycja + 3) / r)

        if self.pochodna:
            x1 = -round(r * cos_pos) + xm
            x_wsk = -round(r * cos_pos_3) + xm
            rotacja = ((self.pozycja / r) + math.pi / 2)
            x2 = x1 + round(self.dlugosc_wskaznia * cos_pos)
        else:
            x1 = round(r * cos_pos) + xm
            x_wsk = round(r * cos_pos_3) + xm
            rotacja = (-(self.pozycja / r) + 3 * math.pi / 2)
            x2 = x1 - round(self.dlugosc_wskaznia * cos_pos)


        y1 = -round(r * sin_pos) + ym
        y2 = y1 + round(self.dlugosc_wskaznia * sin_pos)
        y_wsk = -round(r * math.sin((self.pozycja +3) / r)) + ym
        # [x1,y1] przechowują wsp. zewnętrzne do smugi
        # [x2,y2] przechowują wsp. wewnętrzne do smugi
        # [x_wsk,y_wsk] przechowują wsp.  do wskaźnika

        ####### Rysowanie wskaźnika #####
        if self.pochodna:
            kolor_wskaznik = pozycja_kolor
        else:
            kolor_wskaznik = (math.pi*r - self.pozycja)/ 500* 255
            
        IPS.polygon(self.wskaznik(-self.dlugosc_wskaznia+1, 1), x_wsk, y_wsk,
                    self.kolor_obreczy_i_int(self.wybor_motywu_obrecz, kolor_wskaznik), rotacja)


        ####### Rysowanie smugi #####
        self.draw_line(x1,y1,x2,y2,pozycja_kolor)
        self.pozycja += 1 # przesuwamy się o jedną pozycję dalej 



    @micropython.native
    def draw_line(self,x1,y1,x2,y2,pozycja_kolor):  
        dlugosc_po_x = abs(x1 - x2)  # Wyliczamy różnice po x i y
        dlugosc_po_y = abs(y1 - y2)
        if dlugosc_po_y >= dlugosc_po_x: # prędkość  [12.5 - 37.5]
            self.draw_line_2and3(x1,y1,x2,y2,pozycja_kolor)

        else: # prędkość  [0- 12.5) u (37.5 - 50]
            self.draw_line_1and4(x1,y1,x2,y2,pozycja_kolor,dlugosc_po_x)      
            
    @micropython.native
    def draw_line_2and3(self,x1,y1,x2,y2,pozycja_kolor):
        diff_y = y1 - y2
        if diff_y == 0:
            a = 0
        else:
            a = (x1 - x2)/diff_y  # Teoretycznie wzór wygląda inaczej, ale to jest dobrze
        
        dlugosc_po_y = abs(diff_y)   
        skala = self.dlugosc_wskaznia/dlugosc_po_y
        dlugosc_lini = range(dlugosc_po_y+ 1)
        wybor = self.wybor_motywu_speedo
        r,g,b = Display.kolor_smugi_1(wybor , pozycja_kolor)
        
        if self.pochodna == True:  
            for i in dlugosc_lini:
                arg1 = i * skala     # Konwetujemy zmienną arg1 zgodnie ze skalą aby zachować odpowiedni fade
                x_prim = round(i*a)  # Wyliczam nachylenie prostej, zapisuje do zmiennej lokalnej w celach optymalizacji  
                x = x1+x_prim
                y = y1 + i
                if arg1 <= self.dlugosc_smugi:
                    kolor = Display.kolor_smugi_2(wybor,arg1,r,g,b)
                    IPS.pixel(x   ,y,    kolor)
                    IPS.pixel(x   ,y+1,  kolor)
                else:
                    kolor = st7789.BLACK
                    IPS.pixel(x     ,y,   kolor)
                    IPS.pixel(x     ,y+1, kolor)
                    IPS.pixel(x +1  ,y,   kolor)
        else:                
            for i in dlugosc_lini:  
                x_prim = round(i*a) 
                kolor = st7789.BLACK
                x = x1+x_prim
                y = y1 + i
                IPS.pixel(x     ,y,   kolor)
                IPS.pixel(x     ,y+1, kolor)
                IPS.pixel(x +1  ,y,   kolor)
    @micropython.native
    def draw_line_1and4(self,x1,y1,x2,y2,pozycja_kolor,dlugosc_po_x):
        diff_y = y1 - y2
        if diff_y == 0:
            a = 0
        else:
            a = diff_y/(x1 - x2)

        skala = self.dlugosc_wskaznia/dlugosc_po_x
        dlugosc_lini = range(dlugosc_po_x + 1)
        wybor = self.wybor_motywu_speedo
        r,g,b = Display.kolor_smugi_1(wybor , pozycja_kolor)
        if self.pochodna == True:
            for i in dlugosc_lini:
                arg1 = i * skala      
                y_prim  = round(i*a)
                x_m = x1-i
                y_m = y1 - y_prim 
                x_p = x1+i
                y_p = y1 + y_prim
                if arg1 <= self.dlugosc_smugi:
                    kolor = Display.kolor_smugi_2(wybor,arg1,r,g,b)
                    if x1 <= x2:
                        IPS.pixel(x_p,y_p,   kolor)  # 1 ćwiartka
                        IPS.pixel(x_p,y_p-1, kolor)  
                    else:
                        IPS.pixel(x_m,y_m,   kolor)    # 4 ćwiartka
                        IPS.pixel(x_m,y_m+1, kolor)   
                else:
                    kolor = st7789.BLACK
                    if x1 <= x2 :
                        IPS.pixel(x_p,y_p,   kolor)  # 1 ćwiartka
                        IPS.pixel(x_p,y_p-1, kolor)
                        IPS.pixel(x_p+1,y_p, kolor)
                    else:
                        IPS.pixel(x_m  ,y_m, kolor)  # 4 ćwiartka
                        IPS.pixel(x_m  ,y_m+1,kolor)
                        IPS.pixel(x_m-1,y_m, kolor)
                        
        else:
            for i in dlugosc_lini:   
                y_prim  = round(i*a)
                kolor = st7789.BLACK
                if x1 <= x2 :
                    x = x1+i
                    y = y1 + y_prim
                    IPS.pixel(x,y,   kolor)  # 1 ćwiartka
                    IPS.pixel(x,y-1, kolor)
                    IPS.pixel(x+1,y, kolor)
                else:
                    x = x1-i
                    y = y1 - y_prim
                    IPS.pixel(x  ,y, kolor)  # 4 ćwiartka
                    IPS.pixel(x  ,y+1,kolor)
                    IPS.pixel(x-1,y, kolor)
                    
                    
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
    def motyw_czcionki(self,wybor):
        return {
            0: st7789.BLUE,
            1: st7789.GREEN,
            2: st7789.RED,
            3: st7789.CYAN,
            4: st7789.YELLOW,
            5: st7789.WHITE,
            6: st7789.MAGENTA,
        }.get(wybor, st7789.MAGENTA)
    
    
    ##############################== Kolor po argumencie i po pozycji ==############################################     
    @micropython.native                        
    def kolor_smugi_1(wybor,poz):
        # poz  [0 - 255]  Czyli po pozycj  
        if wybor == 0:   # Turkusowny do magneto - różowego
            RED   = 50 + poz * 8/10
            GREEN = 233 - poz *2/3
            BLUE  = 172  +  poz * 0.3     
        elif wybor == 1: # Z zółtego do czerwonego 
            RED   = 255
            GREEN = 230 -poz * 9/10
            BLUE  = 30 - poz* 0.1
        elif wybor == 2: # Ciemny czerwony do krwistej pomarańczy
            RED   = 100+ poz*6/10
            GREEN = poz*0.3
            BLUE  = 0
        elif wybor == 3: # Cimno niebieski  przez  do szkrałatnego
            RED   = 50 + poz*8/10
            GREEN = 0
            BLUE  = 183 -poz*1/2
        elif wybor == 4: # Jasno zielony 
            RED   = 70 +poz*7/10
            GREEN = 255
            BLUE  = 0
        elif wybor == 5: # Jasno Zielon- żółty   
            RED   = 0+ poz* 1/2
            GREEN = 255 - poz
            BLUE  = 255
        elif wybor == 6: # Turkusowy
            RED   = 0
            GREEN = 255 
            BLUE  = 255
        elif wybor == 7: # Złoty 
            RED   = 244
            GREEN = 196 
            BLUE  = 48 
        return RED,GREEN,BLUE
    
    @micropython.native
    def kolor_smugi_2(wybor, arg, RED, GREEN, BLUE):
        # arg [0 - 36] do fade smugi
        if wybor == 0:   # Turkusowny do magneto - różowego
            fade = 1 - arg /72
            return st7789.color565(int(RED *fade), int(GREEN * fade), int(BLUE * fade))
        elif wybor == 1: # Z zółtego do czerwonego 
            fade = 1 - arg / 60
            return st7789.color565(int(RED * fade), int(GREEN * fade), int(BLUE * fade))
        elif wybor == 2: # Ciemny czerwony do krwistej pomarańczy
            return st7789.color565(int(RED*(1- arg/72))  , int(GREEN*(1- arg/40)),0)
        elif wybor == 3: # Cimno niebieski do szkrałatnego
            fade = 1- arg/50
            return st7789.color565(int(RED * fade), 0, int(BLUE * fade))
        elif wybor == 4: # Jasno zielony 
            fade = 1- arg/60
            return st7789.color565(int(RED*fade)  , int(GREEN*fade), 0)
        elif wybor == 5: # Jasno Zielon- żółty 
            fade = 1 - arg/80
            return st7789.color565(int(RED * fade), int(GREEN * fade), int(BLUE * fade))
        elif wybor == 6: # Turkusowy
            fade = 1- arg/80
            return st7789.color565(0, int(GREEN * fade), int(BLUE * fade))
        elif wybor == 7: # Złoty 
            fade = 1- arg/80
            return st7789.color565(int(RED * fade), int(GREEN * fade), int(BLUE * fade))
############################################################################################################             
    @micropython.native              
    def wskaznik(self,length, radius):
        return [
            (0, 0),
            (-radius, radius),
            (0, length),
            (radius, radius),
            (0,0)
                ]
    @micropython.native 
    def wejscie_speedometer(self,obj_menu):
        if obj_menu.interwal_czas_start_0 == True:       # Czyszczenie dla interwału czasowego 
            IPS.fill_rect(0,0,320,132,st7789.BLACK)
            IPS.fill_rect(0,132,120,108,st7789.BLACK)
            IPS.fill_rect(120,109,30,30, st7789.BLACK)          
            IPS.fill_rect(164,20,156,90,st7789.BLACK)
            IPS.fill_rect(220,115,100,42,st7789.BLACK)
            IPS.fill_rect(120,132,20,5,st7789.BLACK)
        elif  obj_menu.interwal_dystans_start_0 == True:    # Czyszczenie dla interwału dystansowego
            IPS.fill_rect(0,0,320,186,st7789.BLACK)
        else:
            IPS.fill(st7789.BLACK)                          # Standardowe czyszczenie całego ekranu
        self.speed   = 0                                    # Ustawiamy zmienne na defoult aby odpowiednio działało                             
        self.pozycja = -4 
        self.pochodna = True
        self.poprzednia_pochodna = True
        self.prog = 0
        
    @micropython.native 
    def obrecz_speedometer(self,ym,xm,r,odcinek):
        ####### Rysowanie wskaźnika #####
        kolor = self.kolor_obreczy_i_int(self.wybor_motywu_obrecz,0)
        IPS.polygon(self.wskaznik(-self.dlugosc_wskaznia+1 ,1),  xm-r,  ym+2, kolor, math.pi/2 )
        IPS.polygon(self.wskaznik(-self.dlugosc_wskaznia+1 ,1),  xm-r,  ym+3, kolor, math.pi/2 )
        dlugosc = r+4
        for i in range(math.pi*dlugosc):
            i = i - 6
            x = 255*i/(math.pi*dlugosc)
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

        
    @micropython.native            
    def interwal_czas(self,obj_menu,obj_licznik):
        ###=== Część odpowiedzialna czyszczenie danych po cyklu ===###
        
        if obj_menu.czyszczenie == True:
            self.interwal_czas_czyszczenie(obj_menu)
                
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
                
            tekst = str(obj_menu.interwal_czasowy(obj_licznik))
            if tekst == '-1':
                pass
            else:
                IPS.text(font_32,str(obj_menu.interwal_czasowy(obj_licznik)),int(175- a *8 ),174,gold)           
            obj_menu.zmiana_liczb = a
            
        ###=== Część odpowiedzialna za pokazanie grafiki ===###            
        if obj_menu.interwal_czas_start_1 == True:
            self.interwal_czas_grafika(obj_menu,obj_licznik)
                
    @micropython.native 
    def interwal_czas_czyszczenie(self,obj_menu):     
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

    @micropython.native
    def interwal_czas_grafika(self,obj_menu,obj_licznik):
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
                 
        
    @micropython.native          
    def rysowanie_czasu(self,i,kolor):
        x_sin_z =  int(50*math.sin(i/50)) +175
        y_cos_z = -int(50*math.cos(i/50)) + 188
        x_sin_w = x_sin_z - int(14*math.sin(i/50))
        y_cos_w = y_cos_z + int(14*math.cos(i/50))
        #Rysowanie lini pomiędzy 2 obręczami 
        IPS.line(x_sin_z  ,y_cos_z     ,x_sin_w ,  y_cos_w, kolor)
        #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
        IPS.line(x_sin_z , y_cos_z-1  ,x_sin_w , y_cos_w-1, kolor)          

    
    @micropython.native 
    def interwal_dstans(self,obj_menu,obj_licznik):
        ###=== Część odpowiedzialna czyszczenie danych po cyklu ===###
        if obj_menu.czyszczenie == True:
            self.interwal_dstans_czyszczenie(obj_menu)
     
        ###=== Buzzer po przejechaniu cyklu (Zakkończenie i rozpoczecie nowego ===###        
        if obj_menu.flaga_buzzer ==  True and obj_menu.interwal_dystans_start_1 == True:
            obj_menu.buzzer_interwal(2)
            
        ###=== Część odpowiedzialna za pokazanie dystansu ===###
        if obj_menu.interwal_dystans_funkcja(obj_licznik) == -1:
            IPS.fill_rect(111,150,76,34, st7789.BLACK)
        elif obj_menu.interwal_dystans_funkcja(obj_licznik) == -2:
            obj_menu.podsumowanie = True    #Włączamy przycisk
            self.podsumowanie_interwalu(obj_menu,obj_licznik, 2) 
        else:
            
            a = len(str(obj_menu.interwal_dystans_funkcja(obj_licznik)))
            if obj_menu.zmiana_liczb != a:
                IPS.fill_rect(111,150,76,34, st7789.BLACK)
            tekst = str(obj_menu.interwal_dystans_funkcja(obj_licznik))
            if tekst == '-1':
                pass
            else:    
                IPS.text(font_32,tekst,int(149- a *8 ),152,gold)           
                obj_menu.zmiana_liczb = a
            
        ###=== Część odpowiedzialna za pokazanie grafiki ===###            
        if obj_menu.interwal_dystans_start_1 == True:
            self.interwal_dstans_grafika(obj_menu,obj_licznik)
            
            
    @micropython.native 
    def interwal_dstans_czyszczenie(self,obj_menu):
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
            
    @micropython.native
    def interwal_dstans_grafika(self,obj_menu,obj_licznik):
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
                   

    def podsumowanie_interwalu(self,obj_menu,obj_licznik, rodzaj): #interwal jest od rodzaju interwału
        ###== Ta część wykonuje się jednorazowo ==###
        gc.collect()                                  # Just in case 
        obj_menu.deadline_interwal = time.ticks_ms()  # Ustawienie aktualnego czasu do odmierzania buzzera 
        obj_menu.buzzer_interwal(3)                   # Wywołanie buzzera (niech już gra :)
        obj_menu.flaga_buzzer = True                  # Ustawienie flagi na True, aby wykonywała się w While
        obj_menu.zmiana_przycisk = True               # Aby od razu wyświetliły się dane 
        obj_menu.przycisk = obj_menu.przycisk + 1
            ##== Przypisanie zmiennym lokalnym wartości ==##
        kolor_napis = gold
        if rodzaj == 1:
                #= Suma to ilosc przebytej drogi podczas interwału czasowego (w metrach) =#
            suma = sum(obj_menu.przejechany_dystans)*obj_licznik.obwod_kola/1000 
        elif rodzaj ==2:
                #= Suma to czas w jakim przejechane zostały interwały dystansowe (w sekundach) =#
            suma = sum(obj_menu.dlugosc_interwalu)/1000   
        while True:
            # Realizacaj funkcji przyciskow w podsumoaniu 
            if obj_menu.alrm_przycisk_1 == True:
                if time.ticks_diff(time.ticks_ms(), obj_menu.prev_time_butt_1) > 20 and obj_menu.Przycisk_1_Pin.value() == 1:
                    obj_menu.funkcja_przycisku_1()
                    obj_menu.alrm_przycisk_1 = False
                    
            if obj_menu.alrm_przycisk_2 == True :
                if time.ticks_diff(time.ticks_ms(), obj_menu.prev_time_butt_2) > 20 and obj_menu.Przycisk_2_Pin.value() == 1:
                    obj_menu.funkcja_przycisku_2()
                    obj_menu.alrm_przycisk_2 = False         
            
            ##== Buzzer na zakończenie interwału ==##
            if obj_menu.flaga_buzzer == True:
                obj_menu.buzzer_interwal(3)              
            ##== Warunek wyjścia z while  ==##
            if any(obj_menu.przytrzymanie_przycisku(x,500) for x in [1,2,3]):          
                obj_menu.reset_interwalu()     # Resetujemy dane z interwału 
                obj_menu.wyjscie_z_menu()      # Resetujemy dane z menu ( just in case,  i na pewno wracamy do głównego wyświetlania)
                self.wejscie = True            # Ustawiamy flagę wejścia na True 
                break
            ##== Pokazanie danych ==##
            else:        
                #== Rysujemy tylko, gdy przycisk został naciśnięty ==#
                if obj_menu.zmiana_przycisk == True:
                    total_kontury = False  
                    IPS.fill(st7789.BLACK)
                    if obj_menu.podsumowanie_interwalu_przycisk >= obj_menu.ilosc_cykli - 3:  # Na samym dole jest podsumowanie 
                        if rodzaj == 1: # Interwał czasowy '
                            IPS.text(font_32,'Total '+ str(round(suma))+ '   ' + str(round(suma*3.6/(obj_menu.interwal_czas*obj_menu.ilosc_cykli),1)) ,
                                  0,204 ,kolor_napis)
                        elif rodzaj == 2: # Interwał dystansowy
                            IPS.text(font_32,'Total '+ str(round(suma))+ 's  ' + str(round(obj_menu.ilosc_cykli*obj_menu.interwal_dystans*3.6/suma,1)) ,
                                  0,204 ,kolor_napis)
                        total_kontury = True          
                    ###=== Rysowanie konturów interwału ===###
                    self.konutry_intrwal(st7789.color565(150,110,71),obj_menu,total_kontury)     
                    ###=== Wyświetlanie podstawowych statystyk ===###
                    self.nanoszenie_info_interwal(kolor_napis,obj_menu,rodzaj)
                    ###=== Wyświetlanie głównych statystyk ===###
                    self.nanoszenie_glowne_info_interwal(kolor_napis,obj_menu,rodzaj,obj_licznik)
                    obj_menu.zmiana_przycisk = False
                    gc.collect()
                    
                else:
                    pass


    def konutry_intrwal( self, kolor,obj_menu,total_kontury):         
        if obj_menu.podsumowanie_interwalu_przycisk == 0 and total_kontury == False:
            IPS.vline(40, 40, 200, kolor)
            IPS.vline(170, 40, 200, kolor)
        elif obj_menu.podsumowanie_interwalu_przycisk == 0 and total_kontury == True:
            IPS.vline(40, 40, 160, kolor)
            IPS.vline(170, 40, 160, kolor)
        elif total_kontury:
            IPS.vline(40, 0, 200, kolor)
            IPS.vline(170, 0, 200, kolor)     
        else:
            IPS.vline(40, 0, 240, kolor)
            IPS.vline(170, 0, 240, kolor)
          
        IPS.hline(0, 40, 320, kolor)
        IPS.hline(0, 80, 320, kolor)
        IPS.hline(0, 120, 320, kolor)
        IPS.hline(0, 160, 320, kolor)
        IPS.hline(0, 200, 320, kolor)
    

    def nanoszenie_info_interwal(self, kolor_napis,obj_menu,rodzaj):
        prog_2 = 44-(obj_menu.podsumowanie_interwalu_przycisk *40)
        if rodzaj == 1: # Interwał czasowy
            if obj_menu.podsumowanie_interwalu_przycisk == 0:
                IPS.text(font_32,'Czas: ' + str(obj_menu.interwal_czas),0,4,kolor_napis)
                IPS.text(font_32,'Pauza: ' + str(obj_menu.interwal_pause),160,4,kolor_napis)                                         
            if any(obj_menu.podsumowanie_interwalu_przycisk == x for x in [0,1]):
                IPS.text(font_32,'Nr',        4   ,prog_2   ,kolor_napis)
                IPS.text(font_32,'Dys[m]',    60  ,prog_2   ,kolor_napis)
                IPS.text(font_32,'Avg Km/h', 180  ,prog_2   ,kolor_napis)                        
    
        elif rodzaj ==2: #Interwał dystansowy
            if obj_menu.podsumowanie_interwalu_przycisk == 0:
                IPS.text(font_32,'Dys: ' + str(obj_menu.interwal_dystans),0,4            ,kolor_napis)
                IPS.text(font_32,'Pauza: ' + str(obj_menu.interwal_dystans_pause),160,4  ,kolor_napis)
            if any(obj_menu.podsumowanie_interwalu_przycisk == x for x in [0,1]):
                IPS.text(font_32,'Nr',        4   ,prog_2   ,kolor_napis)
                IPS.text(font_32,'Czas[s]',   52  ,prog_2   ,kolor_napis)
                IPS.text(font_32,'Avg Km/h', 180  ,prog_2   ,kolor_napis)
                
    def nanoszenie_glowne_info_interwal(self, kolor_napis,obj_menu,rodzaj,obj_licznik):
        przesuniecie = 40
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

                     

    