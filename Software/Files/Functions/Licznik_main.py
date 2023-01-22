from machine import Pin, I2C   ,lightsleep, PWM                     
import time , gc, sys, math
sys.path.insert(0, '/Libraries/Barometer')            # Uzyskanie dostępu do biblioteki barometru
from mpl3115a2 import MPL3115A2                       # Zimportowanie z biblioteki klasy MPL3115A2
i2cbus = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)# Towrzenie obietki I2C dla MPL3115A2
mpl = MPL3115A2(i2cbus, mode=MPL3115A2.ALTITUDE)      # Tworzenie obiektu MPL3115A2 pod nazwą mpl


class Licznik_main(): #Główna funkcja
    current_speed, obwod_kola, ilosc_impulsow     = 0, 0 ,1
    zmienne_modulo, time_beetwen , finish         = 0, 0, 0
    Odliczanie_impulsow, licznikPin               = 0, 0 
    proporcja, odliczanie                         = 0, 0
    flaga, flaga_1, spac                          = False,False,False
    prev_time,prev_time_cadence                   = 0, 0
### Zmienna do liczenia kadencji ###
    current_cadence,cadence_odliczanie,CadencePin = 0, 0, 0
    prev_time_cadence,finish_cadence,modulo_cadence      = 0, 0, 0
### Zmienne do liczenia przewyższeń ###
    tablica_wysokosc,flaga_h_diff ,plaska_jazda ,barometr_flaga= [],False, 0, False
    aktualna_wyskosc,flaga_skok_dodatni,flaga_skok_ujemny = 0, False, False
    plaska_jazda_tab , flaga_skok,flaga_skok_opoznienie = [], False , False
### Zmienne do wyswietlania danych ###
    counter,       v_max,       przeywzszenia,       rtc_czas_total  = 0,0,0,[0,0,0,0]  
    counter_podroz,v_max_podroz,przeywzszenia_podroz,rtc_czas_podroz = 0,0,0,[0,0,0,0]   
### zmienne do liczenia czasu ###
    rtc, rtc_tablica_start = 0,[]
    flaga_czas,wrzesien    = False,False
    current_speed_tab ,nr_sciezki = [], 0
    
#################################### FUNKCJE PRZERWANIA ##########################################################################################
    #Funkcja wykonuje się w ok 0.1ms 
    def Obroty_kola(self,pin):   # Funkcja realizująca przerwanie obrotów koła
        if time.ticks_diff(time.ticks_ms(), self.prev_time) > 60: # Wejście do funkcji, jeżeli upłyneło minimum 60ms
            start = time.ticks_us()
            self.prev_time = time.ticks_ms()# Przypisanie aktualnego czasu po wejściu do funkcji  
            self.counter += 1               # Zwiększenie zmiennej od przejechanego dystansu o 1
            self.counter_podroz += 1        # Zwiększenie zmiennej od przejechanego dystansu podróży o 1
            self.barometr_flaga = True      # Wywołanie flagi do pomiaru wysokości 
            self.zmienne_modulo += 1        # Odliczanie impulsów
            self.Odliczanie_impulsow = self.zmienne_modulo % self.ilosc_impulsow
            
            #====  Liczenie czasu jazdy ##
            if self.flaga_czas == False:
                self.rtc_tablica_start = self.rtc.datetime()  # Przypisanie czasu 'startu' do zmiennej
                self.flaga_czas = True                        # Wygaszenie flagi do momentu zatrzymania się 
                     
            #==== Warunek gdy przez ponad 2 sekundy nie została zmieniona prędkość chwilowa ##        
            if self.flaga == True and self.current_speed != 0:
                self.awaryjna_predkosc_chwilowa()
             
            #==== Wyliczenie aktualnej prędkości kiedy zliczyliśmy odpowiednią ilość ilmulsów ##
            if self.Odliczanie_impulsow == 0:
                self.wyliczanie_predkosci()

    
    
    @micropython.native
    def Kadencja(self, pin):
        print('helo')
        if time.ticks_diff(time.ticks_ms(), self.prev_time_cadence) > 80:
            
            self.prev_time_cadence =time.ticks_ms()  
            self.cadence_odliczanie += 1                               # Inkrementujemy zmienną co wykrycie obortu korbą 
            if self.cadence_odliczanie % self.modulo_cadence == 0:     # Sprawdzamy, czy zmienna odliczyła już odpowiednią ilość 
                time_beetwen  = time.ticks_diff(time.ticks_ms() ,self.finish_cadence)  # Lokalna zmienna z czasem pomiędzy ostanim liczeniem aktualnej kadencji 
                self.finish_cadence = time.ticks_ms()                                  # Starsza wartość czasu po zliczeniu impulsów        
                self.current_cadence = self.modulo_cadence*60_000/time_beetwen         # Wyliczanie aktualnej kadencji 
                self.modulo_cadence = 2                                               # Przypisanie, aby kolenjnym razem zliczało 4 oboroty 
                self.cadence_odliczanie = 0                                            # Zresetowanie zmiennej od odliczania (Just in case)
             

