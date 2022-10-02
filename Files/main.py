from machine import Pin, Timer, I2C, lightsleep, PWM
from micropython import const
import time, math, sys , gc
sys.path.insert(0, '/Libraries/Gyroscope')
sys.path.insert(0, '/Functions')
from imu import MPU6050
from Licznik_main import Licznik_main
from Menu import Menu 
from Screen import Display
from Screen_menu import Display_menu

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)   # Towrzenie obietki I2C
imu = MPU6050(i2c)                                  # Towrzenie obietki IMU
delta = 0         # Do liczenia czasu ( do wywalenia)
start = 0         # Do liczenia czasu ( do wywalenia)


#####========= Przypisanie wartosci do obiektu klasy'Licznik' ===============#####
Licznik = Licznik_main()         # tworzenie obiektu klasy 'Licznik'

        ########## Zmienne do prawidłowego działania licznika ##########
Licznik.current_speed = 0        # Aktualna prędkość
Licznik.obwod_kola = const(2155) # Dla obręczy 27.5 cala [mm] funkcja const() w celu optymalizacji 
Licznik.ay_kat = 0               # Kąt nachylenia
Licznik.ay = 0                   # obj_zmienne do której zosataje przypisywana wartość sinusa kąta nachylenia
Licznik.ilosc_impulsow = 2       # obj_zmienne która determinuje w zależności od ostatniej prędkości chwilowej ile należy zliczyć impulsów aby wyświetlenie kolejnej wartości mieściło się w granicach czasowych 
Licznik.zmienne_modulo = 0       # Dodatkowa obj_zmienne potrzeba do zliczania pełnych obortów koła służąca do wyliczania wartości bezwzględnej ze zmiennej "obj_zmienne.ilosc_impulsow"
Licznik.time_beetwen = 0         # Czas pomiędzy osatnim dczytem prędkości chwilowej
Licznik.finish = 0               # Czas po jakim zostały zliczone pełne obroty koła
Licznik.Odliczanie_impulsow =0   # Wynik operacji modulo potrzebny do wyliczenia prędkości chwilowej
Licznik.flaga = False            # Zmienna potrzeba do wykrycia stanu, że w ciągu 3 sekund nie zostały zliczone wszystkie impulsy

Licznik.licznikPin = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP) #Zestyk kontraktonu do zliczania obrotów z koła 

        ########## Zmienne do wyswietlania danch ##########
Licznik.counter = 0              # Zliczanie wszystkich impulsów z koła
Licznik.v_max = 0                # Maksymalna prędkość chwilowa całości 
Licznik.przeywzszenia = 0        # Wartość_przewyższenia
Licznik.rtc_czas_total = [0,0,0,0]     # Tablica Dni/Godzin/Minut/Sekund total czasu
Licznik.v_srednie = 0

Licznik.counter_podroz = 0
Licznik.v_max_podroz = 0
Licznik.przeywzszenia_podroz = 0
Licznik.rtc_czas_podroz  = [0,0,0,0]
        ########## Zmienne do liczenia czasu ##########
Licznik.rtc = machine.RTC()                        # Tworzenie obkeitu RTC 
Licznik.rtc.datetime((2020, 7, 1, 2, 0, 0, 40, 0)) # Przypisanie mu czasu na 1 lipca 2020r
Licznik.flaga_czas = False                         # Zmienna mówiąca, kiedy liczyć a kiedy nie liczyć czasu
Licznik.wrzesien = False                           # Zmienna z czytej fanaberii 

#####========= Przypisanie wartosci do obiektu klasy 'Menu' ===============#####
Obj_Menu = Menu()            #Create an object of class 'Menu'

        ########## Przyciski do zarządzaniem menu i zmianą obrazu na wyświeltaczu [1/2]
Obj_Menu.Przycisk_1_Pin = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP) 
Obj_Menu.Przycisk_2_Pin = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

Obj_Menu.interaction_przycisk = 0                # Ustawienie aktualnego czasu po kliknięcu przycisku
Obj_Menu.time_beetwen_interaction_przycisk = 0   # Odliczanie czasu od klikniecia przycisku 
        ########## Zmienna potrzebna do prawidłowego działa funkcji przytrzmania przycisków [1/2]
Obj_Menu.Flaga_przycisk_lewy = False  
Obj_Menu.Flaga_przycisk_prawy = False 

