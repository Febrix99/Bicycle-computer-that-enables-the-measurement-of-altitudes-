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
gold =  st7789.color565(190 , 130 , 60 )

class Display_menu():
    
    ########################### MENU ##################################
    
    ##======= Funkcje w menu ==============##
    def menu(obj_Display,obj_Menu,obj_licznik):
     
        if obj_Menu.warunek_ktory_wyswietlacz_menu==0:
            if obj_Display.wejscie == False: #Jeżeli wyszliśmy z funkcji #Spedometer to czyścimy jednorazowo screena
                gc.collect() # Just in case, bo nie ma framebuffera  
                IPS.fill(st7789.BLACK)
                Display_menu.menu_text()
                obj_Display.wejscie = True
            if obj_Menu.zmiana_przycisk == True:
                gc.collect() # Just in case, bo nie ma framebuffera  
                Display_menu.menu_chose(obj_Display,obj_Menu)
                obj_Menu.zmiana_przycisk = False
                
         
         
        ##=== Zresetowanie Podróży ===##
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==1:   
            if obj_Display.wejscie_do_menu == True:
                # Tutaj pojawiają się rzeczy które wywyołują się jednorazowo po wejściu do menu 
                IPS.fill(st7789.BLACK)
                IPS.text(font_32, 'Czy na pewno chcesz', 5,15,gold)
                IPS.text(font_32, 'zaczac nowa podroz?', 5,55,gold)
                Display_menu.show_picture_menu(obj_Menu.warunek_ktory_wyswietlacz_menu)
                obj_Display.wejscie_do_menu = False
            if obj_Menu.zmiana_przycisk == True:
                gc.collect() # Just in case, bo nie ma framebuffera  
                if obj_Menu.wybor_w_menu == 0:
                    Display_menu.gold_rect(st7789.BLACK, 167) 
                    Display_menu.gold_rect(st7789.color565(183,145,75), 107)                              
                elif obj_Menu.wybor_w_menu == 1:
                    Display_menu.gold_rect(st7789.BLACK, 107)
                    Display_menu.gold_rect(st7789.color565(183,145,75), 167)
                obj_Menu.zmiana_przycisk = False
                   
        ##=== Interwasł czasowy ===##
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==2:  
            if obj_Display.wejscie_do_menu == True:
                IPS.fill(st7789.BLACK)
                Display_menu.show_picture_menu(obj_Menu.warunek_ktory_wyswietlacz_menu)
                Display_menu.konutry_menu_intrwal(st7789.color565(150 , 110 , 71 )    )
                Display_menu.napisy_w_interwale(obj_Menu.warunek_ktory_wyswietlacz_menu)
                obj_Display.wejscie_do_menu = False   

            
            if obj_Menu.zmiana_przycisk == True:
                gc.collect() # Just in case, bo nie ma framebuffera  


                if obj_Menu.flaga_2_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Display.poprzedni_wybor , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu
                    
                elif obj_Menu.flaga_3_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Menu.wybor_w_menu , obj_Menu.flaga_2_prog_menu,  obj_Display.poprzedni_wybor, False)
                    Display_menu.gold_rect_menu(st7789.BLACK, obj_Menu.wybor_w_menu  , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal,obj_Display.wymazanie_prostokata)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu_interwal
                    obj_Display.wymazanie_prostokata = False
                    
                
                Display_menu.gold_rect_menu(gold,              obj_Menu.wybor_w_menu,       obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                obj_Menu.zmiana_przycisk = False
                
                
            Display_menu.wyswietlanie_liczb_interwal(obj_Display,obj_Menu)   
                
        ##=== Interwasł dystansowy ===##        
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==3:         
            if obj_Display.wejscie_do_menu == True:
                gc.collect() # Just in case, bo nie ma framebuffera  
                IPS.fill(st7789.BLACK)
                Display_menu.show_picture_menu   (obj_Menu.warunek_ktory_wyswietlacz_menu)
                Display_menu.konutry_menu_intrwal(st7789.color565(150 ,110, 71) )
                Display_menu.napisy_w_interwale   (obj_Menu.warunek_ktory_wyswietlacz_menu)
                obj_Display.wejscie_do_menu = False
                
            if obj_Menu.zmiana_przycisk == True:
                gc.collect() # Just in case, bo nie ma framebuffera  
                if obj_Menu.flaga_2_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Display.poprzedni_wybor , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu
                    
                elif obj_Menu.flaga_3_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Menu.wybor_w_menu , obj_Menu.flaga_2_prog_menu,  obj_Display.poprzedni_wybor, False)
                    Display_menu.gold_rect_menu(st7789.BLACK, obj_Menu.wybor_w_menu  , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal,obj_Display.wymazanie_prostokata)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu_interwal
                    obj_Display.wymazanie_prostokata = False
                    
                
                Display_menu.gold_rect_menu(gold,              obj_Menu.wybor_w_menu,       obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                obj_Menu.zmiana_przycisk = False
                
                
            Display_menu.wyswietlanie_liczb_interwal(obj_Display,obj_Menu)                   
                
                
                
        ##=== Dostosowanie wyglądu===##          
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==4:   #Customizing view
            if obj_Display.wejscie_do_menu == True: # Jednorazowo po wejściu 
                gc.collect() # Just in case, bo nie ma framebuffera  
                IPS.fill(st7789.BLACK)
                Display_menu.strzalki_wyboru(gold)
                
                # Tutaj pojawiają się aktualne wybrane motywy
                Display_menu.wybor_koloru_obreczy(obj_Display)
                Display_menu.wybor_koloru_smugi(320,obj_Display,obj_licznik)
                IPS.draw(romand, str(69), 75, 130,obj_Display.motyw_czcionki(obj_Display.kolor_czcionki), 1.7)
                Display_menu.wybor_koloru_int_czas(314,obj_Display)
                Display_menu.wybor_koloru_int_dys(255,obj_Display)
                
                obj_Display.wejscie_do_menu = False
                
            if obj_Menu.flaga_motywy_menu  == False :# Zmienna odróżniająca zmiane ptrzytrzymania przycisku od kliknięcia
                Display_menu.wybor_ktory_motyw_fun(obj_Display, obj_Menu) 
                obj_Menu.zmiana_przycisk = False
                obj_Menu.flaga_motywy_menu  = True
                obj_Menu.flaga_motywy_menu_1  = True
                
            elif obj_Menu.zmiana_przycisk == True:  
                gc.collect() # Just in case, bo nie ma framebuffera
                if obj_Menu.flaga_motywy_menu_1 == False:
                    Display_menu.wybor_ktory_kolor_w_motywie(obj_Menu,obj_Display,obj_licznik)
                obj_Menu.flaga_motywy_menu_1 = False
                obj_Menu.zmiana_przycisk = False
                
                
   ########## Funckje od castomizowania menu ###########################                
    ### Funkcje wyświetlające zmianie koloru  ###    
    def wybor_koloru_obreczy(obj_Display):
        ym = 165
        xm = 160
        r = 157 + 4 
        odcinek = 3
        kolor = obj_Display.kolor_obreczy_i_int(obj_Display.wybor_motywu_obrecz,0)
        ####### Rysowanie wskaźnika #####
        IPS.polygon(obj_Display.wskaznik(-obj_Display.dlugosc_wskaznia+1 ,1),  xm-r,  ym-1, kolor, math.pi/2 )
        IPS.polygon(obj_Display.wskaznik(-obj_Display.dlugosc_wskaznia+1 ,1),  xm-r,  ym-2, kolor, math.pi/2 )
        for i in range(math.pi*r*0.70):
            x = 255*i/(math.pi*r*0.70)
            kolor = obj_Display.kolor_obreczy_i_int(obj_Display.wybor_motywu_obrecz,x)
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
      
      
############################################################################################
    @micropython.native     
    def wybor_koloru_smugi(arg,obj_Display,obj_licznik):
        ym = 165
        xm = 160
        r = 157
        obj_Display.pochodna = True
        ## Dane do smugi    
        for i in range(arg):
            x1 = -round(r*math.cos(i/r)) + xm   
            x2 = x1 + round(obj_Display.dlugosc_wskaznia*math.cos(i/r))
            y1 = -round(r*math.sin(i/r)) + ym
            y2 = y1 + round(obj_Display.dlugosc_wskaznia*math.sin(i/r))
            # [x1,y1] przechowują wsp. zewnętrzne do smugi
            # [x2,y2] przechowują wsp. wewnętrzne do smugi
            
            ## Dane do wskaźnika
            x_wsk = -round(r*math.cos((i+3)/r)) + xm
            y_wsk =   -round(r*math.sin((i+3)/r)) + ym
            rotacja = ((i/r) +math.pi/2)              # Rotujemy od pi/2 do 3*pi/2
            
            
            kolor  = 254*i/320 
            ####### Rysowanie wskaźnika #####
            IPS.polygon(obj_Display.wskaznik(-obj_Display.dlugosc_wskaznia+1 ,1),  x_wsk,  y_wsk,
                        obj_Display.kolor_obreczy_i_int(obj_Display.wybor_motywu_obrecz,kolor), rotacja )
            

            ####### Rysowanie smugi #####
            obj_Display.draw_line(x1,y1,x2,y2,kolor)
            
############################################################################################             
    @micropython.native               
    def wybor_koloru_int_czas(arg,obj_Display):
        for i in range(arg):
            x = 255 * i/314
            kolor = obj_Display.kolor_obreczy_i_int(obj_Display.wybor_motywu_czas,x)
            x_sin_z =  int(50*math.sin(i/50)) +208
            y_cos_z = -int(50*math.cos(i/50)) + 125
            x_sin_w = x_sin_z - int(14*math.sin(i/50))
            y_cos_w = y_cos_z + int(14*math.cos(i/50))
            #Rysowanie lini pomiędzy 2 obręczami 
            IPS.line(x_sin_z  ,y_cos_z     ,x_sin_w ,  y_cos_w, kolor)
            #Rysowanie 2 lini pomiędzy obręczami jeden pixel na y niżej aby wypełnić całość 
            IPS.line(x_sin_z , y_cos_z-1  ,x_sin_w , y_cos_w-1, kolor)
        
        
############################################################################################          
    def wybor_koloru_int_dys(arg,obj_Display):
        for i in range(arg):
            x = 255 * i/314
            IPS.vline(2 + i, 188, 49,obj_Display.kolor_obreczy_i_int(obj_Display.wybor_motywu_dyst ,x))

############################################################################################   
    ### Funkcje wybroru ###
    def wybor_ktory_kolor_w_motywie(obj_Menu,obj_Display,obj_licznik):
        if obj_Menu.wybor_ktory_motyw == 0:  # Dla obręczy
            obj_Display.wybor_motywu_obrecz = obj_Menu.wybor_w_menu          # Przpisanie nowej wartości wyboru motywu
            
            Display_menu.wybor_koloru_obreczy(obj_Display) # Wywołanie funkcji z nową wartością 
            
        elif obj_Menu.wybor_ktory_motyw ==1: # Dla smugi
            obj_Display.wybor_motywu_speedo = obj_Menu.wybor_w_menu          # Przpisanie nowej wartości wyboru motywu
            
            Display_menu.wybor_koloru_smugi(320,obj_Display,obj_licznik) # Wywołanie funkcji z nową wartością 

            
        elif obj_Menu.wybor_ktory_motyw ==2: # Dla int_czas
            obj_Display.wybor_motywu_czas = obj_Menu.wybor_w_menu            # Przpisanie nowej wartości wyboru motywu 
            
            Display_menu.wybor_koloru_int_czas(314,obj_Display) # Wywołanie funkcji z nową wartością 
            
        elif obj_Menu.wybor_ktory_motyw ==3: # Dla int_dys 
            obj_Display.wybor_motywu_dyst = obj_Menu.wybor_w_menu            # Przpisanie nowej wartości wyboru motywu 
            
            Display_menu.wybor_koloru_int_dys(255,obj_Display) # Wywołanie funkcji z nową wartością 
            
        elif obj_Menu.wybor_ktory_motyw ==4: # Dla czcionki:
            IPS.fill_rect(72,112,70,40, st7789.BLACK)
            obj_Display.kolor_czcionki = obj_Menu.wybor_w_menu 
            IPS.draw(romand, str(69), 75, 130,obj_Display.motyw_czcionki(obj_Display.kolor_czcionki), 1.7)
            
            
    def wybor_ktory_motyw_fun(obj_Display ,obj_Menu):
        Display_menu.prostokat_wyboru(obj_Display.poprzedni_wybor, st7789.BLACK)
        Display_menu.prostokat_wyboru(obj_Menu.wybor_ktory_motyw, gold)
        obj_Display.poprzedni_wybor = obj_Menu.wybor_ktory_motyw 
        
    def prostokat_wyboru(wybor,kolor):
        przesuniecie_po_y = 40
        x = 274
        y = 24 + przesuniecie_po_y*wybor
        IPS.rect(x,    y,     46,   33,  kolor)
        IPS.rect(x+1,  y+1,   44,   31,  kolor)      
        
        
    def strzalki_wyboru(kolor):  
        przesuniecie_po_y = 40
        x = 295
        for i in range(5):
            y = 43 + przesuniecie_po_y*i
            IPS.hline(x ,y     ,20,   kolor)
            IPS.hline(x ,y-1   ,20,   kolor)
            IPS.hline(x ,y-4   ,20,   kolor)
            IPS.hline(x ,y-5  ,20,   kolor)
            
            IPS.line(x - 8 ,y-3    ,x+2    ,y-13, kolor)
            IPS.line(x - 7 ,y-3    ,x+3    ,y-13, kolor)
            IPS.line(x - 8 ,y-2    ,x+2    ,y+8, kolor)
            IPS.line(x - 7 ,y-2    ,x+3    ,y+8, kolor)

   ########## Funkcje od 1 progu menu ###########################
    def menu_text():
        IPS.text(font_32, 'Nowa podroz',     int(160 -len('Nowa podroz')*8),      8 , gold)
        IPS.text(font_32, 'Int. czasowy',    int(160 -len('Int. czasowy')*8),     56 , gold)
        IPS.text(font_32, 'Int. dystansowy', int(160 -len('Int. dystansowy')*8) , 104 , gold)    
        IPS.text(font_32, 'Dostosuj wyglad', int(160 -len('Dostosuj wyglad')*8) , 152 , gold)
        IPS.text(font_32, 'Wyjscie',         int(160 -len('Wyjscie')*8) ,         200 , gold)
        
 
        
    def menu_chose(obj_Display,obj_Menu):
        karmazynowy = st7789.color565(71, 1, 1 )
        IPS.rect(0, 0, 319, 239, karmazynowy)
        IPS.rect(1, 1, 317, 237, karmazynowy)
        
        ### Czyszczenie poprzedniego
        rect_y_poprzedni =  48 * obj_Display.poprzedni_wybor
        Display_menu.gold_rect(st7789.BLACK, rect_y_poprzedni)
        obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu 
           
        rect_y = 48 * obj_Menu.wybor_w_menu
        Display_menu.gold_rect(gold, rect_y)
    


    def gold_rect(kolor,rect_y):
        rect_x = 10    
        rect_len = 300
        rect_h = 48
     
        IPS.rect(rect_x, rect_y+1, rect_len, 46, kolor)
        IPS.hline(rect_x +10 ,          rect_y +3,            rect_len - 21,kolor)
        IPS.hline(rect_x +10 ,          rect_y + rect_h -4,   rect_len - 21,kolor)     
        IPS.vline(rect_x +3 ,           rect_y +10 ,          rect_h - 21,  kolor)
        IPS.vline(rect_x +rect_len -4 , rect_y +10,           rect_h - 21,  kolor)

        IPS.hline(rect_x + 3,           rect_y +10,            7,           kolor)
        IPS.hline(rect_x +rect_len -11, rect_y +10,            7,           kolor)
        IPS.hline(rect_x + 3,           rect_y +rect_h -11,    7,           kolor)
        IPS.hline(rect_x +rect_len -11, rect_y +rect_h -11,    7,           kolor)

        IPS.vline(rect_x +10,           rect_y +3,             7,           kolor)
        IPS.vline(rect_x +rect_len -11, rect_y +3,             7,           kolor)
        IPS.vline(rect_x +10,           rect_y +rect_h -11,    7,           kolor)
        IPS.vline(rect_x +rect_len -11, rect_y +rect_h -11,    7,           kolor)

   ########## Funkcje od interwałów ###########################
    def konutry_menu_intrwal(kolor):
        lines = [(35, 0, 180), (130, 0, 180), (230, 0, 180), (0, 45, 320), (0, 90, 320), (0, 135, 320), (0, 180, 320)]
        for line in lines:
            if line[0] > 0:
                IPS.vline(line[0], line[1], line[2], kolor)
            else:
                IPS.hline(0, line[1], line[2], kolor)
    
    def show_picture_menu( wybor):
        if wybor ==1:
            IPS.jpg('/Libraries/Pictures/tak.jpg',52,110, st7789.SLOW)  #216x40
            IPS.jpg('/Libraries/Pictures/nie.jpg',54,170, st7789.SLOW)  #213 x40
        elif wybor ==2 or wybor ==3 :
            IPS.jpg('/Libraries/Pictures/start_wyjscie.jpg',3,190, st7789.SLOW) #311x29
        else:
            pass        
            

    def gold_rect_menu( kolor, wybor,prog, wybor_interwalu, wymazanie):
        y_len = 38
        if prog ==True or wymazanie == True  : #wbieranie rodzaju menu
            x_len= 30
            x = 3
            if wybor ==  0: # Gotowy 1 intewał
                y = 49           
            elif wybor ==1: # Gotowy 2 intewał
                y = 94
            elif wybor ==2: # Własny interwał
                y = 139           
            elif wybor ==3: # wyjście 
                x = 155
                y = 188
                x_len = 162
        elif  prog ==False:    #wybrany interwał
            if wybor == 0:            # Gotowy 1 intewał
                if wybor_interwalu ==0:     # Ustawienie ilości cykli
                    x = 248
                    y = 49 
                    x_len= 53
                elif wybor_interwalu ==1:   # Ustawienie Interwału  
                    x = 0
                    y = 188
                    x_len = 158
                elif wybor_interwalu ==2:   # Wyjście z interwału 
                    x = 155
                    y = 188
                    x_len = 162
            elif wybor == 1:          # Gotowy 2 intewał
                if wybor_interwalu ==0:      # Ustawienie ilości cykli 
                    x = 248
                    y = 94
                    x_len= 53
                elif wybor_interwalu ==1:    # Ustawienie Interwału 
                    x = 0
                    y = 188
                    x_len = 158
                elif wybor_interwalu ==2:    # Wyjście z interwału 
                    x = 155
                    y = 188
                    x_len = 162                
            elif wybor == 2:          # Własny interwał
                if wybor_interwalu ==0:      # Ustawienie długości interwału 
                    x = 39
                    y = 139
                    x_len= 88
                elif wybor_interwalu ==1:    # Ustawienie przerwy interwału 
                    x = 134
                    y = 139
                    x_len= 92
                elif wybor_interwalu ==2:    # Ustawienie ilości cykli 
                    x = 248
                    y = 139
                    x_len= 53
                elif wybor_interwalu ==3:    # Ustawienie Interwału 
                    x = 0
                    y = 188
                    x_len = 158
                elif wybor_interwalu ==4:    # Wyjście z interwału 
                    x = 155
                    y = 188
                    x_len = 162

                    
        IPS.rect(x,     y     , x_len,     y_len, kolor)
        IPS.rect(x+1,  y+1  , x_len -2   , y_len-2, kolor)
        IPS.vline(x, y, y_len, st7789.BLACK)
        IPS.vline(x+1, y, y_len, st7789.BLACK)
        
        IPS.vline(x, y, 10, kolor)
        IPS.vline(x+1, y, 10, kolor)
        IPS.line(x,  y+10, x+9, y+18,kolor)
        IPS.line(x+1,y+10, x+10,y+18,kolor)
        
        IPS.vline(x, y+28, 10, kolor)
        IPS.vline(x+1, y+28, 10, kolor)
        IPS.line(x    ,y+28,x+9,y+19,kolor)
        IPS.line(x+1  ,y+28,x+10,y+19,kolor)
        
    def napisy_w_interwale(warunek):       
        IPS.text(font_32,"Cykle",239,8,gold)
        IPS.text(font_32,"1",13,53,gold)
        IPS.text(font_32,"2",13,98,gold)
        IPS.text(font_32,"3",13,143,gold)
        if warunek == 2:
            IPS.text(font_32,"Czas",50,8,gold)
            IPS.text(font_32,"Pauza",142,8,gold)
            IPS.text(font_32,"30",66,53,gold)
            IPS.text(font_32,"45",66,98,gold)
            IPS.text(font_32,"90",163,53,gold)
            IPS.text(font_32,"120",155,98,gold)          
        elif warunek ==3:
            IPS.text(font_32,"Jazda",42,8,gold)
            IPS.text(font_32,"Pauza",142,8,gold)            
            IPS.text(font_32,"500",60,53,gold)
            IPS.text(font_32,"1000",52,98,gold)
            IPS.text(font_32,"500",158,53,gold)
            IPS.text(font_32,"1000",150,98,gold)
            
    def wyswietlanie_liczb_interwal(obj_Display,obj_Menu):
        okres = 550
        if time.ticks_diff((time.ticks_ms()) ,obj_Display.deadline) > 0:
            if obj_Display.mruganie_liczb == False:
                IPS.text(font_32,"4",270,53,gold)
                IPS.text(font_32,"4",270,98,gold)
                
                if obj_Menu.flaga_3_prog_menu == True and obj_Menu.wybor_w_menu ==2:
                    pass
                else:
                    IPS.text(font_32,"4",270,143,gold)
                    Display_menu.dane_interwalow(obj_Menu)
                obj_Display.mruganie_liczb = True
                
            elif obj_Display.mruganie_liczb == True:
                kolor = st7789.BLACK
                IPS.fill_rect(270,52, 16,32, kolor)
                IPS.fill_rect(270,97, 16,32,kolor)
                IPS.fill_rect(270,142, 16,32,kolor)
                
                IPS.fill_rect(50 ,142, 73,32,  kolor)
                IPS.fill_rect(145,142, 78,32, kolor)                
                obj_Display.mruganie_liczb = False
                
            obj_Display.deadline = time.ticks_add(time.ticks_ms(), okres)
            
        if obj_Menu.flaga_3_prog_menu == True:
            if   obj_Menu.wybor_w_menu ==0  : #1 gotowy interwał
                IPS.text(font_32,str(obj_Menu.ilosc_cykli),270,53,gold)
            elif obj_Menu.wybor_w_menu ==1  : #2 gotowy interwał
                IPS.text(font_32,str(obj_Menu.ilosc_cykli),270,98,gold)
            
            elif obj_Menu.wybor_w_menu ==2  : #własny interwał
                IPS.text(font_32,str(obj_Menu.ilosc_cykli),270,143,gold)
                Display_menu.dane_interwalow(obj_Menu)
            
        else:
            pass
     
     
    def dane_interwalow(obj_Menu):
        if obj_Menu.warunek_ktory_wyswietlacz_menu ==2: # Interwał czosowy 
            IPS.text(font_32,str(obj_Menu.interwal_czas)    ,
                     int(82 - len(str(obj_Menu.interwal_czas)*8 ))   ,143     ,gold)
            IPS.text(font_32,str(obj_Menu.interwal_pause)
                     ,int(180 - len(str(obj_Menu.interwal_pause)*8))  ,143     ,gold)
            
        elif obj_Menu.warunek_ktory_wyswietlacz_menu ==3: # Interwał dystansowy
            if obj_Menu.interwal_dystans < 10000:
                IPS.text(font_32,str(obj_Menu.interwal_dystans)          ,
                         int(84 - len(str(obj_Menu.interwal_dystans))*8)      ,143     ,gold)
            else:    
                IPS.text(font_32,str(int(obj_Menu.interwal_dystans/1000)) +'km'         ,
                         int(92 - len(str(obj_Menu.interwal_dystans))*8)      ,143     ,gold)
                
            if obj_Menu.interwal_dystans_pause <10000:
                IPS.text(font_32,str(obj_Menu.interwal_dystans_pause)    ,
                         int(182- len(str(obj_Menu.interwal_dystans_pause))*8)  ,143     ,gold)
            else:
                IPS.text(font_32,str(int(obj_Menu.interwal_dystans_pause/1000)) +'km'    ,
                         int(190- len(str(obj_Menu.interwal_dystans_pause))*8)  ,143     ,gold)                        
                        
        
