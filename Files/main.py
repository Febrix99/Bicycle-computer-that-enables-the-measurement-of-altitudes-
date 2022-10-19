from machine import Pin, Timer, lightsleep, PWM
import  micropython
from micropython import const           # Importowanie const
import time, math, sys , gc
sys.path.insert(0, '/Functions')        # Dostęp do widoczności plików 
from Licznik_main import Licznik_main   # Importowanie klas 
from Menu import Menu 
from Screen import Display
from Screen_menu import Display_menu
start = 0

#####========= Przypisanie wartosci do obiektu klasy'Licznik' ===============#####
Licznik = Licznik_main()         # Tworzenie obiektu klasy 'Licznik_main'
        ########## Zmienne do prawidłowego działania licznika ##########
Licznik.current_speed = 0        # Aktualna prędkość
Licznik.obwod_kola = const(2155) # Dla obręczy 27.5 cala [mm] funkcja const() w celu optymalizacji    
Licznik.ilosc_impulsow = 2       # obj_zmienne która determinuje w zależności od ostatniej prędkości chwilowej ile należy zliczyć impulsów aby wyświetlenie kolejnej wartości mieściło się w granicach czasowych 
Licznik.zmienne_modulo = 0       # Dodatkowa obj_zmienne potrzeba do zliczania pełnych obortów koła służąca do wyliczania wartości bezwzględnej ze zmiennej "obj_zmienne.ilosc_impulsow"
Licznik.time_beetwen = 0         # Czas pomiędzy osatnim dczytem prędkości chwilowej
Licznik.finish = 0               # Czas po jakim zostały zliczone pełne obroty koła
Licznik.Odliczanie_impulsow =0   # Wynik operacji modulo potrzebny do wyliczenia prędkości chwilowej
Licznik.flaga = False            # Zmienna potrzeba do wykrycia stanu, że w ciągu 3 sekund nie zostały zliczone wszystkie impulsy
Licznik.flaga_1 = False          # Flaga drugiego stopania informująca o tym, że w ciągu 3 sekund nie zostały zliczone wszystkie impulsy
Licznik.proporcja = 0            # Zmienna do precyzyjniejszego wyliczania prędkości aktualnej podczas sytuacji 'awaryjnej'
Licznik.spac = False             # Zmienna deklarująca, że warunek pójścia spać został zrealizowany
Licznik.flaga_sen_stop = False   # Zmienna aktywna w trakcie snu (dezaktywacja poprzez interakcję z funckją przerwania)
Licznik.licznikPin = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP) #Zestyk kontraktonu do zliczania obrotów z koła0
Licznik.Pin17_state = 0          # Zmienna do debouncingu
Licznik.tablica_sin = [0,0,0,0,0,0,0,0,0,0]     # Tablica do pracy z katami
Licznik.tablica_g_force = [0,0,0,0,0,0,0,0,0,0] # Tablica do pracy z przeciazeniami
Licznik.odliczanie = 0
        ########## Zmienne do liczenia kadencji  ##########
Licznik.CadencePin = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)  #Zestyk kontraktonu do zliczania kadencji jazdy
Licznik.current_cadence = 0      # Aktualna kadencja 
Licznik.Pin8_state = 0           # Zmienna do debouncingu 
Licznik.cadence_odliczanie = 0   # Zmienna odliczająca wymaganą ilość obortów kroby 
Licznik.finish_cadence = 0       # Zmienna przechowująca aktualny czas po zliczeniu wymaganych obrotów koła 
Licznik.modulo_cadence = 2       # Zmienna deklarująca wymaganą ilość obortów

        ########## Zmienne do wyswietlania danch ##########
Licznik.counter = 0                    # Zliczanie wszystkich impulsów z koła
Licznik.v_max = 0                      # Maksymalna prędkość chwilowa całości 
Licznik.przeywzszenia = 0              # Wartość_przewyższenia
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
Obj_Menu = Menu()            # Create an object of class 'Menu'

        ########## Przyciski do zarządzaniem menu i zmianą obrazu na wyświeltaczu [1/2]
Obj_Menu.Przycisk_1_Pin = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP) 
Obj_Menu.Przycisk_2_Pin = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
Obj_Menu.Pin16_state, Obj_Menu.Pin18_state = 0, 0 # Zmienne do debouncingu styków 
Obj_Menu.interaction_przycisk = 0                 # Ustawienie aktualnego czasu po kliknięcu przycisku
Obj_Menu.time_beetwen_interaction_przycisk = 0    # Odliczanie czasu od klikniecia przycisku 
        ########## Zmienna potrzebna do prawidłowego działa funkcji przytrzmania przycisków [1/2]
Obj_Menu.Flaga_przycisk_lewy = False  
Obj_Menu.Flaga_przycisk_prawy = False 