Obj_Menu.przycisk = 0                  # Zmienna do zmiany obrazu wyświetlacza
Obj_Menu.warunek_ktory_wyswietlacz = 0 # Wybór podstawowoego wyświetlania 

        ########## Zmienne do prawidłowego działania funkcji przytrzymania przycisków ##########
Obj_Menu.ustawienie_czasu = 0          # Zmienna odliczająca czas od przytrzymania przycisku w menu 
Obj_Menu.nr_przycisku = 0              # Przypisanie który przycisk został przyciśnięty  
Obj_Menu.funkcja_przycisk = 0          # Ustawienie możliwości resetu czasu tylko tą funkcją

        ########## Zmienne do działania Menu ##########
Obj_Menu.menu = False                        # Zmienna decydująca czy jest się w menu
Obj_Menu.warunek_ktory_wyswietlacz_menu = 0  # Wybór wyświetlania w menu 1 rzędu
Obj_Menu.ilosc_wyborow_w_menu = 0            # Przypisanie ile będzie dostępnych wyborów w następnym progu menu
Obj_Menu.wybor_w_menu = 0                    # Wybranie jednego z dostępnych wyborów 

Obj_Menu.flaga_1_prog_menu = False           # Wykrywanie w którym progu menu jesteśmy 
Obj_Menu.flaga_2_prog_menu = False
Obj_Menu.flaga_3_prog_menu = False           # Dotyczny tylko interwałów 


        ########## Wspólne zmienne do interwałów ##########
Obj_Menu.zmiana_liczb = 0                    # Wykrycie zmiany długości wyświetlanych danych i wyczyszczenie jednorazowo ekranu wyświetlania danych  
Obj_Menu.czyszczenie = True                  # Czyszczenie grafiki po przejechanym cyklu 
Obj_Menu.cykle       = 0                     # Odmierznie "pół cykli" ( Czyli i jazdy i pzerwy)
Obj_Menu.Odmierzanie_grafiki = 0             # Zmienna potrzeban do odmierzania postepu w interwale           
Obj_Menu.flaga_buzzer = False                # Wywołanie funkcji buzzera 
Obj_Menu.dodatkowe_czyszczenie = False       # Wykrycie warunku, że interwał się jeszcze nie zaczał a weszliśmy do menu 
Obj_Menu.podsumowanie_interwalu_przycisk = 0 # Zmienna do pzycisku od menu podsumowania interwałów 
Obj_Menu.podsumowanie = False                # Wykrycie wejścia w podsumowanie   
Obj_Menu.pwm15 = PWM(Pin(15))                # Stworzenie obiektu PWM pod pinem nr 15 
Obj_Menu.pwm15.freq(2000)                    # Ustalenie częstoliwości PWM 
Obj_Menu.mruganie_liczb_interwal = False     # Zmienna od mrugania liczb przed rozpoczeciem interwału 
Obj_Menu.deadline_interwal = 0               # Odmierzanie czasu działania buzzera 
Obj_Menu.ilosc_cykli = 4                     # Ilość cykli interwału
Obj_Menu.wybor_w_menu_interwal = 0           # Poruszanie się po menu 3 progu 
Obj_Menu.wlasny_interwal = False             # Rodzaj wybranego interwału [Gotowy/Własny]
Obj_Menu.ustawienie_danych = False           # Zmienna do istaiwnia danych w interwale 

        ########## Zmienne do Interwału Czasowego ########## 
Obj_Menu.interwal_czas = 30
Obj_Menu.interwal_pause = 60
Obj_Menu.interwal_czas_start_0 = False       # Ustawienie interwału 
Obj_Menu.interwal_czas_start_1 = False       # Rozpoczecie interwału 
Obj_Menu.przejechany_dystans = []            # Tablica która przechowuje przejechany dystans w interwale 
Obj_Menu.odliczanie = 0


        ########## Zmienne do Interwału Dystansowego ########## 
Obj_Menu.interwal_dystans = 700       
Obj_Menu.interwal_dystans_pause = 500
Obj_Menu.interwal_dystans_start_0 = False    # Ustawienie interwału 
Obj_Menu.interwal_dystans_start_1 = False    # Rozpoczecie interwału 
Obj_Menu.dlugosc_interwalu = []              # Tablica która przechowuje czas interwału

#####========= Przypisanie wartosci do obiektu klasy 'Display' ===============#####

Obj_Display = Display()  #Kiedyś was opisze ;P 
Obj_Display.zmiana_przycisk = True
Obj_Display.wyswietlana_predkosc = 0
Obj_Display.zmiana_czasu = 0