#################################### KONIEC funckji Przerwania ####################################################    
                
################### Do wywalnia na przyszłość! ###################
    @micropython.native
    def zapis_jazdy_do_pliku(self):
        Tab = ["/Dane_nowe/Dane_nowe_1.txt","/Dane_nowe/Dane_nowe_2.txt","/Dane_nowe/Dane_nowe_3.txt","/Dane_nowe/Dane_nowe_4.txt","/Dane_nowe/Dane_nowe_5.txt",
               "/Dane_nowe/Dane_nowe_6.txt","/Dane_nowe/Dane_nowe_7.txt","/Dane_nowe/Dane_nowe_8.txt","/Dane_nowe/Dane_nowe_9.txt","/Dane_nowe/Dane_nowe_10.txt",
               "/Dane_nowe/Dane_nowe_11.txt","/Dane_nowe/Dane_nowe_12.txt","/Dane_nowe/Dane_nowe_13.txt","/Dane_nowe/Dane_nowe_14.txt","/Dane_nowe/Dane_nowe_15.txt"]
        # Zapisywanie danych do pliku co 10 obrotów koła
        zapis = open(Tab[self.nr_sciezki] ,"a")     # "a" append, czyli dodaje do końca listy
        for i in range(len(self.tablica_wysokosc)):     
            text = str("%.2f" %self.current_speed_tab[i])
            # str("%.5f" %self.tablica_wysokosc[i])+ '   ' + 
            zapis.write(text + '\n')  # Zapisanie po kolei tablicy z danymido końca listy
        zapis.close()
    
    def odczyt_zmiennej(self):
        odczyt = open("zmienna.txt","r")
        self.nr_sciezki = 1+ int(odczyt.read())
        odczyt.close() 
    def zapis_zmiennej(self):
        zapis = open("zmienna.txt","w")
        zapis.write(str(self.nr_sciezki))
        zapis.close()
####################################################################
        
        
        