Obj_Menu.przycisk = 0                  # Zmienna do zmiany obrazu wyświetlacza
Obj_Menu.warunek_ktory_wyswietlacz = 0 # Wybór podstawowoego wyświetlania 
Obj_Menu.flaga_sen_stop_menu = False
Obj_Menu.spac_menu = False                 
        ########## Zmienne do prawidłowego działania funkcji przytrzymania przycisków ##########
Obj_Menu.ustawienie_czasu = 0          # Zmienna odliczająca czas od przytrzymania przycisku w menu 
Obj_Menu.nr_przycisku = 0              # Przypisanie który przycisk został przyciśnięty  
Obj_Menu.funkcja_przycisk = 0          # Ustawienie możliwości resetu czasu tylko tą funkcją

        ########## Zmienne do działania Menu ##########
Obj_Menu.zmiana_przycisk = True
Obj_Menu.menu = False                        # Zmienna decydująca czy jest się w menu
Obj_Menu.warunek_ktory_wyswietlacz_menu = 0  # Wybór wyświetlania w menu 1 rzędu
Obj_Menu.ilosc_wyborow_w_menu = 0            # Przypisanie ile będzie dostępnych wyborów w następnym progu menu
Obj_Menu.wybor_w_menu = 0                    # Wybranie jednego z dostępnych wyborów 
Obj_Menu.wybor_ktory_motyw = 0

Obj_Menu.flaga_motywy_menu   = False
Obj_Menu.flaga_motywy_menu_1 = False

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
Obj_Menu.interwal_czas_start_0 = True       # Ustawienie interwału 
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

Obj_Display = Display()                   # Create an object of class 'Display'
Obj_Display.zmiana_czasu = 0              # Wykrycie zmiany pokazywanego czasu aby odświeżyć monitor 
Obj_Display.wyswietlana_predkosc = 0.001  # Zminne przechowywujące poprzednie wartości prędkość i kadencji    
Obj_Display.wyswietlana_cadence = 0.001   # Osobne dla speedometera osobne dla pozostałych, aby refreshowały się po kliknięciu 
##### Do speedometera
Obj_Display.wyswietlana_cadence_speedometer  = 0.001  # Wartości domyslnie na mała liczbę, aby po uruchomieniu pokazało się 0 
Obj_Display.wyswietlana_predkosc_speedometer = 0.001
Obj_Display.wejscie = True                # Flaga mówiąca, czy jest się w funkcji speedometera czy nie 
Obj_Display.speed   = 0                   # Przechowywanie poprzedniej aktualnej prędkości chwilowej
Obj_Display.roznica = 0                   # Przechowanie różnicy pomiędzy poprzednią, a nową wartością chwilową
Obj_Display.prog    = 0                   # Do jakiego miejsca mamy rysować naszą funkcję 
Obj_Display.pochodna= True                # Informacja, czy mamy wzrost, czy spadek wartości prędkości chwilowej
Obj_Display.poprzednia_pochodna = True    # Przechowywanie poprzedniej wartości pochodnej 
Obj_Display.pozycja = 0                   # Zmienna mówiąca nam w jakim miejscu aktualnie się znajdujemy
Obj_Display.pozycja_x = 0                 # Wsp. speedometera po x            
Obj_Display.pozycja_y = 0                 # Wsp. speedometera po y  
Obj_Display.speedometer_stop = True       # Flaga powiadamiająca o osiągnięciu progu
Obj_Display.dlugosc_smugi = const(36)     # Długość smugi     [w pixelach]
Obj_Display.dlugosc_wskaznia = const(47)  # Długość Wskaźnika [w pixelach]
Obj_Display.aktualna_pozycja = 0          # Wyliczenie aktualnej pozycji speedometera w momencie wykrycia zmiany prędkości

##### Do zmiany koloru
Obj_Display.wybor_motywu_obrecz = 0       # Zmienne deklarujące który motyw koloru chcemy wybrać 
Obj_Display.wybor_motywu_speedo = 0
Obj_Display.wybor_motywu_czas = 0
Obj_Display.wybor_motywu_dyst = 0
Obj_Display.kolor_czcionki    = 0 
Obj_Display.kolor_podrozy     = 0 
##### Do menu 
Obj_Display.poprzedni_wybor = 0           # Zmienna pozwalająca wymazanie poprzedniego wyboru 
Obj_Display.wejscie_do_menu = False       # Ustawienie flagi informującej o wejściu do menu   
Obj_Display.wymazanie_prostokata = True   
Obj_Display.mruganie_liczb = False        # Flaga deklarująca pokazanie, bądź nie pokazanie liczby 
Obj_Display.deadline = 0                  # Zmienna odmierzająca czas od mrugania liczb w menu             

# Zmienne globalne # 
Flaga_start = True    # Zmienna realizujaca funkcję startową