##### Do speedometera
Obj_Display.wyswietlana_predkosc_speedometer = 0
Obj_Display.wejscie = True
Obj_Display.speed = 0
Obj_Display.polowka = 0
Obj_Display.prog = 0
Obj_Display.bramka_speedometer_plus = True
Obj_Display.bramka_speedometer_minus = True 
##### Do menu 
Obj_Display.poprzedni_wybor = 0
Obj_Display.wejscie_do_menu = False
Obj_Display.wymazanie_prostokata = True
Obj_Display.mruganie_liczb = False
Obj_Display.deadline = 0 
Obj_Display.pochodna = True
Obj_Display.poprzednia_pochodna = True
Obj_Display.x_prim = 0
Obj_Display.y_prim = 0
Obj_Display.przedluzenie_wykresu = False

#####======================== Zmienne Globalne =====================================#####

proporcja = 0       #moze do wyciepania   #Współczynnik pomiędzy 0-1 który poprawia jakość prędkości chwilowej podczas "sytuacji awaryjnej"
Flaga_start = True                       #Zmienna realizujaca funkcję startową
spac = False                             #Zmienna deklarująca, że warunek pójścia spać został zrealizowany 

Pin16_state,Pin17_state,Pin18_state  = 0,0,0  #Zmienne potrzebna do rozwiązania problemu drgania styków

#################################### FUNKCJE PRZERWANIA ##########################################################################################

def Przycisk_1(pin):#[LEWY/ ZIELONY] Funkcja realizująca przerwanie przycisku od zmiany wyświetlacza [1]
    global  Pin16_state , flaga_sen_stop, spac
    if (Obj_Menu.Przycisk_1_Pin.value() == 1) and (Pin16_state == 0 ):
        Pin16_state = 1
        

        
        ##===== Wykrycie kliknięcia przycisku ========##
            #=== Warunek, aby wyczyścić odpowiednią część na wyświetlaczu ==============#
        if Obj_Display.zmiana_przycisk == False:
            Obj_Display.zmiana_przycisk = True
            #=== Warunek, aby po przytrzymaniu przycisku nie nastąpiła żadna operacja ==#  
        if Obj_Menu.Flaga_przycisk_lewy == True:
            Obj_Menu.Flaga_przycisk_lewy = False
            
            #=== standarodowy warunk dzialania przycisku gdy nie jest w menu ============#    
        elif Obj_Menu.menu == False: #
            Obj_Menu.przycisk += 1
            Obj_Menu.warunek_ktory_wyswietlacz = Obj_Menu.przycisk % 5 + 1
            
            #======== Wybór w menu 1 progu ======# 
        elif  Obj_Menu.flaga_1_prog_menu == True: 
            Obj_Menu.przycisk += 1
            Obj_Menu.wybor_w_menu = Obj_Menu.przycisk % Obj_Menu.ilosc_wyborow_w_menu 
            
            #======== Wybór w menu 2 progu ======# 
        elif  Obj_Menu.flaga_2_prog_menu == True: 
            Obj_Menu.przycisk += 1
            Obj_Menu.wybor_w_menu = Obj_Menu.przycisk % Obj_Menu.ilosc_wyborow_w_menu
            
            #======== Wybór w menu 3 progu ======# 
        elif  Obj_Menu.flaga_3_prog_menu == True: #Dotyczy tylko interwałów
            Obj_Menu.interwal_dane(Obj_Menu.add)
            
            
        if Obj_Menu.podsumowanie == True and Obj_Menu.ilosc_cykli >3 : 
            Obj_Menu.podsumowanie_interwalu_przycisk =  Obj_Menu.przycisk % (Obj_Menu.ilosc_cykli - 2) #Bo operacja modulo, czyli 1 mniej niż logika podpowiada 
             
        Obj_Menu.interaction_przycisk = time.ticks_ms() # przypisanie aktualnego czasu po kliknięciu        
        ##===== Wybudzenie ze snu ========##       
        if spac == True :
            flaga_sen_stop = False
            print("Wybudzenie ze snu!")
        #==================================#            
        
    elif (Obj_Menu.Przycisk_1_Pin.value() == 0) and (Pin16_state == 1 ):
        Pin16_state = 0
        
    Obj_Menu.Przycisk_1_Pin.irq(handler=Przycisk_1)    

 
