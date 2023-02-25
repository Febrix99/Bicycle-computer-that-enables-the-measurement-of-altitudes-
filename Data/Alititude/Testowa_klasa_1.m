classdef Testowa_klasa_1
      
    properties 
        Altitude  
        objectt
    end 
    
    
    properties (Dependent)
       avg_Altitude
    end    
    
    
    methods
        %- Wywołanie konstruktora 
        function thisTestowa_klasa_1 = Testowa_klasa_1(Altitude, object)
            thisTestowa_klasa_1.Altitude = Altitude;
            thisTestowa_klasa_1.objectt = object;
            
        end
        %- Funkcja wyliczająca właściwości zależne
        function avg_Altitude = get.avg_Altitude(Testowa_klasa_1)
            avg_Altitude = Testowa_klasa_1.objectt.mean_function(Testowa_klasa_1.Altitude);
        end  

    end 
end 