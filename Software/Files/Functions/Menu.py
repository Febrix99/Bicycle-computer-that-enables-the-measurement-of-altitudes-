import time , gc
import  micropython
from machine import Pin, PWM

class Menu():   
    Przycisk_2_Pin,      Przycisk_1_Pin                  = 0 , 0 
    Flaga_przycisk_lewy, Flaga_przycisk_prawy   , menu   = False, False , False
    przycisk,            warunek_ktory_wyswietlacz       = 0 , 0 
    ustawienie_czasu,    nr_przycisku, Funkcja_przycisk  = 0 , 0 ,0
    warunek_ktory_wyswietlacz_menu                       = 0
    ilosc_wyborow_w_menu,wybor_w_menu                    = 0, 0
    flaga_1_prog_menu,   flaga_2_prog_menu, flaga_3_prog_menu = False, False,False
    ilosc_cykli,         wybor_w_menu_interwal           = 0, 0
    wlasny_interwal,     blik_ract                       = False , 0    
    interwal_czas,       interwal_pause                  = 0, 0
    interwal_czas_start_0, interwal_czas_start_1         = False, False
    przejechany_dystans, dlugosc_interwalu               = [], []
    ustawienie_danych                                    = False  
    interwal_dystans,    interwal_dystans_pause          = 0, 0
    odliczanie ,prev_time_butt_1, prev_time_butt_2       = 0,0,0
    interwal_dystans_start_0, interwal_dystans_start_1   = False , False
    time_beetwen_interaction_przycisk , interaction_przycisk = 0 ,0
    mruganie_liczb_interwal,deadline_interwal            = False, 0
    pwm15, flaga_buzzer                                  = 0 ,True
    Odmierzanie_grafiki, cykle =  0 , 0
    czyszczenie , zmiana_liczb, dodatkowe_czyszczenie    = False, 0, False
    podsumowanie_interwalu_przycisk, podsumowanie        = 0, True
    zmiana_przycisk    = False
    spac_menu  ,wybor_ktory_motyw                        =  False, 0 
    flaga_motywy_menu    , flaga_motywy_menu_1           = False, False
    alrm_przycisk_1,alrm_przycisk_2 = False, False
#################################### FUNKCJE PRZERWANIA ##########################################################################################    

    def Przycisk_1(self,pin):#[LEWY/ ZIELONY] Funkcja realizująca przerwanie przycisku od zmiany wyświetlacza [1]
        if time.ticks_diff(time.ticks_ms(), self.prev_time_butt_1) > 60:        
            if self.spac_menu == True:
                self.spac_menu = False
                self.alrm_przycisk_1 = False
            else:
                self.alrm_przycisk_1 = True
        self.prev_time_butt_1 =time.ticks_ms()
        
    def Przycisk_2(self,pin):  # [PRAWY/ CZERWONY]Funkcja realizująca przerwanie przycisku od zmiany wyświetlacza [2]     
        if time.ticks_diff(time.ticks_ms(), self.prev_time_butt_2) > 60: 
            if self.spac_menu == True:
                self.spac_menu = False
                self.alrm_przycisk_2 = False 
            else:
                self.alrm_przycisk_2 = True 
        self.prev_time_butt_2 =time.ticks_ms()
               
    def funkcja_przycisku_1(self):
            #=== Warunek, aby wyczyścić odpowiednią część na wyświetlaczu ==============#
        if self.zmiana_przycisk == False:
            self.zmiana_przycisk = True
            #=== Warunek, aby po przytrzymaniu przycisku nie nastąpiła żadna operacja ==#  
        if self.Flaga_przycisk_lewy == True:
            self.Flaga_przycisk_lewy = False
            
            #=== standarodowy warunk dzialania przycisku gdy nie jest w menu ============#    
        elif self.menu == False: 
            self.przycisk += 1
            self.warunek_ktory_wyswietlacz = self.przycisk % 5 + 1
            #======== Wybór w menu 1 progu ======# 
        elif  self.flaga_1_prog_menu == True: 
            self.przycisk += 1
            self.wybor_w_menu = self.przycisk % self.ilosc_wyborow_w_menu 
            
            #======== Wybór w menu 2 progu ======# 
        elif  self.flaga_2_prog_menu == True: 
            self.przycisk += 1
            self.wybor_w_menu = self.przycisk % self.ilosc_wyborow_w_menu
            
            #======== Wybór w menu 3 progu ======# 
        elif  self.flaga_3_prog_menu == True: #Dotyczy tylko interwałów
            self.interwal_dane(self.add)
            
        if self.podsumowanie == True and self.ilosc_cykli >3 : 
            self.podsumowanie_interwalu_przycisk =  self.przycisk % (self.ilosc_cykli - 2) #Bo operacja modulo, czyli 1 mniej niż logika podpowiada 
             
        self.interaction_przycisk =time.ticks_ms()
    def funkcja_przycisku_2(self):
            #=== Warunek, aby wyczyścić odpowiednią część na wyświetlaczu ==============#
        if self.zmiana_przycisk == False:
            self.zmiana_przycisk = True              
            #=== Warunek, aby po przytrzymaniu przycisku nie nastąpiła żadna operacja ==#     
        if self.Flaga_przycisk_prawy == True: 
            self.Flaga_przycisk_prawy = False
            
            #=== standarodowy warunk dzialania przycisku gdy nie jest w menu #       
        elif self.menu == False:
            self.przycisk -= 1  
            self.warunek_ktory_wyswietlacz = self.przycisk % 5 + 1
     
            #======== Wybór w menu 1 progu ======# 
        elif  self.flaga_1_prog_menu == True: 
            self.przycisk -= 1
            self.wybor_w_menu = self.przycisk % self.ilosc_wyborow_w_menu 
            
            #======== Wybór w menu 2 progu ======# 
        elif  self.flaga_2_prog_menu == True: 
            self.przycisk -= 1
            self.wybor_w_menu = self.przycisk % self.ilosc_wyborow_w_menu       
            #======== Wybór w menu 3 progu ======# 
        elif  self.flaga_3_prog_menu == True: 
            self.interwal_dane(self.sub)
            
        if self.podsumowanie == True and self.ilosc_cykli >3 : 
            self.podsumowanie_interwalu_przycisk =  self.przycisk % (self.ilosc_cykli - 2)#Bo operacja modulo, czyli 1 mniej niż logika podpowiada 
        self.interaction_przycisk =time.ticks_ms()    