def Przycisk_2(pin):# [PRAWY/ CZERWONY]Funkcja realizująca przerwanie przycisku od zmiany wyświetlacza [2]
    global Pin18_state, spac,  flaga_sen_stop     
    if (Obj_Menu.Przycisk_2_Pin.value() == 1) and (Pin18_state == 0 ):
        Pin18_state = 1
        

        
       ##===== Wykrycie kliknięcia przycisku ========##
            #=== Warunek, aby wyczyścić odpowiednią część na wyświetlaczu ==============#
        if Obj_Display.zmiana_przycisk == False:
            Obj_Display.zmiana_przycisk = True              
            #=== Warunek, aby po przytrzymaniu przycisku nie nastąpiła żadna operacja ==#     
        if Obj_Menu.Flaga_przycisk_prawy == True: 
            Obj_Menu.Flaga_przycisk_prawy = False
            
            #=== standarodowy warunk dzialania przycisku gdy nie jest w menu #       
        elif Obj_Menu.menu == False:
            Obj_Menu.przycisk -= 1
                #Jeżeli nie jest w menu, wyświetla jedną z 4 funkcji 
            Obj_Menu.warunek_ktory_wyswietlacz = Obj_Menu.przycisk % 5 + 1 
                
            #======== Wybór w menu 1 progu ======# 
        elif  Obj_Menu.flaga_1_prog_menu == True: 
            Obj_Menu.przycisk -= 1
            Obj_Menu.wybor_w_menu = Obj_Menu.przycisk % Obj_Menu.ilosc_wyborow_w_menu 
            
            #======== Wybór w menu 2 progu ======# 
        elif  Obj_Menu.flaga_2_prog_menu == True: 
            Obj_Menu.przycisk -= 1
            Obj_Menu.wybor_w_menu = Obj_Menu.przycisk % Obj_Menu.ilosc_wyborow_w_menu       
            #======== Wybór w menu 3 progu ======# 
        elif  Obj_Menu.flaga_3_prog_menu == True: 
            Obj_Menu.interwal_dane(Obj_Menu.sub)
            
        if Obj_Menu.podsumowanie == True and Obj_Menu.ilosc_cykli >3 : 
            Obj_Menu.podsumowanie_interwalu_przycisk =  Obj_Menu.przycisk % (Obj_Menu.ilosc_cykli - 2)#Bo operacja modulo, czyli 1 mniej niż logika podpowiada 
            
        Obj_Menu.interaction_przycisk = time.ticks_ms()   # przypisanie aktualnego czasu po kliknięciu przycisku
        ##===== Wybudzenie ze snu ========##
        if spac == True : 
            flaga_sen_stop = False
            print("Wybudzenie ze snu!")
        #==================================#
          
    elif (Obj_Menu.Przycisk_2_Pin.value() == 0) and (Pin18_state == 1 ):
        Pin18_state = 0
        
    Obj_Menu.Przycisk_2_Pin.irq(handler=Przycisk_2)
    
             


def Obroty_kola(pin):   #Funkcja realizująca przerwanie obrotów koła 
    global  delta , start ,Pin17_state, spac, proporcja , flaga_sen_stop
    if (Licznik.licznikPin.value() == 1) and (Pin17_state == 0 ):      
        Pin17_state = 1
        Licznik.counter += 1
        Licznik.counter_podroz += 1
#============================ Odzytanie wartości sinusa kąta nachylenia =======================================#
        Licznik.ay =  round(imu.accel.y,3)
        gy = round(imu.gyro.y,3) # Przeciążenie? 
        
        if Licznik.ay>=1:
            Licznik.ay = 1
            
        Licznik.ay_kat = 180* math.asin(Licznik.ay)/math.pi       
        #Zapisywanie każdego pomiaru z żyroskopu i akcelerometru  do pliku
        #dodaj tutaj funkcje jak chcesz szybciej ! 
#         miara_katow = open("dane_z_zyroskopu_3.txt" ,"a")
#         dane_gyro_str = str(gy)
#         dane_zyro_str = str(Licznik.ay_kat)
#         dane_curret_speed = str(Licznik.current_speed)
#         text = dane_zyro_str  + "   " + dane_gyro_str + "   " + dane_curret_speed
#         miara_katow.write(text + '\n')
#         miara_katow.close()              
        # AY to wartość sinusa kąta (prototyp mierzenia przerwyższenia)
        if Licznik.ay > 0:           
            Licznik.przeywzszenia += Licznik.ay * Licznik.obwod_kola/ 1000        
            Licznik.przeywzszenia_podroz += Licznik.ay * Licznik.obwod_kola/ 1000 
