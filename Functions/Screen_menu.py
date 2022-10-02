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
gold =  st7789.color565(179 , 139 , 91 )


class Display_menu():
    
    ########################### MENU ##################################
    def pokazanie_danych(obj_Display ,obj_licznik, obj_menu):         
        pass        

    ##======= Funkcje w menu ==============##
    def menu(obj_Display,obj_Menu,obj_licznik):   
        if obj_Menu.warunek_ktory_wyswietlacz_menu==0:
            if obj_Display.wejscie == False: #Jeżeli wyszliśmy z funkcji #Spedometer to czyścimy jednorazowo screena
                #tutaj też ta funkcja co usyawia defultowo zmienne od speedometera
                IPS.fill(st7789.BLACK)
                Display_menu.menu_text()
                obj_Display.wejscie = True
            if obj_Display.zmiana_przycisk == True:
                Display_menu.menu_chose(obj_Display,obj_Menu)
                obj_Display.zmiana_przycisk = False
                
         
         
        ##=== Zresetowanie czasu ===##
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==1:   
            if obj_Display.wejscie_do_menu == True:
                IPS.fill(st7789.BLACK)
                IPS.text(font_32, 'Czy na pewno chcesz', 5,15,st7789.color565(183,145,75))
                IPS.text(font_32, 'zaczac nowa podroz?', 5,55,st7789.color565(183,145,75))
                Display_menu.show_picture_menu(obj_Menu.warunek_ktory_wyswietlacz_menu)
                obj_Display.wejscie_do_menu = False
            if obj_Display.zmiana_przycisk == True: 
                if obj_Menu.wybor_w_menu == 0:
                    Display_menu.gold_rect(st7789.BLACK, 167) 
                    Display_menu.gold_rect(st7789.color565(183,145,75), 107)                              
                elif obj_Menu.wybor_w_menu == 1:
                    Display_menu.gold_rect(st7789.BLACK, 107)
                    Display_menu.gold_rect(st7789.color565(183,145,75), 167)
                obj_Display.zmiana_przycisk = False
                   
        ##=== Interwasł czasowy ===##
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==2:  
            if obj_Display.wejscie_do_menu == True:
                IPS.fill(st7789.BLACK)
                Display_menu.show_picture_menu(obj_Menu.warunek_ktory_wyswietlacz_menu)
                Display_menu.konutry_menu_intrwal(st7789.color565(150 , 110 , 71 )    )
                Display_menu.napisy_w_interwale(obj_Menu.warunek_ktory_wyswietlacz_menu)
                obj_Display.wejscie_do_menu = False   

            
            if obj_Display.zmiana_przycisk == True:


                if obj_Menu.flaga_2_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Display.poprzedni_wybor , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu
                    
                elif obj_Menu.flaga_3_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Menu.wybor_w_menu , obj_Menu.flaga_2_prog_menu,  obj_Display.poprzedni_wybor, False)
                    Display_menu.gold_rect_menu(st7789.BLACK, obj_Menu.wybor_w_menu  , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal,obj_Display.wymazanie_prostokata)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu_interwal
                    obj_Display.wymazanie_prostokata = False
                    
                
                Display_menu.gold_rect_menu(gold,              obj_Menu.wybor_w_menu,       obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                obj_Display.zmiana_przycisk = False
                
                
            Display_menu.wyswietlanie_liczb_interwal(obj_Display,obj_Menu)   
                
        ##=== Interwasł dystansowy ===##        
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==3:         
            if obj_Display.wejscie_do_menu == True:
                IPS.fill(st7789.BLACK)
                Display_menu.show_picture_menu   (obj_Menu.warunek_ktory_wyswietlacz_menu)
                Display_menu.konutry_menu_intrwal(st7789.color565(150 ,110, 71) )
                Display_menu.napisy_w_interwale   (obj_Menu.warunek_ktory_wyswietlacz_menu)
                obj_Display.wejscie_do_menu = False
                
            if obj_Display.zmiana_przycisk == True:
                if obj_Menu.flaga_2_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Display.poprzedni_wybor , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu
                    
                elif obj_Menu.flaga_3_prog_menu == True:
                    Display_menu.gold_rect_menu(st7789.BLACK,  obj_Menu.wybor_w_menu , obj_Menu.flaga_2_prog_menu,  obj_Display.poprzedni_wybor, False)
                    Display_menu.gold_rect_menu(st7789.BLACK, obj_Menu.wybor_w_menu  , obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal,obj_Display.wymazanie_prostokata)
                    obj_Display.poprzedni_wybor = obj_Menu.wybor_w_menu_interwal
                    obj_Display.wymazanie_prostokata = False
                    
                
                Display_menu.gold_rect_menu(gold,              obj_Menu.wybor_w_menu,       obj_Menu.flaga_2_prog_menu,  obj_Menu.wybor_w_menu_interwal, False)
                obj_Display.zmiana_przycisk = False
                
                
            Display_menu.wyswietlanie_liczb_interwal(obj_Display,obj_Menu)                   
                
                
                
        ##=== Dostosowanie wyglądu===##          
        elif obj_Menu.warunek_ktory_wyswietlacz_menu==3:   #Customizing view
            pass




   ########## Funkcje ###########################
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
        Display_menu.gold_rect(st7789.color565(183,145,75), rect_y)
    


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



    def konutry_menu_intrwal( kolor):
        IPS.vline(38, 0, 180, kolor)
        IPS.vline(123, 0, 180, kolor)
        IPS.vline(224, 0, 180, kolor)       
        IPS.hline(0, 45, 320, kolor)
        IPS.hline(0, 90, 320, kolor)
        IPS.hline(0, 135, 320, kolor)
        IPS.hline(0, 180, 320, kolor)
        
    
    def show_picture_menu( wybor):
        if wybor ==1:
            IPS.jpg('/Libraries/Pictures/tak.jpg',52,110, st7789.SLOW)  #216x40
            IPS.jpg('/Libraries/Pictures/nie.jpg',54,170, st7789.SLOW)  #213 x40
        elif wybor ==2 or wybor ==3 :
            IPS.jpg('/Libraries/Pictures/start_wyjscie.jpg',3,190, st7789.SLOW) #311x29
        else :
            pass        
            


        
        
    def gold_rect_menu( kolor, wybor,prog, wybor_interwalu, wymazanie):
        y_len = 38
        if prog ==True or wymazanie == True  : #wbieranie rodzaju menu
            x_len= 34
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
                    x = 243
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
                    x = 243
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
                    x = 41
                    y = 139
                    x_len= 80
                elif wybor_interwalu ==1:    # Ustawienie przerwy interwału 
                    x = 126
                    y = 139
                    x_len= 95
                elif wybor_interwalu ==2:    # Ustawienie ilości cykli 
                    x = 243
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
        IPS.text(font_32,"Cykle",235,8,gold)
        IPS.text(font_32,"1",17,53,gold)
        IPS.text(font_32,"2",17,98,gold)
        IPS.text(font_32,"3",17,143,gold)
        if warunek == 2:
            IPS.text(font_32,"Czas",48,8,gold)
            IPS.text(font_32,"Pauza",134,8,gold)
            IPS.text(font_32,"45",64,53,gold)
            IPS.text(font_32,"90",64,98,gold)
            IPS.text(font_32,"90",158,53,gold)
            IPS.text(font_32,"150",150,98,gold)          
        elif warunek ==3:
            IPS.text(font_32,"Jazda",42,8,gold)
            IPS.text(font_32,"Pauza",134,8,gold)            
            IPS.text(font_32,"1000",48,53,gold)
            IPS.text(font_32,"1000",48,98,gold)
            IPS.text(font_32,"500",150,53,gold)
            IPS.text(font_32,"1000",142,98,gold)
                  
    def wyswietlanie_liczb_interwal(obj_Display,obj_Menu):
        okres = 600
        if time.ticks_diff((time.ticks_ms()) ,obj_Display.deadline) > 0:
            if obj_Display.mruganie_liczb == False:
                IPS.text(font_32,"4",265,53,gold)
                IPS.text(font_32,"4",265,98,gold)
                
                if obj_Menu.flaga_3_prog_menu == True and obj_Menu.wybor_w_menu ==2:
                    pass
                else:
                    IPS.text(font_32,"4",265,143,gold)
                    Display_menu.dane_interwalow(obj_Menu)
                obj_Display.mruganie_liczb = True
                
            elif obj_Display.mruganie_liczb == True:
                IPS.fill_rect(265,53, 16,33, st7789.BLACK)
                IPS.fill_rect(265,98, 16,33,st7789.BLACK)
                IPS.fill_rect(265,143, 16,33,st7789.BLACK)
                IPS.fill_rect(40,143, 80,33,  st7789.BLACK)
                IPS.fill_rect(135,143, 87,33,st7789.BLACK)                
                obj_Display.mruganie_liczb = False
                
            obj_Display.deadline = time.ticks_add(time.ticks_ms(), okres)
            
        if obj_Menu.flaga_3_prog_menu == True:
            if   obj_Menu.wybor_w_menu ==0  : #1 gotowy interwał
                IPS.text(font_32,str(obj_Menu.ilosc_cykli),265,53,gold)
            elif obj_Menu.wybor_w_menu ==1  : #2 gotowy interwał
                IPS.text(font_32,str(obj_Menu.ilosc_cykli),265,98,gold)
            
            elif obj_Menu.wybor_w_menu ==2  : #własny interwał
                IPS.text(font_32,str(obj_Menu.ilosc_cykli),265,143,gold)
                Display_menu.dane_interwalow(obj_Menu)
            
        else:
            pass
     
     
    def dane_interwalow(obj_Menu):
        if obj_Menu.warunek_ktory_wyswietlacz_menu ==2: # Interwał czosowy 
            IPS.text(font_32,str(obj_Menu.interwal_czas)    ,
                     int(88 - len(str(obj_Menu.interwal_czas)*8 ))   ,143     ,gold)
            IPS.text(font_32,str(obj_Menu.interwal_pause)
                     ,int(180 - len(str(obj_Menu.interwal_pause)*8))  ,143     ,gold)
            
        elif obj_Menu.warunek_ktory_wyswietlacz_menu ==3: # Interwał dystansowy
            if obj_Menu.interwal_dystans < 10000 and obj_Menu.interwal_dystans_pause <10000:
                IPS.text(font_32,str(obj_Menu.interwal_dystans)          ,
                         int(88 - len(str(obj_Menu.interwal_dystans))*8)      ,143     ,gold)
                IPS.text(font_32,str(obj_Menu.interwal_dystans_pause)    ,
                         int(180- len(str(obj_Menu.interwal_dystans_pause))*8)  ,143     ,gold)
            else:
                IPS.text(font_32,str(int(obj_Menu.interwal_dystans/1000)) +'km'         ,
                         int(88 - len(str(obj_Menu.interwal_dystans))*8)      ,143     ,gold)
                IPS.text(font_32,str(int(obj_Menu.interwal_dystans_pause/1000)) +'km'    ,
                         int(180- len(str(obj_Menu.interwal_dystans_pause))*8)  ,143     ,gold)                        
                        
        
