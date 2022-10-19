from machine import Pin, I2C                        
import time , gc, sys, math
sys.path.insert(0, '/Libraries/Gyroscope')          # Uzyskanie dostępu do biblioteki żyroskopu 
from imu import MPU6050                             # Zimportowanie z biblioteki klasy MPU6050
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)   # Towrzenie obietki I2C
imu = MPU6050(i2c)                                  # Tworzenie obiektu MPU6050 pod nazwą imu
class Licznik_main(): #Główna funkcja
    current_speed, obwod_kola, ilosc_impulsow     = 0, 0 ,1
    zmienne_modulo, time_beetwen , finish         = 0, 0, 0
    Odliczanie_impulsow, licznikPin, Pin17_state  = 0, 0 ,0
    proporcja, odliczanie                         = 0, 0
    flaga, flaga_1, spac                          = False,False,False
    tablica_sin , tablica_g_force                 = [], []
### Zmienna do liczenia kadencji ###
    current_cadence,cadence_odliczanie,CadencePin = 0, 0, 0
    Pin8_state,finish_cadence,modulo_cadence      = 0, 0, 0
### Zmienne do przechowania danych ###
    counter,       v_max,       przeywzszenia,       rtc_czas_total  = 0,0,0,[0,0,0,0]  
    counter_podroz,v_max_podroz,przeywzszenia_podroz,rtc_czas_podroz = 0,0,0,[0,0,0,0]   
### zmienne do liczenia czasu ###
    rtc, rtc_tablica_start = 0,[]
    flaga_czas,wrzesien    = False,False

#################################### FUNKCJE PRZERWANIA ##########################################################################################
    
    def Obroty_kola(self,pin):   # Funkcja realizująca przerwanie obrotów koła 
        if (self.licznikPin.value() == 1) and (self.Pin17_state == 0 ):
            
            self.Pin17_state = 1      # Zmiana zmiennej do debouncingu 
            self.counter += 1         # Zwiększenie zmiennej od przejechanego dystansu o 1
            self.counter_podroz += 1  # Zwiększenie zmiennej od przejechanego dystansu podróży o 1
            
    #============================ Odzytanie wartości sinusa kąta nachylenia =======================================#
#             start = time.ticks_us() # get millisecond counter
#             delta = time.ticks_diff(time.ticks_us(), start) # compute time difference
#             print(delta)
            self.tablica_sin[self.odliczanie]    = -imu.accel.y        # Nadpisanie wartości kąta sinusa do tabeli
            self.tablica_g_force[self.odliczanie]= imu.accel.magnitude # Nadpisanie wartości przeciążenia do tabeli
            self.odliczanie += 1
            if self.odliczanie %10 == 0:
                self.odliczanie = 0
                # Pewnbie to przewy będziemy jeszcze skalować przez obwód koła albo coś 
                przewy = Licznik_main.cal_przeywzszenia(self.tablica_sin, self.tablica_g_force) # Wartość przewyższenia 
                
                if przewy !=0: 
                    self.przeywzszenia += przewy
                    self.przeywzszenia_podroz += przewy        
            #== Zapisywanie pomiaru do pliku  ==#
#             Licznik_main.zapis_kata_do_pliku(sin_gyro, g_gryo,self.current_speed)
    #============================================= KONIEC Sinusa ========================================================#        
            
            ## Liczenie czasu jazdy ##
            if self.flaga_czas == False:
                self.rtc_tablica_start = self.rtc.datetime()  # Przypisanie czasu 'startu' do zmiennej
                self.flaga_czas = True                        # Wygaszenie flagi do momentu zatrzymania się 
                
           
            ## Warunek gdy przez ponad 3 sekundy nie została zmieniona prędkość chwilowa ##        
            if self.flaga == True and self.current_speed != 0:       
                okres_obortu = (self.obwod_kola*3.6)/self.current_speed               # Wyliczenie okresu oborktu (w ms) dla aktualnej prędkości
                self.time_beetwen  = time.ticks_diff(time.ticks_ms() ,self.finish)    # Dodatkowo dla większej dokładności wyliczamy czas od ostatniego poleczenia predkości aktualnej 
                self.proporcja = self.time_beetwen /okres_obortu                      # Policzenie proporcji, ile czasu upłyneło od zmiany prędkości a okresu obortu
                if self.proporcja >= 1:                                               # Jeżeli większa niż 1 to nie bierzemy tego w ogóle pod uwagę
                    self.proporcja = 1
                self.flaga = False                                                    # Wygaszamy flagę alarmującą, aby więcej już nie wchodziło w tą sekcje kodu 
                self.flaga_1 = True                                                   # Ustawiamy kolejną flagę, aby po ziczeniu impulsów dobrze policzyło aktualną prędkość 
                
            self.zmienne_modulo += 1
            self.Odliczanie_impulsow = self.zmienne_modulo % self.ilosc_impulsow

            if self.Odliczanie_impulsow == 0:
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
                
                if self.current_speed > self.v_max :         # Przypisanie maksymalnej prędkośći chwilowej [Total]
                    self.v_max  = self.current_speed
                if self.current_speed > self.v_max_podroz :  # Przypisanie maksymalnej prędkośći chwilowej [Podroz]
                    self.v_max_podroz  = self.current_speed
                                
                if self.spac == True:
                    self.spac = False
        ##  Dalsza część funkcji realizująca przerwanie odpowiedzialna za debouncing ##
        elif (self.licznikPin.value() == 0) and (self.Pin17_state == 1):
            self.Pin17_state = 0    # Do debouncingu     
        self.licznikPin.irq(handler = self.Obroty_kola)
        