####================================ FUNKCJE PRZERWANIA ================================================================####
Licznik.licznikPin.irq(     trigger = Pin.IRQ_FALLING, handler = Licznik.Obroty_kola) # Wywołwanie funkcji przerwania do zliczania obrotów koła
Licznik.CadencePin.irq(     trigger = Pin.IRQ_FALLING, handler = Licznik.Kadencja)    # Wywołwanie funkcji przerwania do liczenia kadencji
Obj_Menu.Przycisk_1_Pin.irq(trigger = Pin.IRQ_FALLING, handler = Obj_Menu.Przycisk_1) # Wywołwanie funkcji przerwania przycisku od wyświetlacza  [1]
Obj_Menu.Przycisk_2_Pin.irq(trigger = Pin.IRQ_FALLING, handler = Obj_Menu.Przycisk_2) # Wywołwanie funkcji przerwania przycisku od wyświetlacza  [2]


# start = 0
# start = time.ticks_ms() # get millisecond counter
# delta = time.ticks_diff(time.ticks_us(), start) # compute time difference
# print(delta)

if __name__=='__main__':   
    while True:
               
###============ Funkcja Startowa ======================================================####  
        if Flaga_start == True :
            Licznik.odczyt_z_plikow_podroz_i_total()
            Obj_Menu.odczyt_motywow(Obj_Display)
            Obj_Display.funkcja_startowa()
            Licznik.finish = time.ticks_ms()           
            Obj_Menu.warunek_ktory_wyswietlacz = 0
            Flaga_start = False
            
        # https://docs.micropython.org/en/latest/library/micropython.html#micropython.alloc_emergency_exception_buf
        micropython.alloc_emergency_exception_buf(100)
        
#         delta = time.ticks_diff(time.ticks_us(), start) # compute time difference
#         print(delta)  
#         start = time.ticks_us() # get millisecond counter  
        ##====== Odliczanie czasu ================================##
        Licznik.time_beetwen                       = time.ticks_diff(time.ticks_ms() ,Licznik.finish)               # Czas od ostatniej aktualnej predkosci
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
            elif Obj_Menu.flaga_2_prog_menu == True:
                if Obj_Menu.przytrzymanie_przycisku(2,1700) == 2:
                    Obj_Menu.wybor_opcji_w_menu_2_prog(Licznik,Obj_Display)
                elif Obj_Menu.przytrzymanie_przycisku(1,2000) == 1 and Obj_Menu.flaga_motywy_menu == True:
                    Obj_Menu.zatwierdzenie_motywow(Licznik,Obj_Display)            
            #======== Wybór w menu 3 progu ======#
            elif Obj_Menu.flaga_3_prog_menu == True:
                if Obj_Menu.przytrzymanie_przycisku(2,800) == 2:                
                    Obj_Menu.wybor_opcji_w_menu_3_prog( Licznik)
                    Obj_Menu.zmiana_przycisk = True
                    
                if Obj_Menu.przytrzymanie_przycisku(1,1250) == 1:
                    Obj_Menu.Ustawienie_interwalu( Licznik)     
            #======== Wyjście z Menu ===================#            
            elif Obj_Menu.time_beetwen_interaction_przycisk > 15_000 :
                Obj_Menu.wyjscie_z_menu()
                Obj_Menu.interaction_przycisk = time.ticks_ms() # przypisanie czasu po powrocie z menu do głównego wyświetlania
                
###============ Kadencja ================================================================####
        if time.ticks_diff(time.ticks_ms() ,Licznik.finish_cadence) > 5000 :
            Licznik.cadence_over_5s()
###============ Sleep Mode ==============================================================####
            #(tutaj jest duzo nie optymalnie, ale na razie dziala)#
        ##======  Pójście spać jeżeli od ostatniej interakcji mineło więcej niż 15s ===##        
        elif Licznik.time_beetwen > 243_000  and Obj_Menu.time_beetwen_interaction_przycisk > 20_000:
            print("Spac!")
            Licznik.spac = True       # Zmienna mówiąca, że jest się w fazie snu
            Obj_Menu.spac_menu = True # Zmienna mówiąca, że jest się w fazie snu
            Licznik.zapis_do_pliku_total()
            Licznik.zapis_do_pliku_podroz()
            Obj_Menu.wyjscie_z_menu()
            Obj_Display.funkcja_sleep()
            Licznik.flaga_sen_stop = True
            Obj_Menu.flaga_sen_stop_menu = True
            # wyłączyć wyświetlacz (RS albo tranzystro na 3v3 Out)
            # Deep sleep aż do wybudzenia (kappa), bo jest light sleep)
            while Licznik.flaga_sen_stop == True and Obj_Menu.flaga_sen_stop_menu == True: # Wejście w pętle snu az do momentu "wybudzenia" ;D 
                lightsleep(1500)
                
            Obj_Menu.spac_menu = False  # Wyjście z fazny snu i przypisanie wartości False obu zmiennym 
            Licznik.spac = False       
            Flaga_start = True          # Włączenie funkcji startowej po wyjściu ze snu 
########################################### KONIEC ############################################################