#################################### KONIEC funckji Przerwania ####################################################  
    
    
    
    def sub(self,a,b):
        return a -b
    def add(self,a,b):
        return a +b

    def przytrzymanie_przycisku(self,wybor_przycisku ,podany_czas): 
        if wybor_przycisku == 1: # Lewy przycisk 
            
            if (self.Przycisk_1_Pin.value() == 0 and self.Przycisk_2_Pin.value() == 1 and self.Flaga_przycisk_lewy == False):
                if self.ustawienie_czasu == 0:
                    self.funkcja_przycisk = 1
                    self.ustawienie_czasu = time.ticks_ms() #przypisanie aktualnego czasu do momoentu wciśnięcia przycisku
                    self.nr_przycisku = self.warunek_ktory_wyswietlacz_menu # usuniecie mozliwosci, że podczas trzymania kliknie sie szybko drugi przycisk
                    # i przeskoczy menu, ale operacja i tak dalej sie bedzie wykonywac
                    
                if self.ustawienie_czasu != 0 and  time.ticks_diff(time.ticks_ms(),self.ustawienie_czasu) > podany_czas :# Przytrzymanie przez podany czas              
                    self.ustawienie_czasu = 0  #Zresetowanie czasu, aby powyższy warunek wykonał się tylko raz (na 2 sekund)    
                    self.Flaga_przycisk_lewy = True
                    return 1
                
            # Zresetowanie czasu, jeżeli przycisk został odkliknięty                
            elif self.ustawienie_czasu != 0 and self.funkcja_przycisk == 1 and ( self.Przycisk_1_Pin.value() == 1 or self.warunek_ktory_wyswietlacz_menu != self.nr_przycisku or  self.Przycisk_2_Pin.value() == 0):           
                self.ustawienie_czasu = 0 # ustawienie wartosci na 0 tak, aby po wejsciu przypisac aktualny czas
                self.funkcja_przycisk = 0
              
        if wybor_przycisku == 2: # prawy przycisk (czerwony)
            if (self.Przycisk_2_Pin.value() == 0 and self.Przycisk_1_Pin.value() == 1 and self.Flaga_przycisk_prawy == False):

                if self.ustawienie_czasu == 0:
                    self.funkcja_przycisk = 2 #ustawienie możliwości resetu czasu tylko tą funkcją 
                    self.ustawienie_czasu = time.ticks_ms() #przypisanie aktualnego czasu do momoentu wciśnięcia przycisku
                    self.nr_przycisku = self.warunek_ktory_wyswietlacz_menu

                if self.ustawienie_czasu != 0 and  time.ticks_diff(time.ticks_ms(),self.ustawienie_czasu) > podany_czas :# Przytrzymanie przez podany czas              
                    self.ustawienie_czasu = 0  #Zresetowanie czasu, aby powyższy warunek wykonał się tylko raz (na 2 sekund)
                    self.Flaga_przycisk_prawy = True
                    return 2
            # Zresetowanie czasu, jeżeli przycisk został odkliknięty 
            elif self.ustawienie_czasu != 0 and self.funkcja_przycisk == 2 and  (self.Przycisk_2_Pin.value() == 1 or self.warunek_ktory_wyswietlacz_menu != self.nr_przycisku or  self.Przycisk_1_Pin.value() == 0):          
                self.ustawienie_czasu = 0 # ustawienie wartosci na 0 tak, aby po wejsciu przypisac aktualny czas            
                self.funkcja_przycisk = 0
                   
        if wybor_przycisku == 3: # Oba przyciski
            if self.Przycisk_2_Pin.value() == 0 and self.Przycisk_1_Pin.value() == 0 and  self.Flaga_przycisk_lewy == False and self.Flaga_przycisk_prawy == False:
                if self.ustawienie_czasu == 0:
                    self.ustawienie_czasu = time.ticks_ms() #przypisanie aktualnego czasu do momoentu wciśnięcia przycisku
                    self.funkcja_przycisk = 3
                if self.ustawienie_czasu != 0 and  time.ticks_diff(time.ticks_ms(),self.ustawienie_czasu) > podany_czas :# Przytrzymanie przez podany czas              
                    self.ustawienie_czasu = 0  #Zresetowanie czasu, aby powyższy warunek wykonał się tylko raz (na 2 sekund)
                    self.Flaga_przycisk_prawy = True
                    self.Flaga_przycisk_lewy = True
                    return 3
            # Zresetowanie czasu, jeżeli któryś z przycisków został odkliknięty    
            elif self.ustawienie_czasu != 0 and self.funkcja_przycisk == 3 and ( self.Przycisk_1_Pin.value() == 1 or self.Przycisk_2_Pin.value() == 1):          
                self.ustawienie_czasu = 0 # ustawienie wartosci na 0 tak, aby po wejsciu przypisac aktualny czas
                self.funkcja_przycisk = 0
     
     
    def wejscie_do_Menu(self,Obj_Display):
        self.menu = True
        self.flaga_1_prog_menu = True #Ustawienie flagi mówiącej, że jest się w  1 progu menu    
        self.warunek_ktory_wyswietlacz_menu = 0 #ustawienie 1 opcji w menu
        self.przycisk = 0 #ustawienie wartosci przycisku na 0 aby modulo działało poprawnie
        self.ilosc_wyborow_w_menu = 5 
        self.wybor_w_menu_interwal = 0
        
        Obj_Display.wejscie = False
        self.zmiana_przycisk = True        
    def wyjscie_z_menu(self):
        self.menu = False # wyjście z funkcji menu jeżeli żaden przycisk nie został kliknięty przez 10s 
        self.flaga_1_prog_menu = False #aby po ponowym wejsciu do menu nastapiła opcja 1 progu wyboru
        self.flaga_2_prog_menu = False
        self.flaga_3_prog_menu = False
        self.warunek_ktory_wyswietlacz = 0 # Wrócenie do głównej funkcji wyświetlacza
        self.wybor_w_menu = 0 #aby po ponowym wejsciu do menu prostokat byl w dobrym miejscu  
        self.przycisk = -1  
        self.wybor_w_menu_interwal = 0  
        self.czyszczenie = True    
        self.wybor_ktory_motyw = 0
        self.flaga_motywy_menu   = False
        self.flaga_motywy_menu_1 = False
        
        if self.interwal_czas_start_1 == True or self.interwal_dystans_start_1 == True :
            self.reset_interwalu()
        elif self.interwal_czas_start_0 == True or self.interwal_dystans_start_0 == True :
            self.dodatkowe_czyszczenie = True
        
    def reset_interwalu(self):
        #Ustawianie na domyślne wszystkich zmiennych od interwałów
        self.interwal_dystans_start_1 = False
        self.interwal_dystans_start_0 = False
        self.interwal_czas_start_0 = False
        self.interwal_czas_start_1 = False
        self.wlasny_interwal = False
        self.ustawienie_danych = False 
        self.interwal_dystans = 700        
        self.interwal_dystans_pause = 500
        self.interwal_czas = 30
        self.interwal_pause = 60
        self.ilosc_cykli = 4
        self.przejechany_dystans = []
        self.dlugosc_interwalu = []
        self.zmiana_liczb = 0 
        self.czyszczenie = True
        self.cykle       = 0 
        self.Odmierzanie_grafiki = 0
        self.flaga_buzzer = False
        self.dodatkowe_czyszczenie = False
        self.podsumowanie_interwalu_przycisk = 0
        self.podsumowanie = False
        
    def wybor_opcji_w_menu_1_prog(self,Obj_Display):
        self.warunek_ktory_wyswietlacz_menu =  self.wybor_w_menu +1 #przypisanie ktory wyswietlacz w menu ma sie wyswietlac
        self.flaga_2_prog_menu = True
        self.flaga_1_prog_menu = False
        self.przycisk = 0 #aby modulo działało jak należy
        self.zmiana_przycisk = True  
        Obj_Display.wejscie_do_menu = True
        if self.wybor_w_menu == 0: #Zresetowanie podróży 
        #przypisanie ilości wyborów w kolejnym oknie menu
            self.ilosc_wyborow_w_menu = 2
            self.wybor_w_menu = 0 #ustawienie domyślengo wyboru na 1 wartość     
           
            
        elif self.wybor_w_menu == 1: #interwał czasowy 
            self.ilosc_wyborow_w_menu = 4
            self.wybor_w_menu = 0 #ustawienie domyślengo wyboru na 1 wartość     
                       
        elif self.wybor_w_menu == 2: #interwał dystansowy 
            self.ilosc_wyborow_w_menu = 4
            self.wybor_w_menu = 0 #ustawienie domyślengo wyboru na 1 wartość
            
        elif self.wybor_w_menu == 3: #Customizowanie menu
            self.ilosc_wyborow_w_menu = 4 # To jest ilosc wyborow dla obreczy i wskaźnika
            self.wybor_w_menu = 0    # Ustawienie domyślengo wyboru na 1 wartość     
                   
        elif self.wybor_w_menu == 4: #wyjscie z menu 
            self.wyjscie_z_menu()
            
  
  
  
    def wybor_opcji_w_menu_2_prog(self, licznik,Obj_Display):
        self.flaga_3_prog_menu = True   
        self.flaga_2_prog_menu = False
        self.flaga_1_prog_menu = False
        self.przycisk = 0
        self.zmiana_przycisk = True
        Obj_Display.wymazanie_prostokata = True
            #== Menu zresetowania podróży ==# 
        if self.warunek_ktory_wyswietlacz_menu == 1:
            if self.wybor_w_menu == 0:          # Zresetowanie podrozy            
                # Ustawienie zmiennych podróży na 0
                licznik.counter_podroz = 0
                licznik.v_max_podroz = 0
                licznik.przeywzszenia_podroz = 0
                licznik.rtc_czas_podroz  = [0,0,0,0]
                # Zapisanie przypisanyh wartości do pliku 
                licznik.zapis_do_pliku_podroz()
                self.wyjscie_z_menu()
            elif self.wybor_w_menu == 1:        # Wyjscie z menu  
                self.wyjscie_z_menu()
                
            #== Menu Interwału czasowego oraz Interwału dystansowego ==#
                # Oba menu są zrobione na tej samej zasadzie, i mogą tak samo byc obsługiwane # 
        elif self.warunek_ktory_wyswietlacz_menu == 2 or self.warunek_ktory_wyswietlacz_menu == 3:
            self.przycisk = 4                    # Przypisanie ilości cykli
            
            if self.interwal_czas_start_0 == True or self.interwal_dystans_start_0 == True:
                self.reset_interwalu()
                           
            if self.wybor_w_menu == 0 or self.wybor_w_menu == 1: # Wybór gotowego interwału
                self.Flaga_przycisk_prawy = True
                                          
            elif self.wybor_w_menu == 2:         # Stworzenie własnego interwału
                self.Flaga_przycisk_prawy = True
                self.wlasny_interwal = True 

            elif self.wybor_w_menu == 3:         # Wyjscie z menu  
                self.wyjscie_z_menu()
                
                
            #== Menu casomizowania wyglądu ==#                                        
        elif self.warunek_ktory_wyswietlacz_menu == 4:
            self.flaga_3_prog_menu = False          # Po to, aby pozostać w tym progu Menu 
            self.flaga_2_prog_menu = True
            
            self.flaga_motywy_menu = False      
            self.wybor_ktory_motyw += 1             # Przytrzymaliśmy przycisk, więc inkrementujemy wartość 
            self.wybor_ktory_motyw = self.wybor_ktory_motyw %5 # Mod z 5, bo mamy do wyboru 5 opcji
            
            # Ustawiamy aktualną wartość wyboru w menu na tą, do której jest dopisany aktualny wybrany motyw
            # Robimy to po każdej zmianie, bo chcemy zmienić aktualny i wybrany (logicznie)
            
            if self.wybor_ktory_motyw == 0:  # Dla obręczy i wsk
                self.przycisk = Obj_Display.wybor_motywu_obrecz    
                self.ilosc_wyborow_w_menu = 8
                
            elif self.wybor_ktory_motyw ==1: # Dla smugi
                self.przycisk = Obj_Display.wybor_motywu_speedo
                self.ilosc_wyborow_w_menu = 9

            elif self.wybor_ktory_motyw ==2: # Dla int_czas
                self.przycisk = Obj_Display.wybor_motywu_czas
                self.ilosc_wyborow_w_menu = 5
                
            elif self.wybor_ktory_motyw ==3: # Dla int_dys
                self.przycisk = Obj_Display.wybor_motywu_dyst
                self.ilosc_wyborow_w_menu = 5
                
            elif self.wybor_ktory_motyw ==4: # Dla czcionki
                self.przycisk = Obj_Display.kolor_czcionki
                self.ilosc_wyborow_w_menu = 7      
            
            
              
    def wybor_opcji_w_menu_3_prog(self, licznik):   # Tylko dla interwałów 
        if self.wybor_w_menu == 0 or self.wybor_w_menu == 1:  # Wybranie opcji gotowego interwału 
            self.wybor_w_menu_interwal += 1
            self.wybor_w_menu_interwal = self.wybor_w_menu_interwal %3 
                
        elif self.wybor_w_menu == 2:                # Wybranie opcji własnego interwału 
            self.wybor_w_menu_interwal += 1
            self.wybor_w_menu_interwal = self.wybor_w_menu_interwal % 5
 
 
       
    def interwal_dane(self, ope):
        if self.wlasny_interwal == False and self.wybor_w_menu_interwal == 0: # Wybór gotowego interwału 
            self.przycisk = ope(self.przycisk,1) 
            self.ilosc_cykli = self.przycisk % 9 +1 # Bo bo nie może być 0
            
          # Wybór własnego interwału czasowego   
        elif self.warunek_ktory_wyswietlacz_menu == 2 and self.wlasny_interwal == True:                          
            if self.wybor_w_menu_interwal == 0:
                if self.interwal_czas <= 0:
                    self.interwal_czas = 1
                elif self.interwal_czas < 120 :
                    self.interwal_czas = ope(self.interwal_czas, 5) 
                elif self.interwal_czas >= 120 and self.interwal_czas < 240:
                    self.interwal_czas = ope(self.interwal_czas,15 ) 
                elif self.interwal_czas >= 240 and self.interwal_czas < 600:
                    self.interwal_czas = ope(self.interwal_czas,30 ) 
                elif self.interwal_czas >= 600: 
                    self.interwal_czas = ope(self.interwal_czas, 60) 
                    
            elif self.wybor_w_menu_interwal == 1:
                if self.interwal_pause <= 0:
                    self.interwal_pause = 1
                elif self.interwal_pause < 120:
                    self.interwal_pause = ope(self.interwal_pause, 5)
                elif self.interwal_pause >= 120 and self.interwal_pause < 240:
                    self.interwal_pause = ope(self.interwal_pause, 15)
                elif self.interwal_pause >= 240 and self.interwal_pause < 600:
                    self.interwal_pause = ope(self.interwal_pause, 30)
                elif self.interwal_pause >= 600: 
                    self.interwal_pause = ope(self.interwal_pause, 60)
                    
            elif self.wybor_w_menu_interwal == 2:
                self.przycisk = ope(self.przycisk,1)
                self.ilosc_cykli = self.przycisk  % 9 +1
          # Wybór własnego interwału dystansowego                  
        elif self.warunek_ktory_wyswietlacz_menu == 3 and self.wlasny_interwal == True:   
            if self.wybor_w_menu_interwal == 0:
                if self.interwal_dystans <= 0:
                    self.interwal_dystans = 0
                elif self.interwal_dystans <= 100:
                    self.interwal_dystans = ope(self.interwal_dystans, 10) 
                elif self.interwal_dystans >= 100   and self.interwal_dystans < 1000:
                    self.interwal_dystans = ope(self.interwal_dystans, 100)     
                elif self.interwal_dystans >= 1_000 and self.interwal_dystans < 2_000:
                    self.interwal_dystans = ope(self.interwal_dystans, 200) 
                elif self.interwal_dystans >= 2_000 and self.interwal_dystans < 5_000:
                    self.interwal_dystans = ope(self.interwal_dystans, 500) 
                elif self.interwal_dystans >= 5_000 and self.interwal_dystans < 15_000:
                    self.interwal_dystans = ope(self.interwal_dystans, 1000) 
                elif self.interwal_dystans >= 15_000:
                    self.interwal_dystans = ope(self.interwal_dystans, 5000) 
                    
            elif self.wybor_w_menu_interwal == 1:
                if self.interwal_dystans_pause <= 0:
                    self.interwal_dystans_pause = 0
                if self.interwal_dystans_pause <= 100:
                    self.interwal_dystans_pause =ope(self.interwal_dystans_pause , 10) 
                elif self.interwal_dystans_pause >= 100   and self.interwal_dystans_pause < 1000:
                    self.interwal_dystans_pause =ope(self.interwal_dystans_pause , 100)     
                elif self.interwal_dystans_pause >= 1_000 and self.interwal_dystans_pause < 2_000:
                    self.interwal_dystans_pause =ope(self.interwal_dystans_pause , 200) 
                elif self.interwal_dystans_pause >= 2_000 and self.interwal_dystans_pause < 5_000:
                    self.interwal_dystans_pause =ope(self.interwal_dystans_pause , 500) 
                elif self.interwal_dystans_pause >= 5_000 and self.interwal_dystans_pause < 15_000:
                    self.interwal_dystans_pause =ope(self.interwal_dystans_pause , 1000) 
                elif self.interwal_dystans_pause >= 15_000:
                    self.interwal_dystans_pause =ope(self.interwal_dystans_pause , 5000) 
                    
            elif self.wybor_w_menu_interwal == 2:  
                self.przycisk = ope(self.przycisk,1)
                self.ilosc_cykli = self.przycisk  % 9 +1            
        else:
            pass
    
    def Ustawienie_interwalu(self, Licznik):
        if self.wybor_w_menu == 0 or self.wybor_w_menu == 1:
            if self.warunek_ktory_wyswietlacz_menu == 2: #Dla czasowego 
                if self.wybor_w_menu_interwal == 1: #Zatwierdzenie 
                    if self.wybor_w_menu == 0: #zatwierdzenie 1 gotowoego interwału
                        #przypisanie wartosci zmiennym odliczającym interwał
                        self.interwal_czas = 30
                        self.interwal_pause = 90
                        
                    elif self.wybor_w_menu == 1:#zatwierdzenie 2 gotowoego interwału
                        self.interwal_czas = 45
                        self.interwal_pause = 120
                        
                    self.interwal_czas_start_0 = True  
                    self.wyjscie_z_menu()
                    
                elif self.wybor_w_menu_interwal == 2: #Zatwierdzenie wyjscia z menu       
                    self.wyjscie_z_menu()
                                   
                    
            elif self.warunek_ktory_wyswietlacz_menu == 3: #Dla dystansowego 
                if self.wybor_w_menu_interwal == 1: #Zatwierdzenie
                    if self.wybor_w_menu == 0: #zatwierdzenie 1 gotowoego interwału
                        #przypisanie wartosci zmiennym odliczającym interwał
                        self.interwal_dystans = 1000
                        self.interwal_dystans_pause = 500  
                    elif self.wybor_w_menu == 1: #zatwierdzenie 2 gotowoego interwału
                        self.interwal_dystans = 2000 
                        self.interwal_dystans_pause = 1000
                    self.interwal_dystans_start_0 = True
                    self.wyjscie_z_menu()
                elif self.wybor_w_menu_interwal == 2: #Zatwierdzenie wyjscia z menu       
                    self.wyjscie_z_menu()
                else:
                    pass
                             
                
        elif self.wybor_w_menu == 2: #Zatwierdzenie własnego interwału
            if self.wybor_w_menu_interwal == 3:
                if self.warunek_ktory_wyswietlacz_menu == 2:
                    self.interwal_czas_start_0 = True
                elif self.warunek_ktory_wyswietlacz_menu == 3:
                    self.interwal_dystans_start_0 = True
                self.wyjscie_z_menu() 
        

            elif self.wybor_w_menu_interwal == 4: #Zatwierdzenie wyjscia z menu    
                self.wyjscie_z_menu() 

        else:
            pass


    def buzzer_interwal(self, numer): 
        czas = time.ticks_diff((time.ticks_ms()) ,self.deadline_interwal)
        
        if numer ==1: # Sekwencja do startu 
            if  czas < 300:
                self.pwm15.duty_u16(15_000)
            elif czas >= 300 and czas <1000:
                self.pwm15.duty_u16(0)
            elif czas >= 1000 and czas <1400:
                self.pwm15.duty_u16(15_000)
            elif czas >= 1400 and czas <2000:
                self.pwm15.duty_u16(0)
            elif  czas >= 2000 and czas <3000:
                self.pwm15.duty_u16(15_000)
            elif czas >= 3000 :
                
                self.pwm15.duty_u16(0)
                self.pwm15.deinit()       
                self.interwal_czas_start_1 = True
                self.interwal_dystans_start_1 = True #Obie te flagi mogą się równać True, bo i tak tylko jeden się wyświetla
                
        elif numer ==2: #Krótki sygnał 
            if  czas < 500:
                self.pwm15.duty_u16(15_000)
            elif czas >= 500:
                self.pwm15.duty_u16(0)
                self.pwm15.deinit()
                self.flaga_buzzer = False
                
        elif numer ==3: 
            if  czas < 1500:
                self.pwm15.duty_u16(15_000)
            elif czas >= 1500:
                self.pwm15.duty_u16(0)
                self.pwm15.deinit()
                self.flaga_buzzer = False
                
                
    def interwal_czasowy(self, obj_licznik):
        ####==== Przygotowanie do interwału ====#####
        if self.interwal_czas_start_1 == False:
            ##=== Wywołujemy rozpoczecie interwału ===###
            if self.przytrzymanie_przycisku(1,1000) == 1: 
                self.flaga_buzzer = True
                self.cykle  = self.ilosc_cykli *2
                self.deadline_interwal = time.ticks_ms() #WPrzypisujemy zmiennej aktualny czas po wejściu w funkcję
                return self.interwal_czas
            
            ##=== Wywoływanie buzzera ===###
            elif self.flaga_buzzer ==True:               
                self.buzzer_interwal(1)
                return self.interwal_czas
            
            ##=== Mruganie liczbami ===###
            else:
                okres = 600
                if time.ticks_diff((time.ticks_ms()) ,self.deadline_interwal) > 0:
                    self.deadline_interwal = time.ticks_add(time.ticks_ms(), okres)
                    if self.mruganie_liczb_interwal == False:
                        self.mruganie_liczb_interwal = True
                        return self.interwal_czas             
                    elif self.mruganie_liczb_interwal == True:       
                        self.mruganie_liczb_interwal = False
                        return -1
                elif  self.mruganie_liczb_interwal ==False:
                    return self.interwal_czas
                elif  self.mruganie_liczb_interwal ==True:
                    return -1  

        ####==== Prawdziwy interwał ====##### 
        elif self.interwal_czas_start_1 == True:
            ##=== przypisanie czasu i aktualnego przejechanego dystansu ===##
            if self.ustawienie_danych == False and self.cykle > 0:
                self.ustawienie_danych = True
                self.czyszczenie = True
                self.cykle -= 1
                
                if self.cykle  %2 == 1:
                    self.interwal_dystans_czas = obj_licznik.counter
                    self.deadline = time.ticks_add(time.ticks_ms(), self.interwal_czas*1000)
                    
                ##=== przypisanie do konca tablicy przejechanej odelglosci podczas ostatniego interwału ===##    
                elif self.cykle  %2 == 0:
                    self.przejechany_dystans.append( obj_licznik.counter - self.interwal_dystans_czas)
                    self.deadline = time.ticks_add(time.ticks_ms(), self.interwal_pause*1000)
                    
            ##=== Zakończenie interwału ===##
            elif self.cykle == 0:
                return -2

            ##=== Odliczanie czasu ===###
            self.odliczanie = time.ticks_diff(self.deadline, time.ticks_ms())/1000
            if self.odliczanie > 0:
                return int(self.odliczanie)
            elif self.odliczanie <= 0:
                self.ustawienie_danych = False
                return -1

    def interwal_dystans_funkcja(self, obj_licznik):
        ####==== Przygotowanie do interwału ====##### 
        if self.interwal_dystans_start_1 == False:
            ##=== Wywołujemy rozpoczecie interwału ===###
            if self.przytrzymanie_przycisku(1,1000) == 1:
                
                self.cykle  = self.ilosc_cykli *2      
                self.flaga_buzzer = True
                self.deadline_interwal = time.ticks_ms() #WPrzypisujemy zmiennej aktualny czas po wejściu w funkcję
                return self.interwal_dystans               
                  
            ##=== Wywoływanie buzzera ===###
            elif self.flaga_buzzer ==True:
                self.buzzer_interwal(1)
                return self.interwal_dystans               
            ##=== Mruganie liczbami ===###
            else:
                okres = 600
                if time.ticks_diff((time.ticks_ms()) ,self.deadline_interwal) > 0:
                    self.deadline_interwal = time.ticks_add(time.ticks_ms(), okres)
                    if self.mruganie_liczb_interwal == False:
                        self.mruganie_liczb_interwal = True
                        return self.interwal_dystans             
                    elif self.mruganie_liczb_interwal == True:       
                        self.mruganie_liczb_interwal = False
                        return -1
                elif  self.mruganie_liczb_interwal ==False:
                    return self.interwal_dystans
                elif  self.mruganie_liczb_interwal ==True:
                    return -1  


    
    
    
        ####==== Prawdziwy interwał ====#####     
        elif self.interwal_dystans_start_1 == True:
            if self.ustawienie_danych == False and self.cykle > 0:
                self.ustawienie_danych = True
                self.czyszczenie = True
                self.cykle -= 1
                ##=== przypisanie czasu i  ustawienie dystansu ===##
                if self.cykle  %2 == 1:
                    self.start_interwalu = time.ticks_ms()
                    self.deadline =  obj_licznik.counter + self.interwal_dystans* 1000/obj_licznik.obwod_kola
                    
                ##=== przypisanie do konca tablicy czasu w jakim przejechalem dystans podczas ostatniego interwału  
                elif self.cykle  %2 == 0:            
                    self.dlugosc_interwalu.append(time.ticks_diff(time.ticks_ms(), self.start_interwalu))
                    self.deadline =  obj_licznik.counter + self.interwal_dystans_pause* 1000/obj_licznik.obwod_kola
                    
            ##=== Zakończenie interwału ===##
            elif self.cykle == 0:
                return -2
            
            ##=== Odliczanie dystansu ===###
            
            self.odliczanie = self.deadline - obj_licznik.counter
            if self.odliczanie > 0:
                return int(self.odliczanie *obj_licznik.obwod_kola/1000)
            elif self.odliczanie <= 0:
                self.ustawienie_danych = False
                return -1
     
    def zatwierdzenie_motywow(self,Licznik,Obj_Display):      
        # Zapis do pliku każdej z wartości:
        zapis_motywow = open("/Libraries/motywy.txt" ,"w")
        zapis_motywow.write(str(Obj_Display.wybor_motywu_obrecz) + '\n')
        zapis_motywow.write(str(Obj_Display.wybor_motywu_speedo) + '\n')       
        zapis_motywow.write(str(Obj_Display.wybor_motywu_czas) + '\n')
        zapis_motywow.write(str(Obj_Display.wybor_motywu_dyst) + '\n')
        zapis_motywow.write(str(Obj_Display.kolor_czcionki) + '\n')
        zapis_motywow.close()
         
        self.Flaga_przycisk_lewy = True
        self.wyjscie_z_menu()
    def odczyt_motywow(self, Obj_Display):        
        j = 0 
        odczyt_motywow = open("/Libraries/motywy.txt" ,"r")
        motywy = odczyt_motywow.readlines()
        for motyw in motywy:
            motyw = motyw.replace("\n", "")  # usuwanie znaku końca linii
            if j == 0:
                Obj_Display.wybor_motywu_obrecz = int(motyw)
                
            elif j == 1:
                Obj_Display.wybor_motywu_speedo = int(motyw)
                
            elif j == 2:
                Obj_Display.wybor_motywu_czas   = int(motyw)
                
            elif j == 3:
                Obj_Display.wybor_motywu_dyst  = int(motyw)
                
            elif j == 4:
                Obj_Display.kolor_czcionki     = int(motyw)               
            j += 1
            
        odczyt_motywow.close()
              
        