######== Funkcje związne z mierzeniem wysokości ==######
    @micropython.native           
    def barometr(self):
        self.tablica_wysokosc[self.odliczanie]= mpl.altitude() # Nadpisanie wartości kąta sinusa do tabeli
        
        #dane do zapisu do pliku #
        self.current_speed_tab[self.odliczanie] = self.current_speed
        ###
        
        self.odliczanie += 1
        if self.odliczanie %10 == 0:
            self.odliczanie = 0
            self.flaga_h_diff = True
            
    def current_h(self):
        return mpl.altitude()
    
    @micropython.native  #Praca z wypełnioną tablicą 
    def h_diff(self):
        start = time.ticks_us() # get millisecond counter
        # Próg wykrycia błędu
        for i in range(9): #Sprawdzenie, czy nastąpiła skokowa zmiana wysokości o ponad 2m pomiedzy pomiarami
            r = abs(self.tablica_wysokosc[i+1] - self.tablica_wysokosc[i])
            if r >= 2:
                # Wykrycie kierunku spadku
                if self.tablica_wysokosc[i+1] > self.tablica_wysokosc[i]:
                    self.flaga_skok_dodatni = True
                else:    
                    self.flaga_skok_ujemny = True
                                
        if self.flaga_skok_ujemny == True and self.flaga_skok_dodatni == True:
            self.flaga_skok_ujemny = False
            self.flaga_skok_dodatni = False
            return

        elif  self.flaga_skok_ujemny == True or self.flaga_skok_dodatni == True:
            if self.flaga_skok == False:
                self.flaga_skok =True
                return 
            else:
                if flaga_skok_opoznienie == False:
                    self.flaga_skok_opoznienie =True
                    return
                else: 
                    self.flaga_skok_ujemny = False
                    self.flaga_skok_dodatni = False            
                    self.flaga_skok = False
                    self.flaga_skok_opoznienie =False
                    
        ###== Standarowy warunek mierzenie przewyższeń, gdy nie ma żadnych skoków ==###
        avg_h = sum(self.tablica_wysokosc)/10 # Wyliczenie średniej  wysokości       
        # Histereza dobrana na podstawie jazd testowych  +-1.3 [m] 
        if avg_h - self.aktualna_wyskosc < - 1.3: 
            self.aktualna_wyskosc = avg_h
            self.plaska_jazda = 0
            
        elif avg_h - self.aktualna_wyskosc > 1.3:
            self.przeywzszenia += avg_h - self.aktualna_wyskosc
            self.przeywzszenia_podroz += avg_h - self.aktualna_wyskosc
            self.aktualna_wyskosc = avg_h
            self.plaska_jazda = 0
            
        else: #Jeżeli jedziemy po płaskim już długo to uśredniamy całą tą drogę do jednej wysokości
            self.plaska_jazda_tab[self.plaska_jazda] = avg_h
            self.plaska_jazda += 1
            if self.plaska_jazda >9:
                self.plaska_jazda = 0
                self.aktualna_wyskosc = sum(self.plaska_jazda_tab)/10