#============================================= KONIEC Sinusa ========================================================#        
        
        
        if Licznik.flaga_czas == False:
            Licznik.flaga_czas = True
            Licznik.rtc_tablica_start = Licznik.rtc.datetime() #przypisanie czasu'startu' do zmiennej 
            
       
        ## Warunek gdy przez ponad 3 sekundy nie została zmieniona prędkość chwilowa ##        
        if Licznik.flaga == True and Licznik.current_speed != 0:
            
            okres_obortu = (Licznik.obwod_kola*3.6)/Licznik.current_speed            
            proporcja = Licznik.time_beetwen /okres_obortu
            if proporcja >= 1:
                proporcja = 1
                       
        Licznik.zmienne_modulo += 1
        Licznik.Odliczanie_impulsow = Licznik.zmienne_modulo % Licznik.ilosc_impulsow         
        if Licznik.Odliczanie_impulsow == 0:

            Licznik.time_beetwen  = time.ticks_diff(time.ticks_ms() ,Licznik.finish)
            Licznik.finish = time.ticks_ms() #Starsza wartość czasu po zliczeniu impulsów

            
            # standardowy warunek wyliczania prędkości chwilowej          
            if Licznik.flaga  == False:
                Licznik.current_speed = Licznik.ilosc_impulsow *3.6*Licznik.obwod_kola/Licznik.time_beetwen  #  3.6  (m/s => km/h)
                Licznik.flaga_zapis = True
            # warunek wyliczania prędkości chwilowej gdy prędzej w ciągu 3 sekund nie zostały zliczone wszystkie impulsy     
            elif Licznik.flaga  == True: 
                Licznik.current_speed =(Licznik.ilosc_impulsow + proporcja -1 )*Licznik.obwod_kola*3.6/Licznik.time_beetwen  #3.6  (m/s => km/h)
                Licznik.flaga  = False              
                proporcja = 0
                
            #Zależności dla porządanej ilości impiulsów od prędkości chwilowej
            start = time.ticks_us() # get millisecond counter
            Licznik.zaleznosci(start)           
            if Licznik.current_speed > Licznik.v_max : # Przypisanie maksymalnej prędkośći chwilowej [Total]
                Licznik.v_max  = Licznik.current_speed
            if Licznik.current_speed > Licznik.v_max_podroz :  # Przypisanie maksymalnej prędkośći chwilowej [Podroz]
                Licznik.v_max_podroz  = Licznik.current_speed
                
                
            if spac == True :
                flaga_sen_stop = False
                print("Wybudzenie ze snu!")
                
 
    # dalsza część funkcji realizująca przerwanie odpowiedzialna za eliminację dragń styków     
    elif (Licznik.licznikPin.value() == 0) and (Pin17_state == 1 ):
        Pin17_state = 0
        
    Licznik.licznikPin.irq(handler=Obroty_kola)

 
Licznik.licznikPin.irq(trigger = Pin.IRQ_FALLING, handler = Obroty_kola)  #Wywołwanie funkcji przerwania do zliczania obrotów koła
Obj_Menu.Przycisk_1_Pin.irq(trigger = Pin.IRQ_FALLING, handler = Przycisk_1)  #Wywołwanie funkcji przerwania przycisku od wyświetlacza  [1]
Obj_Menu.Przycisk_2_Pin.irq(trigger = Pin.IRQ_FALLING, handler = Przycisk_2)  #Wywołwanie funkcji przerwania przycisku od wyświetlacza  [2]
#################################### KONIEC funckji Przerwania ####################################################
 
import os

def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

def free(full=False):
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

i = 0
 
if __name__=='__main__':   
    while True:
               
###============ Funkcja Startowa ======================================================####  
        if Flaga_start == True :
            Licznik.odczyt_z_plikow_podroz_i_total()
            Obj_Display.funkcja_startowa()
            Licznik.finish = time.ticks_ms()           
            Obj_Menu.warunek_ktory_wyswietlacz = 0
            Flaga_start = False

        ##====== Odliczanie czasu ================================##
        Licznik.time_beetwen  = time.ticks_diff(time.ticks_ms() ,Licznik.finish)  
        Obj_Menu.time_beetwen_interaction_przycisk = time.ticks_diff(time.ticks_ms(),Obj_Menu.interaction_przycisk) # Czas od ostaniego kliknięcia przycisku 