################### Do wywalnia na przyszłość ! ###################
    @micropython.native
    def zapis_kata_do_pliku(sinus, przeciazenie, speed):
        # Zamienienie danych na strin kąta, przeciążenie i prędkość aktualna
        text = str(180*math.asin(sinus)/math.pi) + "   " + str(przeciazenie) + "   " + str(speed)   
        zapis = open("dane_z_zyroskopu_3.txt" ,"a")     # "a" append, czyli dodaje do końca listy 
        zapis.write(text + '\n')                        # Dlatego \n żeby przejść linijkę niżej 
        zapis.close()
####################################################################
        
        
    @micropython.native  #Praca nad wypełnioną tablicą 
    def cal_przeywzszenia(tab_sin, tab_g):
        max_sin = max(tab_sin)
        min_sin = min(tab_sin)
        max_g = max(tab_g)

#         if max_sin*min_sin < 0:
#             return 0
        avg_sin = sum(tab_sin)/10
        avg_g   = sum(tab_g)/10
        # No i w zależności od avg_g możemy domniemać po jakiej nawieżchni jedziemy
        # A to może klasyfikować do różnych 'progów" filtracji, albo można stworzyć doświadczalnie
        # Zależność nawierzchni od g_force i używać funkcji odwrotnej (tylko po co?)
        # Celem jest wyliczenie przewyższeń
        # Należy zobaczyć jak cenna jest informacja avg_sin
        # Przetestować na przewyższeniu, i na płaskim
        # Na dzirach, i na gładkim Pozystać dane
        return 0
    @micropython.native
    def Kadencja(self, pin):    
        if (self.CadencePin.value() == 1) and (self.Pin8_state == 0 ):      
            self.Pin8_state = 1                                        # Do debouncingu 
            
            self.cadence_odliczanie += 1                               # Inkrementujemy zmienną co wykrycie obortu korbą 
            if self.cadence_odliczanie % self.modulo_cadence == 0:     # Sprawdzamy, czy zmienna odliczyła już odpowiednią ilość 
                time_beetwen  = time.ticks_diff(time.ticks_ms() ,self.finish_cadence)  # Lokalna zmienna z czasem pomiędzy ostanim liczeniem aktualnej kadencji 
                self.finish_cadence = time.ticks_ms()                                  # Starsza wartość czasu po zliczeniu impulsów        
                self.current_cadence = self.modulo_cadence*60_000/time_beetwen         # Wyliczanie aktualnej kadencji 
                self.modulo_cadence = 4                                                # Przypisanie, aby kolenjnym razem zliczało 4 oboroty 
                self.cadence_odliczanie = 0                                            # Zresetowanie zmiennej od odliczania (Just in case)
                
        # Dalsza część funkcji realizująca przerwanie odpowiedzialna za eliminację dragń styków     
        elif (self.CadencePin.value() == 0) and (self.Pin8_state == 1 ):
            self.Pin8_state = 0
       
        self.CadencePin.irq(handler = self.Kadencja)  
    
#################################### KONIEC funckji Przerwania ####################################################    
    
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
#         elif speed <= 43    and speed> 54:
#             return 8
#         elif speed <= 55    and speed> 43:
#             return 9
#         else speed > 55:
#             return 11
        
    @micropython.native
    def over_3s_and_speed_0(self):
        self.current_speed  = 0
        self.zmienne_modulo = 0
        
    @micropython.native
    def over_3s_and_speed_non_0(self):
        self.time_beetwen = time.ticks_diff(time.ticks_ms(),self.finish)
        self.finish = time.ticks_ms()       # Starsza wartość czasu po policzeniu aktualnego czasu pomiędzy impulasami            
        self.current_speed = self.Odliczanie_impulsow*3.6*self.obwod_kola/self.time_beetwen                 
        self.Odliczanie_impulsow = 0        # Ustawienie tej zmiennej na 0 sprawia, że dobrze odliczy wymagane impulsy 
        self.ilosc_impulsow  = Licznik_main.zaleznosci(self.current_speed)
        self.zmienne_modulo = 0
        self.flaga = True                   # Flaga alarmująca o tym, że w 3 sekundy nie zostały zliczone wszystkie impulsy
    
    @micropython.native
    def cadence_over_5s(self):
        self.current_cadence = 0            # Ustawiamy aktualną kadencję na 0 
        self.cadence_odliczanie = 0         # Ustawiamy wartość zmiennej od odliczania na 0 (Just in case)
        self.modulo_cadence = 1             # Ustawiamy zmienną modulo na 1 aby po wykryciu 1 obortu zreetował się czas pomiędzy 
    
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
  