######== Funkcje związne z prędkością chwilową ==######           
    @micropython.native           
    def awaryjna_predkosc_chwilowa(self):
        okres_obortu = (self.obwod_kola*3.6)/self.current_speed           # Wyliczenie okresu oborktu (w ms) dla aktualnej prędkości
        self.time_beetwen  = time.ticks_diff(time.ticks_ms() ,self.finish)# Dodatkowo dla większej dokładności wyliczamy czas od ostatniego poleczenia predkości aktualnej 
        self.proporcja = self.time_beetwen /okres_obortu                  # Policzenie proporcji, ile czasu upłyneło od zmiany prędkości a okresu obortu
        if self.proporcja >= 1:                                           # Jeżeli większa niż 1 to nie bierzemy tego w ogóle pod uwagę
            self.proporcja = 1
        self.flaga = False                                                # Wygaszamy flagę alarmującą, aby więcej już nie wchodziło w tą sekcje kodu 
        self.flaga_1 = True                                               # Ustawiamy kolejną flagę, aby po ziczeniu impulsów dobrze policzyło aktualną prędkość 
    
    @micropython.native      
    def wyliczanie_predkosci(self):
        self.time_beetwen  = time.ticks_diff(time.ticks_ms() ,self.finish)
        self.finish = time.ticks_ms()   # Starsza wartość czasu po zliczeniu impulsów
   
        # Standardowy warunek wyliczania prędkości chwilowej          
        if self.flaga_1  == False:
            self.current_speed = self.ilosc_impulsow *3.6*self.obwod_kola/self.time_beetwen  # 3.6  (m/s => km/h)
        # Warunek wyliczania prędkości chwilowej gdy prędzej w ciągu 3 sekund nie zostały zliczone wszystkie impulsy     
        elif self.flaga_1  == True: 
            self.current_speed =(self.ilosc_impulsow + self.proporcja -1 )*self.obwod_kola*3.6/self.time_beetwen  #3.6  (m/s => km/h)                
            self.flaga_1  = False
            self.proporcja = 0
            
        # Zależności dla porządanej ilości impiulsów od prędkości chwilowej
        self.ilosc_impulsow  = Licznik_main.zaleznosci(self.current_speed)
        self.zmienne_modulo = 0
        if  self.current_speed > 99:
            self.current_speed = 99
        if self.current_speed > self.v_max :         # Przypisanie maksymalnej prędkośći chwilowej [Total]
            self.v_max  = self.current_speed
        if self.current_speed > self.v_max_podroz :  # Przypisanie maksymalnej prędkośći chwilowej [Podroz]
            self.v_max_podroz  = self.current_speed
                     
        if self.spac == True:
            self.spac = False

    @micropython.native
    def zaleznosci(speed):
        if speed <= 10.3:  
            return 1       
        elif speed <=15.55  and speed> 10.3:
            return 2
        elif speed <= 23.41 and speed>15.55:
            return 3
        elif speed <= 31 and speed>23.41:
            return 4
        elif speed <=38.7  and speed> 31:
            return 5
        elif speed <=46    and speed> 38.7:
            return 6
        else :
            return 7

        
    @micropython.native
    def over_2s_and_speed_0(self):
        self.current_speed  = 0
        self.zmienne_modulo = 0
        
    @micropython.native
    def over_2s_and_speed_non_0(self):
        self.time_beetwen = time.ticks_diff(time.ticks_ms(),self.finish)
        self.finish = time.ticks_ms()       # Starsza wartość czasu po policzeniu aktualnego czasu pomiędzy impulasami            
        self.current_speed = self.Odliczanie_impulsow*3.6*self.obwod_kola/self.time_beetwen                 
        self.Odliczanie_impulsow = 0        # Ustawienie tej zmiennej na 0 sprawia, że dobrze odliczy wymagane impulsy 
        self.ilosc_impulsow  = Licznik_main.zaleznosci(self.current_speed)
        self.zmienne_modulo = 0
        self.flaga = True                   # Flaga alarmująca o tym, że w 3 sekundy nie zostały zliczone wszystkie impulsy
    
         

    
    def zapis_do_pliku_total(self):      
        total_dystans = open("/Dane/Total/total_dystans.txt" ,"w")    # Total dystans
        total_dystans.write(str(self.counter))                        # Zapis do pliku zmiennej zmienionej na str 
        total_dystans.close()                                         # Zamknięcie pliku
        
        total_max = open("/Dane/Total/total_max.txt" ,"w")            # Maksymalna prędkość chwilowas 
        total_max.write(str(self.v_max)) 
        total_max.close()
       
        total_przewyzszenia = open("/Dane/Total/total_przewyzszenia.txt" ,"w") # Całkowite przewyższenia
        total_przewyzszenia.write(str(self.przeywzszenia)) 
        total_przewyzszenia.close()
        
        total_czas = open("/Dane/Total/total_czas.txt" ,"w")
        for i in range(len(self.rtc_czas_total)):
            total_czas.write(str(self.rtc_czas_total[i]) + '\n')      # Zapisanie po kolei tablicy z czasem total 
        total_czas.close()
        
    def zapis_do_pliku_podroz(self):
        podroz_dystans = open("/Dane/Podroz/podroz_dystans.txt" ,"w") # Dystans podróży         
        podroz_dystans.write(str(self.counter_podroz) )               # Zapis do pliku zmiennej zmienionej na str
        podroz_dystans.close()                                        # Zamknięcie pliku
        
        podroz_max = open("/Dane/Podroz/podroz_max.txt" ,"w")         # Maksymalna prędkość podróży 
        podroz_max.write(str(self.v_max_podroz))
        podroz_max.close()
        
        podroz_przewyzszenia = open("/Dane/Podroz/podroz_przewyzszenia.txt" ,"w")  # Przewyższenia podróży
        podroz_przewyzszenia.write(str(self.przeywzszenia_podroz))
        podroz_przewyzszenia.close()

        podroz_czas = open("/Dane/Podroz/podroz_czas.txt" ,"w")
        for i in range(len(self.rtc_czas_podroz)):
            podroz_czas.write(str(self.rtc_czas_podroz[i]) + '\n')# Zapisanie po kolei tablicy z czasem total 
        podroz_czas.close()
        
    def odczyt_z_plikow_podroz_i_total(self):
        ####################### Odczytywanie danych z total  ##################        
        total_dystans = open("/Dane/Total/total_dystans.txt" ,"r")   # Total dystans
        self.counter = int(total_dystans.read())
        total_dystans.close()

        total_max = open("/Dane/Total/total_max.txt" ,"r")           # Maksymalna prędkość chwilowa
        self.v_max = float(total_max.read())
        total_max.close()    
        
        total_przewyzszenia = open("/Dane/Total/total_przewyzszenia.txt" ,"r")# Całkowite przewyższenia 
        self.przeywzszenia = float(total_przewyzszenia.read()) 
        total_przewyzszenia.close()
              
        i = 0
        total_czas = open("/Dane/Total/total_czas.txt" ,"r")
        total = total_czas.readlines()
        for dane_czas_total in total:
            dane_czas_total = dane_czas_total.replace("\n", "")  # usuwanie znaku końca linii
            self.rtc_czas_total[i] = int(dane_czas_total)
            i += 1
        total_czas.close()

        ####################### Odczytywanie danych z podrozy  ##################       
        podroz_dystans = open("/Dane/Podroz/podroz_dystans.txt" ,"r") # Dystans podróży 
        self.counter_podroz = int(podroz_dystans.read())
        podroz_dystans.close()
        
        podroz_max = open("/Dane/Podroz/podroz_max.txt" ,"r")         # Maksymalna prędkość podróży 
        self.v_max_podroz = float(podroz_max.read())
        podroz_max.close()
               
        podroz_przewyzszenia = open("/Dane/Podroz/podroz_przewyzszenia.txt" ,"r") # Przewyższenia podróży
        self.przeywzszenia_podroz = float(podroz_przewyzszenia.read())
        podroz_dystans.close()
        
        j = 0 
        podroz_czas = open("/Dane/Podroz/podroz_czas.txt" ,"r")
        podroz = podroz_czas.readlines()
        for dane_czas_podroz in podroz:
            dane_czas_podroz = dane_czas_podroz.replace("\n", "")  # usuwanie znaku końca linii
            self.rtc_czas_podroz[j] = int(dane_czas_podroz)
            j += 1
        podroz_czas.close()
            