####============ Prędkość Chwilowa ======================================================#### 
        ##====== Realizacja przypadków gdy time_beetwen większy od 3s ===========##      
        if Licznik.time_beetwen  > 3_000 and Licznik.Odliczanie_impulsow > 0:
            Licznik.over_3s_and_speed_non_0()
            
        elif Licznik.time_beetwen  > 3_000 and Licznik.Odliczanie_impulsow == 0: # osobny if, po to, żeby 'time_beetwen' był większy niż 3s, czyli pierwszy impuls z koła nie dał dużej prędkości chwilowej
            Licznik.over_3s_and_speed_0()
            if Licznik.flaga_czas == True :                 
                Licznik.rtc_czas()
                Licznik.zapis_do_pliku_total()
                Licznik.zapis_do_pliku_podroz()                
                Licznik.flaga_czas = False
                gc.collect() #just in case

####============ Wyświetlacz ============================================================####
        ##====== Podstawowe wyswietlanie ================================##
        if Obj_Menu.menu == False:
            Obj_Display.screen(Obj_Menu,Licznik)
            
            #======== Wejście do Menu ===================#
            if Obj_Menu.przytrzymanie_przycisku(3,2000) == 3:
                Menu.wejscie_do_Menu(Obj_Menu,Obj_Display)
                
            #======== Wrócenie do głównej funkcji =======#                         
            elif Obj_Menu.time_beetwen_interaction_przycisk > 8000:
                Obj_Menu.warunek_ktory_wyswietlacz = 0 
                Obj_Menu.przycisk = 0  #przypisanie zmienne przycisk wartości 0, aby program działał prawidłowo (modulo)  
               
        
        ##====== Wejście do menu ================================##
        elif Obj_Menu.menu == True:
            Display_menu.menu(Obj_Display,Obj_Menu,Licznik)
    
            #======== Wybór w menu 1 progu ======#             
            if Obj_Menu.flaga_1_prog_menu == True and Obj_Menu.przytrzymanie_przycisku(2,1500) == 2:
                Menu.wybor_opcji_w_menu_1_prog(Obj_Menu,Obj_Display)
    
            #======== Wybór w menu 2 progu ======#  
            elif Obj_Menu.flaga_2_prog_menu == True and Obj_Menu.przytrzymanie_przycisku(2,1200) == 2:
                Menu.wybor_opcji_w_menu_2_prog(Obj_Menu, Licznik,Obj_Display)
                
            #======== Wybór w menu 3 progu ======#
            elif Obj_Menu.flaga_3_prog_menu == True:
                if Obj_Menu.przytrzymanie_przycisku(2,800) == 2:                
                    Menu.wybor_opcji_w_menu_3_prog(Obj_Menu, Licznik)
                    Obj_Display.zmiana_przycisk = True
                    
                if Obj_Menu.przytrzymanie_przycisku(1,1250) == 1:
                    Menu.Ustawienie_interwalu(Obj_Menu, Licznik)     
            #======== Wyjście z Menu ===================#            
            elif Obj_Menu.time_beetwen_interaction_przycisk > 15_000 :
                Menu.wyjscie_z_menu(Obj_Menu)
                Obj_Menu.interaction_przycisk = time.ticks_ms() # przypisanie czasu po powrocie z menu do głównego wyświetlania       
            

###============ Sleep Mode ==============================================================####
            #(tutaj jest duzo nie optymalnie, ale na razie dziala)#
        ##======  Pójście spać jeżeli od ostatniej interakcji mineło więcej niż 15s ===##        
        if Licznik.time_beetwen > 243_000  and Obj_Menu.time_beetwen_interaction_przycisk > 20_000:
            print("Spac!")
            #Dodaj, że jak jest interwał na TRUE to go wyłącza 
            spac = True # Zmienna mówiąca, że jest się w fazie snu 
            Licznik.zapis_do_pliku_total()
            Licznik.zapis_do_pliku_podroz()
            Menu.wyjscie_z_menu(Obj_Menu)
            Obj_Display.funkcja_sleep()
            flaga_sen_stop = True   
            # wyłączyć wyświetlacz ( RS albo tranzystro na 3v3 Out)
            #deep sleep aż do wybudzenia (kappa), bo jest light sleep)
            while flaga_sen_stop == True: # Wejście w pętle snu az do momentu "wybudzenia" ;D 
                lightsleep(1500) 
               
            spac = False # Wyjście z fazny snu i przypisanie wartości False 
            Flaga_start = True # Włączenie funkcji startowej po wyjściu ze snu 
         
########################################### KONIEC ############################################################
