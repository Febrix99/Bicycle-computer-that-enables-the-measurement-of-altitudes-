%%-- Tworzenie klasy 

classdef MyData_nowe
    
    properties
        Altitude
        Current_speed   
        
    end 
    properties (Dependent)
        
        avg_speed      
        avg_Altitude
        

        avg_Altitude_10
        
        kat    
        plotter
        

    end
    
    methods
        %-- Konstruktor 
        function thisMyData_nowe = MyData_nowe( altitude, Speed)
            

            thisMyData_nowe.Altitude = altitude;
            thisMyData_nowe.Current_speed = Speed;
            
        end 
        



    
        %-- Średnia wysokosc        
        function avg_Altitude = get.avg_Altitude(theMyData_nowe)
            
            avg_Altitude = mean(theMyData_nowe.Altitude);
         
        end    
        %-- Średnia predkosc        
        function avg_speed = get.avg_speed(theMyData_nowe)
            
            avg_speed = mean(theMyData_nowe.Current_speed);
         
        end  
     
        

        %-- Średnia wysokosc z 10 obortów    
        function avg_Altitude_10 = get.avg_Altitude_10(theMyData_nowe)
            avg_Altitude_10 = mean(reshape(theMyData_nowe.Altitude,...
                [10, max(size(theMyData_nowe.Altitude))/10]));     
            d = 1:1:max(size(avg_Altitude_10));
            plot(d,avg_Altitude_10); grid on;
            title('Srednia z 10 obrotow');
            xlabel('nr_pomiaru') , ylabel('Kat[stopnie]');     
            axis([0,(max(size(theMyData_nowe.avg_Altitude_10)+1)), min(theMyData_nowe.avg_Altitude_10)-2, max(theMyData_nowe.avg_Altitude_10)+2])
        end
        
        
        %-- Wykresy danych       
        function plotter = get.plotter(theMyData_nowe)
            %- Dziedzina 
            x = 1:1:max(size(theMyData_nowe.Current_speed)); % Tyle x ile pomiarów 
            
            %- Wysokosc      
            subplot(2,1,1)
            y3 = theMyData_nowe.Altitude;
            plot(x,y3, 'g','LineWidth',2);
            set(gca,'FontSize',14)
            title('Wysokość n.p.m','FontSize',16,'FontWeight','bold'); 
            xlabel('nr','FontSize',16,'FontWeight','bold'); ylabel('[m]','FontSize',16,'FontWeight','bold');   grid on ;
            axis([0,( max(size(theMyData_nowe.Current_speed)+5)), (min(theMyData_nowe.Altitude)-1), (max(theMyData_nowe.Altitude)+1)])    
            %-Zmienić czcionkę 
            %- Predkosc chwilowa        
            subplot(2,1,2)
            y4 = theMyData_nowe.Current_speed;
            plot(x,y4, 'r','LineWidth',2);
            set(gca,'FontSize',14)
            title('Predkość chwilowa','FontSize',16,'FontWeight','bold'); 
            xlabel('nr','FontSize',16,'FontWeight','bold'); ylabel('[Km/h]','FontSize',16,'FontWeight','bold');   grid on ;
            axis([0,( max(size(theMyData_nowe.Current_speed)+5)), 0, (max(theMyData_nowe.Current_speed)+5)])


        end 
             
    end
end