#### Funckja od kadencji 
    @micropython.native
    def cadence_over_3s(self):
        self.current_cadence = 0            # Ustawiamy aktualną kadencję na 0 
        self.cadence_odliczanie = 0         # Ustawiamy wartość zmiennej od odliczania na 0 (Just in case)
        self.modulo_cadence = 1             # Ustawiamy zmienną modulo na 1 aby po wykryciu 1 obortu zreetował się czas pomiędzy 
    
#### Funckje związne z liczeniem czasu 
    
    def rtc_czas(self):
        if self.flaga_czas == True:
            self.rtc_tablica_stop = self.rtc.datetime() # Przypisanie aktualnego czasu do zmienej lokalnej stop
            ##################=== Prawidłowe odczytanie  ===######################
                ###############== Sekundy ==###############
            if self.rtc_tablica_stop[6] >= self.rtc_tablica_start[6]:
                self.rtc_czas_total[3] += (self.rtc_tablica_stop[6] - self.rtc_tablica_start[6])
                self.rtc_czas_podroz[3] += (self.rtc_tablica_stop[6] - self.rtc_tablica_start[6])
                
            else:
                self.rtc_czas_total[3] +=  ((self.rtc_tablica_stop[6] - self.rtc_tablica_start[6]) + 60)
                self.rtc_czas_total[2] -= 1
                
                self.rtc_czas_podroz[3] +=  ((self.rtc_tablica_stop[6] - self.rtc_tablica_start[6]) + 60)            
                self.rtc_czas_podroz[2] -= 1
                
            if self.rtc_czas_total[3] > 59:    # Dla total 
                self.rtc_czas_total[2] += 1
                self.rtc_czas_total[3] -= 60
                
            if self.rtc_czas_podroz[3] > 59:   # Dla podroz
                self.rtc_czas_podroz[2] += 1
                self.rtc_czas_podroz[3] -= 60
                
                
                ###############== Minuty ==################
            if self.rtc_tablica_stop[5] >= self.rtc_tablica_start[5]:
                self.rtc_czas_total[2] += (self.rtc_tablica_stop[5] - self.rtc_tablica_start[5])
                self.rtc_czas_podroz[2] += (self.rtc_tablica_stop[5] - self.rtc_tablica_start[5])
            else:
                self.rtc_czas_total[2] +=  (self.rtc_tablica_stop[5] - self.rtc_tablica_start[5] + 60)
                self.rtc_czas_total[1] -= 1
                self.rtc_czas_podroz[2] +=  (self.rtc_tablica_stop[5] - self.rtc_tablica_start[5] + 60)
                self.rtc_czas_podroz[1] -= 1
                
            if self.rtc_czas_total[2] > 59:    # Dla total             
                self.rtc_czas_total[1] += 1
                self.rtc_czas_total[2] -= 60
                
            if self.rtc_czas_podroz[2] > 59:   # Dla podroz          
                self.rtc_czas_podroz[1] += 1
                self.rtc_czas_podroz[2] -= 60
                
                ###############== Godziny ==###############
            if self.rtc_tablica_stop[4] >= self.rtc_tablica_start[4]:
                self.rtc_czas_total[1] += (self.rtc_tablica_stop[4] - self.rtc_tablica_start[4])
                self.rtc_czas_podroz[1] += (self.rtc_tablica_stop[4] - self.rtc_tablica_start[4])   
            else: 
                self.rtc_czas_total[1] += (self.rtc_tablica_stop[4] - self.rtc_tablica_start[4] + 24)
                self.rtc_czas_total[0] -= 1
                self.rtc_czas_podroz[1] += (self.rtc_tablica_stop[4] - self.rtc_tablica_start[4] + 24)
                self.rtc_czas_podroz[0] -= 1
                
            if self.rtc_czas_total[1] > 23:   # Dla total 
                self.rtc_czas_total[0] += 1
                self.rtc_czas_total[1] -=24
                
            if self.rtc_czas_podroz[1] > 23:  # Dla podroz
                self.rtc_czas_podroz[0] += 1
                self.rtc_czas_podroz[1] -=24
                
                ###############== Dni ==###################
            if self.rtc_tablica_stop[2] >= self.rtc_tablica_start[2]:
                self.rtc_czas_total[0] += (self.rtc_tablica_stop[2] - self.rtc_tablica_start[2])
                self.rtc_czas_podroz[0] += (self.rtc_tablica_stop[2] - self.rtc_tablica_start[2])
            else:
                self.rtc_czas_total[0] += (self.rtc_tablica_stop[2] - self.rtc_tablica_start[2]+ 31)
                self.rtc_czas_podroz[0] += (self.rtc_tablica_stop[2] - self.rtc_tablica_start[2]+ 31)
                
            if self.rtc_czas_total[0] > 92 and self.wrzesien == False: # Bo we wrzesniu jest 30 dni ;) 
                self.wrzesien = True
                self.rtc_czas_total[0] -= 1

            
            self.rtc_tablica_start = self.rtc.datetime()   # Przypisanie aktualnego czasu do zmienej start  
        else:
            return

    @micropython.native
    def v_srednie_t(self): #funkcja zwracajaca predkos srednia totalu
        self.rtc_czas()
            #Wynik w godzinach 
        czas_total = self.rtc_czas_total[0]*24 + self.rtc_czas_total[1] +self.rtc_czas_total[2]/60 + self.rtc_czas_total[3]/3600 
            #Wynik w kilometrach
        dystans = self.counter * self.obwod_kola/1_000_000
        
        if czas_total != 0 and dystans != 0:
            return dystans/czas_total
        else :
            return 0
        
    @micropython.native    
    def v_srednie_p(self): #funkcja zwracajaca predkos srednia podrozy
        self.rtc_czas()
            #Wynik w godzinach 
        czas_total = self.rtc_czas_podroz[0]*24 + self.rtc_czas_podroz[1] +self.rtc_czas_podroz[2]/60 + self.rtc_czas_podroz[3]/3600 
            #Wynik w kilometrach 
        dystans = self.counter_podroz * self.obwod_kola/1_000_000       
        if czas_total != 0:
            return dystans/czas_total
        else :
            pass
  