import time , gc

class Licznik_main(): #Główna funkcja
    
    current_speed = 0 
    obwod_kola = 0 
    ay_kat = 0
    ay = 0
    ilosc_impulsow = 1
    zmienne_modulo = 0
    time_beetwen = 0
    finish = 0
    Odliczanie_impulsow = 0
    flaga = False
  
    counter = 0
    v_max = 0
    przeywzszenia = 0    
    rtc_czas_total = [0,0,0,0]
   
    counter_podroz = 0
    v_max_podroz = 0
    przeywzszenia_podroz = 0
    rtc_czas_podroz = [0,0,0,0]   
         
### zmienne do liczenia czasu ###
    rtc = 0
    rtc_tablica_start = []
    flaga_czas = False
    wrzesien = False

        
    def zapis_do_pliku_total(self):      
        total_dystans = open("/Dane/Total/total_dystans.txt" ,"w") #total dystans
        total_dystans.write(str(self.counter))              # Zapis do pliku zmiennej zmienionej na str 
        total_dystans.close()                               # Zamknięcie pliku
        
        total_max = open("/Dane/Total/total_max.txt" ,"w") # Maksymalna prędkość chwilowas 
        total_max.write(str(self.v_max)) 
        total_max.close()
       
        total_przewyzszenia = open("/Dane/Total/total_przewyzszenia.txt" ,"w") # Całkowite przewyższenia
        total_przewyzszenia.write(str(self.przeywzszenia)) 
        total_przewyzszenia.close()
        
        total_czas = open("/Dane/Total/total_czas.txt" ,"w")
        for i in range(len(self.rtc_czas_total)):
            total_czas.write(str(self.rtc_czas_total[i]) + '\n')# Zapisanie po kolei tablicy z czasem total 
        total_czas.close()
        
    def zapis_do_pliku_podroz(self):
        podroz_dystans = open("/Dane/Podroz/podroz_dystans.txt" ,"w") # Dystans podróży         
        podroz_dystans.write(str(self.counter_podroz) )               # Zapis do pliku zmiennej zmienionej na str        podroz_dystans.close()                                        # Zamknięcie pliku
        
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
                
        
    def zaleznosci(self):
        self.zmienne_modulo = 0
        if self.current_speed <= 9:            
            self.ilosc_impulsow =1       
        elif self.current_speed <=13.63  and self.current_speed> 9:
            self.ilosc_impulsow =2
        elif self.current_speed <= 18.21 and self.current_speed>13.63:
            self.ilosc_impulsow =3
        elif self.current_speed <= 22.86 and self.current_speed>18.21:
            self.ilosc_impulsow =4
        elif self.current_speed <=27.35  and self.current_speed> 22.86:
            self.ilosc_impulsow = 5
        elif self.current_speed <32.5    and self.current_speed> 27.35:
            self.ilosc_impulsow =6
        elif self.current_speed <= 37.5  and self.current_speed> 30.5:
            self.ilosc_impulsow =7
        elif self.current_speed <= 43    and self.current_speed> 37.5:
            self.ilosc_impulsow =8
        elif self.current_speed <= 55    and self.current_speed> 43:
            self.ilosc_impulsow =9
        elif self.current_speed > 55:
            self.ilosc_impulsow =11

    def over_3s_and_speed_0(self) :
        self.current_speed = 0
        self.zmienne_modulo = 0
        
    def over_3s_and_speed_non_0(self) :
        self.time_beetwen = time.ticks_diff(time.ticks_ms(),self.finish)
        self.finish = time.ticks_ms() # Starsza wartość czasu po zliczeniu impulsów           
        self.current_speed = self.Odliczanie_impulsow*3.6*self.obwod_kola/self.time_beetwen                 
        self.Odliczanie_impulsow = 0     
        self.flaga = True  #Flaga alarmująca o tym, że w 3 sekundy nie zostały zliczone wszystkie impulsy       
        gc.collect()

    
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
  